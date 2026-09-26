<!-- 本文件由 scripts/render.py 自动生成，请修改 data/*.yaml，不要直接编辑 -->
# Awesome Origen

Origen 关注的前沿技术、工程实践与工具精选。每一项都写明了**我们为什么关注它**，并用技术雷达标注团队态度。

共 **67** 个项目：[🔭 前沿 14](docs/frontier.md) · [📐 实践 6](docs/practice.md) · [🛠 工具 47](docs/tool.md) · [🎯 按雷达查看](docs/radar.md)

- 类型：🔭 **前沿**：前沿模型、研究代码、论文合集 · 📐 **实践**：工程实践、Cookbook、参考实现、教程 · 🛠 **工具**：可直接使用的框架、平台、库
- 雷达：**采用**（adopt）：已在项目中使用，推荐默认选型 · **试用**（trial）：值得在真实项目中小范围试用 · **评估**（assess）：值得关注和调研，尚未实践 · **暂缓**（hold）：不再推荐（停更、被替代或不适配）

## 目录

- [AI Native](#ai-native)（19）— Agent、LLM 应用工程与 AI 基础设施
- [Ontology 与知识图谱](#ontology)（11）— 本体建模、语义网、图数据库、GraphRAG
- [VLM 视觉语言模型](#vlm)（11）— 多模态大模型、视觉基础模型、训练与评测
- [遥感与地理空间](#remote-sensing)（13）— 遥感基础模型、遥感智能解译、地理空间数据基础设施
- [知识库与 RAG](#knowledge-base)（13）— RAG 引擎、文档解析、向量数据库、知识库应用

<a id="ai-native"></a>

## AI Native

> Agent、LLM 应用工程与 AI 基础设施

### Agent 框架与编排

| 项目 | 类型 | 雷达 | 为什么关注 | ⭐ | 最近推送 |
|---|---|---|---|---|---|
| [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) | 🛠 工具 | 评估 | 有状态、可持久化的 Agent 图编排 | 42.3k | 2026-09-26 |
| [openai/openai-agents-python](https://github.com/openai/openai-agents-python) | 🛠 工具 | 评估 | 轻量多 Agent 框架，handoff / guardrail 设计值得参考 | - | - |
| [microsoft/autogen](https://github.com/microsoft/autogen) | 🛠 工具 | 评估 | 多 Agent 对话式协作框架 | - | - |
| [crewAIInc/crewAI](https://github.com/crewAIInc/crewAI) | 🛠 工具 | 评估 | 基于角色的多 Agent 协作 | - | - |

### AI 编程与自主 Agent

| 项目 | 类型 | 雷达 | 为什么关注 | ⭐ | 最近推送 |
|---|---|---|---|---|---|
| [OpenHands/OpenHands](https://github.com/OpenHands/OpenHands) | 🛠 工具 | 评估 | 开源自主软件工程 Agent | 89.2k | 2026-09-26 |
| [anthropics/claude-code](https://github.com/anthropics/claude-code) | 🛠 工具 | 评估 | 终端 AI 编程 Agent，skill / hook / MCP 扩展体系 | - | - |
| [browser-use/browser-use](https://github.com/browser-use/browser-use) | 🛠 工具 | 评估 | 让 Agent 操作浏览器 | - | - |

### MCP 与工具生态

| 项目 | 类型 | 雷达 | 为什么关注 | ⭐ | 最近推送 |
|---|---|---|---|---|---|
| [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) | 🛠 工具 | 评估 | MCP 官方参考 Server 集合 | - | - |

### LLM 应用平台

| 项目 | 类型 | 雷达 | 为什么关注 | ⭐ | 最近推送 |
|---|---|---|---|---|---|
| [langgenius/dify](https://github.com/langgenius/dify) | 🛠 工具 | 评估 | 可视化 LLM 应用 / 工作流平台 | - | - |
| [n8n-io/n8n](https://github.com/n8n-io/n8n) | 🛠 工具 | 评估 | 工作流自动化，内置 AI 节点 | - | - |

### 推理与部署

| 项目 | 类型 | 雷达 | 为什么关注 | ⭐ | 最近推送 |
|---|---|---|---|---|---|
| [vllm-project/vllm](https://github.com/vllm-project/vllm) | 🛠 工具 | 评估 | 高吞吐 LLM 推理服务 | - | - |
| [sgl-project/sglang](https://github.com/sgl-project/sglang) | 🛠 工具 | 评估 | 高性能推理框架，结构化输出强 | - | - |
| [ollama/ollama](https://github.com/ollama/ollama) | 🛠 工具 | 评估 | 本地模型一键运行 | - | - |

### 观测、评测与网关

| 项目 | 类型 | 雷达 | 为什么关注 | ⭐ | 最近推送 |
|---|---|---|---|---|---|
| [BerriAI/litellm](https://github.com/BerriAI/litellm) | 🛠 工具 | 评估 | 统一多模型调用的网关 | - | - |
| [langfuse/langfuse](https://github.com/langfuse/langfuse) | 🛠 工具 | 评估 | LLM 调用链观测、评测与 Prompt 管理 | - | - |

### 工程实践与学习资料

| 项目 | 类型 | 雷达 | 为什么关注 | ⭐ | 最近推送 |
|---|---|---|---|---|---|
| [anthropics/claude-cookbooks](https://github.com/anthropics/claude-cookbooks) | 📐 实践 | 评估 | Claude 官方工程实践示例 | 53.0k | 2026-09-24 |
| [openai/openai-cookbook](https://github.com/openai/openai-cookbook) | 📐 实践 | 评估 | OpenAI 官方工程实践示例 | - | - |
| [dair-ai/Prompt-Engineering-Guide](https://github.com/dair-ai/Prompt-Engineering-Guide) | 📐 实践 | 评估 | Prompt / Context 工程指南 | - | - |
| [mlabonne/llm-course](https://github.com/mlabonne/llm-course) | 📐 实践 | 评估 | LLM 系统学习路线 | - | - |

<a id="ontology"></a>

## Ontology 与知识图谱

> 本体建模、语义网、图数据库、GraphRAG

### 本体建模与语义网

| 项目 | 类型 | 雷达 | 为什么关注 | ⭐ | 最近推送 |
|---|---|---|---|---|---|
| [protegeproject/protege](https://github.com/protegeproject/protege) | 🛠 工具 | 评估 | 经典 OWL 本体编辑器 | - | - |
| [linkml/linkml](https://github.com/linkml/linkml) | 🛠 工具 | 评估 | 用 YAML 定义数据模型 / 本体，可生成多种 schema | - | - |
| [RDFLib/rdflib](https://github.com/RDFLib/rdflib) | 🛠 工具 | 评估 | Python RDF / SPARQL 基础库 | - | - |

### 图数据库与三元组存储

| 项目 | 类型 | 雷达 | 为什么关注 | ⭐ | 最近推送 |
|---|---|---|---|---|---|
| [apache/jena](https://github.com/apache/jena) | 🛠 工具 | 评估 | Java 语义网框架 + Fuseki 三元组存储 | - | - |
| [oxigraph/oxigraph](https://github.com/oxigraph/oxigraph) | 🛠 工具 | 评估 | Rust 实现的轻量 SPARQL 图数据库 | - | - |
| [neo4j/neo4j](https://github.com/neo4j/neo4j) | 🛠 工具 | 评估 | 主流属性图数据库 | - | - |

### GraphRAG 与 Agent 记忆

| 项目 | 类型 | 雷达 | 为什么关注 | ⭐ | 最近推送 |
|---|---|---|---|---|---|
| [microsoft/graphrag](https://github.com/microsoft/graphrag) | 🔭 前沿 | 评估 | 基于知识图谱的 RAG | - | - |
| [HKUDS/LightRAG](https://github.com/HKUDS/LightRAG) | 🔭 前沿 | 评估 | 轻量 GraphRAG，支持增量更新 | - | - |
| [OpenSPG/KAG](https://github.com/OpenSPG/KAG) | 🔭 前沿 | 评估 | 知识增强生成，逻辑推理问答 | - | - |
| [getzep/graphiti](https://github.com/getzep/graphiti) | 🛠 工具 | 评估 | 时序知识图谱，适合做 Agent 记忆 | - | - |
| [topoteretes/cognee](https://github.com/topoteretes/cognee) | 🛠 工具 | 评估 | 知识图谱式 Agent 记忆层 | - | - |

<a id="vlm"></a>

## VLM 视觉语言模型

> 多模态大模型、视觉基础模型、训练与评测

### 开源 VLM 模型

| 项目 | 类型 | 雷达 | 为什么关注 | ⭐ | 最近推送 |
|---|---|---|---|---|---|
| [OpenBMB/MiniCPM-V](https://github.com/OpenBMB/MiniCPM-V) | 🔭 前沿 | 评估 | 端侧可部署的 VLM | 26.5k | 2026-09-08 |
| [QwenLM/Qwen3-VL](https://github.com/QwenLM/Qwen3-VL) | 🔭 前沿 | 评估 | 通义千问多模态模型 | 20.0k | 2026-01-30 |
| [OpenGVLab/InternVL](https://github.com/OpenGVLab/InternVL) | 🔭 前沿 | 评估 | 书生多模态模型系列 | - | - |
| [deepseek-ai/DeepSeek-VL2](https://github.com/deepseek-ai/DeepSeek-VL2) | 🔭 前沿 | 评估 | MoE 架构 VLM | - | - |
| [haotian-liu/LLaVA](https://github.com/haotian-liu/LLaVA) | 🔭 前沿 | 评估 | 视觉指令微调的奠基工作 | - | - |

### 视觉基础模型（分割 / 检测）

| 项目 | 类型 | 雷达 | 为什么关注 | ⭐ | 最近推送 |
|---|---|---|---|---|---|
| [facebookresearch/sam2](https://github.com/facebookresearch/sam2) | 🔭 前沿 | 评估 | 图像与视频的通用分割 | - | - |
| [IDEA-Research/GroundingDINO](https://github.com/IDEA-Research/GroundingDINO) | 🔭 前沿 | 评估 | 开放词汇目标检测 | - | - |

### 训练、微调与评测

| 项目 | 类型 | 雷达 | 为什么关注 | ⭐ | 最近推送 |
|---|---|---|---|---|---|
| [hiyouga/LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory) | 🛠 工具 | 评估 | 一站式 LLM / VLM 微调 | - | - |
| [modelscope/ms-swift](https://github.com/modelscope/ms-swift) | 🛠 工具 | 评估 | 魔搭大模型 / 多模态训练框架 | - | - |
| [open-compass/VLMEvalKit](https://github.com/open-compass/VLMEvalKit) | 🛠 工具 | 评估 | VLM 评测工具集 | - | - |

### 论文与资料合集

| 项目 | 类型 | 雷达 | 为什么关注 | ⭐ | 最近推送 |
|---|---|---|---|---|---|
| [BradyFU/Awesome-Multimodal-Large-Language-Models](https://github.com/BradyFU/Awesome-Multimodal-Large-Language-Models) | 🔭 前沿 | 评估 | 多模态大模型论文追踪 | - | - |

<a id="remote-sensing"></a>

## 遥感与地理空间

> 遥感基础模型、遥感智能解译、地理空间数据基础设施

### 遥感基础模型与遥感 VLM

| 项目 | 类型 | 雷达 | 为什么关注 | ⭐ | 最近推送 |
|---|---|---|---|---|---|
| [mbzuai-oryx/GeoChat](https://github.com/mbzuai-oryx/GeoChat) | 🔭 前沿 | 评估 | 遥感领域 VLM | - | - |
| [ChenDelong1999/RemoteCLIP](https://github.com/ChenDelong1999/RemoteCLIP) | 🔭 前沿 | 评估 | 遥感视觉-语言基础模型 | - | - |
| [IBM/terratorch](https://github.com/IBM/terratorch) | 🛠 工具 | 评估 | 地理空间基础模型（Prithvi 等）微调工具 | - | - |

### 遥感深度学习工具

| 项目 | 类型 | 雷达 | 为什么关注 | ⭐ | 最近推送 |
|---|---|---|---|---|---|
| [torchgeo/torchgeo](https://github.com/torchgeo/torchgeo) | 🛠 工具 | 评估 | PyTorch 地理空间数据集 / 采样器 / 模型 | 4.2k | 2026-09-25 |
| [opengeos/segment-geospatial](https://github.com/opengeos/segment-geospatial) | 🛠 工具 | 评估 | SAM 用于遥感影像分割 | - | - |
| [open-mmlab/mmrotate](https://github.com/open-mmlab/mmrotate) | 🛠 工具 | 评估 | 旋转目标检测（遥感常用） | - | - |

### 地理空间数据基础设施

| 项目 | 类型 | 雷达 | 为什么关注 | ⭐ | 最近推送 |
|---|---|---|---|---|---|
| [OSGeo/gdal](https://github.com/OSGeo/gdal) | 🛠 工具 | 评估 | 栅格 / 矢量数据处理基石 | - | - |
| [rasterio/rasterio](https://github.com/rasterio/rasterio) | 🛠 工具 | 评估 | Pythonic 栅格数据读写 | - | - |
| [stac-utils/pystac](https://github.com/stac-utils/pystac) | 🛠 工具 | 评估 | STAC 时空资产目录标准 | - | - |
| [developmentseed/titiler](https://github.com/developmentseed/titiler) | 🛠 工具 | 评估 | 动态瓦片服务（COG / STAC） | - | - |
| [opengeos/leafmap](https://github.com/opengeos/leafmap) | 🛠 工具 | 评估 | Notebook 里的交互式地图分析 | - | - |

### 论文与资料合集

| 项目 | 类型 | 雷达 | 为什么关注 | ⭐ | 最近推送 |
|---|---|---|---|---|---|
| [satellite-image-deep-learning/techniques](https://github.com/satellite-image-deep-learning/techniques) | 📐 实践 | 评估 | 卫星影像深度学习技术汇总 | - | - |
| [Jack-bo1220/Awesome-Remote-Sensing-Foundation-Models](https://github.com/Jack-bo1220/Awesome-Remote-Sensing-Foundation-Models) | 🔭 前沿 | 评估 | 遥感基础模型论文合集 | - | - |

<a id="knowledge-base"></a>

## 知识库与 RAG

> RAG 引擎、文档解析、向量数据库、知识库应用

### RAG 引擎与框架

| 项目 | 类型 | 雷达 | 为什么关注 | ⭐ | 最近推送 |
|---|---|---|---|---|---|
| [infiniflow/ragflow](https://github.com/infiniflow/ragflow) | 🛠 工具 | 评估 | 深度文档理解的 RAG 引擎 | - | - |
| [run-llama/llama_index](https://github.com/run-llama/llama_index) | 🛠 工具 | 评估 | 数据接入与检索框架 | - | - |
| [deepset-ai/haystack](https://github.com/deepset-ai/haystack) | 🛠 工具 | 评估 | 生产级 RAG / 搜索管线 | - | - |

### 文档解析

| 项目 | 类型 | 雷达 | 为什么关注 | ⭐ | 最近推送 |
|---|---|---|---|---|---|
| [opendatalab/MinerU](https://github.com/opendatalab/MinerU) | 🛠 工具 | 评估 | PDF → Markdown，公式 / 表格识别强 | - | - |
| [docling-project/docling](https://github.com/docling-project/docling) | 🛠 工具 | 评估 | IBM 文档解析与转换 | - | - |
| [microsoft/markitdown](https://github.com/microsoft/markitdown) | 🛠 工具 | 评估 | Office / PDF 等文件转 Markdown | - | - |
| [PaddlePaddle/PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) | 🛠 工具 | 评估 | 多语种 OCR 与版面分析 | - | - |

### 向量数据库

| 项目 | 类型 | 雷达 | 为什么关注 | ⭐ | 最近推送 |
|---|---|---|---|---|---|
| [milvus-io/milvus](https://github.com/milvus-io/milvus) | 🛠 工具 | 评估 | 分布式向量数据库 | - | - |
| [qdrant/qdrant](https://github.com/qdrant/qdrant) | 🛠 工具 | 评估 | Rust 向量数据库，过滤检索强 | - | - |

### 知识库应用

| 项目 | 类型 | 雷达 | 为什么关注 | ⭐ | 最近推送 |
|---|---|---|---|---|---|
| [open-webui/open-webui](https://github.com/open-webui/open-webui) | 🛠 工具 | 评估 | 自托管 AI 对话 + 知识库界面 | - | - |
| [Mintplex-Labs/anything-llm](https://github.com/Mintplex-Labs/anything-llm) | 🛠 工具 | 评估 | 一体化私有知识库应用 | - | - |
| [labring/FastGPT](https://github.com/labring/FastGPT) | 🛠 工具 | 评估 | 知识库问答 + 工作流编排 | - | - |

### RAG 工程实践

| 项目 | 类型 | 雷达 | 为什么关注 | ⭐ | 最近推送 |
|---|---|---|---|---|---|
| [NirDiamant/RAG_Techniques](https://github.com/NirDiamant/RAG_Techniques) | 📐 实践 | 评估 | RAG 进阶技巧 Notebook 合集 | - | - |

## 贡献

见 [CONTRIBUTING.md](CONTRIBUTING.md)。推荐在本仓库中使用 Claude Code 的 `/curate add <url>` 添加项目。
