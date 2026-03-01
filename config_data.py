# hash
md5_path = "./md5.text"

# chroma
chroma_name = "mini-rag"
persist_directory = "./chroma_db"


# spliter
chunk_size = 1000 
chunk_overlap = 100
separators = ["\n\n", "\n", " ", "", ",", ".", "!", "?", "，", "。", "！", "？"]
max_split_char_num = 1000


# vector_store
similarity_threshold = 2


# model
embedding_model_name = "text-embedding-v4"
chat_model = "qwen3-max"


# 会话配置
session_config = {
    "configurable" : {
        "session_id" : "user"
    }
}