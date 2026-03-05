# Python 标准库
import hashlib
from datetime import datetime

# LangChain 组件：向量库、Embedding 与文本切分
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 环境变量加载
from dotenv import load_dotenv
import os

# 项目配置
import config as config


load_dotenv()


# 检查内容哈希是否已存在（用于去重）
def check_md5(md5_str:str) -> bool:

    if not os.path.exists(config.md5_path):
        # 首次运行时创建哈希记录文件
        open(config.md5_path, 'w', encoding = "utf-8").close()
        return False

    else:
        # 已存在记录文件时，逐行检查是否已有相同哈希
        for line in open(config.md5_path,'r',encoding = "utf-8").readlines():
            line = line.strip()  
            if line == md5_str:
                return True

        return False


# 追加保存已入库内容的哈希值
def save_md5(md5_str:str):
    with open(config.md5_path,'a',encoding = "utf-8") as f:
        f.write(md5_str + '\n')


# 计算字符串的 MD5 哈希
def get_string_md5(input_str:str) -> str:

    # 字符串先编码为字节
    str_bytes = input_str.encode(encoding = 'utf-8')

    # 计算并返回十六进制哈希串
    md5_obj = hashlib.md5()
    md5_obj.update(str_bytes)
    md5_hex = md5_obj.hexdigest()

    return md5_hex


# 知识库写入服务：负责文本切分、向量入库和去重记录
class KnowledgeBaseService:

    def __init__(self):

        # 确保持久化目录存在
        os.makedirs(
            config.persist_directory, 
            exist_ok = True
            )

        # 初始化 Chroma 向量库（含 embedding 函数）
        self.chroma = Chroma(
            collection_name=config.chroma_name,
            embedding_function=DashScopeEmbeddings(
                model = "text-embedding-v4",
                dashscope_api_key = os.getenv("DASHSCOPE_API_KEY")
                ),
            persist_directory = config.persist_directory
        )

        # 初始化文本切分器（长文本按配置切块）
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size = config.chunk_size,
            chunk_overlap = config.chunk_overlap,
            separators = config.separators,
        )


    # 上传纯文本到向量库：去重 -> 切分 -> 入库 -> 记录哈希
    def upload_by_str(self, data:str, filename):

        # 对原文做哈希，作为幂等去重依据
        md5_hex = get_string_md5(data)

        # 已入库则直接跳过
        if check_md5(md5_hex):
            return "[跳过]文本已在知识库中"

        # 超长文本按切分器拆块；短文本直接入库
        if len(data) > config.max_split_char_num:
            knowledge_chunks : list[str] = self.spliter.split_text(data)
        else:
            knowledge_chunks = [data]

        # 每个文本块附带统一元数据
        metadata = {
            "source" : filename,
            "create_time" : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator" : "uploader",
        }

        # 将文本块写入向量库
        self.chroma.add_texts(
            knowledge_chunks,
            metadatas = [metadata for _ in knowledge_chunks]
        )

        # 记录哈希，避免重复导入
        save_md5(md5_hex)

        return "[成功]内容已成功载入向量库"
