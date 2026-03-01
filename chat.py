# 第三方库
import streamlit as st

# 项目内模块
from rag import RagService
import config_data as config


# 页面基础信息
st.title("SuperMini-RAG")
st.divider()


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
