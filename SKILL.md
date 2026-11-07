---
name: adaptive-model-research
description: Run rigorous, visible, self-repairing, continuously evolving model-training research. Use for dataset replacement, architecture/capacity/recipe comparison, long GPU training, current-main-chat monitoring, failure recovery, experiment resumption, model selection, or final research reporting across forecasting, classification, regression, vision, language, and multimodal tasks; do not use for ordinary application development or one-off inference.
---

# Adaptive Model Research

把模型训练当作可审计、可续跑、可证伪的科研闭环，而不是一次性脚本。持续共同优化数据、任务、特征、损失、训练方法、容量、架构和部署，并保留失败证据与停止依据。

## 按任务读取模块

- **定义问题、数据、切分和指标**：读 [references/experiment-contract.md](references/experiment-contract.md)。
- **启动长训练或查看进度**：必须读 [references/live-main-chat-monitoring.md](references/live-main-chat-monitoring.md)。
- **中断、异常、续跑或自修复**：再读 [references/recovery-and-resume.md](references/recovery-and-resume.md)。
- **持续迭代或追求更优模型**：读 [references/research-loop.md](references/research-loop.md) 和 [references/coevolution-axes.md](references/coevolution-axes.md)。
- **比较架构、参数量或训练配方**：读 [references/architecture-capacity-recipes.md](references/architecture-capacity-recipes.md)。
- **验收、排名和报告**：读 [references/acceptance-and-reporting.md](references/acceptance-and-reporting.md)。
- **模型晋级、切换、集成和生产回退**：读 [references/model-lifecycle.md](references/model-lifecycle.md)。
- **实现可续跑状态**：读 [references/research-state-schema.md](references/research-state-schema.md)。

只读取会改变当前决策的模块，不一次加载全部参考文件。

## 不可破坏的边界

1. 严格隔离训练、验证、测试；所有可学习预处理只拟合训练集。超参数、架构、容量、融合、路由和阈值只用开发证据选择。
2. 测试集只用于冻结方案的最终确认。看到测试结果后提出的新想法必须标为探索性，并用新开发折、外部数据或新批次验证。
3. 同一比较共享数据版本、输入、目标、切分、预算和评估代码；至少保留简单基线与强基线。
4. 自修复不得静默改变实验口径。任何数据、切分、指标、容量、批量或训练配方变化都必须产生新指纹与新实验记录。
5. 不预设自研模型必胜，不伪造领先、不删不利种子、不以测试集调参、不把别人的模型换名。
6. 长训练必须附着在**当前主会话**的可观察执行会话中。不得交给后台、隐藏窗口、计划任务、另一个聊天或无人回报的代理托管。
7. 主会话稳定期静态等待，默认约每 30 分钟检查并给出紧凑可见心跳；关键节点和异常立即介入，最终结果必须在同一主会话主动交付。

## 核心闭环

1. 固化问题契约、数据/代码/配置/环境指纹、基线与预算，完成数据门禁、专项测试、硬件冒烟和耗时基准。
2. 按预声明的架构×容量×训练配方运行候选；每个候选即时落盘规格、曲线、指标、检查点和资源记录。
3. 只按开发验证证据晋级；先单种子筛选，再多种子复验；冻结后才运行最终测试。
4. 每批完成先做全面验收，再提出 1–3 个可证伪假设。持续研究中 `batch_complete` 只是检查点，不代表结束。
5. 迭代不得只围绕换架构或加参数；优先选择能解释当前短板的最小改动，并用消融确认因果。
6. 机器负责逐 epoch 记录、早停和硬异常检测；模型仅在心跳、候选完成、异常修复、研究决策和最终验收时深入分析。
7. 最终分别给出主指标冠军、关键子任务冠军、效率拐点、稳健候选和生产候选，不用单一总分掩盖取舍。

## 完成标准

交付数据与泄漏门禁、基线/候选表、架构与容量边界、训练配方消融、多种子稳定性、分任务指标、曲线诊断、参数量与资源成本、失败与修复记录、研究轨迹、模型切换依据，以及明确的继续/停止结论。同步记录变更、原因、验证结果和科研价值。
