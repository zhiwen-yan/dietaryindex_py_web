# Citation Guide

## 这份文档在做什么

这份文档用来明确两件事：

1. 别人如果使用 `dietaryindex-py`，应该怎样引用。
2. 哪些内容适合写在论文的致谢、方法学说明或软件声明里。

---

## 核心原则

本项目采用 `AGPL-3.0-or-later`，它可以保护代码在网络服务场景下的开源义务。
但学术论文里的“必须引用哪篇文章”，通常不能只靠软件许可证强制完成。

所以这里采用的是双层策略：

- 许可证负责代码使用边界
- 引用文件与学术说明负责引用规范

---

## 建议的学术引用要求

如果研究者使用了以下任一内容，建议至少引用本仓库的软件版本：

- 指标计算代码
- Next.js 本地与桌面工作流
- 本地 API 工作流
- FII / FISI 数据库整理结果
- 本项目提供的统一映射、上传、预处理与结果导出流程

如果研究者的工作直接依赖本项目对应的 SCI 论文方法实现、平台设计或数据库整理思想，则还应同时引用对应 SCI 论文。

---

## 目前建议怎么写

### 1. 软件引用

优先使用仓库中的 [CITATION.cff](../CITATION.cff)。

在论文中可以写成类似：

```text
Dietary index computation was performed using DietaryIndex-Py
(Zhiwen Yan, version 0.2.1, AGPL-3.0-or-later).
```

### 2. SCI 论文引用

当你的 SCI 论文正式发表后，建议把下列内容补进仓库：

- 论文标题
- 期刊名
- 年份
- 卷期页码
- DOI

然后同步更新：

- `CITATION.cff`
- `README.md`
- `NOTICE`

---

## 推荐的论文写法

### 方法部分

```text
Dietary pattern scores were calculated using the dietaryindex-py platform,
which provides local-first Python, Next.js, desktop, and API workflows for
dietary index computation and reproducible preprocessing.
```

### 致谢部分

```text
We acknowledge the dietaryindex-py project for providing the computational
implementation and reproducible workflow used in this study.
```

### 软件声明部分

```text
This study used dietaryindex-py for dietary index computation.
Software metadata and citation information are available in the public repository.
```

---

## 如果论文还没发表

在你的 SCI 论文正式接收和上线前，当前最稳妥的做法是：

- 先要求别人引用仓库
- 在 README 和 NOTICE 里明确写明：SCI 论文发表后应补引对应论文

这样不会因为文章尚未分配 DOI 而让引用信息悬空。

---

## 你真正能“硬一点”要求的是什么

更现实地说，你最容易要求成功的是：

- 保留作者和项目署名
- 引用软件仓库
- 在学术使用场景中按照仓库说明补引论文

相比之下，单靠开源许可证直接硬性约束“投稿 SCI 必须引用某篇论文”，法律上通常并不如代码许可义务那么直接。

所以最有效的组合是：

- `LICENSE`
- `CITATION.cff`
- `NOTICE`
- `README`
- 论文与仓库中的明确引用说明

---

## 建议的后续动作

1. SCI 论文接收后，第一时间更新 `CITATION.cff`
2. 在 README 首页增加正式 DOI
3. 在网站首页和 API / Codex 页面增加 “How to cite”
4. 在论文补充材料中写明本项目仓库地址和版本号
