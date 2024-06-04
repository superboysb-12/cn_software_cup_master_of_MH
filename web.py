import streamlit as st
import time

st.title('ADS')
def static_analyzer():
    st.header('静态分析模式')

    # 初始化 session_state
    if 'analysis_complete' not in st.session_state:
        st.session_state['analysis_complete'] = False
    if 'recognition_complete' not in st.session_state:
        st.session_state['recognition_complete'] = False

    if st.button('开始解析'):
        if not file_uploaded:
            st.info('请先上传APK')
        else:
            try:
                #在这里对APK进行解析得到各种特征
                #将特征赋值给变量,且保存到一个临时文件temp里
                st.session_state['analysis_complete'] = True
            except Exception as e:
                st.session_state['analysis_complete'] = False
                st.exception(e)
    if st.session_state['analysis_complete'] == True:
            st.success('解析完成')

    if st.button('开始识别'):
        if st.session_state['analysis_complete'] == False:
            st.info('请先解析APK')
        else:
            try:
                #在这里调用模型,将上面的特征输入
                st.session_state['recognition_complete'] = True
            except Exception as e:
                st.session_state['recognition_complete'] = False
                st.error('识别失败')
                st.exception(e)
        if st.session_state['recognition_complete'] == True:
            st.success('识别结果为:')
def dynamic_analyzer():
    st.header('动态分析模式')
    st.write('在这里展示动态分析的信息。')

#侧栏选择分析方式
option = st.sidebar.selectbox(
    label='分析方式',
    options=['静态分析', '动态分析']
)

#文件上传

uploaded_file = st.sidebar.file_uploader(
    label = "请上传文件",
    type=['apk'],
    help="请选择APK文件进行上传"
)
# 文件上传成功
file_uploaded = False
if uploaded_file is not None:
    st.sidebar.write("文件上传成功！")
    original_apk = uploaded_file.getbuffer()
    file_uploaded = True
else:
    file_uploaded = False

if option == '静态分析':
    static_analyzer()
elif option == '动态分析':
    dynamic_analyzer()