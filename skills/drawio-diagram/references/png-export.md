# Draw.io → PNG 导出工作流

## 安装

```bash
# macOS
brew install --cask drawio
# 安装后命令行可用: drawio
```

## 导出命令

```bash
# 基本导出（2x 分辨率）
drawio --export --format png --scale 2 --output output.png input.drawio

# 透明底色（推荐——图表融入使用场景）
drawio --export --format png --scale 2 --transparent --output output.png input.drawio

# SVG 矢量
drawio --export --format svg --output output.svg input.drawio

# PDF
drawio --export --format pdf --output output.pdf input.drawio
```

## 导出前 XML 验证（必须）

```bash
python3 -c "
import xml.etree.ElementTree as ET
tree = ET.parse('input.drawio')
cells = tree.findall('.//mxCell')
v = [c for c in cells if c.get('vertex')=='1']
e = [c for c in cells if c.get('edge')=='1']
print(f'✅ Valid | {len(cells)} cells ({len(v)} vertices, {len(e)} edges)')
"
```

## 常见 XML 错误及修复

| 错误 | 原因 | 修复 |
|------|------|------|
| `mismatched tag` | `<Array>` 对 `</mxArray>` | `sed -i '' 's/<\/mxArray>/<\/Array>/g' file.drawio` |
| `not well-formed` | 中文引号 `""` 在 XML attribute 中 | 去掉引号，如 `"已上线"` → `已上线` |
| `duplicate id` | 两个元素用了相同 ID | 确保 ID 从 0 递增且不重复 |

## 批量导出脚本

```bash
# 导出目录下所有 .drawio 文件
for f in *.drawio; do
  drawio --export --format png --scale 2 --transparent \
    --output "${f%.drawio}.png" "$f"
done
```
