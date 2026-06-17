# 苏大 sudathesis（thuthesis 派生）适配记录

## 模板信息

- 版本: v2.3.1
- 来源: shadowofgost/sudathesis-soochow-university-latex-template
- GitHub: iftaken/suda-thesis-231
- TeXPage: https://www.texpage.com/template/c05aaf0d-7a14-4a1c-96b5-938556f726b4
- 分类: 苏州大学学位论文（本科/硕士/博士/博士后）

## 关键发现：本地字体检测分支

此模板是 thuthesis 的深度修改版，与原版 thu-thesis 适配策略不同：

### 模板的字体检测链

模板在 `sudathesis.cls` 中有两级字体检测：

**第一层：fontset 检测（约749行）**
```latex
\IfFileExists{./fonts/simsun.ttc}{
  \thusetup{fontset = windows}
}{
  \IfFontExistsTF{SimSun}{
    \thusetup{fontset = windows}
  }{
    % ... fallback to mac/ubuntu/fandol
  }
}
```

**第二层：CJK 字体加载（约1023行）**
```latex
\IfFileExists{./fonts/simsun.ttc}{
  \setCJKmainfont[..., Path=fonts/]{simsun.ttc}
  \setCJKsansfont[..., Path=fonts/]{simhei.ttf}
  \setCJKfamilyfont{zhkai}[..., Path=fonts/]{simkai.ttf}
  \setCJKfamilyfont{zhfs}[..., Path=fonts/]{simfang.ttf}
}{
  % fallback: 系统字体名（KaiTi, FangSong → Docker 中不可用）
}
```

### 适配策略（与标准 thu-thesis 不同）

**不需要** patch CJK 字体分支或强制 `fontset=ubuntu`！

只需：
1. **init.sh 下载 4 个字体**（simsun.ttc, simhei.ttf, simkai.ttf, simfang.ttf）到 `fonts/`
2. **两个英文系统字体替换**：
   - `\setsansfont{Arial}` → `\setsansfont{Liberation Sans}`
   - `\setmonofont{Courier New}` → `\setmonofont{Liberation Mono}`
3. 模板自身的 `\IfFileExists{./fonts/simsun.ttc}` 检测成功 → 走本地字体分支 → CJK 字体全部正确加载

### 为什么比标准 thu-thesis 更简单

标准 thu-thesis 在 Docker 中 `\IfFontExistsTF{SimSun}` 返回 true → 进入 windows 分支 → 使用系统级 KaiTi/FangSong → 必须 patch 字体加载逻辑。

此模板作者添加了 `\IfFileExists{./fonts/simsun.ttc}` 作为第一优先级检测，只要 fonts/ 目录存在，就走本地路径分支。这是更友好的 Docker 适配策略。

### 所需字体 COS URL

```
simsun.ttc:  https://xinhepaperdev-1257733029.cos.ap-shanghai.myqcloud.com/font/simsun.ttc
simhei.ttf:  https://xinhepaperdev-1257733029.cos.ap-shanghai.myqcloud.com/font/simhei.ttf
simkai.ttf:  https://xinhepaperdev-1257733029.cos.ap-shanghai.myqcloud.com/font/simkai.ttf
simfang.ttf: https://xinhepaperdev-1257733029.cos.ap-shanghai.myqcloud.com/font/simfang.ttf
```

### 编译结果

- tectonic 编译通过 (exit 0)
- main.pdf: 463KB
- 警告: algorithm.sty UTF-8 字节（已知安全），Underfull hbox（非阻断）
- BibTeX 警告（已忽略，不影响输出）

## 适用模板识别

当遇到 thuthesis 派生模板时，先 grep `IfFileExists.*fonts.*simsun` 判断是否有本地字体检测：
```bash
grep -n 'IfFileExists.*fonts.*simsun' *.cls
```

如果有 → 走本地字体策略（仅需 init.sh + 英文字体替换）
如果没有 → 走标准 thuthesis 策略（patch fontset + CJK 分支）
