# hash
md5_path = "./md5.text"

# chroma
chroma_name = "supermini-rag"
persist_directory = "./chroma_db"


# spliter
chunk_size = 1000 
chunk_overlap = 100
separators = ["\n\n", "\n", " ", "", ",", ".", "!", "?", "，", "。", "！", "？"]
max_split_char_num = 1000


# vector_store
similarity_threshold = 2


# model
embedding_model = "Qwen/Qwen3-Embedding-8B"
chat_model = "deepseek-ai/DeepSeek-V3.2"


# 会话配置
session_config = {
    "configurable" : {
        "session_id" : "user"
    }
}