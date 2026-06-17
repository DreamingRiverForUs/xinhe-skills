# Draw.io 手绘/草图模式

Draw.io 支持通过 style 属性启用 sketch 渲染，给矩形和连线添加手绘抖动效果。

## 启用方式

在每个 vertex 节点的 style 属性前添加：

```
sketch=1;jiggle=2;curveFitting=1;
```

示例：
```
style="sketch=1;jiggle=2;curveFitting=1;rounded=1;whiteSpace=wrap;html=1;fillColor=#E0F7F6;..."
```

## 参数说明

| 参数 | 作用 | 推荐值 |
|------|------|--------|
| `sketch=1` | 启用手绘渲染 | 1 |
| `jiggle` | 线条抖动幅度 | 2（适中） |
| `curveFitting` | 曲线拟合程度 | 1（轻度） |

## 批量添加

```bash
# 给 .drawio 文件中所有 vertex 节点添加 sketch 属性
sed -i '' 's/style="/style="sketch=1;jiggle=2;curveFitting=1;/g' file.drawio
# 验证不会破坏 XML 结构
python3 -c "import xml.etree.ElementTree as ET; ET.parse('file.drawio'); print('OK')"
```

## 注意

- sketch 模式会显著增加导出文件大小（2-3倍）
- 命令行 `drawio --export` 支持 sketch 属性，无需在 app 中手动开启
- edge（连线）节点不需要 sketch 属性，但加了也没坏处
