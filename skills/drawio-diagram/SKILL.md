---
name: drawio-diagram
description: 为深度学习模型、网络架构、算法流程等生成标准 Draw.io (.drawio) 格式的可视化图表；支持从零生成与风格迁移两种模式。从零生成：模型架构图、流程图、感受野示意图等；风格迁移：参考图 + 内容描述/项目 → 按参考图风格生成新图。确保 XML 格式正确，可直接在 Draw.io 中打开编辑。
---

# Draw.io 图表

本 Skill 指导 Agent 生成**标准的 Draw.io 格式图表**（.drawio 文件），支持两种模式：**从零生成**（模型架构、算法流程等）与**风格迁移**（参考图 + 内容 → 按参考图风格生成新图）。

## Step 0：任务识别

| 条件 | 执行 |
|------|------|
| 用户提供**参考图**，且希望「按这张图的风格」画新图 | 执行 `reference/style-migration.md` |
| 其他情况（从零生成） | 执行 `reference/generation.md` |

## 使用时机

**从零生成：**
- 用户需要为深度学习模型（如 Transformer、CNN、RNN 等）生成架构图
- 用户需要绘制算法流程图、数据流图、系统架构图
- 用户需要可视化特定概念（如感受野、注意力机制、特征提取过程等）
- 用户提到「画个图」「生成架构图」「可视化模型结构」「绘制流程图」等需求

**风格迁移：**
- 用户提供参考图，希望「按这个风格画」「照着这个排版/配色画」

## 通用规范（两种模式共用）

### 1. XML 格式严格性

- ✅ 所有标签必须正确闭合：`<mxCell>` 对应 `</mxCell>`，绝不能写成 `</mCell>`
- ✅ 使用 `vertex="1"` 标记节点，`edge="1"` 标记连线
- ✅ 每个元素必须有唯一 `id`，从 0 开始递增
- ✅ 特殊字符必须转义：`&` → `&amp;`，`<` → `&lt;`，`>` → `&gt;`

### 2. 标准文件结构

```xml
<mxfile host="app.diagrams.net">
  <diagram name="图表名称" id="图表id">
    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="宽度" pageHeight="高度" background="#F5F5DC">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <!-- 所有图形元素从 id="2" 开始 -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

### 3. 常用样式

- **2D 节点**：`rounded=1;whiteSpace=wrap;html=1;fillColor=#颜色;strokeColor=#333333;strokeWidth=1;fontSize=11`
- **3D 节点（推荐用于神经网络层）**：`shape=cube;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;darkOpacity=0.05;darkOpacity2=0.1;size=20;fillColor=#颜色;strokeColor=#333333;strokeWidth=1.5`
- **连线**：`edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#000000;strokeWidth=2;endArrow=classic`
- **虚线（残差）**：`dashed=1`

### 4. 输出要求

1. 图表说明（2–3 行）
2. 使用指南：Draw.io 打开、导出 PNG/SVG/PDF、图题与论文引用示例

### 5. 视觉偏好（用户定制）

生成图表时遵循以下偏好，避免"AI视觉太重"：

- **每阶段独立色系**：用左侧细色条（8px 宽）区分阶段，五个阶段五种颜色
- **浅色底+深色字**：输出/结论框用浅色填充+深色粗体文字，**禁止白字深底**（手绘模式下不可读）
- **去框化**：不要灰色大框包裹阶段，用色条+留白区分即可
- **大圆角**：arcSize=15-30，柔和视觉
- **透明背景**：导出 PNG 时加 `--transparent`
- **手绘模式**：在 mxGraphModel 加 `sketch="1"`，元素 style 加 `sketch=1;jiggle=2;curveFitting=1`
- **字体大小**：输出框字号≥14px，确保可读

## 参考资源

保存 .drawio 文件后必须验证 XML 合法性，详见 `references/xml-validation.md`。

快速验证命令：
```bash
python3 -c "
import xml.etree.ElementTree as ET
tree = ET.parse('FILE.drawio')
cells = tree.findall('.//mxCell')
v = [c for c in cells if c.get('vertex')=='1']
e = [c for c in cells if c.get('edge')=='1']
print(f'OK: {len(cells)} cells ({len(v)} vertices, {len(e)} edges)')
"
```

### 6. 常见陷阱

- **中文引号 `""` 出现在 XML attribute 中** → 属性值中的中文引号必须去掉，不能用转义。例如 `状态→"已上线"` 改为 `状态→已上线`
- **`gh repo clone` 不支持 `--depth`** → 用 `git clone --depth 1` 代替
- **连线 source/target 指向不存在的节点 ID** → 确保连线引用的 ID 已在前面定义为 vertex 节点

## 设计风格指南（关键——避免「AI视觉」）

生成图表时最容易犯的错误：每个阶段用同一套绿-黄-蓝-红配色循环，灰色虚线大框套小框，整体看起来沉闷单调——这就是"AI视觉"。以下规则避免这个问题：

### 核心原则

1. **每阶段独立色系**：不要所有阶段共用绿/黄/蓝/红四色循环。给每个阶段一个主题色，同一阶段内用该色的深浅变体区分起点/过程/输出。
2. **轻量化底色**：中间过程节点用 `fillColor` 极淡色 + `strokeColor` 主题色的浅变体 + 细边框（1.5px）。输出节点用主题色的中等深度填充（如 #B2DFDB 对应青绿主题）+ 主题色深色粗体文字（如 #00695C），**严禁实心底+白字**——白字在深底色上可读性极差，用户明确反馈「看不清楚，太丑了」。
3. **不要灰色大框**：用左侧细色条（宽8px）+ 阶段编号作为视觉锚点，替代全包围灰色虚线框。"框"越少越轻盈。
4. **加大圆角**：`arcSize=15-30`，去掉方盒子的机械感。
5. **透明画布**：`background="none"`，让图表融入使用场景而非自带"卡片感"。

### 推荐五阶段配色

| 阶段 | 主题色 | 淡底色 | 边框色 | 适用场景 |
|------|--------|--------|--------|---------|
| 数据/输入 | #0D7377 青绿 | #E0F7F6 | #14A3A8 | 数据预处理、信息采集 |
| 模型/分析 | #6C3FAF 紫色 | #F3E8FF | #8B5CF6 | 建模、算法、代理模型 |
| 优化/计算 | #D97706 琥珀 | #FEF3C7 | #F59E0B | 优化求解、参数调优 |
| 工程/设计 | #2563EB 蓝色 | #DBEAFE | #3B82F6 | 场景适配、工程化 |
| 验证/结论 | #059669 翠绿 | #D1FAE5 | #10B981 | 鲁棒验证、测试评估 |

### 用户反馈提炼

- ❌ 每阶段同色系循环 → ✅ 每阶段独立色系
- ❌ 灰色虚线大框 → ✅ 左侧细色条标记
- ❌ 方盒直角 → ✅ 大圆角 arcSize=20
- ❌ 画布带底色 → ✅ 透明背景
- ❌ 字号统一小 → ✅ 标题22px，关键数字20px，正文11-12px

## PNG 导出

导出工作流详见 `references/png-export.md`。快速命令：

```bash
# 安装
brew install --cask drawio

# 导出（透明底色，2倍分辨率）
drawio --export --format png --scale 2 --transparent \
  --output output.png input.drawio
```

## 参考资源

- Draw.io：https://app.diagrams.net/
- 官方文档：https://www.drawio.com/doc/