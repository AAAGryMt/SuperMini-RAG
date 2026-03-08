# SuperMiniRAG

一个基于 **LangChain + Chroma + OpenAI-compatible API + Streamlit** 构建的极简 RAG（Retrieval-Augmented Generation）问答系统，用于对本地知识库进行检索增强问答。

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
- 基于 OpenAI-compatible API 的生成式问答
- Streamlit 可视化界面

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/AAAGryMt/SuperMini-RAG.git
cd SuperMini-RAG
```

### 2. 使用 uv 创建并同步环境

```bash
uv venv
uv sync
```

### 3. 配置环境变量

创建 `.env` 文件：

```bash
OPENAI_API_KEY=your_api_key
BASE_URL=your_api_base_url
```

### 4. 启动项目

```bash
uv run streamlit run start.py
```

## 项目结构

```bash
SuperMini-RAG/
├── start.py                 # Streamlit 入口：左侧知识库上传，右侧对话问答
├── rag.py                   # RAG 编排层：检索 + Prompt + 模型 + 历史会话
├── knowledge_base.py        # 知识入库层：文本去重、切分、向量化写入 Chroma
├── vector_store.py          # 检索适配层：封装 Chroma retriever
├── file_history_store.py    # 会话持久化层：按 session_id 存取历史消息
├── config.py                # 全局配置中心：模型名、切分参数、会话配置等
├── pyproject.toml           # 项目依赖与元信息
├── uv.lock                  # uv 锁文件（精确依赖快照）
└── .env.example             # 环境变量模板
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

- 完全依赖单一 OpenAI-compatible 模型
- 不支持多模型调度

### 工程能力

- 无用户鉴权
- 无并发控制
- 无缓存优化
- 无生产级部署支持
