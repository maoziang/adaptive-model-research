# Adaptive Model Research · 自适应模型研究

面向 Codex 的模型训练研究技能，适用于预测、分类、回归、视觉、语言及多模态任务。将实验设计、训练监控、故障恢复、模型迭代与结果验收组织为可追溯的研究流程。

## 核心能力

- **在当前主会话持续监控**。长训练保留可观察的执行会话，稳定阶段约每 30 分钟检查一次，里程碑与异常及时处理，结果在同一会话交付。
- **按结果决定下一轮实验**。从现有模型和 1—3 个有依据的改动开始，依据对照结果保留、修正或淘汰假设，再决定是否扩大训练。
- **共同优化数据与模型**。覆盖数据、任务、特征、损失、训练配方、容量、架构、融合与部署，围绕已定位的短板开展消融。
- **支持断点续跑与有界恢复**。记录实验状态、检查点和指纹，复用已完成的有效工件，保留失败、恢复与停止依据。
- **保持公平比较和数据隔离**。统一数据、输入、目标、切分和预算，使用开发证据选型，冻结方案后开展最终测试，完整保留不利结果。
- **核对指标与实际权重**。从保存的预测和真实标签复算指标，重载检查点复验，核查时间对齐、预处理边界及跨设备数值差异。
- **区分研究结果与生产候选**。分别报告综合精度、关键子任务、效率和稳定性，并依据预先确定的门槛判断是否晋级。

## 本次同步的改进

本次更新吸收了实际模型研究中的反馈，重点完善四个方面。

1. 将候选清单作为实验备选库，围绕当前目标启用必要的实验，明确区分待尝试、主动放弃、失败和待补齐的确认。
2. 连续出现微小或无收益结果时，优先复核剩余开发时段、目标和预测时距，再决定是否新增模块。
3. 明确训练路径的耗时基准、模型实现变更的默认行为回归，以及历史结果复用时的来源与指纹核查。
4. 使用未舍入数值判断晋级，区分多种子独立结果与实际集成结果，并保留检查点重载、CPU/GPU 差异和容差依据。

这些改进用于提高实验决策和证据质量，实际模型表现仍需通过对应任务的实验验证。

## 安装

将本仓库复制到 Codex 的技能目录，保留 `SKILL.md`、`agents/`、`references/` 和 `scripts/` 的相对位置。

默认目录为 `~/.codex/skills/adaptive-model-research`。Windows 通常位于以下位置，自定义 Codex 目录时请使用实际配置。

```text
C:\Users\<用户名>\.codex\skills\adaptive-model-research
```

也可使用 Git 安装。

```powershell
git clone https://github.com/maoziang/adaptive-model-research.git "$env:USERPROFILE/.codex/skills/adaptive-model-research"
```

技能列表未自动更新时，重新加载 Codex。对于通过 Git 安装且工作区干净的版本，可在技能目录执行 `git pull --ff-only` 更新。手动复制安装的版本，请先备份本地修改，再同步所需文件。

## 使用示例

```text
$adaptive-model-research 优化当前预测模型。先核对数据、切分、基线和预算，在当前主会话持续监控训练，先做少量有依据的对照，再根据结果安排多种子确认，最后给出可复核的研究报告。
```

```text
$adaptive-model-research 继续中断的实验，核对代码和数据指纹，复用已完成结果，定位失败原因，在原授权和预算内恢复训练。
```

具体训练代码、数据和项目约束由使用方提供。该技能支持模型研究流程，适用范围包括数据迁移、模型比较、持续优化和研究报告。

## 文件结构

| 文件 | 用途 |
| --- | --- |
| `SKILL.md` | 技能入口、关键约束与按需阅读指引 |
| `agents/openai.yaml` | 中文显示信息、默认提示与自动调用配置 |
| `references/experiment-contract.md` | 问题定义、数据切分、指标和实验契约 |
| `references/live-main-chat-monitoring.md` | 主会话训练监控与低开销心跳 |
| `references/recovery-and-resume.md` | 故障恢复与断点续跑 |
| `references/research-loop.md` | 假设驱动的持续迭代和停止依据 |
| `references/coevolution-axes.md` | 数据、任务、模型与部署的共同优化 |
| `references/architecture-capacity-recipes.md` | 架构、容量与训练配方对照 |
| `references/acceptance-and-reporting.md` | 指标复核、结果验收与报告 |
| `references/model-lifecycle.md` | 模型晋级、切换、集成和回退 |
| `references/research-state-schema.md` | 可续跑研究状态的数据结构 |
| `scripts/inspect_training_run.py` | 只读训练状态检查工具 |
| `scripts/test_inspect_training_run.py` | 状态检查工具的回归测试 |

## 检查工具

在仓库目录运行以下命令可执行回归测试。

```powershell
python -m unittest discover -s scripts -p "test_*.py"
```

使用只读工具查看实际实验目录。

```powershell
python scripts/inspect_training_run.py --run-dir <实验目录>
```

研究状态和工件约定见 [状态结构说明](references/research-state-schema.md)，长训练监控方式见 [主会话监控说明](references/live-main-chat-monitoring.md)。

## 结果解释

报告应标明开发、探索、最终测试的范围，给出分目标效果、随机性和资源成本。对跨项目或论文的比较，应先核对数据、任务与评测方法。达到预算、完成一批实验、研究收敛和满足最终目标，各自保留对应的状态与证据。

## 许可证

采用 [MIT 许可证](LICENSE)。
