from func_get_app_information import  get_app_information,get_dynamic_analysis_information
from PDFGenerator import  PDFGenerator
from  util import Five_Bert
import os

local_capture_file = "temp\capture.csv"
folder_for_downloaded_apk = r"temp\data"

class AnalysisTool():

    def __init__(self):
        self.static_analysis_finished = False
        self.dynamic_analysis_finished = False
        self.five_label = '未识别'
        self.downloaded_apk_data = [(None,'不选择')]
        self.downloaded_apk_names = ['不选择']
        self.target_apk = None

    def load_apk_data(self,original_data):
        self.target_apk = original_data

    def static_analysis(self):
        if self.target_apk is None:
            return
        apk_data = self.target_apk
        self.app_information,self.apk_path,self.five_info = get_app_information(apk_data=apk_data)
        self.app_information['five_label'] = self.five_label
        self.icon_path = self.app_information['icon_path'][0]
        self.static_analysis_finished = True

    def dynamic_analysis(self):
        self.dynamic_analysis_finished = True

    def get_static_analysis_information(self):
        if self.target_apk is None:
            return
        self.static_analysis()
        # 返回前端所需数据
        df = self.app_information
        details_permissions = df['details_permissions'][0]
        url = df['url'][0]
        classes = df['classes'][0]
        apk_path = self.apk_path
        basic = df.loc[:, 'name': 'providers']
        df_transposed = basic.transpose()
        df_transposed.columns = df_transposed.iloc[0]
        df_transposed = df_transposed.drop(df_transposed.index[0])

        # 在这里对APK进行解析得到各种特征得到多个df(基本信息, 应用权限, 相关url, 类, activity,image)以及apk_path
        return (df_transposed, details_permissions, url, classes, df.loc[:, ['main_activity', 'activities']],
                df['icon_path']), apk_path

    def generate_pdf(self,static_result:bool = True,dynamic_result:bool = False):
        generator  =  PDFGenerator()
        if(static_result and self.static_analysis_finished):
            generator.load_static_information(self.app_information)
        if(dynamic_result and self.dynamic_analysis_finished):
            generator.load_dynamic_information(local_capture_file)
        generator.generate_report()

    def get_classes(self):
        model = Five_Bert()
        self.five_label = model.predict(self.five_info)
        if self.app_information:
            self.app_information['five_label'] = self.five_label

    def list_downloaded_apks(self):

        for filename in os.listdir(folder_for_downloaded_apk):
            file_path = os.path.join(folder_for_downloaded_apk, filename)
            if os.path.isfile(file_path):
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = file.read()
                    self.downloaded_apk_data.append((data, os.path.splitext(filename)[0]))  # 文件数据和不带后缀的文件名
                    self.downloaded_apk_names.append(os.path.splitext(filename)[0])  # 不带后缀的文件名

        return self.downloaded_apk_names

    def select_downloaded_apk(self, name):
        if name == '不选择':
            return
        for data, file_name in self.downloaded_apk_data:
            if file_name == name:
                self.load_apk_data(data)







