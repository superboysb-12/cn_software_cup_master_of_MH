import streamlit as st
import time
import pandas as pd
from PIL import Image
from util import *
from dynamic_analysis import PacketCapture
from AnalysisTool import AnalysisTool
from androguard.util import  set_log

#streamlit run web.py

if "log_set" not in st.session_state:
    set_log("ERROR")  # set log message only ERROR
    st.session_state['log_set'] = True

st.title('ADS')
if 'AnalysisTool' not in st.session_state:
    st.session_state['AnalysisTool'] = AnalysisTool()

def highlight_dangerous(s):
    return ['background-color: red' if 'dangerous' in v else '' for v in s]

# 重置分析状态的函数
def reset_session_state():
    st.session_state['static_completed'] = False
    st.session_state['dynamic_completed'] = False
    st.session_state['report_completed'] = False
    st.session_state['download_stats'] = 1
    st.session_state['progress'] = 0
    st.session_state['df1'] = pd.DataFrame()
    st.session_state['df2'] = pd.DataFrame()
    st.session_state['df3'] = pd.DataFrame()
    st.session_state['df4'] = pd.DataFrame()
    st.session_state['df5'] = pd.DataFrame()
    st.session_state['image'] = None

def static_analyzer(uploaded_file):
    # 初始化 session_state
    if 'static_analysis' not in st.session_state:
        st.session_state['static_analysis'] = False

    if 'static_progress' not in st.session_state or st.session_state['static_progress'] == 1:
        st.session_state['static_progress'] = []

    static_progress_state = st.empty()

    def static_callback():
        message = ''.join(st.session_state['static_progress'])
        #static_progress_state.write(message)


    st.header('静态分析模式')
    if st.button('开始分析'):
        if st.session_state['AnalysisTool'].target_apk is None:
            st.info('请先上传APK')
        else:
            with st.spinner('分析中...'):
                (st.session_state['df1'],st.session_state['df2'],st.session_state['df3'],st.session_state['df4'],st.session_state['df5'],st.session_state['image']),st.session_state['apk_path'] = st.session_state['AnalysisTool'].get_static_analysis_information(static_callback)
                st.session_state['image']=st.session_state['image'][0]

            st.session_state['static_analysis'] = True
            st.session_state['static_completed'] = True



    if st.session_state['static_completed'] == True:
        def data_visualization(df1,df2,df3,df4,df5,image):
            st.image(image,
                     caption='APP图像',
                     width=100
                     )
            data_option = st.selectbox(
                index=0,
                label='分析结果',
                options=['基本信息', '应用权限','通联地址','Class','Activity']
            )
            if data_option == '基本信息':
                st.write(df1)
            elif data_option == '应用权限':
                st.dataframe(st.session_state['df2'].style.apply(highlight_dangerous, subset=['Security']))
            elif data_option == '通联地址':
                st.dataframe(st.session_state['df3'].style.apply(highlight_dangerous, subset=['Security']))
            elif data_option == 'Class':
                st.write(df4)
            else:
                st.write(df5)

        data_visualization(st.session_state['df1'],
                           st.session_state['df2'],
                           st.session_state['df3'],
                           st.session_state['df4'],
                           st.session_state['df5'],
                           st.session_state['image'],
                           )

    if st.button('涉诈识别'):
        if st.session_state['static_analysis'] == False:
            st.info('请先完成APK分析')
        else:
            st.session_state['AnalysisTool'].classify_two_label()
            st.success(str(st.session_state['AnalysisTool'].get_label()[0]) + " 置信度:" + str(st.session_state['AnalysisTool'].get_label()[1]))
    if st.button('APP分类识别'):
        if st.session_state['static_analysis'] == False:
            st.info('请先完成APK分析')
        else:
            st.session_state['AnalysisTool'].classify_five_label()
            st.success(str(st.session_state['AnalysisTool'].get_label()[2]))





def dynamic_analyzer():
    if 'dynamic_completed' not in st.session_state:
        st.session_state['dynamic_completed'] = False
    if 'capturing' not in st.session_state:
        st.session_state['capturing'] = 0
    if 'capture_pkts' not in st.session_state:
        st.session_state['capture_pkts'] = None

    st.header('动态分析模式')
    show_pkts = st.empty()

    # Create packet capture object
    if 'capture_thread' not in st.session_state:
        st.session_state['capture_thread'] = PacketCapture()

    if st.button('开始抓包'):
        st.session_state['AnalysisTool'].dynamic_analysis()
        st.session_state['capturing'] = 1
        if not st.session_state['capture_thread'].is_alive():
            st.session_state['capture_thread'].start()

    if st.session_state['capture_thread']:
        st.session_state['capture_pkts'] = st.session_state['capture_thread'].get_data()
        show_pkts.write(st.session_state['capture_pkts'])

        if st.session_state['capturing'] == 1:
            if st.button('停止抓包'):
                st.session_state['capture_thread'].stop()
                st.info('已停止抓包')
                st.session_state['capturing'] = 2
                st.session_state['capture_thread'].join()#等待退出

    if st.session_state['capturing'] == 1:
        st.info('正在抓包')

    # 实时更新抓包数据显示
    while st.session_state['capturing'] == 1:
        st.session_state['capture_pkts'] = st.session_state['capture_thread'].get_data()  # 获取最新抓包数据
        show_pkts.write(st.session_state['capture_pkts'])  # 更新显示最新抓包数据
        time.sleep(1)  # 调整间隔时间，以控制实时显示频率

    # 停止抓包后
    if st.session_state['capturing'] == 2:
        show_pkts.write(st.session_state['capture_pkts'])  # 显示最终抓包数据

        IPs = st.session_state['capture_pkts'][st.session_state['capture_pkts'].columns[2]].value_counts()
        st.write(IPs)

        st.session_state['dynamic_completed'] = True

        if st.button('添加到黑/白名单'):
            #add_list(IPs)
            st.success('添加成功')
            pass



def adlist():
    list = namelist()
    list_name = st.text_input('名单名称')
    if st.button('新建名单'):
        list.add_tables(list_name)


    IP = st.text_input('IP')
    URL = st.text_input('URL')
    option = st.selectbox(
        label='黑白名单',
        options=list.show_tables()
    )
    if st.button('添加至该名单'):
        list.add_list(IP,URL,option)
        st.success('添加成功')

    st.write(list.get_list(option))


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
            label='分析方式/黑白名单',
            options=['静态分析', '动态分析','黑白名单']
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
            st.session_state['AnalysisTool'].load_apk_data(uploaded_file.getbuffer())

        def download():
            if 'progress' not in st.session_state:
                st.session_state['progress'] = 0
            def progress_callback():
                progress_bar.progress(st.session_state['progress'])

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
            if 'download_method' not in st.session_state:
                st.session_state['download_method'] = 0

            if download_methods == '链接下载':
                link = st.text_input('请输入链接')
                if link == None:
                    st.info('请输入链接')
                elif st.session_state['link'] != link:
                    st.session_state['download_method'] = 1
                    st.session_state['link'] = link

            elif download_methods == '二维码下载':
                uploaded_image = st.file_uploader(
                    label="请上传二维码",
                    type=['jpg','png'],
                    help="限jpg,png格式"
                )
                if uploaded_image is not None:
                    QR_code = uploaded_image.getbuffer()
                    if st.session_state['QR_code'] != QR_code:
                        st.session_state['download_method'] = 2
                        st.session_state['QR_code'] = QR_code
                else:
                    st.info('请上传二维码')

            else:
                web = st.text_input('请输入网址')
                if web == None:
                    st.info('请输入网址')
                elif st.session_state['web'] != web:
                    st.session_state['download_method'] = 3
                    st.session_state['web'] = web

            progress_bar = st.empty()
            if st.button('开始下载'):
                if st.session_state['download_method'] == 0:
                    st.info('')
                elif st.session_state['download_method'] == 1:
                    st.session_state['download_stats'] = download_apk(1, st.session_state['link'], progress_callback=progress_callback)
                elif st.session_state['download_method'] ==2:
                    st.session_state['download_stats'] = download_apk(2, st.session_state['QR_code'], progress_callback=progress_callback)
                elif st.session_state['download_method'] ==3:
                    st.session_state['download_stats'] = download_apk(3, st.session_state['web'], progress_callback=progress_callback)
            if 'download_stats' not in st.session_state:
                st.session_state['download_stats'] = 1
            if st.session_state['download_stats'] == 0:
                st.success('下载成功')
            elif st.session_state['download_stats'] == -1:
                st.error('下载失败')
            else:
                pass

            chosen_file = st.selectbox("请选择文件",
                st.session_state['AnalysisTool'].list_downloaded_apks()
            )
            st.session_state['AnalysisTool'].select_downloaded_apk(chosen_file)

        download()
        def generate_visual_report():
            static_result = st.checkbox('静态分析结果',value = True)
            dynamic_result = st.checkbox('动态分析结果',value = True)
            if st.button('生成结果报告',help = '请勾选报告内容,报告保存在/report中'):
                if not (static_result or dynamic_result):
                    st.info('请勾选至少一项')
                elif not ((static_result == True and st.session_state['AnalysisTool'].static_analysis_finished == False) or (dynamic_result == True and st.session_state['AnalysisTool'].dynamic_analysis_finished == False)):
                    with st.spinner('正在生成'):
                        st.session_state['AnalysisTool'].generate_pdf(static_result,dynamic_result)
                        #传入可视化包含的结果,生成对应的报告
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
    else:
        adlist()

side_bar()