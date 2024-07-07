from func_get_app_information import  get_app_information,get_dynamic_analysis_information
from PDFGenerator import  PDFGenerator
from  util import Five_Bert

local_capture_file = "temp\capture.csv"

class AnalysisTool():

    def __init__(self):
        self.static_analysis_finished = False
        self.dynamic_analysis_finished = False

    def static_analysis(self,apk_data):
        self.apk_data = apk_data
        self.app_information,self.apk_path,self.five_info = get_app_information(apk_data=apk_data)
        self.icon_path = self.app_information['icon_path'][0]
        self.static_analysis_finished = True

    def dynamic_analysis(self):
        self.dynamic_analysis_finished = True

    def get_static_analysis_information(self):
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
        type = model.predict(self.five_info)




