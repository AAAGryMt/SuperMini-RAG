# LangChain 组件：向量库
from langchain_chroma import Chroma

# 项目内模块
import config as config 


# 向量存储服务：负责初始化 Chroma 并提供统一检索入口
class VectorStoreService:

    # 初始化向量库连接（集合名、向量模型、持久化目录）
    def __init__(self, embedding):
        self.embedding = embedding

        self.vector_store = Chroma(
            collection_name = config.chroma_name,
            embedding_function = self.embedding,
            persist_directory = config.persist_directory
        )

    # 返回 retriever：
    # 输入 query 后会做向量相似度检索，并返回 top-k 文档片段
    # 其中 k 由 search_kwargs 控制（返回结果数量）
    def get_retriever(self):
        return self.vector_store.as_retriever(
            search_kwargs = {"k" : config.similarity_threshold}
            )
