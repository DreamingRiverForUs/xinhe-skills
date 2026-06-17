# Draw.io XML 验证指南

生成 .drawio 文件后，必须验证 XML 合法性再交付。

## 快速验证脚本

```bash
python3 -c "
import xml.etree.ElementTree as ET
tree = ET.parse('FILE.drawio')
# mxCell 可能在默认命名空间中也可能没有
cells = tree.findall('.//{http://www.w3.org/1999/xhtml}mxCell') or tree.findall('.//mxCell')
vertices = [c for c in cells if c.get('vertex') == '1']
edges = [c for c in cells if c.get('edge') == '1']
print(f'OK: {len(cells)} cells ({len(vertices)} vertices, {len(edges)} edges)')
"
```

## 常见 XML 错误与修复

### 1. 中文引号在 attribute 中

错误示例：
```xml
<mxCell value="状态→"已上线"" />
```

原因：XML 解析器把 `"已上线"` 中的 `"` 当作 attribute 值的结束符。

修复：去掉中文引号，用裸文本：
```xml
<mxCell value="状态→已上线" />
```

### 2. 标签名不匹配

Draw.io 的 mxCell 标签必须是 `<mxCell ...>` `</mxCell>`，常被误写成 `</mCell>`。

Draw.io 使用的 `<Array as="points">` 标签，闭合必须是 `</Array>`，不能是 `</mxArray>`。

修复：
```bash
sed -i '' 's/<\/mxArray>/<\/Array>/g' file.drawio
```

### 3. 特殊字符未转义

| 字符 | 转义 |
|------|------|
| `&` | `&amp;` |
| `<` | `&lt;` |
| `>` | `&gt;` |

注意：value 属性中的 `&lt;br&gt;` 用来表示换行，这是正确的。

### 4. 连线 source/target 指向不存在

连线的 `source="X"` 和 `target="Y"` 必须指向已定义的 vertex 节点 ID。建议按生成顺序分配 ID 并确保连线 ID 在所有节点 ID 之后。

## 批量验证目录下所有 .drawio 文件

```bash
for f in path/to/images/**/*.drawio; do
  python3 -c "
import xml.etree.ElementTree as ET
try:
    tree = ET.parse('$f')
    cells = tree.findall('.//mxCell')
    v = sum(1 for c in cells if c.get('vertex')=='1')
    e = sum(1 for c in cells if c.get('edge')=='1')
    print(f'✅ {f}: {len(cells)} cells ({v}v, {e}e)')
except Exception as ex:
    print(f'❌ {f}: {ex}')
"
done
```
