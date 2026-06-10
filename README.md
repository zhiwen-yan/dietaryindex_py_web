# dietaryindex (Python)

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

* [English](#english)
* [中文说明](#中文说明)

---

## English

A pure Python implementation of the `dietaryindex` package, fully replicating the scoring algorithms of the original [`dietaryindex` R package](https://github.com/jamesjiadazhan/dietaryindex) (by James J. Zhan) for 12 internationally recognized dietary quality indices.

### 📊 Supported Dietary Indices

| Index | Name | Components | Score Range |
|-------|------|:----------:|:-----------:|
| 🔥 **DII** | Dietary Inflammatory Index | 45 | No upper limit |
| 📊 **HEI-2020** | Healthy Eating Index 2020 | 13 | 0–100 |
| 📊 **HEI-2015** | Healthy Eating Index 2015 | 13 | 0–100 |
| 🫀 **AHEI** | Alternative Healthy Eating Index | 11 | 0–110 |
| 🤰 **AHEIP** | AHEI Pregnancy | 9 | 0–90 |
| 💚 **DASH** | DASH Diet Score | 8 | 8–40 |
| ❤️ **DASHI** | DASH Nutrient Density | 9 | 0–9 |
| 🫒 **MED** | Mediterranean Diet Index | 9 | 0–9 |
| 🐟 **MEDI** | MEDI (PREDIMED) | 11 | 0–11 |
| 🎗️ **ACS2020** | ACS Cancer Prevention | 8 | 0–15 |
| 🌍 **PHDI** | Planetary Health Diet Index | 16 | 0–150 |
| 🦠 **DI-GM** | Dietary Index for Gut Microbiota | 14 | 0–14 |

---

### 🚀 Installation

#### Option 1: Via PyPI (Recommended)

```bash
# Core package only (numpy + pandas + scipy)
pip install dietaryindex

# With NHANES adapters (requires pyreadstat for SAS/XPT files)
pip install dietaryindex[adapters]

# With Streamlit Web Interface (plotly + openpyxl)
pip install dietaryindex[streamlit]

# Install all dependencies
pip install dietaryindex[all]
```

#### Option 2: From Source

```bash
git clone https://github.com/zhiwen-yan/dietaryindex_py.git
cd dietaryindex_py
pip install -e .
```

#### Option 3: Docker (Run Streamlit App)

```bash
docker compose up --build
```
Once started, visit `http://localhost:8501`.

---

### 📖 Quick Start

#### Core Computation (Any Data Source)

```python
import pandas as pd
from dietaryindex import compute_hei2020

# Load your prepared dietary data
df = pd.read_csv("my_diet_data.csv")

result = compute_hei2020(
    data=df,
    respondent_id=df["ID"].values,
    age=df["AGE"].values,
    total_kcal=df["KCAL"].values,
    total_fruit=df["FRUIT"].values,
    whole_fruit=df["WHOLE_FRUIT"].values,
    total_vegetable=df["VEG"].values,
    greens_and_beans=df["GREENS"].values,
    whole_grains=df["WGRAIN"].values,
    dairy=df["DAIRY"].values,
    total_protein=df["PROTEIN"].values,
    seafood_plant_protein=df["SEAFOOD"].values,
    fatty_acids=df["FA_RATIO"].values,
    refined_grains=df["RGRAIN"].values,
    sodium=df["SODIUM"].values,
    added_sugars=df["SUGAR"].values,
    saturated_fat=df["SFAT"].values,
)

print(result.head())
```

#### NHANES FPED Adapter (2005+, One-Step Calculation)

```python
from dietaryindex import compute_hei2020_nhanes_fped

result = compute_hei2020_nhanes_fped(
    fped_path="fped_dr1tot_1718.sas7bdat",
    nutrient_path="DR1TOT_J.XPT",
    demo_path="DEMO_J.XPT",
)
```

#### ASA24 / DHQ3 / BLOCK FFQ Adapters

```python
from dietaryindex import compute_dii_asa24, compute_dii_dhq3, compute_dii_block

# ASA24 Totals.csv
result = compute_dii_asa24("Totals.csv")

# DHQ3 Total Daily Results
result = compute_dii_dhq3("results.csv")

# BLOCK FFQ raw data
result = compute_dii_block("block_data.csv")
```

---

### 🧪 Streamlit Web Interface

Run the local web application:

```bash
pip install dietaryindex[streamlit]
cd streamlit_app
python -m streamlit run app.py
```
Open `http://localhost:8501` in your browser to upload data, map columns, view interactive plots, and export results.

---

### 📁 Data Source Support

| Data Source | Mode | File Format | API |
|-------------|------|-------------|-----|
| **Generic** | Column Mapping | CSV / Excel | `compute_xxx(data, ...)` |
| **NHANES FPED** (2005+) | Auto-parsed | .sas7bdat + .XPT | `compute_xxx_nhanes_fped(...)` |
| **NHANES MPED** (1999–2004) | Auto-parsed | equiv.txt + .XPT | `compute_xxx_nhanes_mped(...)` |
| **ASA24** | Auto-summarized | Totals.csv | `compute_dii_asa24(...)` |
| **DHQ3** | One-step | detail.csv | `compute_xxx_dhq3(...)` |
| **BLOCK FFQ** | One-step | CSV | `compute_xxx_block(...)` |

---

## 中文说明

**纯 Python 实现的 dietaryindex 膳食指数计算包**，完整复现 [dietaryindex R 包](https://github.com/jamesjiadazhan/dietaryindex) (James J. Zhan) 的全部 12 个国际通用膳食质量评估指数。

### 📊 支持的膳食指数

| 指数 | 英文名 | 组分 | 总分 |
|------|--------|:---:|:----:|
| 🔥 **DII** | Dietary Inflammatory Index | 45 | 无上限 |
| 📊 **HEI-2020** | Healthy Eating Index 2020 | 13 | 0–100 |
| 📊 **HEI-2015** | Healthy Eating Index 2015 | 13 | 0–100 |
| 🫀 **AHEI** | Alternative Healthy Eating Index | 11 | 0–110 |
| 🤰 **AHEIP** | AHEI Pregnancy | 9 | 0–90 |
| 💚 **DASH** | DASH Diet Score | 8 | 8–40 |
| ❤️ **DASHI** | DASH Nutrient Density | 9 | 0–9 |
| 🫒 **MED** | Mediterranean Diet Index | 9 | 0–9 |
| 🐟 **MEDI** | MEDI (PREDIMED) | 11 | 0–11 |
| 🎗️ **ACS2020** | ACS Cancer Prevention | 8 | 0–15 |
| 🌍 **PHDI** | Planetary Health Diet Index | 16 | 0–150 |
| 🦠 **DI-GM** | Dietary Index for Gut Microbiota | 14 | 0–14 |

---

### 🚀 安装

#### 方式一：PyPI（推荐）

```bash
# 仅核心计算（numpy + pandas + scipy）
pip install dietaryindex

# 含 NHANES 适配器（需要 pyreadstat 读取 SAS/XPT 文件）
pip install dietaryindex[adapters]

# 含 Streamlit Web 界面（plotly 图表 + Excel 导出）
pip install dietaryindex[streamlit]

# 全部安装
pip install dietaryindex[all]
```

#### 方式二：从源码安装

```bash
git clone https://github.com/zhiwen-yan/dietaryindex_py.git
cd dietaryindex_py
pip install -e .
```

#### 方式三：Docker 运行 Streamlit

```bash
docker compose up --build
```
启动后访问 `http://localhost:8501`。

---

### 📖 快速开始

#### 核心计算（任何数据源）

```python
import pandas as pd
from dietaryindex import compute_hei2020

# 读取已整理好的膳食数据
df = pd.read_csv("my_diet_data.csv")

result = compute_hei2020(
    data=df,
    respondent_id=df["ID"].values,
    age=df["AGE"].values,
    total_kcal=df["KCAL"].values,
    total_fruit=df["FRUIT"].values,
    whole_fruit=df["WHOLE_FRUIT"].values,
    total_vegetable=df["VEG"].values,
    greens_and_beans=df["GREENS"].values,
    whole_grains=df["WGRAIN"].values,
    dairy=df["DAIRY"].values,
    total_protein=df["PROTEIN"].values,
    seafood_plant_protein=df["SEAFOOD"].values,
    fatty_acids=df["FA_RATIO"].values,
    refined_grains=df["RGRAIN"].values,
    sodium=df["SODIUM"].values,
    added_sugars=df["SUGAR"].values,
    saturated_fat=df["SFAT"].values,
)

print(result.head())
```

#### NHANES FPED 适配器（2005 年后，一步式计算）

```python
from dietaryindex import compute_hei2020_nhanes_fped

result = compute_hei2020_nhanes_fped(
    fped_path="fped_dr1tot_1718.sas7bdat",
    nutrient_path="DR1TOT_J.XPT",
    demo_path="DEMO_J.XPT",
)
```

#### ASA24 / DHQ3 / BLOCK FFQ 适配器

```python
from dietaryindex import compute_dii_asa24, compute_dii_dhq3, compute_dii_block

# ASA24 Totals.csv
result = compute_dii_asa24("Totals.csv")

# DHQ3 Total Daily Results
result = compute_dii_dhq3("results.csv")

# BLOCK FFQ 原始数据
result = compute_dii_block("block_data.csv")
```

---

### 🧪 Streamlit Web 界面

启动本地 Web 应用：

```bash
pip install dietaryindex[streamlit]
cd streamlit_app
python -m streamlit run app.py
```
浏览器自动打开 `http://localhost:8501`，即可在图形界面中上传数据、映射列名、查看图表并导出结果。

---

### 📁 数据源支持

| 数据源 | 模式 | 文件格式 | API |
|--------|------|---------|-----|
| **通用** | 列名映射 | CSV / Excel | `compute_xxx(data, ...)` |
| **NHANES FPED** (2005+) | 自动解析 | .sas7bdat + .XPT | `compute_xxx_nhanes_fped(...)` |
| **NHANES MPED** (1999–2004) | 自动解析 | equiv.txt + .XPT | `compute_xxx_nhanes_mped(...)` |
| **ASA24** | 自动汇总 | Totals.csv | `compute_dii_asa24(...)` |
| **DHQ3** | 一步式 | detail.csv | `compute_xxx_dhq3(...)` |
| **BLOCK FFQ** | 一步式 | CSV | `compute_xxx_block(...)` |

---

## 🔧 Dependencies / 依赖

| Package / 依赖包 | Required / 是否必需 | Usage / 用途 |
|------------------|:-------------------:|--------------|
| numpy ≥ 1.24 | ✅ | 数值计算 / Numerical computing |
| pandas ≥ 2.0 | ✅ | 数据处理 / Data processing |
| scipy ≥ 1.10 | ✅ | 统计函数 / Statistical functions |
| pyreadstat ≥ 1.2 | ❌ | SAS/XPT 文件读取 / Reading SAS/XPT files (NHANES) |
| streamlit ≥ 1.28 | ❌ | Web 界面 / Web interface |
| plotly ≥ 5.18 | ❌ | 图表可视化 / Data visualization |
| openpyxl ≥ 3.1 | ❌ | Excel 导出 / Excel export |

---

## 📚 References / 参考文献

1. Shivappa N, et al. "Designing and developing a literature-derived, population-based dietary inflammatory index." *Public Health Nutrition*, 2014.
2. Krebs-Smith SM, et al. "Update of the Healthy Eating Index: HEI-2015." *J Acad Nutr Diet*, 2018.
3. Chiuve SE, et al. "Alternative dietary indices both strongly predict risk of chronic disease." *J Nutr*, 2012.
4. Fung TT, et al. "Adherence to a DASH-style diet and risk of coronary heart disease and stroke." *Arch Intern Med*, 2008.
5. Trichopoulou A, et al. "Adherence to a Mediterranean diet and survival in a Greek population." *N Engl J Med*, 2003.
6. Cacau LT, et al. "Development and Validation of an Index Based on EAT-Lancet Recommendations." *J Nutr*, 2021.
7. Kase BE, et al. "Development and evaluation of a dietary index assessing diet-gut microbiome interactions." *J Nutr*, 2023.

---

## 📄 License / 协议

MIT License. Based on the [dietaryindex R package](https://github.com/jamesjiadazhan/dietaryindex).
