# 计算准确性核验报告（2026-09-11，修订版）

> 核验对象：当前 `dietaryindex` 0.3.0 源码快照。
> 核验口径：通用上传链路使用归档输入与归档 R 输出；NHANES FPED
> 个体食物链路使用原始 Day 1/Day 2 文件重新计算，并按 `SEQN` 与归档 R
> 输出逐行逐列比较。

## 一、通用上传链路

归档的 16 个计算变体全部通过。15 个变体逐位相等；DII 的最大绝对差为
`8.882e-16`，属于浮点精度。

`generated_upload_parity/parity_mismatches.csv` 只记录该组小型上传链路用例，
不能用于代表 NHANES 大样本验证。

## 二、NHANES 2017-2018 FPED 个体食物链路

### 2.1 本次发现并修复的问题

独立源码目录最初会尝试从仓库外的兄弟目录
`dietaryindex-main/R/*.R` 动态读取 FNDDS 食物代码。兄弟目录不存在时会静默
退回不完整的应急列表，导致同一批 6,488 名参与者出现：

| 指数 | 受影响组分 | 受影响行数 | 修复前最大总分差 |
|---|---|---:|---:|
| DASH | SSB / 非 100% 果汁 | 1,499 | 4.0 |
| MEDI | SSB、甜食、离散脂肪 | 5,384 | 2.5 |
| DI-GM | 西兰花、咖啡、发酵乳、绿茶 | 3,800 | 2.5 |

修复方式：将 DASH、MEDI、DI-GM 使用的 15 份 FNDDS 代码表随 Python 包
分发，并让运行时只读取包内数据。代码表由
`scripts/vendor_r_adapter_codes.py` 从上游 R 适配器生成；包运行时不再依赖
本机存在 R 源码仓库。

旧归档 Python 结果中的 5 条 DASH 差异来自 Day 1
`REDPROC_MEAT_SERV=0.68` 恰好落在 60% 分位切点。当前显式 R type-7
边界实现已将这 5 条修正，修复后与归档 R 输出一致。

### 2.2 修复后复算结果

比较容差为 `1e-11`；四组数据均为 6,488 个唯一 `SEQN`，两边无缺行、
无多行，也没有重复主键。

| 指数 | R 行数 | Python 行数 | 共同输出列 | 超容差单元格 | MaxAbsDiff | 状态 |
|---|---:|---:|---:|---:|---:|---|
| DASH | 6,488 | 6,488 | 9 | 0 | 0 | PASS |
| AHEI | 6,488 | 6,488 | 12 | 0 | 5.898e-12 | PASS |
| MEDI | 6,488 | 6,488 | 13 | 0 | 0 | PASS |
| DI-GM `score_average` | 6,488 | 6,488 | 16 | 0 | 0 | PASS |

AHEI 的微小差异来自当前 SAS/XPT 读取和浮点运算环境，未造成评分档位差异。

## 三、样本量统一口径

以后所有“跨语言一致性 N”均定义为：**归档 R 与 Python 输出按参与者主键
成功配对、且进入该指数比较的唯一参与者数**。不得用原始文件总行数、上游
候选人数或其他指数的样本量替代。

| 指数 | 验证数据 | 跨语言比较 N |
|---|---|---:|
| DII | NHANES FPED total | 6,174 |
| HEI-2015 | NHANES FPED total | 6,177 |
| HEI-2020 | NHANES FPED total | 6,315 |
| AHEI | NHANES FPED individual-food | 6,488 |
| DASH | NHANES FPED individual-food | 6,488 |
| DASHI | NHANES nutrient total | 6,488 |
| MED | NHANES FPED total | 6,174 |
| MEDI | NHANES FPED individual-food | 6,488 |
| DI-GM | NHANES FPED individual-food | 6,488 |
| AHEI-P / ACS2020 / PHDI | 合成边界验证 | 1,000，各自不属于 NHANES N |

旧资料中的 `8,704`、`7,641` 是未被明确定义的上游候选/文件口径，不能再
用于跨语言配对结果。若以后需要报告筛选前人数，必须另列“上游候选 N”并附
筛选流程，不能与“跨语言比较 N”共用同一列。

## 四、与文献一致性的边界

- 共有的 R 指数已经具备通用上传链路和部分 NHANES 真实数据对照。
- 引用和组分定义具有可追溯性，但目前仍缺少覆盖所有指数的“论文公开示例值
  回归测试”。
- Python 独有指数不能因为通过软件单元测试就表述为已完成 R 等价验证。
- 本报告是软件计算核验，不替代独立科学复核或论文方法学审查。

## 五、可复现命令

```powershell
python scripts/verify_nhanes_archive_parity.py `
  --nhanes-root "D:\path\to\NHANES\2017-2018" `
  --archive-dir "D:\path\to\archived_r_outputs"
```

默认容差为 `1e-11`。脚本发生缺行、多行或任一共同数值列超出容差时返回非零
退出码。
