import streamlit as st
import time
import pandas as pd
from PIL import Image
from func_get_app_information import get_app_information as static_analyzer_apk
from utils_download import download_apk
from GeneratePDF import GeneratePDF

st.title('ADS')
#streamlit run web.py

def highlight_dangerous(s):
    return ['background-color: red' if 'dangerous' in v else '' for v in s]

# 重置分析状态的函数
def reset_session_state():
    st.session_state['analysis_complete'] = False
    st.session_state['recognition_complete'] = False
    st.session_state['static_completed'] = False
    st.session_state['dynamic_completed'] = False
    st.session_state['report_completed'] = False
    st.session_state['df1'] = pd.DataFrame()
    st.session_state['df2'] = pd.DataFrame()
    st.session_state['df3'] = pd.DataFrame()
    st.session_state['df4'] = pd.DataFrame()
    st.session_state['df5'] = pd.DataFrame()
    st.session_state['image'] = None
    st.session_state["prediction_type"] = None

def static_analyzer(uploaded_file):
    # 初始化 session_state
    if 'analysis_complete' not in st.session_state:
        st.session_state['analysis_complete'] = False
    if 'recognition_complete' not in st.session_state:
        st.session_state['recognition_complete'] = False

    st.header('静态分析模式')
    if st.button('开始解析'):
        if uploaded_file is None:
            st.info('请先上传APK')
        else:
            try:
                original_apk = uploaded_file.getbuffer()
                with st.spinner('解析中...'):
                    time.sleep(2)
                    (st.session_state['df1'],st.session_state['df2'],st.session_state['df3'],st.session_state['df4'],st.session_state['df5'],st.session_state['image']),st.session_state['apk_path'] = static_analyzer_apk(original_apk)
                    st.session_state['image']=st.session_state['image'][0]

                    #在这里对APK进行解析得到各种特征得到多个df(基本信息,应用权限,相关url,类,activity)和image


                st.session_state['analysis_complete'] = True
            except Exception as e:
                st.session_state['analysis_complete'] = False
                st.exception(e)
    if st.session_state['analysis_complete'] == True:
            st.success('解析完成')

    if st.session_state['analysis_complete'] == True:
        def data_visualization(df1,df2,df3,df4,df5,image):
            st.image(image,
                     caption='APP图像',
                     width=100
                     )
            data_option = st.selectbox(
                index=0,
                label='解析结果',
                options=['基本信息', '应用权限','相关URL','Class','Activity']
            )
            if data_option == '基本信息':
                st.write(df1)
            elif data_option == '应用权限':
                st.dataframe(st.session_state['df2'].style.apply(highlight_dangerous, subset=['Security']))
            elif data_option == '相关URL':
                st.write(df3)
            elif data_option == 'Class':
                st.write(df4)
            else:
                st.write(df5)

        data_visualization(st.session_state['df1'],
                           st.session_state['df2'],
                           st.session_state['df3'],
                           st.session_state['df4'],
                           st.session_state['df5'],
                           st.session_state['image'])

    if st.button('开始识别'):
        if st.session_state['analysis_complete'] == False:
            st.info('请先解析APK')
        else:
            try:
                with st.spinner('识别中...'):
                    time.sleep(2)
                    #st.session_state['prediction_type'] = predict(data)
                    #在这里调用模型,将上面的特征输入,返回识别出的类型
                    st.session_state['prediction_type'] = '色情'
                st.session_state['recognition_complete'] = True
            except Exception as e:
                st.session_state['recognition_complete'] = False
                st.error('识别失败')
                st.exception(e)
    if st.session_state['recognition_complete'] == True:
        st.session_state['static_completed'] = True
        if st.session_state["prediction_type"] == '正常':
            st.success('识别结果为: 正常 APP')
        st.warning(f'识别结果为: {st.session_state["prediction_type"]} 类APP')

def dynamic_analyzer():
    st.header('动态分析模式')
    st.write('在这里展示动态分析的信息。')
    #st.session_state['dynamic_completed'] = True

def side_bar():
    if 'static_completed' not in st.session_state:
        st.session_state['static_completed'] = False
    if 'dynamic_completed' not in st.session_state:
        st.session_state['dynamic_completed'] = False
    if 'report_completed' not in st.session_state:
        st.session_state['report_completed'] = False

    #侧栏选择分析方式
    with st.sidebar:
        option = st.selectbox(
            label='分析方式',
            options=['静态分析', '动态分析']
        )

        #文件上传
        uploaded_file = st.file_uploader(
            label = "请上传文件",
            type=['apk'],
            help="请选择APK文件进行上传"
        )
        # 文件上传成功
        if uploaded_file is not None:
            st.write("文件上传成功！")
        else:
            reset_session_state()
        def download():
            download_stats = 1
            if 'link' not in st.session_state:
                st.session_state['link'] = ''
            if 'QR_code' not in st.session_state:
                st.session_state['QR_code'] = None
            if 'web' not in st.session_state:
                st.session_state['web'] = ''

            download_methods = st.selectbox(
                label='下载APK',
                options=('链接下载', '二维码下载', '网页下载'),
                format_func=str,
                help='非必须,下载的APK在/apks中'
            )
            if download_methods == '链接下载':
                link = st.text_input('请输入链接')
                if link == None:
                    st.info('请输入链接')
                elif st.session_state['link'] != link:
                    st.session_state['link'] = link
                    with st.spinner('下载中...'):
                        time.sleep(2)
                        download_stats = download_apk(1, link)
                        #下载的文件保存在/data中
                        #1,2,3对应3个下载方式
                        #返回下载情况,true和false
            elif download_methods == '二维码下载':
                uploaded_image = st.file_uploader(
                    label="请上传二维码",
                    type=['jpg','png'],
                    help="限jpg,png格式"
                )
                if uploaded_image is not None:
                    QR_code = uploaded_image.getbuffer()
                    if st.session_state['QR_code'] != QR_code:
                        st.session_state['QR_code'] = QR_code
                        with st.spinner('下载中...'):
                            download_stats = download_apk(2,qrcode = QR_code)
                else:
                    st.info('请上传二维码')

            else:
                web = st.text_input('请输入网址')
                if web == None:
                    st.info('请输入网址')
                elif st.session_state['web'] != web:
                    st.session_state['web'] = web
                    with st.spinner('下载中...'):
                        time.sleep(2)
                        download_stats = download_apk(3, web)
            #print('stats:',download_stats)
            if download_stats == 0:
                st.success('下载成功')
            elif download_stats == -1:
                st.error('下载失败')
            else:
                pass

        download()
        def generate_visual_report():
            static_result = st.checkbox('静态分析结果',value = True)
            dynamic_result = st.checkbox('动态分析结果',value = True)
            if st.button('生成结果报告',help = '请勾选报告内容,报告保存在/report中'):
                if not (static_result or dynamic_result):
                    st.info('请勾选至少一项')
                elif not ((static_result == True and st.session_state['static_completed'] == False) or (dynamic_result == True and st.session_state['dynamic_completed'] == False)):
                    with st.spinner('正在生成'):
                        tool = GeneratePDF(apk_path=st.session_state['apk_path'])
                        tool.generate_report()
                        #传入可视化包含的结果,生成对应的报告
                        time.sleep(2)
                        st.session_state['report_completed'] = True
                else:
                    st.info('勾选的内容尚未分析完成')
            if st.session_state['report_completed']:
                st.success('报告已生成')
        generate_visual_report()

    if option == '静态分析':
        static_analyzer(uploaded_file)
    elif option == '动态分析':
        dynamic_analyzer()

side_bar()

#目前问题:
#1.二维码传不了路径
#2.当链接不完整时无法判断为下载失败