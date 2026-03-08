# 模型与链路组件
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableWithMessageHistory,RunnableLambda

# 环境变量
from dotenv import load_dotenv
import os 

# 项目内模块
from vector_store import VectorStoreService
import config as config
from file_history_store import get_history


load_dotenv()


# RAG 服务：检索相关文档并基于历史对话生成回答
class RagService:

    def __init__(self):

        # 初始化向量检索服务
        self.vector_store = VectorStoreService(
            embedding=OpenAIEmbeddings(
                model = config.embedding_model,
                api_key = os.getenv("OPENAI_API_KEY"),
                base_url = os.getenv("BASE_URL")
            )
        )

        # 提示词模板：包含检索上下文、历史对话和当前问题
        self.prompt_template= ChatPromptTemplate.from_messages(
            [
                ("system", "以我提供的已知参考资料为主，"
                "简洁和专业的回答用户问题。参考资料:{context}。"),
                ("system","并且我将提供用户对话的历史记录，如下"),
                MessagesPlaceholder("history"),
                ("user", "请回答用户提问: {input}")
            ]
        )

        # 初始化对话模型
        self.chat_model= ChatOpenAI(
            model = config.chat_model,
            api_key = os.getenv("OPENAI_API_KEY"),
            base_url = os.getenv("BASE_URL")
        )

        # 构建可调用链
        self.chain= self.__get_chain()


    # 构建 RAG 主链
    def __get_chain(self):
        retriever = self.vector_store.get_retriever()

        # 统一组装 prompt 所需字段：input / context / history 
        def format_func(value: dict) -> dict:
            question = value["input"]
            history = value.get("history", [])
            docs = retriever.invoke(question)

            if not docs:
                context = "无相关资料"
            else:
                formatted_str = ""
                for doc in docs:
                    formatted_str += f"文档片段：{doc.page_content}\n文档元数据：{doc.metadata}\n\n"
                context = formatted_str

            return {
                "input": question,
                "context": context,
                "history": history
            }

        # 执行顺序：参数组装 -> Prompt -> LLM -> 文本解析
        chain = (
            RunnableLambda(format_func)
            | self.prompt_template
            | self.chat_model
            | StrOutputParser()
        )


        # 包装会话记忆：根据 session_id 自动读取和写入历史
        conversation_chain = RunnableWithMessageHistory(
            chain,
            get_history,
            input_messages_key="input",
            history_messages_key="history"
        )


        return conversation_chain
