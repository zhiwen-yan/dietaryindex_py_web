# Release Plan

## 这份文档在解决什么

这份文档面向两个未来目标：

1. 让用户可以 `pip install dietaryindex`
2. 让外部用户可以稳定调用你的 API

---

## 一、Python 包发布目标

理想状态下，用户将来可以直接这样安装：

```bash
pip install dietaryindex
pip install dietaryindex[api]
pip install dietaryindex[all]
```

当前项目已经具备这些前置条件：

- `pyproject.toml`
- 包入口 `dietaryindex`
- CLI 脚本入口
- 可选依赖分组

---

## 二、发布前建议检查项

### 1. 包内容检查

确认以下内容都能随包发布：

- `dietaryindex/`
- `dietaryindex/data/*.csv`
- 必要 reference 数据
- CLI 入口

### 2. 安装测试

建议在干净环境中测试：

```bash
pip install -e .[all]
python -c "import dietaryindex; print(dietaryindex.__version__ if hasattr(dietaryindex, '__version__') else 'ok')"
dietaryindex-cli catalog
```

### 3. 文档一致性

发布前检查 README 中的：

- 安装命令
- API 路径
- Web 启动命令
- 示例代码

---

## 三、PyPI 发布建议步骤

### 1. 构建分发包

建议未来加上：

```bash
python -m pip install build twine
python -m build
twine check dist/*
```

### 2. 发布到 TestPyPI

```bash
twine upload --repository testpypi dist/*
```

### 3. 实际发布到 PyPI

```bash
twine upload dist/*
```

---

## 四、版本管理建议

建议采用一个清晰的节奏：

- `0.1.x`：MVP 阶段
- `0.2.x`：API / 页面 / 数据库逐步稳定
- `0.3.x`：公网准备阶段
- `1.0.0`：正式公开发布

---

## 五、API 发布目标

对于 API，不只是“能跑”，还要考虑：

- 文档
- 健康检查
- 错误信息一致性
- 上传文件规范
- 结果轮询接口

当前已经具备：

- `/docs`
- `/openapi.json`
- `/healthz`
- 统一计算入口
- 多文件上传模式支持

---

## 六、给用户的两种长期接入方式

未来你的用户可以有两种长期稳定方案：

### 方案 A：调用你的公网 API

适合：

- Codex
- 其他 AI agent
- 外部网页
- 自动化平台

### 方案 B：本地安装 Python 包

适合：

- 高级研究用户
- Notebook 用户
- 需要本地跑敏感数据的团队

这两种方式最好同时保留，因为它们面对的是两类不同用户。

---

## 七、为什么“API + 包”要同时做

只做 API 的问题：

- 高级用户无法完全离线
- 敏感数据用户不一定愿意上传
- 本地批处理不方便

只做包的问题：

- 普通用户门槛高
- AI / 网站接入不顺
- 平台化能力弱

所以你现在的方向是对的：

- 网页端提供易用性
- API 提供可集成性
- Python 包提供研究级复用性

---

## 八、下一阶段最值得做的发布相关事项

1. 增加 `__version__`
2. 增加构建命令说明
3. 做一次干净环境安装测试
4. 检查哪些数据文件必须随包发布
5. 补一个最小 changelog
6. 做一次 TestPyPI 演练

---

## 九、当前结论

这个项目现在已经具备“可发布基础”，但还处于：

- 功能 MVP 已成型
- 文档和部署基础已补齐
- 正式 PyPI 发布前还需要一次打包演练

也就是说，离“真正能被别人稳定安装和使用”已经不远了。
