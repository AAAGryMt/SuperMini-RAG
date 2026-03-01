# Python 标准库
import json
import os
from typing import List, Sequence

# LangChain 组件库
from langchain_core.messages import BaseMessage, message_to_dict, messages_from_dict
from langchain_core.chat_history import BaseChatMessageHistory


# 文件历史存储模块：
# 将 LangChain 的会话消息持久化到本地 JSON 文件，按 session_id 隔离。


# 根据 session_id 返回对应会话历史对象
def get_history(session_id: str):
    return FileChatMessageHistory(storage_path="./chat_history", session_id=session_id)


# 基于文件系统的消息历史实现
class FileChatMessageHistory(BaseChatMessageHistory):

    def __init__(self, storage_path: str, session_id: str):
        self.session_id = session_id
        self.storage_path = storage_path
        self.file_path = os.path.join(self.storage_path, self.session_id)
        # 确保存储目录存在
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    # 统一落盘入口：BaseMessage 列表 -> dict 列表 -> JSON 文件
    def _save_messages(self, messages: List[BaseMessage]) -> None:
        new_messages = [message_to_dict(m) for m in messages]
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(new_messages, f)

    # 追加单条消息
    def add_message(self, message: BaseMessage) -> None:
        all_messages = list(self.messages)
        all_messages.append(message)
        self._save_messages(all_messages)

    # 批量追加消息
    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        all_messages = list(self.messages)
        all_messages.extend(messages)
        self._save_messages(all_messages)

    # 读取当前会话的全部消息
    @property
    def messages(self) -> List[BaseMessage]:
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                messages_data = json.load(f)
                return messages_from_dict(messages_data)
        except FileNotFoundError:
            return []

    # 清空当前会话历史
    def clear(self) -> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([], f)
