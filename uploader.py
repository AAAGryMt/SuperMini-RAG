# 第三方库
import streamlit as st
import time 

# 项目内模块
from knowledge_base import KnowledgeBaseService


# 页面标题
st.title("知识库文件更新")


# 文件上传组件（仅支持单个 txt 文件）
uploader_file = st.file_uploader(
    "请上传文件",
    type = ['txt'],
    accept_multiple_files=False
)


# 将知识库服务实例持久化到会话状态，避免重复初始化
if "service" not in st.session_state:
    st.session_state["service"] = KnowledgeBaseService()


# 处理上传文件
if uploader_file is not None:

    # 读取文件基础信息
    file_name = uploader_file.name
    file_type = uploader_file.type
    file_size = uploader_file.size / 1024  # 单位：KB

    # 展示文件信息
    st.subheader(f"文件名：{file_name}")
    st.write(f"格式：{file_type}|大小：{file_size:.2f}KB")

    # 读取并展示文件内容
    text = uploader_file.getvalue().decode("utf-8")
    st.write(text)

    # 调用知识库写入并展示结果
    with st.spinner("上传中..."):
        time.sleep(0.5)
        res = st.session_state["service"].upload_by_str(data = text,filename = file_name)
        st.write(res)
