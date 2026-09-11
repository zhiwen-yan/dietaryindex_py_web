# Prelaunch Checklist

## 一、环境与配置

- [ ] 复制 `.env.example` 为 `.env`
- [ ] 设置 `DIETARYINDEX_RUNTIME_DIR`
- [ ] 如果要公网开放 API，设置 `DIETARYINDEX_API_KEY`
- [ ] 把 `DIETARYINDEX_REQUIRE_API_KEY=true` 打开
- [ ] 确认服务器磁盘空间足够保存上传和结果文件

## 二、服务启动

- [ ] API 可以正常启动：`uvicorn dietaryindex_api.app:app --host 0.0.0.0 --port 8000`
- [ ] Next.js 可以正常启动并访问计算器与 FII 页面
- [ ] Windows 桌面软件可以正常启动
- [ ] `GET /healthz` 返回 `status=ok`
- [ ] `GET /docs` 正常打开

## 三、关键业务流程

- [ ] 通用模式上传 CSV 后能完成预览与映射
- [ ] 至少一个通用指数能成功计算
- [ ] 至少一个 NHANES 模式能成功计算
- [ ] FII 数据库页面能搜索苹果、香蕉、酸奶等食物
- [ ] 中文 / 英文切换后页面不跳回错误语言

## 四、文件与日志

- [ ] `runtime_data/uploads` 已配置持久化
- [ ] `runtime_data/results` 已配置持久化
- [ ] 明确日志保留策略
- [ ] 运行一次 `python scripts/cleanup_runtime.py --days 7`
- [ ] 如果确认无误，再运行 `python scripts/cleanup_runtime.py --days 7 --apply`

## 五、安全

- [ ] 公网环境不要裸奔开放 `/v1/*`
- [ ] 至少启用 `x-api-key`
- [ ] 反向代理限制上传大小
- [ ] 反向代理加 HTTPS
- [ ] 记录基本访问日志

## 六、发布说明

- [ ] README 安装说明与当前实际发布方式一致
- [ ] API / Web / CLI 命令都能跑通
- [ ] 对外说明中区分“本地源码安装”和“未来 PyPI 安装”
- [ ] 准备一个首发说明页，告诉用户支持哪些指数、哪些模式

## 七、首发建议

首发时建议优先展示：

- 首页
- 核心指数页
- PHDI / PDI 家族页
- FII 数据库页
- API / Codex 接入页

先把最重要的体验做稳，再扩展更多指标和更复杂的公网用户系统。
