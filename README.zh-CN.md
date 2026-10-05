<!-- 本文件由 scripts/render.py 自动生成，请修改 data/*.yaml，不要直接编辑 -->
# Awesome Origen

[English](README.md)

Origen 关注的前沿技术、工程实践与工具精选。每一项都写明了**我们为什么关注它**，并用技术雷达标注团队态度。

🌐 可搜索、可筛选的交互式雷达：**https://origen-ae.github.io/awesome-origen/?lang=zh**

共 **67** 个项目： [🔭 前沿 14](docs/frontier.zh-CN.md) · [📐 实践 6](docs/practice.zh-CN.md) · [🛠 工具 47](docs/tool.zh-CN.md) · [🎯 按雷达查看](docs/radar.zh-CN.md)

- 类型: 🔭 **前沿**: 前沿模型、研究代码、论文合集 · 📐 **实践**: 工程实践、Cookbook、参考实现、教程 · 🛠 **工具**: 可直接使用的框架、平台、库
- 雷达: **采用** (adopt): 已在项目中使用，推荐默认选型 · **试用** (trial): 值得在真实项目中小范围试用 · **评估** (assess): 值得关注和调研，尚未实践 · **暂缓** (hold): 不再推荐（停更、被替代或不适配）

## 目录

- [AI Native](#ai-native) (19) — Agent、LLM 应用工程与 AI 基础设施
- [Ontology 与知识图谱](#ontology) (11) — 本体建模、语义网、图数据库、GraphRAG
- [VLM 视觉语言模型](#vlm) (11) — 多模态大模型、视觉基础模型、训练与评测
- [遥感与地理空间](#remote-sensing) (13) — 遥感基础模型、遥感智能解译、地理空间数据基础设施
- [知识库与 RAG](#knowledge-base) (13) — RAG 引擎、文档解析、向量数据库、知识库应用

<a id="ai-native"></a>

## AI Native

> Agent、LLM 应用工程与 AI 基础设施

### Agent 框架与编排

| 项目 | 类型 | 雷达 | 为什么关注 | ⭐ | 最近推送 |
|---|---|---|---|---|---|
| [microsoft/autogen](https://github.com/microsoft/autogen) | 🛠 工具 | 评估 | 多 Agent 对话式协作框架 | 61.3k | 2026-04-15 |
| [crewAIInc/crewAI](https://github.com/crewAIInc/crewAI) | 🛠 工具 | 评估 | 基于角色的多 Agent 协作 | 59.4k | 2026-10-03 |
| [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) | 🛠 工具 | 评估 | 有状态、可持久化的 Agent 图编排 | 42.7k | 2026-10-04 |
| [openai/openai-agents-python](https://github.com/openai/openai-agents-python) | 🛠 工具 | 评估 | 轻量多 Agent 框架，handoff / guardrail 设计值得参考 | 29.8k | 2026-10-05 |

### AI 编程与自主 Agent

| 项目 | 类型 | 雷达 | 为什么关注 | ⭐ | 最近推送 |
|---|---|---|---|---|---|
| [anthropics/claude-code](https://github.com/anthropics/claude-code) | 🛠 工具 | 评估 | 终端 AI 编程 Agent，skill / hook / MCP 扩展体系 | 149.4k | 2026-10-05 |
| [browser-use/browser-use](https://github.com/browser-use/browser-use) | 🛠 工具 | 评估 | 让 Agent 操作浏览器 | 117.2k | 2026-10-03 |
| [OpenHands/OpenHands](https://github.com/OpenHands/OpenHands) | 🛠 工具 | 评估 | 开源自主软件工程 Agent | 90.0k | 2026-10-05 |

### MCP 与工具生态

| 项目 | 类型 | 雷达 | 为什么关注 | ⭐ | 最近推送 |
|---|---|---|---|---|---|
| [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) | 🛠 工具 | 评估 | MCP 官方参考 Server 集合 | 91.0k | 2026-10-05 |

### LLM 应用平台

| 项目 | 类型 | 雷达 | 为什么关注 | ⭐ | 最近推送 |
|---|---|---|---|---|---|
| [n8n-io/n8n](https://github.com/n8n-io/n8n) | 🛠 工具 | 评估 | 工作流自动化，内置 AI 节点 | 206.7k | 2026-10-05 |
| [langgenius/dify](https://github.com/langgenius/dify) | 🛠 工具 | 评估 | 可视化 LLM 应用 / 工作流平台 | 157.9k | 2026-10-05 |

### 推理与部署

| 项目 | 类型 | 雷达 | 为什么关注 | ⭐ | 最近推送 |
|---|---|---|---|---|---|
| [ollama/ollama](https://github.com/ollama/ollama) | 🛠 工具 | 评估 | 本地模型一键运行 | 182.2k | 2026-10-04 |
| [vllm-project/vllm](https://github.com/vllm-project/vllm) | 🛠 工具 | 评估 | 高吞吐 LLM 推理服务 | 93.2k | 2026-10-05 |
| [sgl-project/sglang](https://github.com/sgl-project/sglang) | 🛠 工具 | 评估 | 高性能推理框架，结构化输出强 | 36.8k | 2026-10-05 |

### 观测、评测与网关

| 项目 | 类型 | 雷达 | 为什么关注 | ⭐ | 最近推送 |
|---|---|---|---|---|---|
| [BerriAI/litellm](https://github.com/BerriAI/litellm) | 🛠 工具 | 评估 | 统一多模型调用的网关 | 60.1k | 2026-10-05 |
| [langfuse/langfuse](https://github.com/langfuse/langfuse) | 🛠 工具 | 评估 | LLM 调用链观测、评测与 Prompt 管理 | 35.4k | 2026-10-05 |

### 工程实践与学习资料

| 项目 | 类型 | 雷达 | 为什么关注 | ⭐ | 最近推送 |
|---|---|---|---|---|---|
| [mlabonne/llm-course](https://github.com/mlabonne/llm-course) | 📐 实践 | 评估 | LLM 系统学习路线 | 83.3k | 2026-02-05 |
| [dair-ai/Prompt-Engineering-Guide](https://github.com/dair-ai/Prompt-Engineering-Guide) | 📐 实践 | 评估 | Prompt / Context 工程指南 | 78.8k | 2026-03-11 |
| [openai/openai-cookbook](https://github.com/openai/openai-cookbook) | 📐 实践 | 评估 | OpenAI 官方工程实践示例 | 76.4k | 2026-10-05 |
| [anthropics/claude-cookbooks](https://github.com/anthropics/claude-cookbooks) | 📐 实践 | 评估 | Claude 官方工程实践示例 | 53.2k | 2026-09-28 |

<a id="ontology"></a>

## Ontology 与知识图谱

> 本体建模、语义网、图数据库、GraphRAG

### 本体建模与语义网

| 项目 | 类型 | 雷达 | 为什么关注 | ⭐ | 最近推送 |
|---|---|---|---|---|---|
| [RDFLib/rdflib](https://github.com/RDFLib/rdflib) | 🛠 工具 | 评估 | Python RDF / SPARQL 基础库 | 2.5k | 2026-10-03 |
| [protegeproject/protege](https://github.com/protegeproject/protege) | 🛠 工具 | 评估 | 经典 OWL 本体编辑器 | 1.6k | 2026-10-01 |
| [linkml/linkml](https://github.com/linkml/linkml) | 🛠 工具 | 评估 | 用 YAML 定义数据模型 / 本体，可生成多种 schema | 645 | 2026-10-02 |

### 图数据库与三元组存储

| 项目 | 类型 | 雷达 | 为什么关注 | ⭐ | 最近推送 |
|---|---|---|---|---|---|
| [neo4j/neo4j](https://github.com/neo4j/neo4j) | 🛠 工具 | 评估 | 主流属性图数据库 | 17.3k | 2026-09-22 |
| [oxigraph/oxigraph](https://github.com/oxigraph/oxigraph) | 🛠 工具 | 评估 | Rust 实现的轻量 SPARQL 图数据库 | 2.0k | 2026-10-04 |
| [apache/jena](https://github.com/apache/jena) | 🛠 工具 | 评估 | Java 语义网框架 + Fuseki 三元组存储 | 1.5k | 2026-10-05 |

### GraphRAG 与 Agent 记忆

| 项目 | 类型 | 雷达 | 为什么关注 | ⭐ | 最近推送 |
|---|---|---|---|---|---|
| [HKUDS/LightRAG](https://github.com/HKUDS/LightRAG) | 🔭 前沿 | 评估 | 轻量 GraphRAG，支持增量更新 | 40.0k | 2026-10-03 |
| [microsoft/graphrag](https://github.com/microsoft/graphrag) | 🔭 前沿 | 评估 | 基于知识图谱的 RAG | 36.2k | 2026-10-05 |
| [getzep/graphiti](https://github.com/getzep/graphiti) | 🛠 工具 | 评估 | 时序知识图谱，适合做 Agent 记忆 | 31.4k | 2026-10-04 |
| [topoteretes/cognee](https://github.com/topoteretes/cognee) | 🛠 工具 | 评估 | 知识图谱式 Agent 记忆层 | 31.4k | 2026-10-05 |
| [OpenSPG/KAG](https://github.com/OpenSPG/KAG) | 🔭 前沿 | 评估 | 知识增强生成，逻辑推理问答 | 9.1k | 2026-01-28 |

<a id="vlm"></a>

## VLM 视觉语言模型

> 多模态大模型、视觉基础模型、训练与评测

### 开源 VLM 模型

| 项目 | 类型 | 雷达 | 为什么关注 | ⭐ | 最近推送 |
|---|---|---|---|---|---|
| [OpenBMB/MiniCPM-V](https://github.com/OpenBMB/MiniCPM-V) | 🔭 前沿 | 评估 | 端侧可部署的 VLM | 26.5k | 2026-09-08 |
| [haotian-liu/LLaVA](https://github.com/haotian-liu/LLaVA) 💤一年未更新 | 🔭 前沿 | 评估 | 视觉指令微调的奠基工作 | 25.1k | 2024-08-12 |
| [QwenLM/Qwen3-VL](https://github.com/QwenLM/Qwen3-VL) | 🔭 前沿 | 评估 | 通义千问多模态模型 | 20.0k | 2026-01-30 |
| [OpenGVLab/InternVL](https://github.com/OpenGVLab/InternVL) 💤一年未更新 | 🔭 前沿 | 评估 | 书生多模态模型系列 | 10.2k | 2025-09-22 |
| [deepseek-ai/DeepSeek-VL2](https://github.com/deepseek-ai/DeepSeek-VL2) 💤一年未更新 | 🔭 前沿 | 评估 | MoE 架构 VLM | 5.4k | 2025-02-26 |

### 视觉基础模型（分割 / 检测）

| 项目 | 类型 | 雷达 | 为什么关注 | ⭐ | 最近推送 |
|---|---|---|---|---|---|
| [facebookresearch/sam2](https://github.com/facebookresearch/sam2) | 🔭 前沿 | 评估 | 图像与视频的通用分割 | 20.0k | 2026-05-30 |
| [IDEA-Research/GroundingDINO](https://github.com/IDEA-Research/GroundingDINO) 💤一年未更新 | 🔭 前沿 | 评估 | 开放词汇目标检测 | 10.6k | 2024-08-12 |

### 训练、微调与评测

| 项目 | 类型 | 雷达 | 为什么关注 | ⭐ | 最近推送 |
|---|---|---|---|---|---|
| [hiyouga/LlamaFactory](https://github.com/hiyouga/LlamaFactory) | 🛠 工具 | 评估 | 一站式 LLM / VLM 微调 | 75.3k | 2026-09-28 |
| [modelscope/ms-swift](https://github.com/modelscope/ms-swift) | 🛠 工具 | 评估 | 魔搭大模型 / 多模态训练框架 | 15.8k | 2026-10-04 |
| [open-compass/VLMEvalKit](https://github.com/open-compass/VLMEvalKit) | 🛠 工具 | 评估 | VLM 评测工具集 | 4.4k | 2026-09-30 |

### 论文与资料合集

| 项目 | 类型 | 雷达 | 为什么关注 | ⭐ | 最近推送 |
|---|---|---|---|---|---|
| [BradyFU/Awesome-Multimodal-Large-Language-Models](https://github.com/BradyFU/Awesome-Multimodal-Large-Language-Models) | 🔭 前沿 | 评估 | 多模态大模型论文追踪 | 18.0k | 2026-10-01 |

<a id="remote-sensing"></a>

## 遥感与地理空间

> 遥感基础模型、遥感智能解译、地理空间数据基础设施

### 遥感基础模型与遥感 VLM

| 项目 | 类型 | 雷达 | 为什么关注 | ⭐ | 最近推送 |
|---|---|---|---|---|---|
| [torchgeo/terratorch](https://github.com/torchgeo/terratorch) | 🛠 工具 | 评估 | 地理空间基础模型（Prithvi 等）微调工具 | 867 | 2026-09-30 |
| [mbzuai-oryx/GeoChat](https://github.com/mbzuai-oryx/GeoChat) 💤一年未更新 | 🔭 前沿 | 评估 | 遥感领域 VLM | 759 | 2024-11-28 |
| [ChenDelong1999/RemoteCLIP](https://github.com/ChenDelong1999/RemoteCLIP) 💤一年未更新 | 🔭 前沿 | 评估 | 遥感视觉-语言基础模型 | 596 | 2024-06-27 |

### 遥感深度学习工具

| 项目 | 类型 | 雷达 | 为什么关注 | ⭐ | 最近推送 |
|---|---|---|---|---|---|
| [torchgeo/torchgeo](https://github.com/torchgeo/torchgeo) | 🛠 工具 | 评估 | PyTorch 地理空间数据集 / 采样器 / 模型 | 4.2k | 2026-10-04 |
| [opengeos/segment-geospatial](https://github.com/opengeos/segment-geospatial) | 🛠 工具 | 评估 | SAM 用于遥感影像分割 | 4.2k | 2026-09-28 |
| [open-mmlab/mmrotate](https://github.com/open-mmlab/mmrotate) 💤一年未更新 | 🛠 工具 | 评估 | 旋转目标检测（遥感常用） | 2.2k | 2024-09-28 |

### 地理空间数据基础设施

| 项目 | 类型 | 雷达 | 为什么关注 | ⭐ | 最近推送 |
|---|---|---|---|---|---|
| [OSGeo/gdal](https://github.com/OSGeo/gdal) | 🛠 工具 | 评估 | 栅格 / 矢量数据处理基石 | 6.1k | 2026-10-03 |
| [opengeos/leafmap](https://github.com/opengeos/leafmap) | 🛠 工具 | 评估 | Notebook 里的交互式地图分析 | 3.8k | 2026-09-28 |
| [rasterio/rasterio](https://github.com/rasterio/rasterio) | 🛠 工具 | 评估 | Pythonic 栅格数据读写 | 2.6k | 2026-10-02 |
| [developmentseed/titiler](https://github.com/developmentseed/titiler) | 🛠 工具 | 评估 | 动态瓦片服务（COG / STAC） | 1.2k | 2026-10-03 |
| [stac-utils/pystac](https://github.com/stac-utils/pystac) | 🛠 工具 | 评估 | STAC 时空资产目录标准 | 465 | 2026-10-01 |

### 论文与资料合集

| 项目 | 类型 | 雷达 | 为什么关注 | ⭐ | 最近推送 |
|---|---|---|---|---|---|
| [satellite-image-deep-learning/techniques](https://github.com/satellite-image-deep-learning/techniques) | 📐 实践 | 评估 | 卫星影像深度学习技术汇总 | 10.3k | 2026-09-26 |
| [Jack-bo1220/Awesome-Remote-Sensing-Foundation-Models](https://github.com/Jack-bo1220/Awesome-Remote-Sensing-Foundation-Models) | 🔭 前沿 | 评估 | 遥感基础模型论文合集 | 1.9k | 2026-05-07 |

<a id="knowledge-base"></a>

## 知识库与 RAG

> RAG 引擎、文档解析、向量数据库、知识库应用

### RAG 引擎与框架

| 项目 | 类型 | 雷达 | 为什么关注 | ⭐ | 最近推送 |
|---|---|---|---|---|---|
| [infiniflow/ragflow](https://github.com/infiniflow/ragflow) | 🛠 工具 | 评估 | 深度文档理解的 RAG 引擎 | 91.7k | 2026-10-04 |
| [run-llama/llama_index](https://github.com/run-llama/llama_index) | 🛠 工具 | 评估 | 数据接入与检索框架 | 52.4k | 2026-10-01 |
| [deepset-ai/haystack](https://github.com/deepset-ai/haystack) | 🛠 工具 | 评估 | 生产级 RAG / 搜索管线 | 26.7k | 2026-10-05 |

### 文档解析

| 项目 | 类型 | 雷达 | 为什么关注 | ⭐ | 最近推送 |
|---|---|---|---|---|---|
| [microsoft/markitdown](https://github.com/microsoft/markitdown) | 🛠 工具 | 评估 | Office / PDF 等文件转 Markdown | 188.5k | 2026-10-04 |
| [PaddlePaddle/PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) | 🛠 工具 | 评估 | 多语种 OCR 与版面分析 | 90.6k | 2026-09-16 |
| [opendatalab/MinerU](https://github.com/opendatalab/MinerU) | 🛠 工具 | 评估 | PDF → Markdown，公式 / 表格识别强 | 81.1k | 2026-09-30 |
| [docling-project/docling](https://github.com/docling-project/docling) | 🛠 工具 | 评估 | IBM 文档解析与转换 | 68.4k | 2026-10-05 |

### 向量数据库

| 项目 | 类型 | 雷达 | 为什么关注 | ⭐ | 最近推送 |
|---|---|---|---|---|---|
| [milvus-io/milvus](https://github.com/milvus-io/milvus) | 🛠 工具 | 评估 | 分布式向量数据库 | 46.3k | 2026-10-05 |
| [qdrant/qdrant](https://github.com/qdrant/qdrant) | 🛠 工具 | 评估 | Rust 向量数据库，过滤检索强 | 34.9k | 2026-10-05 |

### 知识库应用

| 项目 | 类型 | 雷达 | 为什么关注 | ⭐ | 最近推送 |
|---|---|---|---|---|---|
| [open-webui/open-webui](https://github.com/open-webui/open-webui) | 🛠 工具 | 评估 | 自托管 AI 对话 + 知识库界面 | 154.0k | 2026-10-05 |
| [Mintplex-Labs/anything-llm](https://github.com/Mintplex-Labs/anything-llm) | 🛠 工具 | 评估 | 一体化私有知识库应用 | 66.7k | 2026-10-04 |
| [labring/FastGPT](https://github.com/labring/FastGPT) | 🛠 工具 | 评估 | 知识库问答 + 工作流编排 | 29.8k | 2026-10-01 |

### RAG 工程实践

| 项目 | 类型 | 雷达 | 为什么关注 | ⭐ | 最近推送 |
|---|---|---|---|---|---|
| [NirDiamant/RAG_Techniques](https://github.com/NirDiamant/RAG_Techniques) | 📐 实践 | 评估 | RAG 进阶技巧 Notebook 合集 | 29.7k | 2026-09-21 |

## 贡献

见 [CONTRIBUTING.zh-CN.md](CONTRIBUTING.zh-CN.md)。最简单的方式：用 **推荐项目 / Recommend a project** 模板新建 issue 并贴上 GitHub 链接，或者在本仓库中使用 Claude Code 的 `/curate add <url>`。
