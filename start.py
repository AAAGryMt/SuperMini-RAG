# 第三方库
import streamlit as st
import time
import hashlib
from datetime import datetime


# 项目内模块
from rag import RagService
import config as config
from knowledge_base import KnowledgeBaseService


# 页面基础信息
st.title("SuperMini-RAG")
st.divider()
col1, col2 = st.columns([1,2])


with col1:
    st.subheader("知识库文件更新")

    # 文件上传组件（仅支持单个 txt 文件）
    uploader_file = st.file_uploader(
        "请上传文件",
        type = ['txt'],
        accept_multiple_files=False
    )

    # 将知识库服务实例持久化到会话状态，避免重复初始化
    if "service" not in st.session_state:
        st.session_state["service"] = KnowledgeBaseService()

    # 持久化保留上传记录至前端页面
    if "uploaded_files" not in st.session_state:
        st.session_state["uploaded_files"] = []

    if "uploaded_file_ids" not in st.session_state:
        st.session_state["uploaded_file_ids"] = set()

    # 处理上传文件
    if uploader_file is not None:

        # 读取文件基础信息
        file_name = uploader_file.name
        file_type = uploader_file.type
        file_size = uploader_file.size / 1024  # 单位：KB

        # 读取并展示文件内容
        text = uploader_file.getvalue().decode("utf-8")

        # 构建去重标识，避免 Streamlit rerun 重复处理同一文件
        file_md5 = hashlib.md5(text.encode("utf-8")).hexdigest()
        upload_id = f"{file_name}:{uploader_file.size}:{file_md5}"

        if upload_id not in st.session_state["uploaded_file_ids"]:
            # 调用知识库写入并展示结果
            with st.spinner("上传中..."):
                time.sleep(0.5)
                res = st.session_state["service"].upload_by_str(data = text,filename = file_name)

            st.session_state["uploaded_file_ids"].add(upload_id)
            st.session_state["uploaded_files"].append(
                {
                    "name": file_name,
                    "type": file_type,
                    "size_kb": round(file_size, 2),
                    "status": res,
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
            )

    # 固定展示上传历史（前端会话内持久化）
    st.subheader("已上传文件")
    if st.session_state["uploaded_files"]:
        st.dataframe(st.session_state["uploaded_files"])
    else:
        st.caption("暂无上传记录")


with col2:
    # 初始化会话消息（用于前端聊天记录回放）
    if "message" not in st.session_state:
        st.session_state["message"] = [
            {"role": "assistant", "content": "你好，有什么可以帮助你？"}
        ]

    # 初始化 RAG 服务实例（每个会话复用）
    if "rag" not in st.session_state:
        st.session_state["rag"] = RagService()

    # 回放历史消息
    for mes in st.session_state["message"]:
        st.chat_message(mes["role"]).write(mes["content"])

    # 用户输入框
    prompt = st.chat_input()

    if prompt:
        # 展示并缓存用户输入
        st.chat_message("user").write(prompt)
        st.session_state["message"].append(
            {"role": "user", "content": prompt}
        )

        # 缓存流式输出分片，便于最终拼接完整回复入历史
        res_list = []
        with st.spinner("祈祷中..."):
            # 以流式方式调用 RAG 链
            res_stream = st.session_state["rag"].chain.stream(
                {"input": prompt},
                config.session_config
            )

            # 在转发分片给前端的同时，保留一份副本
            def capture(generator, cache_list):
                for chunk in generator:
                    cache_list.append(chunk)
                    yield chunk

            # 渲染 assistant 的流式回复
            st.chat_message("assistant").write_stream(capture(res_stream, res_list))

            # 将完整回复写入会话消息，供下次页面刷新回放
            st.session_state["message"].append(
                {
                    "role": "assistant",
                    "content": "".join(res_list)
                }
            )
