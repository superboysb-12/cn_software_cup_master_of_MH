import pandas as pd
import concurrent.futures
from func_get_app_information import  get_app_information,get_dynamic_analysis_information
from PDFGenerator import  PDFGenerator
from  util import Predictor,url_check
import os
from util import check_url_with_api
import streamlit as st
from util import namelist
import threading
import ollama

MODEL_NAME = "lama"
# 创建一个锁对象
lock = threading.Lock()

CAPTURE_CSV_PATH =  os.path.join("temp","capture","capture.csv")
APK_FOLDER = os.path.join("temp","data")


def convert_to_int(value):
    return int(value)

class AnalysisTool():

    def __init__(self):
        self.target_apk = None
        self.static_analysis_finished = False
        self.dynamic_analysis_finished = False
        self.two_label = '未识别'
        self.confidence = '未识别'
        self.five_label = '未识别'
        self.tool = None
        self.url = None
        self.raw_url = None
        self.app_information = None
        self.check_downloaded_apk()
        self.file_name = 'None'
        self.namelist = 'None'
        self.lists = namelist()
        self.filtered_url = {}
        print('Analysis tool initialized')

    def load_apk_data(self,original_data):
        if self.target_apk != original_data:
            #self.__init__()
            pass
        self.target_apk = original_data

    def static_analysis(self,progress_callback):
        if self.target_apk is None:
            return
        apk_data = self.target_apk
        self.app_information,self.apk_path,self.five_info,self.tool = get_app_information(apk_data=apk_data,progress_callback = progress_callback)
        self.app_information['five_label'] = self.five_label
        self.icon_path = self.app_information['icon_path'][0]
        self.two_label = self.app_information['two_label']
        self.url = self.app_information['url'][0]
        self.url = self.url[1:]
        self.raw_url = self.url.copy()
        self.app_information['file_name'] = self.file_name
        self.static_analysis_finished = True


    def dynamic_analysis(self):
        self.dynamic_analysis_finished = True

    def get_static_analysis_information(self,progress_callback):
        if self.target_apk is None:
            return
        self.static_analysis(progress_callback)
        st.session_state['static_progress'].append('\n提取 ' + 'url')
        if progress_callback:
            progress_callback()
        self.classify_url()
        #self.classify_two_label()
        # 返回前端所需数据
        df = self.app_information
        details_permissions = df['details_permissions'][0]
        classes = df['classes'][0]
        apk_path = self.apk_path
        basic = df.loc[:,
                ['file_name', 'name', 'file_size', 'package_name', 'md5',
                'signature_name', 'scan_time',
               'version_name', 'version_code', 'min_sdk', 'max_sdk',
               'services','receivers', 'providers','main_activity']
                ]
        df_transposed = basic.transpose()
        df_transposed.columns = df_transposed.iloc[0]
        df_transposed = df_transposed.drop(df_transposed.index[0])

        # 在这里对APK进行解析得到各种特征得到多个df(基本信息, 应用权限, 相关url, 类, activity,image)以及apk_path
        return (df_transposed, details_permissions, self.url, classes, df.loc[:, ['main_activity', 'activities']],
                df['icon_path']), apk_path

    def generate_pdf(self,static_result:bool = True,dynamic_result:bool = False):
        generator  =  PDFGenerator()
        if(static_result and self.static_analysis_finished):
            generator.load_static_information(self.app_information)
            if self.url is not None:
                generator.load_url(self.url)
        if(dynamic_result and self.dynamic_analysis_finished):
            generator.load_dynamic_information(CAPTURE_CSV_PATH)
        generator.generate_report()

    def classify_five_label(self):
        five_info = self.tool.get_five_info()
        types = ["white", "black", "gamble", "sex", "scam"]
        model_name = MODEL_NAME
        send_massage = five_info
        res = ollama.chat(model=model_name,
                          stream=False,
                          messages=[{"role": "user", "content": send_massage}],
                          options={"temperature": 0, "num_keep": 1})
        output = res['message'].content
        # 限制output为types中的一个类型
        # 如果output中包含types中的类型,则将其设置为types中的一个类型
        type = "未识别"
        for t in types:
            if t in output:
                output = t
                type = t
                break
        self.five_label = type
        if self.app_information is not None:
            self.app_information['five_label'] = self.five_label

    def classify_two_label(self):
        predictor = Predictor()  # 涉诈二分类模型
        two_info = self.tool.get_info()
        self.two_label, self.confidence = predictor.predict(two_info)
        self.two_label = '涉诈' if self.two_label else '非涉诈'
        self.confidence = round(self.confidence, 3)
        if self.app_information is not None:
            self.app_information['two_label'] = self.two_label
            self.app_information['confidence'] = self.confidence


    def get_label(self):
        return self.two_label,self.confidence,self.five_label

    def check_downloaded_apk(self):
        self.downloaded_apk_data = [(None,'已上传的APK')]
        self.downloaded_apk_names = ['已上传的APK']
        #print(APK_FOLDER)
        for filename in os.listdir(APK_FOLDER):
            #print(filename)
            file_path = os.path.join(APK_FOLDER, filename)
            if os.path.isfile(file_path):
                try:
                    with open(file_path, 'rb') as file:
                        data = file.read()
                    self.downloaded_apk_data.append((data, os.path.splitext(filename)[0]))  # 文件数据和不带后缀的文件名
                    self.downloaded_apk_names.append(os.path.splitext(filename)[0])  # 不带后缀的文件名
                except Exception as e:
                    print(f"Error processing file {filename}: {e}")

    def list_downloaded_apks(self):
        return self.downloaded_apk_names

    def select_downloaded_apk(self, name):
        if name == '已上传的APK':
            return
        for data, file_name in self.downloaded_apk_data:
            if file_name == name:
                self.file_name = name + '.apk'
                self.load_apk_data(data)
                return
        print('no apk found')




    def classify_url(self):
        output = []
        urlClassifier = url_check()
        url_filter = self.filtered_url

        def process_url(u):
            api_output = check_url_with_api(u)
            reputation = api_output['data']['attributes']['reputation'] if api_output else None
            label = urlClassifier.predict(u)

            reputation_value = int(reputation) if reputation is not None else 0

            return [u, 'dangerous' if label else 'normal', reputation_value,url_filter[u] if u in url_filter else 'no']

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(process_url, u) for u in self.url]

            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                output.append(result)

        output_df = pd.DataFrame(output, columns=['url', 'Security', 'Reputation','Filtered'])
        output_df['Reputation'] = output_df['Reputation'].apply(convert_to_int)

        self.url = output_df










