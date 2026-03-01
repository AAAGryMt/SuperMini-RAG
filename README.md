# SuperMiniRAG

一个基于 **LangChain + Chroma + 通义千问 + Streamlit** 构建的极简 RAG（Retrieval-Augmented Generation）问答系统，用于对本地知识库进行检索增强问答。

## 项目简介

SuperMiniRAG 是一个轻量级本地知识问答系统，支持：

- 文档上传
- 自动切分
- 向量化存储
- 相似度检索
- 基于大模型的上下文增强问答

## 功能特性

- 文档加载（支持常见文本格式）
- 文本切分（Chunk 切分）
- 向量数据库构建（Chroma）
- 语义相似度检索
- 基于通义千问的生成式问答
- Streamlit 可视化界面

## 快速开始

### 1.克隆项目

```bash
git clone https://github.com/AAAGryMt/SuperMini-RAG.git
cd SuperMiniRAG
```

### 2.创建虚拟环境

```bash
python -m venv venv
source venv/bin/activate  # macOS / Linux
venv\Scripts\activate     # Windows
```

### 3.安装依赖

```bash
pip install -r requirements.txt
```

### 4.配置环境变量

创建 `.env` 文件：

```
DASHSCOPE_API_KEY=your_api_key
```

### 5.启动项目

1. 在此上传 txt 文件加入本地知识库

```bash
streamlit run app_file_uploader.py
```

2. 进入聊天界面

```bash
streamlit run chat.py
```

## 项目结构

```bash
SuperMiniRAG/
├── chat.py                  # Streamlit 对话入口：承载聊天 UI，调用 RAG 链并流式输出
├── app_file_uploader.py     # Streamlit 知识库管理入口：上传 txt 并写入向量库
├── rag.py                   # RAG 编排层：组装“检索 + Prompt + 模型 + 会话历史”主链
├── knowledge_base.py        # 知识入库层：文本去重、切分、向量化写入 Chroma
├── vector_store.py          # 检索适配层：封装 Chroma retriever 及检索参数
├── file_history_store.py    # 会话持久化层：按 session_id 将消息历史落盘到本地文件
├── config_data.py           # 全局配置中心：模型名、切分参数、向量库路径、会话配置
├── requirements.txt         # Python 依赖清单
├── .gitignore               # Git 忽略规则
└── .env                     # 本地环境变量
```

## 能力边界

本项目属于最小 RAG 实现，目前存在以下限制：

### 检索能力

- 基于向量相似度
- 不支持复杂结构化查询
- 不支持混合检索（BM25 + Dense）

### 数据规模

- 只适合中小型文档集合

### 生成能力

- 完全依赖通义千问
- 不支持多模型调度

### 工程能力

- 无用户鉴权
- 无并发控制
- 无缓存优化
- 无生产级部署支持
