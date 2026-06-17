# Tectonic 缓存并发竞争诊断指南

## 症状

多个 Docker 容器同时编译不同模板，共享 `~/.cache/paper-tectonic` 时发生：

- **非确定性失败**：同一模板两次编译结果不同（一次 exit 0，一次 exit 1）
- **错误随机漂移**：每次失败的 Undefined control sequence 行号不同
  - `options.def:187` → 重跑变 `metadata.def:271` → 再跑变 `options.def:188`
- **单独编译永远通过**：`docker run` 不加并发时从不失败

## 根因

tectonic 的 bundle 缓存（`~/.cache/paper-tectonic/bundles/`）在多个容器间共享。并发编译时，一个容器正在写入缓存文件，另一个容器读到不完整/损坏的文件 → 解析失败 → 报在随机位置。

## 验证方法

```bash
# 测试1：单独编译
cd ~/project/templates/nwpu-thesis && \
  docker run --rm --platform linux/amd64 -v $(pwd):/app \
    -v ~/.cache/paper-tectonic:/root/.cache/Tectonic \
    crpi-b75iph3qtzyryyvz.cn-hangzhou.personal.cr.aliyuncs.com/paper-prod/paper-sandbox-cli:latest \
    tectonic -X compile main.tex 2>&1 | grep -c "error:"

# 如果 exit 0 → 模板没问题，之前是缓存竞争
# 如果 exit 1 → 真正的模板bug，查 main.log
```

## 预防

1. 不要同时跑多个 tectonic Docker 容器
2. 批量处理时串行编译（或使用独立缓存目录）
3. 子 Agent 并行不受影响（各自独立 Docker 调用，无并发冲突）

## 已确认受影响

- nwputhesis（西北工业大学）：options.def:187/188 和 metadata.def:271 随机报错
