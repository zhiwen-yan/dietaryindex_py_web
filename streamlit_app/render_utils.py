"""
共享页面渲染工具 — 为所有指数页面提供 DII 风格的模式选择和上传 UI

每个指数页面调用 render_full_index_page() 即可获得完整的模式选择 + 计算 UI。
"""

import sys
import os
import tempfile
from io import BytesIO

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.params import INDEX_PARAMS
from config.i18n import t, get_lang, set_lang
from sidebar_utils import render_sidebar as _render_shared_sidebar

# templates / sample_data / utils / dietaryindex 全部延迟加载，避免 import render_sidebar 时触发全量计算引擎

_HEAVY = None

def _lazy_import_heavy():
    """延迟加载 utils 和 dietaryindex 重型模块，仅在进入指数计算页时触发。"""
    global _HEAVY
    if _HEAVY is None:
        from utils import load_data, _run_computation, _show_result
        from dietaryindex import (
            compute_dii_nhanes_fped, compute_hei2015_nhanes_fped,
            compute_hei2020_nhanes_fped, compute_med_nhanes_fped,
            compute_dashi_nhanes_fped, compute_dash_nhanes_fped,
            compute_ahei_nhanes_fped, compute_medi_nhanes_fped,
            compute_di_gm_nhanes_fped, compute_dii_nhanes_mped,
            compute_hei2015_nhanes_mped, compute_hei2020_nhanes_mped,
            compute_med_nhanes_mped, compute_dashi_nhanes_mped,
            compute_ahei_nhanes_mped, compute_medi_nhanes_mped,
            compute_dash_nhanes_mped, compute_di_gm_nhanes_mped,
            compute_dii_asa24, compute_dii_dhq3, compute_ahei_dhq3,
            compute_dii_block, compute_ahei_block, compute_aheip_block,
        )
        _HEAVY = {
            "load_data": load_data,
            "_run_computation": _run_computation,
            "_show_result": _show_result,
            # NHANES FPED adapters
            "compute_dii_nhanes_fped": compute_dii_nhanes_fped,
            "compute_hei2015_nhanes_fped": compute_hei2015_nhanes_fped,
            "compute_hei2020_nhanes_fped": compute_hei2020_nhanes_fped,
            "compute_med_nhanes_fped": compute_med_nhanes_fped,
            "compute_dashi_nhanes_fped": compute_dashi_nhanes_fped,
            "compute_dash_nhanes_fped": compute_dash_nhanes_fped,
            "compute_ahei_nhanes_fped": compute_ahei_nhanes_fped,
            "compute_medi_nhanes_fped": compute_medi_nhanes_fped,
            "compute_di_gm_nhanes_fped": compute_di_gm_nhanes_fped,
            # NHANES MPED adapters
            "compute_dii_nhanes_mped": compute_dii_nhanes_mped,
            "compute_hei2015_nhanes_mped": compute_hei2015_nhanes_mped,
            "compute_hei2020_nhanes_mped": compute_hei2020_nhanes_mped,
            "compute_med_nhanes_mped": compute_med_nhanes_mped,
            "compute_dashi_nhanes_mped": compute_dashi_nhanes_mped,
            "compute_ahei_nhanes_mped": compute_ahei_nhanes_mped,
            "compute_medi_nhanes_mped": compute_medi_nhanes_mped,
            "compute_dash_nhanes_mped": compute_dash_nhanes_mped,
            "compute_di_gm_nhanes_mped": compute_di_gm_nhanes_mped,
            # ASA24 / DHQ3 / BLOCK adapters
            "compute_dii_asa24": compute_dii_asa24,
            "compute_dii_dhq3": compute_dii_dhq3,
            "compute_ahei_dhq3": compute_ahei_dhq3,
            "compute_dii_block": compute_dii_block,
            "compute_ahei_block": compute_ahei_block,
            "compute_aheip_block": compute_aheip_block,
        }
    return _HEAVY


# ═══════════════════════════════════════════════════════════════════════════════
# 各指数支持的模式配置
# ═══════════════════════════════════════════════════════════════════════════════

# 每个指数对应的可用模式列表
INDEX_MODE_CONFIG = {
    "DII": ["general", "nhanes_fped", "nhanes_mped", "asa24", "dhq3", "block"],
    "HEI2015": ["general", "nhanes_fped", "nhanes_mped", "asa24", "dhq3", "block"],
    "HEI2020": ["general", "nhanes_fped", "nhanes_mped", "asa24"],
    "HEI2020_V1": ["general", "nhanes_fped", "nhanes_mped", "asa24"],
    "HEI2020_V2": ["general", "nhanes_fped", "nhanes_mped", "asa24"],
    "AHEI": ["general", "nhanes_fped", "nhanes_mped", "asa24", "dhq3", "block"],
    "AHEIP": ["general", "dhq3", "block"],
    "DASH": ["general", "nhanes_fped", "nhanes_mped", "asa24", "dhq3", "block"],
    "DASHI": ["general", "nhanes_fped", "nhanes_mped"],
    "MED": ["general", "nhanes_fped", "nhanes_mped", "asa24", "dhq3", "block"],
    "MEDI": ["general", "nhanes_fped", "nhanes_mped"],
    "MEDI_V1": ["general", "nhanes_fped", "nhanes_mped"],
    "MEDI_V2": ["general", "nhanes_fped", "nhanes_mped"],
    "ACS2020": ["general"],
    "ACS2020_V1": ["general"],
    "ACS2020_V2": ["general"],
    "PHDI": ["general"],
    "PHDI_V1": ["general"],
    "PHDI_V2": ["general"],
    "DI_GM": ["general", "nhanes_fped", "nhanes_mped"],
}

# FPED tot 级适配器映射（函数名，通过 _lazy_import_heavy() 解析）
FPED_TOT_ADAPTER_KEYS = {
    "HEI2015": "compute_hei2015_nhanes_fped",
    "HEI2020": "compute_hei2020_nhanes_fped",
    "HEI2020_V1": "compute_hei2020_nhanes_fped",
    "HEI2020_V2": "compute_hei2020_nhanes_fped",
    "MED": "compute_med_nhanes_fped",
    "DASHI": "compute_dashi_nhanes_fped",
}

# FPED iff 级适配器映射
FPED_IFF_ADAPTER_KEYS = {
    "DASH": "compute_dash_nhanes_fped",
    "AHEI": "compute_ahei_nhanes_fped",
    "MEDI": "compute_medi_nhanes_fped",
    "MEDI_V1": "compute_medi_nhanes_fped",
    "MEDI_V2": "compute_medi_nhanes_fped",
    "DI_GM": "compute_di_gm_nhanes_fped",
}

# MPED 适配器映射
MPED_ADAPTER_KEYS = {
    "HEI2015": "compute_hei2015_nhanes_mped",
    "HEI2020": "compute_hei2020_nhanes_mped",
    "HEI2020_V1": "compute_hei2020_nhanes_mped",
    "HEI2020_V2": "compute_hei2020_nhanes_mped",
    "MED": "compute_med_nhanes_mped",
    "DASHI": "compute_dashi_nhanes_mped",
    "AHEI": "compute_ahei_nhanes_mped",
    "MEDI": "compute_medi_nhanes_mped",
    "MEDI_V1": "compute_medi_nhanes_mped",
    "MEDI_V2": "compute_medi_nhanes_mped",
    "DASH": "compute_dash_nhanes_mped",
    "DI_GM": "compute_di_gm_nhanes_mped",
}

def _resolve_adapter(adapter_map, key):
    """根据 key 查找适配器函数名，再通过 _lazy_import_heavy() 获取实际函数"""
    h = _lazy_import_heavy()
    return h[adapter_map[key]]

# 模式标签定义
MODE_LABELS_ZH = {
    "general": ("通用版（列名映射）",
                "上传一份整理好的 CSV/Excel 文件，手动映射列名到参数。适用于所有数据来源。"),
    "nhanes_fped": ("NHANES FPED（2005年后）",
                    "直接上传 NHANES FPED 原始数据文件（.sas7bdat + .XPT），系统自动解析并合并 Day1+Day2。"),
    "nhanes_mped": ("NHANES MPED（1999-2004）",
                    "直接上传 NHANES MPED 原始数据文件（equiv.txt + .XPT），适用于 1999-2004 周期。"),
    "asa24": ("ASA24",
             "上传 ASA24 导出的 Totals.csv 文件，系统自动汇总所有回忆记录。"),
    "dhq3": ("DHQ3",
             "上传 DHQ3 导出的 Total Daily Results CSV 文件，一步式计算。"),
    "block": ("BLOCK FFQ",
              "上传 BLOCK 食物频率问卷数据文件，自动识别列名并计算。"),
}

MODE_LABELS_EN = {
    "general": ("General (Column Mapping)",
                "Upload a pre-processed CSV/Excel file and manually map column names to parameters. Works for all data sources."),
    "nhanes_fped": ("NHANES FPED (Post-2005)",
                    "Directly upload NHANES FPED raw data files (.sas7bdat + .XPT). System auto-parses and merges Day1+Day2."),
    "nhanes_mped": ("NHANES MPED (1999-2004)",
                    "Directly upload NHANES MPED raw data files (equiv.txt + .XPT), for 1999-2004 cycles."),
    "asa24": ("ASA24",
             "Upload ASA24 exported Totals.csv file. System auto-aggregates all recall records."),
    "dhq3": ("DHQ3",
             "Upload DHQ3 exported Total Daily Results CSV file. One-step computation."),
    "block": ("BLOCK FFQ",
              "Upload BLOCK food frequency questionnaire data file. Auto-recognizes columns and computes."),
}

def _mode_label(mode):
    """根据当前语言返回模式标签和描述"""
    return MODE_LABELS_EN[mode] if get_lang() == "en" else MODE_LABELS_ZH[mode]

# FPED tot 需要的信息说明
FPED_TOT_FILES_INFO = {
    "HEI2015": """**第1天（Day 1）文件：**
| 文件类型 | 文件名示例 | 格式 |
|---------|-----------|------|
| FPED 数据 | `fpre_dr1tot_1718.sas7bdat` | SAS |
| 总营养素 | `DR1TOT_J.XPT` | XPT |
| 人口数据 | `DEMO_J.XPT` | XPT |

**第2天（Day 2）文件（可选）：**
| 文件类型 | 文件名示例 | 格式 |
|---------|-----------|------|
| FPED 数据 | `fpre_dr2tot_1718.sas7bdat` | SAS |
| 总营养素 | `DR2TOT_J.XPT` | XPT |

**数据合并逻辑**：按 SEQN 合并 Day1+Day2，两日营养素取平均值。仅提供 Day1 时使用 Day1 数据。""",
    "HEI2020": """**第1天（Day 1）文件：**
| 文件类型 | 文件名示例 | 格式 |
|---------|-----------|------|
| FPED 数据 | `fped_dr1tot_1718.sas7bdat` | SAS |
| 总营养素 | `DR1TOT_J.XPT` | XPT |
| 人口数据 | `DEMO_J.XPT` (需含 RIDAGEYR) | XPT |

**第2天（Day 2）文件（可选）：**
| 文件类型 | 文件名示例 | 格式 |
|---------|-----------|------|
| FPED 数据 | `fped_dr2tot_1718.sas7bdat` | SAS |
| 总营养素 | `DR2TOT_J.XPT` | XPT |

**HEI2020 特殊说明**：自动根据 RIDAGEYR 年龄选择 V1（>=2岁）或 Toddlers（1-2岁）版本。""",
    "MED": """**第1天（Day 1）文件：**
| 文件类型 | 文件名示例 | 格式 |
|---------|-----------|------|
| FPED 数据 | `fpre_dr1tot_1718.sas7bdat` | SAS |
| 总营养素 | `DR1TOT_J.XPT` | XPT |
| 人口数据 | `DEMO_J.XPT` | XPT |

**MED 使用中位数评分**，不适用于跨人群比较。建议仅用于单一人群的内部相对排名。""",
    "DASHI": """**DASHI 仅需营养素文件，无需 FPED 食物组数据。**

| 文件类型 | 文件名示例 | 格式 | 说明 |
|---------|-----------|------|------|
| 总营养素 Day1 | `DR1TOT_J.XPT` | XPT | 必需 |
| 总营养素 Day2 | `DR2TOT_J.XPT` | XPT | 可选 |
| 人口数据 | `DEMO_J.XPT` | XPT | 可选 |

**DASHI 核心指标**：总脂肪、饱和脂肪、蛋白质、胆固醇、纤维、钾、镁、钙、钠（均经能量调整）。""",
}

FPED_TOT_FILES_INFO_EN = {
    "HEI2015": """**Day 1 — Required:**
| File Type | Example | Format |
|---------|-----------|------|
| FPED Data | `fpre_dr1tot_1718.sas7bdat` | SAS |
| Total Nutrient | `DR1TOT_J.XPT` | XPT |
| Demographics | `DEMO_J.XPT` | XPT |

**Day 2 — Optional:**
| File Type | Example | Format |
|---------|-----------|------|
| FPED Data | `fpre_dr2tot_1718.sas7bdat` | SAS |
| Total Nutrient | `DR2TOT_J.XPT` | XPT |

**Merge logic**: Day1+Day2 merged by SEQN, nutrients averaged across two days. Day1-only uses Day1 data.""",
    "HEI2020": """**Day 1 — Required:**
| File Type | Example | Format |
|---------|-----------|------|
| FPED Data | `fped_dr1tot_1718.sas7bdat` | SAS |
| Total Nutrient | `DR1TOT_J.XPT` | XPT |
| Demographics | `DEMO_J.XPT` (must include RIDAGEYR) | XPT |

**Day 2 — Optional:**
| File Type | Example | Format |
|---------|-----------|------|
| FPED Data | `fped_dr2tot_1718.sas7bdat` | SAS |
| Total Nutrient | `DR2TOT_J.XPT` | XPT |

**HEI2020 Note**: Auto-selects V1 (>=2 yrs) or Toddlers (1-2 yrs) based on RIDAGEYR age column.""",
    "MED": """**Day 1 — Required:**
| File Type | Example | Format |
|---------|-----------|------|
| FPED Data | `fpre_dr1tot_1718.sas7bdat` | SAS |
| Total Nutrient | `DR1TOT_J.XPT` | XPT |
| Demographics | `DEMO_J.XPT` | XPT |

**MED uses median-based scoring**; not suitable for cross-population comparison. Recommended for within-population relative ranking only.""",
    "DASHI": """**DASHI requires only nutrient files — no FPED food group data needed.**

| File Type | Example | Format | Notes |
|---------|-----------|------|------|
| Total Nutrient Day1 | `DR1TOT_J.XPT` | XPT | Required |
| Total Nutrient Day2 | `DR2TOT_J.XPT` | XPT | Optional |
| Demographics | `DEMO_J.XPT` | XPT | Optional |

**DASHI core indicators**: Total fat, saturated fat, protein, cholesterol, fiber, potassium, magnesium, calcium, sodium (all energy-adjusted).""",
}

# FPED iff 需要的信息说明
FPED_IFF_FILES_INFO = {
    "DASH": """**DASH 需要个体食物级别数据（iff），用于识别特殊食物类别。**

**第1天（Day 1）文件：**
| 文件类型 | 文件名示例 | 格式 |
|---------|-----------|------|
| FPED iff 数据 | `fped_dr1iff_1718.sas7bdat` | SAS |
| 营养素 iff | `DR1IFF_J.XPT` | XPT |
| 人口数据 | `DEMO_J.XPT` | XPT |

**第2天（Day 2）文件（可选）：**
| 文件类型 | 文件名示例 | 格式 |
|---------|-----------|------|
| FPED iff 数据 | `fped_dr2iff_1718.sas7bdat` | SAS |
| 营养素 iff | `DR2IFF_J.XPT` | XPT |

**DASH 使用五分位数评分**，基于食物组份量（杯/盎司等价）。系统自动识别 SSB、脱脂奶、低脂奶酪等食物编码。""",
    "AHEI": """**AHEI 需要个体食物级别数据（iff），用于识别含糖饮料和计算 omega-3 脂肪酸。**

**第1天（Day 1）文件：**
| 文件类型 | 文件名示例 | 格式 |
|---------|-----------|------|
| FPED iff 数据 | `fped_dr1iff_1718.sas7bdat` | SAS |
| 营养素 iff | `DR1IFF_J.XPT` | XPT |
| 人口数据 | `DEMO_J.XPT` (需含 RIAGENDR) | XPT |

**AHEI 需要 DEMO 中的性别 (RIAGENDR)** 用于区分男女评分标准。""",
    "MEDI": """**MEDI 需要个体食物级别数据（iff），用于识别橄榄油、甜食、油脂等特殊食物。**

**第1天（Day 1）文件：**
| 文件类型 | 文件名示例 | 格式 |
|---------|-----------|------|
| FPED iff 数据 | `fped_dr1iff_1718.sas7bdat` | SAS |
| 营养素 iff | `DR1IFF_J.XPT` | XPT |
| 人口数据 | `DEMO_J.XPT` | XPT |

**MEDI 自动识别**：橄榄油、甜食、固体油脂、含糖饮料的食物编码，按克重/份量换算。""",
    "DI_GM": """**DI_GM 需要个体食物级别数据（iff），用于识别多种特定食物类别。**

**第1天（Day 1）文件：**
| 文件类型 | 文件名示例 | 格式 |
|---------|-----------|------|
| FPED iff 数据 | `fped_dr1iff_1718.sas7bdat` | SAS |
| 营养素 iff | `DR1IFF_J.XPT` | XPT |
| 人口数据 | `DEMO_J.XPT` (需含 RIAGENDR) | XPT |

**DI_GM 自动识别 8 类食物**：牛油果、西兰花、鹰嘴豆、咖啡、蔓越莓、发酵乳制品、绿茶、大豆。需要 DEMO 中的性别用于咖啡评分。""",
}

FPED_IFF_FILES_INFO_EN = {
    "DASH": """**DASH requires individual food-level data (iff) to identify specific food categories.**

**Day 1 — Required:**
| File Type | Example | Format |
|---------|-----------|------|
| FPED iff Data | `fped_dr1iff_1718.sas7bdat` | SAS |
| Nutrient iff | `DR1IFF_J.XPT` | XPT |
| Demographics | `DEMO_J.XPT` | XPT |

**Day 2 — Optional:**
| File Type | Example | Format |
|---------|-----------|------|
| FPED iff Data | `fped_dr2iff_1718.sas7bdat` | SAS |
| Nutrient iff | `DR2IFF_J.XPT` | XPT |

**DASH uses quintile-based scoring**, based on food group servings (cup/oz equivalents). Auto-identifies SSBs, skim milk, low-fat cheese, etc.""",
    "AHEI": """**AHEI requires individual food-level data (iff) to identify sugar-sweetened beverages and calculate omega-3 fatty acids.**

**Day 1 — Required:**
| File Type | Example | Format |
|---------|-----------|------|
| FPED iff Data | `fped_dr1iff_1718.sas7bdat` | SAS |
| Nutrient iff | `DR1IFF_J.XPT` | XPT |
| Demographics | `DEMO_J.XPT` (must include RIAGENDR) | XPT |

**AHEI requires gender (RIAGENDR) from DEMO** for sex-specific scoring criteria.""",
    "MEDI": """**MEDI requires individual food-level data (iff) to identify olive oil, sweets, discretionary fats, etc.**

**Day 1 — Required:**
| File Type | Example | Format |
|---------|-----------|------|
| FPED iff Data | `fped_dr1iff_1718.sas7bdat` | SAS |
| Nutrient iff | `DR1IFF_J.XPT` | XPT |
| Demographics | `DEMO_J.XPT` | XPT |

**MEDI auto-identifies**: olive oil, sweets, solid fats, SSBs by food codes, converted by weight/servings.""",
    "DI_GM": """**DI-GM requires individual food-level data (iff) to identify multiple specific food categories.**

**Day 1 — Required:**
| File Type | Example | Format |
|---------|-----------|------|
| FPED iff Data | `fped_dr1iff_1718.sas7bdat` | SAS |
| Nutrient iff | `DR1IFF_J.XPT` | XPT |
| Demographics | `DEMO_J.XPT` (must include RIAGENDR) | XPT |

**DI-GM auto-identifies 8 food categories**: avocado, broccoli, chickpeas, coffee, cranberries, fermented dairy, green tea, soy. Requires gender from DEMO for coffee scoring.""",
}

# 各指数的 DII 风格通用模板
INDEX_GENERAL_TEMPLATES = {
    "DII": {
        "desc": """**适用场景**：您已经将膳食数据整理好（每个参与者一行，每列一个食物/营养素变量），手动映射列名到 DII 参数。
**文件要求**：CSV 或 Excel，每行一个参与者。需要参与者 ID 列。推荐包含至少 28 个 DII 参数以获得准确结果。""",
        "en_desc": """**Use case**: You have pre-processed dietary data (one row per participant, one column per food/nutrient variable) and want to map columns to DII parameters manually.
**File requirements**: CSV or Excel, one row per participant. A participant ID column is required. At least 28 DII parameters are recommended for accurate results.""",
        "output_cols": ["DII_ALL", "DII_NOETOH"],
    },
    "HEI2015": {
        "desc": """**适用场景**：您已经将膳食数据整理好（每个参与者一行），手动映射列名后计算。
**文件要求**：CSV 或 Excel，每行一个参与者。需要参与者 ID 列。
**参数覆盖**：15 个 HEI2015 组分（总量水果、完整水果、总蔬菜、深绿色蔬菜与豆类、总蛋白质食物、海鲜与植物蛋白、全谷物、乳制品、脂肪酸比、精制谷物、钠、添加糖、饱和脂肪）。""",
        "en_desc": """**Use case**: You have pre-processed dietary data (one row per participant) and need to map columns manually.
**File requirements**: CSV or Excel, one row per participant. A participant ID column is required.
**Parameters**: 15 HEI2015 components (Total Fruits, Whole Fruits, Total Vegetables, Greens & Beans, Total Protein Foods, Seafood & Plant Proteins, Whole Grains, Dairy, Fatty Acid Ratio, Refined Grains, Sodium, Added Sugars, Saturated Fat).""",
        "output_cols": ["HEI2015_ALL"],
    },
    "HEI2020": {
        "desc": """**适用场景**：同上，支持 Toddlers (1-2岁) 版本自动切换。
**文件要求**：CSV 或 Excel。需要参与者 ID 和年龄 (AGE) 列。
**参数覆盖**：15 个 HEI2020 组分（同 HEI2015，新增 Toddlers 评分标准）。""",
        "en_desc": """**Use case**: Same as HEI2015, with automatic Toddler (1-2 years) version switching.
**File requirements**: CSV or Excel. Participant ID and age (AGE) column required.
**Parameters**: 15 HEI2020 components (same as HEI2015, with additional Toddler scoring criteria).""",
        "output_cols": ["HEI2020_ALL"],
    },
    "HEI2020_V1": {
        "desc": """**HEI2020 V1 (百分比能量版) \u2014 推荐版本**。添加糖与饱和脂肪以百分比能量 (%energy) 直接进行计算，钠以 g/1000kcal 计。
**文件要求**：CSV 或 Excel。需要参与者 ID、年龄 (AGE) 列。""",
        "en_desc": """**HEI2020 V1 (Energy Percentage) \u2014 Recommended**. Added sugars and saturated fat as % energy. Sodium in g/1000kcal.
**File requirements**: CSV or Excel. Participant ID and age (AGE) column required.""",
        "output_cols": ["HEI2020_ALL"],
    },
    "HEI2020_V2": {
        "desc": """**HEI2020 V2 (原始摄入量版)**。添加糖以茶匙 (tsp)、饱和脂肪以克 (g)、钠以毫克 (mg) 输入，系统自动由总能量进行比例和密度转化。
**文件要求**：CSV 或 Excel。需要参与者 ID、年龄 (AGE)、总能量 (KCAL) 列。""",
        "en_desc": """**HEI2020 V2 (Raw Intake)**. Added sugars in tsp, saturated fat in g, sodium in mg. System auto-converts based on total energy.
**File requirements**: CSV or Excel. Participant ID, age (AGE), and total energy (KCAL) columns required.""",
        "output_cols": ["HEI2020_ALL"],
    },
    "AHEI": {
        "desc": """**适用场景**：已整理好的膳食数据，需包含性别列用于区分男女评分。
**文件要求**：CSV 或 Excel。需要参与者 ID 和性别 (GENDER) 列。
**参数覆盖**：11 个 AHEI 组分（蔬菜、水果、全谷物、坚果豆类、多不饱和脂肪、Omega-3、含糖饮料、红肉加工肉、反式脂肪、钠、酒精）""",
        "en_desc": """**Use case**: Pre-processed dietary data, requires a gender column for sex-specific scoring.
**File requirements**: CSV or Excel. Participant ID and gender (GENDER) column required.
**Parameters**: 11 AHEI components (Vegetables, Fruits, Whole Grains, Nuts & Legumes, PUFA, Omega-3, SSBs, Red & Processed Meat, Trans Fat, Sodium, Alcohol).""",
        "output_cols": ["AHEI_ALL", "AHEI_NOETOH"],
    },
    "AHEIP": {
        "desc": """**AHEIP (AHEI-Pregnancy)** 专为孕期女性设计，评分标准与普通 AHEI 不同。
**文件要求**：CSV 或 Excel。需要参与者 ID。
**参数覆盖**：11 个 AHEIP 组分（孕期特化的评分标准）。""",
        "en_desc": """**AHEIP (AHEI-Pregnancy)** Designed specifically for pregnant women with different scoring criteria from regular AHEI.
**File requirements**: CSV or Excel. Participant ID required.
**Parameters**: 11 AHEIP components (pregnancy-specific scoring criteria).""",
        "output_cols": ["AHEIP_ALL"],
    },
    "DASH": {
        "desc": """**DASH 使用五分位数评分法**，基于食物组份量（份/日）。
**文件要求**：CSV 或 Excel。需要参与者 ID。
**参数覆盖**：8 个 DASH 组分（水果、蔬菜、全谷物、坚果豆类、低脂乳制品、红肉加工肉、钠、含糖饮料）。""",
        "en_desc": """**DASH uses quintile-based scoring** based on food group servings (servings/day).
**File requirements**: CSV or Excel. Participant ID required.
**Parameters**: 8 DASH components (Fruits, Vegetables, Whole Grains, Nuts & Legumes, Low-fat Dairy, Red & Processed Meat, Sodium, SSBs).""",
        "output_cols": ["DASH_ALL"],
    },
    "DASHI": {
        "desc": """**DASHI (DASH Nutrient Index)** 不基于食物组份量，而是基于纯营养素指标。
**文件要求**：CSV 或 Excel。需要参与者 ID 和总能量 (KCAL)。
**参数覆盖**：9 种营养素（总脂肪、饱和脂肪、蛋白质、胆固醇、纤维、钾、镁、钙、钠），均按能量调整。""",
        "en_desc": """**DASHI (DASH Nutrient Index)** Based on nutrient indicators rather than food group servings.
**File requirements**: CSV or Excel. Participant ID and total energy (KCAL) required.
**Parameters**: 9 nutrients (Total Fat, Saturated Fat, Protein, Cholesterol, Fiber, Potassium, Magnesium, Calcium, Sodium), all energy-adjusted.""",
        "output_cols": ["DASHI_ALL"],
    },
    "MED": {
        "desc": """**MED (Mediterranean Diet Score)** 使用中位数排名法评分。
**文件要求**：CSV 或 Excel。需要参与者 ID。
**参数覆盖**：10 个 MED 组分（水果、蔬菜、全谷物、豆类、坚果、鱼类、红肉加工肉、单不饱和脂肪/饱和脂肪比、酒精）。""",
        "en_desc": """**MED (Mediterranean Diet Score)** Uses median-based ranking for scoring.
**File requirements**: CSV or Excel. Participant ID required.
**Parameters**: 10 MED components (Fruits, Vegetables, Whole Grains, Legumes, Nuts, Fish, Red & Processed Meat, MUFA/SFA ratio, Alcohol).""",
        "output_cols": ["MED_ALL"],
    },
    "MEDI": {
        "desc": """**MEDI (Mediterranean Diet Index)** 使用二值化临界值评分（0或1分）。
**文件要求**：CSV 或 Excel。需要参与者 ID。
**参数覆盖**：11 个 MEDI 组分（橄榄油、水果、蔬菜、豆类、坚果、鱼类海鲜、酒精、含糖饮料、甜食、离散油脂、红肉加工肉）。""",
        "en_desc": """**MEDI (Mediterranean Diet Index)** Uses binary threshold scoring (0 or 1).
**File requirements**: CSV or Excel. Participant ID required.
**Parameters**: 11 MEDI components (Olive Oil, Fruits, Vegetables, Legumes, Nuts, Fish & Seafood, Alcohol, SSBs, Sweets, Discretionary Fats, Red & Processed Meat).""",
        "output_cols": ["MEDI_ALL", "MEDI_NOETOH"],
    },
    "MEDI_V1": {
        "desc": """**MEDI V1 (二分评分版) \u2014 推荐版本**。基于 PREDIMED 绝对阈值的 0/1 二分评分，总分 0-11。
**文件要求**：CSV 或 Excel。需要参与者 ID。""",
        "en_desc": """**MEDI V1 (Binary Scoring) \u2014 Recommended**. 0/1 binary scoring based on PREDIMED absolute thresholds, total 0-11.
**File requirements**: CSV or Excel. Participant ID required.""",
        "output_cols": ["MEDI_ALL", "MEDI_NOETOH"],
    },
    "MEDI_V2": {
        "desc": """**MEDI V2 (连续评分版)**。基于份量进行 0-5 连续线性插值评分，总分 0-55。
**文件要求**：CSV 或 Excel。需要参与者 ID。""",
        "en_desc": """**MEDI V2 (Continuous Scoring)**. 0-5 continuous linear interpolation based on servings, total 0-55.
**File requirements**: CSV or Excel. Participant ID required.""",
        "output_cols": ["MEDI_V2_ALL", "MEDI_V2_NOETOH"],
    },
    "ACS2020": {
        "desc": """**ACS2020 (American Cancer Society 2020)** 提供 V1 和 V2 两个版本。
**文件要求**：CSV 或 Excel。需要参与者 ID。
**参数覆盖**：多个 ACS2020 组分（饮食、体重、运动、酒精等生活方式因素）。""",
        "en_desc": """**ACS2020 (American Cancer Society 2020)** Provides V1 and V2 versions.
**File requirements**: CSV or Excel. Participant ID required.
**Parameters**: Multiple ACS2020 components (diet, weight, physical activity, alcohol, and other lifestyle factors).""",
        "output_cols": ["ACS2020_V1_ALL", "ACS2020_V2_ALL"],
    },
    "ACS2020_V1": {
        "desc": """**ACS2020 V1 (百分比能量版) \u2014 推荐版本**。基于四等分评分，总分 0-15。
**文件要求**：CSV 或 Excel。需要参与者 ID、性别 (GENDER)。
**参数覆盖**：8个组分（蔬菜摄入量、蔬菜种类、水果摄入量、水果种类、全谷物、红肉与加工肉、高加工食品与精制谷物比值 (%kcal)、含糖饮料）。""",
        "en_desc": """**ACS2020 V1 (Energy Percentage) \u2014 Recommended**. Quartile-based scoring, total 0-15.
**File requirements**: CSV or Excel. Participant ID and gender (GENDER) required.
**Parameters**: 8 components (Vegetable intake, Vegetable variety, Fruit intake, Fruit variety, Whole grains, Red & processed meat, Ultra-processed & refined grains ratio (%kcal), SSBs).""",
        "output_cols": ["ACS2020_V1_ALL"],
    },
    "ACS2020_V2": {
        "desc": """**ACS2020 V2 (能量标准化 servings 版)**。使用 1000 kcal 能量标准化的高加工食品，总分 0-15。
**文件要求**：CSV 或 Excel。需要参与者 ID、性别 (GENDER)、总能量 (KCAL)。
**参数覆盖**：8个组分（蔬菜摄入量、蔬菜种类、水果摄入量、水果种类、全谷物、红肉与加工肉、高加工食品与精制谷物 servings/day、含糖饮料）。""",
        "en_desc": """**ACS2020 V2 (Energy-standardized servings)**. Uses 1000 kcal energy-standardized ultra-processed foods, total 0-15.
**File requirements**: CSV or Excel. Participant ID, gender (GENDER), and total energy (KCAL) required.
**Parameters**: 8 components (Vegetable intake, Vegetable variety, Fruit intake, Fruit variety, Whole grains, Red & processed meat, Ultra-processed & refined grains servings/day, SSBs).""",
        "output_cols": ["ACS2020_V2_ALL"],
    },
    "PHDI": {
        "desc": """**PHDI (Planetary Health Diet Index)** 评估膳食对地球健康的影响，提供 V1 和 V2 两个版本。
**文件要求**：CSV 或 Excel。需要参与者 ID。
**参数覆盖**：多组 PHDI 组分。""",
        "en_desc": """**PHDI (Planetary Health Diet Index)** Evaluates the environmental impact of diet. Provides V1 and V2 versions.
**File requirements**: CSV or Excel. Participant ID required.
**Parameters**: Multiple PHDI components.""",
        "output_cols": ["PHDI_ALL"],
    },
    "PHDI_V1": {
        "desc": """**PHDI V1 (百分比能量版) \u2014 推荐版本**。脂肪与糖类使用能量占比百分比 (%kcal) 直接进行计算。
**文件要求**：CSV 或 Excel。需要参与者 ID、性别 (GENDER)。
**参数覆盖**：全谷物、淀粉类蔬菜、蔬菜、水果、乳制品、红肉与加工肉、禽肉、鸡蛋、鱼类、坚果、豆类、大豆制品、添加不饱和脂肪 (%kcal)、添加饱和及反式脂肪 (%kcal)、添加糖 (%kcal)。""",
        "en_desc": """**PHDI V1 (Energy Percentage) \u2014 Recommended**. Fats and sugars as %kcal directly.
**File requirements**: CSV or Excel. Participant ID and gender (GENDER) required.
**Parameters**: Whole grains, Starchy vegetables, Vegetables, Fruits, Dairy, Red & processed meat, Poultry, Eggs, Fish, Nuts, Legumes, Soy, Added unsaturated fats (%kcal), Added saturated & trans fats (%kcal), Added sugars (%kcal).""",
        "output_cols": ["PHDI_ALL"],
    },
    "PHDI_V2": {
        "desc": """**PHDI V2 (克数转换版)**。脂肪与糖类使用每日克数 (g/day) 输入，系统会自动根据总能量进行百分比能量转化。
**文件要求**：CSV 或 Excel。需要参与者 ID、性别 (GENDER)、总能量 (KCAL)。
**参数覆盖**：全谷物、淀粉类蔬菜、蔬菜、水果、乳制品、红肉与加工肉、禽肉、鸡蛋、鱼类、坚果、豆类、大豆制品、添加不饱和脂肪 (g/day)、添加饱和及反式脂肪 (g/day)、添加糖 (g/day)。""",
        "en_desc": """**PHDI V2 (Gram Conversion)**. Fats and sugars as g/day, auto-converted to %energy.
**File requirements**: CSV or Excel. Participant ID, gender (GENDER), and total energy (KCAL) required.
**Parameters**: Whole grains, Starchy vegetables, Vegetables, Fruits, Dairy, Red & processed meat, Poultry, Eggs, Fish, Nuts, Legumes, Soy, Added unsaturated fats (g/day), Added saturated & trans fats (g/day), Added sugars (g/day).""",
        "output_cols": ["PHDI_ALL"],
    },
    "DI_GM": {
        "desc": """**DI_GM (Dietary Index-German)** 评估多种特定食物的摄入是否符合德国膳食指南。
**文件要求**：CSV 或 Excel。需要参与者 ID 和性别 (GENDER)。
**参数覆盖**：多种食物组和营养素。""",
        "en_desc": """**DI-GM (Dietary Index for Gut Microbiota)** Evaluates specific food intake against German dietary guidelines.
**File requirements**: CSV or Excel. Participant ID and gender (GENDER) required.
**Parameters**: Multiple food groups and nutrients.""",
        "output_cols": ["DI_GM_ALL"],
    },
}

# ASA24 / DHQ3 / BLOCK 非DII 索引信息
ASA24_INDEX_INFO = {
    "HEI2015": {"adapter_note": "系统自动识别 ASA24 Totals.csv 列名，映射到 HEI2015 参数并计算。"},
    "HEI2020": {"adapter_note": "系统自动识别 ASA24 Totals.csv 列名，映射到 HEI2020 参数。自动检测 Toddlers 版本。"},
    "AHEI": {"adapter_note": "系统自动识别 ASA24 Totals.csv 列名，映射到 AHEI 参数。需含性别列。"},
    "DASH": {"adapter_note": "系统自动识别 ASA24 Totals.csv 列名，映射到 DASH 参数并计算。"},
    "MED": {"adapter_note": "系统自动识别 ASA24 Totals.csv 列名，映射到 MED 参数。使用中位数排名法。"},
}

DHQ3_INDEX_INFO = {
    "HEI2015": {"adapter_note": "系统自动识别 DHQ3 Total Daily Results 列名，映射到 HEI2015 参数。"},
    "AHEI": {"adapter_note": "AHEI 需要使用 DHQ3 的 detail.csv 文件（含 Food ID 列），系统自动按 Respondent ID 分组汇总后计算。"},
    "AHEIP": {"adapter_note": "系统自动识别 DHQ3 Total Daily Results 列名，映射到 AHEIP 参数（孕期专用版）。"},
    "DASH": {"adapter_note": "系统自动识别 DHQ3 Total Daily Results 列名，映射到 DASH 参数。"},
    "MED": {"adapter_note": "系统自动识别 DHQ3 Total Daily Results 列名，映射到 MED 参数。"},
}

BLOCK_INDEX_INFO = {
    "HEI2015": {"adapter_note": "系统自动识别 BLOCK FFQ 列名，映射到 HEI2015 参数并计算。"},
    "AHEI": {"adapter_note": "系统通过 BLOCK FFQ 的频率×份量查找表自动计算 AHEI 成分并评分。"},
    "AHEIP": {"adapter_note": "系统通过 BLOCK FFQ 的频率×份量查找表自动计算 AHEIP 成分并评分。"},
    "DASH": {"adapter_note": "系统自动识别 BLOCK FFQ 列名，映射到 DASH 参数并计算。"},
    "MED": {"adapter_note": "系统自动识别 BLOCK FFQ 列名，映射到 MED 参数并计算。"},
}


# ═══════════════════════════════════════════════════════════════════════════════
# 主入口函数
# ═══════════════════════════════════════════════════════════════════════════════

def _sync_result_bubble(current_page_key, remove_only=False):
    """同步或清理全局结果气泡，避免跨页残留。"""
    components.html(
        f"""
        <script>
        (function() {{
            var doc = window.parent.document;
            var bubble = doc.getElementById('resultBubble');
            if (!bubble) return;
            var owner = bubble.getAttribute('data-owner-page');
            if ({str(remove_only).lower()} || (owner && owner !== {current_page_key!r})) {{
                bubble.remove();
            }}
        }})();
        </script>
        """,
        height=0,
        width=0,
    )


def render_sidebar(current_page_key=None):
    """渲染侧边栏导航。"""
    _render_shared_sidebar(current_page_key=current_page_key, pre_render_callback=_sync_result_bubble)


def get_inputs_hash(index_key):
    """计算当前页面所有输入组件值的哈希，用于检测输入是否发生改变"""
    import hashlib
    vals = []
    for k, v in st.session_state.items():
        k_lower = k.lower()
        idx_lower = index_key.lower()
        if (idx_lower in k_lower or 
            "nhanes" in k_lower or 
            "asa24" in k_lower or 
            "dhq3" in k_lower or 
            "block" in k_lower or 
            "mped" in k_lower):
            if (
                k == f"result_{index_key}"
                or k == f"result_hash_{index_key}"
                or "compute" in k_lower
                or "use_sample" in k_lower
                or "scroll_to_result" in k_lower
            ):
                continue
            if v is not None:
                if hasattr(v, "name"):
                    vals.append(f"{k}:{v.name}_{v.size}")
                else:
                    vals.append(f"{k}:{v}")
    vals.sort()
    print(f"DEBUG: get_inputs_hash({index_key})={vals}", flush=True)
    hasher = hashlib.md5()
    hasher.update(str(vals).encode("utf-8"))
    return hasher.hexdigest()


def render_full_index_page(index_key):
    render_sidebar(index_key)
    """渲染完整的指数页面，包含模式选择和各模式 UI。"""
    actual_key = index_key
    lang = get_lang()
    if index_key == "ACS2020":
        if lang == "en":
            st.title("ACS 2020 Cancer Society Dietary Index")
            st.caption("ACS 2020 Cancer Society Index")
            version = st.radio(
                "Select computation version:",
                ["V1 (Energy Percentage — Recommended, uses %kcal from ultra-processed foods & refined grains)",
                 "V2 (Energy-Standardized Servings — uses servings/d per 1000 kcal)"],
                key="acs2020_version_select"
            )
        else:
            st.title("ACS 2020 癌症协会饮食指数")
            st.caption("ACS 2020 Cancer Society Index")
            version = st.radio(
                "选择计算版本：",
                ["V1 (能量百分比版 \u2014 推荐，使用高加工食品与精制谷物占每日总热量的百分比 %kcal 计算)",
                 "V2 (热量标准化份数版 \u2014 使用每 1000 kcal 每日消耗的份数 servings/d per 1000 kcal 计算)"],
                key="acs2020_version_select"
            )
        if "V1" in version:
            actual_key = "ACS2020_V1"
        else:
            actual_key = "ACS2020_V2"
    elif index_key == "PHDI":
        if lang == "en":
            st.title("Planetary Health Diet Index (PHDI)")
            st.caption("Planetary Health Diet Index")
            version = st.radio(
                "Select computation version:",
                ["V1 (Energy Percentage — Recommended, added fats & sugars as %kcal)",
                 "V2 (Gram Conversion — added fats & sugars as g/day, auto-converted by energy)"],
                key="phdi_version_select"
            )
        else:
            st.title("行星健康饮食指数 (PHDI)")
            st.caption("Planetary Health Diet Index")
            version = st.radio(
                "选择计算版本：",
                ["V1 (百分比能量版 \u2014 推荐，添加不饱和脂肪、添加饱和及反式脂肪、添加糖直接以占总能量的百分比 %kcal 作为输入)",
                 "V2 (克数转换版 \u2014 所有的添加不饱和脂肪、添加饱和及反式脂肪、添加糖均以每日摄入克数 g/day 输入，由系统根据总能量自动转换)"],
                key="phdi_version_select"
            )
        if "V1" in version:
            actual_key = "PHDI_V1"
        else:
            actual_key = "PHDI_V2"
    elif index_key == "HEI2020":
        if lang == "en":
            st.title("Healthy Eating Index 2020 (HEI-2020)")
            st.caption("Healthy Eating Index 2020")
            version = st.radio(
                "Select computation version:",
                ["V1 (Energy Density & Percentage — Recommended, added sugar & saturated fat as % energy, sodium in g)",
                 "V2 (Raw Intake & Auto Conversion — added sugar in tsp, saturated fat in g, sodium in mg, auto-converted)"],
                key="hei2020_version_select"
            )
        else:
            st.title("健康饮食指数 2020 (HEI-2020)")
            st.caption("Healthy Eating Index 2020")
            version = st.radio(
                "选择计算版本：",
                ["V1 (能量密度与百分比版 \u2014 推荐，添加糖和饱和脂肪使用占总能量的百分比 % energy 输入，钠以克 g 作为单位输入)",
                 "V2 (原始摄入量与自动转换版 \u2014 添加糖以茶匙 tsp 输入，饱和脂肪以克 g 输入，钠以毫克 mg 输入，系统基于每日总热量自动换算)"],
                key="hei2020_version_select"
            )
        if "V1" in version:
            actual_key = "HEI2020_V1"
        else:
            actual_key = "HEI2020_V2"
    elif index_key == "MEDI":
        if lang == "en":
            st.title("MEDI Mediterranean Diet Index (PREDIMED-based)")
            st.caption("MEDI (PREDIMED-based)")
            version = st.radio(
                "Select computation version:",
                ["V1 (Binary Scoring — Recommended, 0/1 scoring based on PREDIMED absolute thresholds, total 11 points)",
                 "V2 (Continuous Scoring — 0-5 linear interpolation based on serving thresholds, total 55 points)"],
                key="medi_version_select"
            )
        else:
            st.title("MEDI 地中海饮食指数（改进版）")
            st.caption("MEDI (PREDIMED-based)")
            version = st.radio(
                "选择计算版本：",
                ["V1 (二分评分版 \u2014 推荐，基于 PREDIMED 试验的 11 个组分绝对阈值进行 0/1 二分得失分计算，总分 11 分)",
                 "V2 (连续评分版 \u2014 基于份量的最小/最大推荐阈值进行 0-5 分连续线性插值评分，总分 55 分)"],
                key="medi_version_select"
            )
        if "V1" in version:
            actual_key = "MEDI_V1"
        else:
            actual_key = "MEDI_V2"

    cfg = INDEX_PARAMS[actual_key]
    modes = INDEX_MODE_CONFIG.get(actual_key, ["general"])

    if index_key not in ["ACS2020", "PHDI", "HEI2020", "MEDI"]:
        if lang == "en":
            st.title(cfg["title_en"])
            st.caption("")
        else:
            st.title(cfg["title"])
            st.caption(cfg["title_en"])

    if lang == "en":
        desc_en = cfg.get("description_en", cfg["description"])
        max_score_label = cfg.get('max_score', 'No upper limit')
        st.markdown(f"""
        <div class="info-box">
            <p>{desc_en}</p>
            <div style="margin-top: 0.5rem; display: flex; gap: 1rem; font-size: 0.82rem; color: #5a5a5a;">
                <span>\U0001f4ca Score Range: <b>{max_score_label}</b></span>
                <span>\U0001f4e1 {len(modes)} upload mode{"s" if len(modes) != 1 else ""}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        max_score_label = cfg.get('max_score', '无上限')
        st.markdown(f"""
        <div class="info-box">
            <p>{cfg["description"]}</p>
            <div style="margin-top: 0.5rem; display: flex; gap: 1rem; font-size: 0.82rem; color: #5a5a5a;">
                <span>\U0001f4ca 总分范围: <b>{max_score_label}</b></span>
                <span>\U0001f4e1 {len(modes)} 种上传模式</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 延迟导入重型工具模块
    h = _lazy_import_heavy()
    _run_computation = h["_run_computation"]
    _show_result = h["_show_result"]

    result_key = f"result_{actual_key}"
    if result_key in st.session_state:
        pass  # 气泡在下方结果区域统一渲染

    st.markdown("---")
    st.subheader(t("ui.select_mode")) if lang == "zh" else st.subheader("Select Data Upload Mode")

    mode_options = []
    for m in modes:
        label, desc = _mode_label(m)
        mode_options.append((label, m, desc))

    mode = st.radio(
        t("ui.select_mode_prompt") if lang == "zh" else "Please select the upload mode based on your data source:",
        options=mode_options,
        format_func=lambda x: f"**{x[0]}** \u2014 {x[2]}",
        key=f"mode_{actual_key}",
    )

    selected_mode = mode[1]

    st.markdown("---")

    # ── 按模式分发 ──
    file_dep = None
    if selected_mode == "general":
        file_dep = _render_general_mode(actual_key, cfg)
    elif selected_mode == "nhanes_fped":
        file_dep = _render_nhanes_fped_mode(actual_key, cfg)
    elif selected_mode == "nhanes_mped":
        file_dep = _render_nhanes_mped_mode(actual_key, cfg)
    elif selected_mode == "asa24":
        file_dep = _render_asa24_mode(actual_key, cfg)
    elif selected_mode == "dhq3":
        file_dep = _render_dhq3_mode(actual_key, cfg)
    elif selected_mode == "block":
        file_dep = _render_block_mode(actual_key, cfg)

    # ── 渲染计算结果（全宽展示） ──
    result_key = f"result_{actual_key}"
    if result_key in st.session_state:
        cached = st.session_state[result_key]
        current_hash = get_inputs_hash(actual_key)
        
        # 如果模式、依赖文件或任意输入发生变化，清除缓存不显示过期结果
        if (cached.get("mode") != selected_mode or 
            cached.get("file_dep") != file_dep or 
            cached.get("hash") != current_hash):
            del st.session_state[result_key]
        else:
            st.markdown('<div id="result-section"></div>', unsafe_allow_html=True)
            _show_result(cached["data"], cfg, actual_key)

            should_scroll = bool(st.session_state.get(f"scroll_to_result_{actual_key}"))
            if should_scroll:
                lang = get_lang()
                if lang == "en":
                    st.toast(f"🎉 {cfg['title_en']} computed! Results are shown below.")
                else:
                    st.toast(f"🎉 {cfg['title']} 计算成功！结果图表和数据已在下方生成。")
            if should_scroll:
                lang = get_lang()
                bubble_title = f"{cfg['title_en']} Complete" if lang == "en" else f"{cfg['title']} 计算完成"
                bubble_desc = "Results are shown below" if lang == "en" else "结果图表和数据已在下方生成"
                bubble_btn = "👇 Jump" if lang == "en" else "👇 跳转"
                components.html(
                    f"""
                    <script>
                    (function() {{
                        var doc = window.parent.document;
                        var old = doc.getElementById('resultBubble');
                        if (old) old.remove();

                        if (!doc.getElementById('bubbleStyles')) {{
                            var s = doc.createElement('style');
                            s.id = 'bubbleStyles';
                            s.textContent = `
                                @keyframes bubbleIn {{ 0%{{transform:translateX(120%);opacity:0}} 100%{{transform:translateX(0);opacity:1}} }}
                                @keyframes bubbleOut {{ 0%{{transform:translateX(0);opacity:1}} 100%{{transform:translateX(120%);opacity:0}} }}
                                .result-bubble {{
                                    position:fixed; bottom:2rem; right:2rem; z-index:99999;
                                    background:linear-gradient(135deg,#fff 0%,#f0faf6 100%);
                                    border:1px solid rgba(45,140,110,.2); border-radius:16px;
                                    padding:1rem 1.4rem; max-width:380px;
                                    box-shadow:0 8px 32px rgba(45,140,110,.18),0 2px 8px rgba(0,0,0,.06);
                                    display:flex; align-items:center; gap:.8rem;
                                    animation:bubbleIn .4s cubic-bezier(.34,1.56,.64,1) forwards;
                                    backdrop-filter:blur(10px);
                                    font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
                                }}
                                .result-bubble.hiding {{ animation:bubbleOut .35s ease-in forwards; }}
                                .result-bubble .b-icon {{ font-size:1.6rem; flex-shrink:0; }}
                                .result-bubble .b-body {{ flex:1; min-width:0; }}
                                .result-bubble .b-title {{ font-size:.92rem; font-weight:700; color:#1a6b4a; margin:0 0 .15rem; line-height:1.3; }}
                                .result-bubble .b-desc  {{ font-size:.78rem; color:#6b7b8d; margin:0; line-height:1.4; }}
                                .result-bubble .b-btn {{
                                    flex-shrink:0; background:linear-gradient(135deg,#2d8c6e,#1a6b4a);
                                    color:#fff!important; border:none; border-radius:10px;
                                    padding:.45rem .9rem; font-size:.78rem; font-weight:600;
                                    cursor:pointer; white-space:nowrap;
                                    transition:transform .15s,box-shadow .15s;
                                    box-shadow:0 2px 8px rgba(45,140,110,.25);
                                }}
                                .result-bubble .b-btn:hover {{ transform:translateY(-1px); box-shadow:0 4px 14px rgba(45,140,110,.35); }}
                                .result-bubble .b-x {{
                                    position:absolute; top:.35rem; right:.5rem;
                                    background:none; border:none; color:#b0bec5;
                                    font-size:.85rem; cursor:pointer; padding:.15rem .3rem;
                                    line-height:1; border-radius:50%;
                                    transition:color .15s,background .15s;
                                }}
                                .result-bubble .b-x:hover {{ color:#546e7a; background:rgba(0,0,0,.05); }}
                            `;
                            doc.head.appendChild(s);
                        }}

                        var b = doc.createElement('div');
                        b.className = 'result-bubble';
                        b.id = 'resultBubble';
                        b.setAttribute('data-owner-page', {actual_key!r});
                        b.innerHTML = '<button class="b-x" title="关闭">✕</button>'
                            + '<div class="b-icon">🎉</div>'
                            + '<div class="b-body">'
                            + '<p class="b-title">' + {bubble_title!r} + '</p>'
                            + '<p class="b-desc">' + {bubble_desc!r} + '</p>'
                            + '</div>'
                            + '<button class="b-btn">' + {bubble_btn!r} + '</button>';
                        doc.body.appendChild(b);

                        function scrollToResult() {{
                            var t = doc.getElementById('result-section') || doc.querySelector('.score-report');
                            if (t) t.scrollIntoView({{ behavior:'smooth', block:'start' }});
                        }}

                        function dismiss() {{
                            b.classList.add('hiding');
                            setTimeout(function(){{ b.remove(); }}, 350);
                        }}

                        b.querySelector('.b-x').addEventListener('click', dismiss);
                        b.querySelector('.b-btn').addEventListener('click', function() {{
                            scrollToResult();
                            dismiss();
                        }});

                        setTimeout(function(){{ if(doc.getElementById('resultBubble')) dismiss(); }}, 8000);
                        scrollToResult();
                        setTimeout(scrollToResult, 300);
                        setTimeout(scrollToResult, 800);
                        setTimeout(scrollToResult, 1500);
                    }})();
                    </script>
                    """,
                    height=0,
                    width=0,
                )
            else:
                _sync_result_bubble(actual_key, remove_only=True)
            if should_scroll:
                del st.session_state[f"scroll_to_result_{actual_key}"]


# ═══════════════════════════════════════════════════════════════════════════════
# 模式渲染函数
# ═══════════════════════════════════════════════════════════════════════════════

def _sample_col_mapping(df, cfg):
    """示例数据使用标准列名，直接构造同名映射。"""
    col_mapping = {}
    for extra in cfg.get("extra_params", []):
        name = extra["name"]
        if name in df.columns:
            col_mapping[name] = name
        else:
            col_mapping[name] = extra.get("default")
    for group in cfg.get("groups", []):
        for param in group["params"]:
            if param["name"] in df.columns:
                col_mapping[param["name"]] = param["name"]
    return col_mapping


def _run_profile_sample(index_key, cfg, profile):
    from sample_data import build_profile_sample_dataframe
    sample_df = build_profile_sample_dataframe(index_key, profile, row_count=50)
    h = _lazy_import_heavy()
    return h["_run_computation"](index_key, cfg, sample_df, _sample_col_mapping(sample_df, cfg))

def _render_general_mode(index_key, cfg):
    """通用版上传模式 — 列名映射"""
    from sample_data import (
        sample_profile_meta,
        build_profile_sample_dataframe,
        build_profile_sample_csv_bytes,
    )
    lang = get_lang()
    label, _ = _mode_label("general")
    st.subheader(f"\U0001f4cb {label}")

    tpl = INDEX_GENERAL_TEMPLATES.get(index_key, {})
    if lang == "en":
        st.markdown(tpl.get("en_desc", tpl.get("desc", "")))
    else:
        st.markdown(tpl.get("desc", ""))

    # DII 中英文模板下载
    if index_key == "DII":
        from config.templates import _dii_template_excel_cn, _dii_template_excel_en
        if lang == "en":
            st.caption("The Excel files below are reference templates for column names and parameter descriptions. "
                       "For 50-row sample data, use the Demo or Consistency Test entry below.")
            col_cn, col_en = st.columns(2)
            with col_cn:
                st.download_button(
                    "\U0001f4c4 Download Reference Template (Chinese .xlsx)",
                    data=_dii_template_excel_cn(),
                    file_name="DII_标准列名参考表_中文版.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    help="Excel format, 2 Sheets: column reference + parameter reference. Not 50-row sample data.",
                )
            with col_en:
                st.download_button(
                    "\U0001f4c4 Download Reference Template (English .xlsx)",
                    data=_dii_template_excel_en(),
                    file_name="DII_Reference_Table_EN.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    help="Excel format, 2 Sheets: column reference + parameter guide. This is not the 50-row sample dataset.",
                )
        else:
            st.caption("下方 Excel 为参考模板，用于查看标准列名和参数说明；50 条示例数据请使用下方的演示版或一致性测试版入口。")
            col_cn, col_en = st.columns(2)
            with col_cn:
                st.download_button(
                    "\U0001f4c4 下载参考模板 (中文版 .xlsx)",
                    data=_dii_template_excel_cn(),
                    file_name="DII_标准列名参考表_中文版.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    help="Excel 格式，2个 Sheet：列结构参考 + 参数说明，不是 50 条示例数据。",
                )
            with col_en:
                st.download_button(
                    "\U0001f4c4 Download Reference Template (English .xlsx)",
                    data=_dii_template_excel_en(),
                    file_name="DII_Reference_Table_EN.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    help="Excel format, 2 Sheets: column reference + parameter guide. This is not the 50-row sample dataset.",
                )

    st.markdown("---")

    general_source_key = f"general_source_{index_key}"
    sample_file_dep = "__embedded_sample__"
    uploader_key = f"file_{index_key}_general"
    existing_upload = st.session_state.get(uploader_key)
    has_existing_upload = existing_upload is not None

    st.subheader(t("ui.quick_experience"))
    demo_meta = sample_profile_meta("demo")
    consistency_meta = sample_profile_meta("consistency")
    demo_df = build_profile_sample_dataframe(index_key, "demo", row_count=50)
    demo_csv = build_profile_sample_csv_bytes(index_key, "demo", row_count=50)
    consistency_df = build_profile_sample_dataframe(index_key, "consistency", row_count=50)
    consistency_csv = build_profile_sample_csv_bytes(index_key, "consistency", row_count=50)

    sample_col1, sample_col2 = st.columns(2)
    with sample_col1:
        st.markdown(f"### {t('ui.demo_sample')}")
        demo_desc = demo_meta["description"]
        if isinstance(demo_desc, dict):
            demo_desc = demo_desc.get(lang, demo_desc.get("zh", ""))
        st.caption(str(demo_desc))
        demo_btn_label = t("ui.one_click_analyze_demo")
        demo_help = "Please clear uploaded file first before using sample data." if lang == "en" else "如已上传文件，请先清空上传框后再使用示例数据。"
        if st.button(
            demo_btn_label,
            type="primary",
            use_container_width=True,
            key=f"use_sample_demo_{index_key}_general",
            disabled=has_existing_upload,
            help=demo_help,
        ):
            result = _run_profile_sample(index_key, cfg, "demo")
            if result is not None:
                st.session_state[general_source_key] = f"{sample_file_dep}:demo"
                st.session_state[f"result_{index_key}"] = {
                    "data": result,
                    "mode": "general",
                    "file_dep": f"{sample_file_dep}:demo",
                    "hash": get_inputs_hash(index_key),
                }
                st.session_state[f"scroll_to_result_{index_key}"] = True
                st.rerun()
        st.download_button(
            t("ui.download_demo_csv"),
            demo_csv,
            file_name=f"{index_key}_{demo_meta['file_suffix']}.csv",
            mime="text/csv",
            use_container_width=True,
            help="Download 50-row demo sample data." if lang == "en" else "下载用于前端快速体验的 50 条示例数据。",
        )
    with sample_col2:
        st.markdown(f"### {t('ui.consistency_sample')}")
        consistency_desc = consistency_meta["description"]
        if isinstance(consistency_desc, dict):
            consistency_desc = consistency_desc.get(lang, consistency_desc.get("zh", ""))
        st.caption(str(consistency_desc))
        cons_btn_label = t("ui.one_click_analyze_consistency")
        cons_help = "Please clear uploaded file first before using sample data." if lang == "en" else "如已上传文件，请先清空上传框后再使用示例数据。"
        if st.button(
            cons_btn_label,
            type="secondary",
            use_container_width=True,
            key=f"use_sample_consistency_{index_key}_general",
            disabled=has_existing_upload,
            help=cons_help,
        ):
            result = _run_profile_sample(index_key, cfg, "consistency")
            if result is not None:
                st.session_state[general_source_key] = f"{sample_file_dep}:consistency"
                st.session_state[f"result_{index_key}"] = {
                    "data": result,
                    "mode": "general",
                    "file_dep": f"{sample_file_dep}:consistency",
                    "hash": get_inputs_hash(index_key),
                }
                st.session_state[f"scroll_to_result_{index_key}"] = True
                st.rerun()
        st.download_button(
            t("ui.download_consistency_csv"),
            consistency_csv,
            file_name=f"{index_key}_{consistency_meta['file_suffix']}.csv",
            mime="text/csv",
            use_container_width=True,
            help="Download 50-row consistency test sample." if lang == "en" else "下载保留空列/缺失值场景的 50 条测试样本。",
        )

    with st.expander(t("ui.preview_demo_data"), expanded=False):
        if lang == "en":
            st.caption(f"Demo sample: {len(demo_df)} rows x {len(demo_df.columns)} columns, with populated values for quick start.")
        else:
            st.caption(f"演示版共 {len(demo_df)} 行 × {len(demo_df.columns)} 列，默认尽量填值，适合快速上手。")
        st.dataframe(demo_df.head(20), use_container_width=True)

    with st.expander(t("ui.preview_consistency_data"), expanded=False):
        if lang == "en":
            st.caption(f"Consistency test sample: {len(consistency_df)} rows x {len(consistency_df.columns)} columns, with missing values preserved.")
        else:
            st.caption(f"一致性测试版共 {len(consistency_df)} 行 × {len(consistency_df.columns)} 列，保留空列与缺失值场景。")
        st.dataframe(consistency_df.head(20), use_container_width=True)

    st.markdown("---")

    # Use the existing generic upload rendering
    uploaded_file = st.file_uploader(
        t("ui.upload_file"),
        type=["csv", "xlsx", "xls", "xpt", "sas7bdat"],
        key=uploader_key,
        help="Supports CSV / Excel (.xlsx, .xls) / SAS XPT / SAS sas7bdat" if lang == "en" else "支持 CSV / Excel (.xlsx, .xls) / SAS XPT / SAS sas7bdat 格式",
    )

    file_dep = None
    if uploaded_file is None:
        if str(st.session_state.get(general_source_key, "")).startswith(sample_file_dep):
            file_dep = st.session_state.get(general_source_key)
        elif str(st.session_state.get(general_source_key, "")).startswith("upload:"):
            st.session_state[general_source_key] = None

    if uploaded_file is not None:
        # 检测是否上传了新文件，如果上传了新文件，清空以前保存的下拉框选择状态以重新自动映射
        file_id = f"{uploaded_file.name}_{uploaded_file.size}"
        file_dep = f"upload:{file_id}"
        last_file_key = f"last_file_{index_key}_general"
        if st.session_state.get(last_file_key) != file_id:
            keys_to_clear = [k for k in st.session_state.keys() 
                             if k.startswith(f"param_{index_key}_general_") or 
                                k.startswith(f"ep_{index_key}_general_")]
            for k in keys_to_clear:
                del st.session_state[k]
            st.session_state[last_file_key] = file_id
            st.session_state[general_source_key] = file_dep
            st.rerun()

        h = _lazy_import_heavy()
        df = h["load_data"](uploaded_file)
        if df is None:
            st.stop()

        import hashlib
        file_id_hash = hashlib.md5(file_id.encode("utf-8")).hexdigest()

        if lang == "en":
            st.success(f"Loaded {len(df)} rows x {len(df.columns)} columns")
        else:
            st.success(f"已加载 {len(df)} 行 x {len(df.columns)} 列数据")
        with st.expander("📋 Preview Data" if lang == "en" else "\U0001f4cb 预览数据", expanded=False):
            st.dataframe(df.head(20), use_container_width=True)

        # 尝试自动识别列名并映射
        auto_mapping = _auto_map_columns(df, index_key, cfg)
        print(f"DEBUG: auto_mapping={auto_mapping}")
        print(f"DEBUG: df.columns={list(df.columns)}")
        select_placeholder = "--- Select Column ---" if lang == "en" else "--- 请选择列 ---"
        all_columns = [select_placeholder] + list(df.columns)
        col_mapping = {}

        extra_params = cfg.get("extra_params", [])
        if extra_params:
            if lang == "en":
                st.subheader("Basic Parameters")
            else:
                st.subheader("基本信息参数")
            ep_cols = st.columns(min(len(extra_params), 4))
            for i, ep in enumerate(extra_params):
                with ep_cols[i % 4]:
                    if ep["name"] in ["respondent_id", "gender", "age", "total_kcal"]:
                        mapped_col = auto_mapping.get(ep["name"])
                        default_idx = 0
                        if mapped_col in all_columns:
                            default_idx = all_columns.index(mapped_col)
                        selected = st.selectbox(
                            ep["label_en"] if lang == "en" else ep["label"],
                            all_columns,
                            index=default_idx,
                            key=f"ep_{index_key}_general_{ep['name']}_{file_id_hash}",
                            help=ep.get("label_en", ""),
                        )
                        col_mapping[ep["name"]] = selected if selected != all_columns[0] else None
                    else:
                        col_mapping[ep["name"]] = st.number_input(
                            ep["label_en"] if lang == "en" else ep["label"],
                            value=ep.get("default", 1),
                            key=f"ep_{index_key}_general_{ep['name']}_{file_id_hash}",
                        )

        if lang == "en":
            st.subheader("Column Mapping")
        else:
            st.subheader("数据列映射")
        groups = cfg.get("groups", [])
        for gi, group in enumerate(groups):
            with st.expander(f"{group['name']} ({group['name_en']})", expanded=(gi == 0)):
                params = group["params"]
                pcols = st.columns(min(len(params), 3))
                for i, p in enumerate(params):
                    with pcols[i % 3]:
                        mapped_col = auto_mapping.get(p["name"])
                        default_idx = 0
                        if mapped_col in all_columns:
                            default_idx = all_columns.index(mapped_col)
                        selected = st.selectbox(
                            f"{p['label_en']} [{p['name']}]" if lang == "en" else f"{p['label']} [{p['name']}]",
                            all_columns,
                            index=default_idx,
                            key=f"param_{index_key}_general_{p['name']}_{file_id_hash}",
                            help=p.get("label_en", ""),
                        )
                        col_mapping[p["name"]] = selected if selected != all_columns[0] else None

        st.markdown("---")
        c1, c2, c3, c4 = st.columns([1, 1, 1, 1])
        with c1:
            compute_title = cfg["title_en"] if lang == "en" else cfg["title"]
            if st.button(f"🚀 Compute {compute_title}" if lang == "en" else f"🚀 计算 {compute_title}", type="primary", use_container_width=True,
                         key=f"compute_{index_key}_general"):
                h = _lazy_import_heavy()
                result = h["_run_computation"](index_key, cfg, df, col_mapping)
                if result is not None:
                    st.session_state[general_source_key] = file_dep
                    st.session_state[f"result_{index_key}"] = {
                        "data": result,
                        "mode": "general",
                        "file_dep": file_dep,
                        "hash": get_inputs_hash(index_key)
                    }
                    st.session_state[f"scroll_to_result_{index_key}"] = True
                    st.rerun()
        with c2:
            from config.templates import generate_generic_template
            all_params = []
            if extra_params:
                for ep in extra_params:
                    all_params.append((ep["name"], ep["label"]))
            for group in groups:
                for p in group["params"]:
                    all_params.append((p["name"], p["label"]))
            template_csv = generate_generic_template(all_params)
            st.download_button(
                "📄 Download Blank Template CSV" if lang == "en" else "📄 下载空白模板CSV",
                template_csv,
                file_name=f"{index_key}_template.csv",
                mime="text/csv",
                use_container_width=True,
                help="Column structure only, for self-reporting data; not sample data." if lang == "en" else "仅包含列结构，用于自行填报数据；不是示例数据。",
            )
        with c3:
            st.download_button(
                "📥 Download Demo CSV" if lang == "en" else "📥 下载演示版示例CSV",
                demo_csv,
                file_name=f"{index_key}_{demo_meta['file_suffix']}.csv",
                mime="text/csv",
                use_container_width=True,
                help="Download 50-row demo sample data." if lang == "en" else "下载用于快速体验的 50 条演示版示例数据。",
            )
        with c4:
            st.download_button(
                "📥 Download Test CSV" if lang == "en" else "📥 下载测试版示例CSV",
                consistency_csv,
                file_name=f"{index_key}_{consistency_meta['file_suffix']}.csv",
                mime="text/csv",
                use_container_width=True,
                help="Download 50-row consistency test sample." if lang == "en" else "下载保留空列与缺失值场景的一致性测试样本。",
            )

    return file_dep


def _render_nhanes_fped_mode(index_key, cfg):
    """NHANES FPED 上传模式"""
    lang = get_lang()
    is_en = lang == "en"
    label, _ = _mode_label("nhanes_fped")
    st.subheader(f"\U0001f4e6 {label}")

    is_iff = index_key in ["DASH", "AHEI", "MEDI", "MEDI_V1", "MEDI_V2", "DI_GM"]
    is_dashi = index_key == "DASHI"

    col_info, col_upload = st.columns([2, 3])

    with col_info:
        st.markdown("### \U0001f4cb File Format Info" if is_en else "### \U0001f4cb 文件格式说明")

        if is_iff:
            info_map = FPED_IFF_FILES_INFO_EN if is_en else FPED_IFF_FILES_INFO
            info = info_map.get(index_key, info_map["DASH"])
            st.markdown(info)
        elif is_dashi:
            info_map = FPED_TOT_FILES_INFO_EN if is_en else FPED_TOT_FILES_INFO
            info = info_map.get(index_key, info_map["DASHI"])
            st.markdown(info)
        else:
            info_map = FPED_TOT_FILES_INFO_EN if is_en else FPED_TOT_FILES_INFO
            info = info_map.get(index_key, info_map["HEI2015"])
            st.markdown(info)

    with col_upload:
        st.markdown("### \U0001f4e4 Upload Files" if is_en else "### \U0001f4e4 上传文件")

        if is_iff:
            st.markdown("**Day 1 — Required**" if is_en else "**第1天（Day 1）\u2014 必需**")
            fped1 = st.file_uploader(
                "FPED iff Data Day 1 (.sas7bdat)" if is_en else "FPED iff 数据 Day 1 (.sas7bdat)", type=["sas7bdat"],
                key=f"fped_iff1_{index_key}",
                help="fped_dr1iff_1718.sas7bdat"
            )
            nut1 = st.file_uploader(
                "Nutrient iff Day 1 (.XPT)" if is_en else "营养素 iff Day 1 (.XPT)", type=["xpt", "XPT"],
                key=f"nut_iff1_{index_key}",
                help="DR1IFF_J.XPT"
            )
            demo = st.file_uploader(
                "Demographics DEMO (.XPT)" if is_en else "人口数据 DEMO (.XPT)", type=["xpt", "XPT"],
                key=f"demo_fped_{index_key}",
                help="DEMO_J.XPT"
            )
            st.markdown("**Day 2 — Optional**" if is_en else "**第2天（Day 2）\u2014 可选**")
            fped2 = st.file_uploader(
                "FPED iff Data Day 2 (.sas7bdat)" if is_en else "FPED iff 数据 Day 2 (.sas7bdat)", type=["sas7bdat"],
                key=f"fped_iff2_{index_key}",
                help="fped_dr2iff_1718.sas7bdat (Optional)" if is_en else "fped_dr2iff_1718.sas7bdat (可选)"
            )
            nut2 = st.file_uploader(
                "Nutrient iff Day 2 (.XPT)" if is_en else "营养素 iff Day 2 (.XPT)", type=["xpt", "XPT"],
                key=f"nut_iff2_{index_key}",
                help="DR2IFF_J.XPT (Optional)" if is_en else "DR2IFF_J.XPT (可选)"
            )
        elif is_dashi:
            st.markdown("**Day 1 — Required**" if is_en else "**第1天（Day 1）\u2014 必需**")
            nut1 = st.file_uploader(
                "Total Nutrient Day 1 (.XPT)" if is_en else "总营养素 Day 1 (.XPT)", type=["xpt", "XPT"],
                key=f"nut_tot1_{index_key}",
                help="DR1TOT_J.XPT"
            )
            demo = st.file_uploader(
                "Demographics DEMO (.XPT)" if is_en else "人口数据 DEMO (.XPT)", type=["xpt", "XPT"],
                key=f"demo_fped_{index_key}",
                help="DEMO_J.XPT"
            )
            st.markdown("**Day 2 — Optional**" if is_en else "**第2天（Day 2）\u2014 可选**")
            nut2 = st.file_uploader(
                "Total Nutrient Day 2 (.XPT)" if is_en else "总营养素 Day 2 (.XPT)", type=["xpt", "XPT"],
                key=f"nut_tot2_{index_key}",
                help="DR2TOT_J.XPT (Optional)" if is_en else "DR2TOT_J.XPT (可选)"
            )
            fped1 = fped2 = None
        else:
            st.markdown("**Day 1 — Required**" if is_en else "**第1天（Day 1）\u2014 必需**")
            fped1 = st.file_uploader(
                "FPED tot Data Day 1 (.sas7bdat)" if is_en else "FPED tot 数据 Day 1 (.sas7bdat)", type=["sas7bdat"],
                key=f"fped_tot1_{index_key}",
                help="fpre_dr1tot_1718.sas7bdat / fped_dr1tot_1718.sas7bdat"
            )
            nut1 = st.file_uploader(
                "Total Nutrient Day 1 (.XPT)" if is_en else "总营养素 Day 1 (.XPT)", type=["xpt", "XPT"],
                key=f"nut_tot1_{index_key}",
                help="DR1TOT_J.XPT"
            )
            if index_key == "DII":
                other1 = st.file_uploader(
                    "Other Components Day 1 (.csv) — Optional" if is_en else "其他成分 Day 1 (.csv) — 可选", type=["csv"],
                    key=f"other1_tot_{index_key}",
                    help="Garlic, ginger, onion, pepper, saffron, thyme, turmeric, rosemary, tea, flavonoids, etc." if is_en else "含大蒜、生姜、洋葱、胡椒、藏红花、百里香、姜黄、迷迭香、茶、类黄酮等"
                )
            else:
                other1 = None
            demo = st.file_uploader(
                "Demographics DEMO (.XPT)" if is_en else "人口数据 DEMO (.XPT)", type=["xpt", "XPT"],
                key=f"demo_fped_{index_key}",
                help="DEMO_J.XPT"
            )
            st.markdown("**Day 2 — Optional**" if is_en else "**第2天（Day 2）\u2014 可选**")
            fped2 = st.file_uploader(
                "FPED tot Data Day 2 (.sas7bdat)" if is_en else "FPED tot 数据 Day 2 (.sas7bdat)", type=["sas7bdat"],
                key=f"fped_tot2_{index_key}",
                help="fpre_dr2tot_1718.sas7bdat (Optional)" if is_en else "fpre_dr2tot_1718.sas7bdat (可选)"
            )
            nut2 = st.file_uploader(
                "Total Nutrient Day 2 (.XPT)" if is_en else "总营养素 Day 2 (.XPT)", type=["xpt", "XPT"],
                key=f"nut_tot2_{index_key}",
                help="DR2TOT_J.XPT (Optional)" if is_en else "DR2TOT_J.XPT (可选)"
            )
            if index_key == "DII":
                other2 = st.file_uploader(
                    "Other Components Day 2 (.csv) — Optional" if is_en else "其他成分 Day 2 (.csv) — 可选", type=["csv"],
                    key=f"other2_tot_{index_key}",
                    help="Garlic, ginger, onion, pepper, saffron, thyme, turmeric, rosemary, tea, flavonoids, etc." if is_en else "含大蒜、生姜、洋葱、胡椒、藏红花、百里香、姜黄、迷迭香、茶、类黄酮等"
                )
            else:
                other2 = None

        from config.templates import _nhanes_fped_reference_excel
        st.download_button(
            "📥 Download NHANES FPED Reference (.xlsx)" if is_en else "\U0001f4e5 下载 NHANES FPED 文件结构参考 (.xlsx)",
            data=_nhanes_fped_reference_excel(),
            file_name="NHANES_FPED_文件结构参考.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            help="NHANES FPED file list, column descriptions, bilingual reference" if is_en else "NHANES FPED 文件清单、列名说明、中英文对照",
        )

        compute_title = cfg["title_en"] if is_en else cfg["title"]
        if st.button(f"\U0001f680 Compute {compute_title} (NHANES FPED)" if is_en else f"\U0001f680 开始计算 {compute_title} (NHANES FPED)", type="primary", use_container_width=True,
                     key=f"compute_{index_key}_fped"):
            # Validate required files
            if nut1 is None:
                st.error("Please upload at least the nutrient file (.XPT)" if is_en else "请至少上传营养素文件 (.XPT)")
                return

            if is_dashi and nut1 is not None:
                pass  # DASHI only needs nutrient files
            elif not is_iff and fped1 is None:
                st.error("Please upload the FPED tot data file (.sas7bdat)" if is_en else "请上传 FPED tot 数据文件 (.sas7bdat)")
                return

            with st.spinner(f"Computing {compute_title} (NHANES FPED)..." if is_en else f"正在计算 {compute_title} (NHANES FPED)..."):
                try:
                    def _save_to_temp(f):
                        if f is None:
                            return None
                        suffix = "." + f.name.rsplit(".", 1)[-1]
                        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
                        tmp.write(f.read())
                        tmp.close()
                        return tmp.name

                    fp1 = _save_to_temp(fped1) if not is_dashi else None
                    np1 = _save_to_temp(nut1)
                    dp = _save_to_temp(demo)
                    fp2 = _save_to_temp(fped2) if not is_dashi else None
                    np2 = _save_to_temp(nut2)
                    o1 = _save_to_temp(other1) if index_key == "DII" else None
                    o2 = _save_to_temp(other2) if index_key == "DII" else None

                    if is_iff:
                        adapter = _resolve_adapter(FPED_IFF_ADAPTER_KEYS, index_key)
                        if index_key in ["MEDI_V1", "MEDI_V2"]:
                            result = adapter(
                                fped_ind_path=fp1,
                                nutrient_ind_path=np1,
                                fped_ind_path2=fp2,
                                nutrient_ind_path2=np2,
                                demo_path=dp,
                                version="v1" if index_key == "MEDI_V1" else "v2"
                            )
                        else:
                            result = adapter(
                                fped_ind_path=fp1,
                                nutrient_ind_path=np1,
                                fped_ind_path2=fp2,
                                nutrient_ind_path2=np2,
                                demo_path=dp,
                            )
                    elif is_dashi:
                        adapter = _resolve_adapter(FPED_TOT_ADAPTER_KEYS, index_key)
                        result = adapter(
                            nutrient_path=np1,
                            nutrient_path2=np2,
                            demo_path=dp,
                        )
                    elif index_key == "DII":
                        h = _lazy_import_heavy()
                        result = h["compute_dii_nhanes_fped"](
                            fped_path=fp1,
                            nutrient_path=np1,
                            demo_path=dp,
                            fped_path2=fp2,
                            nutrient_path2=np2,
                            other_ingredients1=o1,
                            other_ingredients2=o2,
                        )
                    else:
                        adapter = _resolve_adapter(FPED_TOT_ADAPTER_KEYS, index_key)
                        result = adapter(
                            fped_path=fp1,
                            nutrient_path=np1,
                            demo_path=dp,
                            fped_path2=fp2,
                            nutrient_path2=np2,
                        )

                    # Cleanup
                    for f in [fp1, np1, dp, fp2, np2, o1, o2]:
                        if f:
                            os.unlink(f)

                    if result is not None:
                        st.session_state[f"result_{index_key}"] = {
                            "data": result,
                            "mode": "nhanes_fped",
                            "file_dep": (
                                fped1.name if fped1 else None, 
                                nut1.name if nut1 else None, 
                                demo.name if demo else None, 
                                fped2.name if fped2 else None, 
                                nut2.name if nut2 else None,
                                other1.name if (index_key == "DII" and other1) else None,
                                other2.name if (index_key == "DII" and other2) else None
                            ),
                            "hash": get_inputs_hash(index_key)
                        }
                        st.session_state[f"scroll_to_result_{index_key}"] = True
                        st.rerun()

                except Exception as e:
                    st.error(f"计算出错: {type(e).__name__}: {e}")
                    st.exception(e)

    return (
        fped1.name if fped1 else None, 
        nut1.name if nut1 else None, 
        demo.name if demo else None, 
        fped2.name if fped2 else None, 
        nut2.name if nut2 else None,
        other1.name if (index_key == "DII" and other1) else None,
        other2.name if (index_key == "DII" and other2) else None
    )


def _render_nhanes_mped_mode(index_key, cfg):
    """NHANES MPED 上传模式 — 对标 DII"""
    lang = get_lang()
    is_en = lang == "en"
    label, _ = _mode_label("nhanes_mped")
    st.subheader(f"\U0001f4e6 {label}")

    col_info, col_upload = st.columns([2, 3])

    with col_info:
        st.markdown("""### \U0001f4cb File Format Info""" if is_en else """### \U0001f4cb 文件格式说明""")
        if is_en:
            st.markdown("""**NHANES MPED (MyPyramid Equivalents Database)** for 1999-2004 cycles.
Key differences from FPED (2005+):

| Item | MPED (1999-2004) | FPED (2005+) |
|--------|:--:|:--:|
| Per 100g data | equiv.txt (Tab-delimited) | .sas7bdat |
| WJFRT | ✅ Built-in | Not needed |
| Nutrient prefix | DRXTR / DR1TR | DR1TR |

**Day 1 — Required:**
| File Type | Example | Format |
|---------|-----------|------|
| MPED per 100g | equiv0102.txt | TXT |
| Total Nutrient | drxtot.xpt | XPT |
| Individual Nutrient | drxiff.xpt | XPT |
| Demographics | demo.xpt | XPT |

**Day 2 — Optional (only 2003-2004 has Day2):**
| File Type | Example | Format |
|---------|-----------|------|
| Total Nutrient | dr2tot_c.xpt | XPT |
| Individual Nutrient | dr2iff_c.xpt | XPT |

ℹ️ **WJFRT is built-in**, no upload needed.""")
        else:
            st.markdown("""### \U0001f4cb 文件格式说明

**NHANES MPED (MyPyramid Equivalents Database)** 适用于 1999\u20132004 周期。
与 FPED (2005+) 的主要区别：

| 差异项 | MPED (1999-2004) | FPED (2005+) |
|--------|:--:|:--:|
| 每100克数据 | equiv.txt（Tab分隔） | .sas7bdat |
| WJFRT | \u2705 已内置 | 不需要 |
| 营养素列前缀 | DRXTR / DR1TR | DR1TR |

**第1天（Day 1）\u2014 必需：**
| 文件类型 | 文件名示例 | 格式 |
|---------|-----------|------|
| MPED 每100克 | equiv0102.txt | TXT |
| 总营养素 | drxtot.xpt | XPT |
| 个体营养素 | drxiff.xpt | XPT |
| 人口数据 | demo.xpt | XPT |

**第2天（Day 2）\u2014 可选（仅2003-2004有Day2）：**
| 文件类型 | 文件名示例 | 格式 |
|---------|-----------|------|
| 总营养素 | dr2tot_c.xpt | XPT |
| 个体营养素 | dr2iff_c.xpt | XPT |

\u2139\ufe0f **WJFRT 已内置**，无需上传。""")

    with col_upload:
        st.markdown("### \U0001f4e4 Upload Files" if is_en else "### \U0001f4e4 上传文件")

        st.markdown("**Day 1 — Required**" if is_en else "**第1天（Day 1）\u2014 必需**")
        equiv_file = st.file_uploader(
            "MPED per 100g equiv.txt" if is_en else "MPED 每100克 equiv.txt", type=["txt"],
            key=f"mped_equiv_{index_key}",
            help="equiv0102.txt / equiv0304.sas7bdat"
        )
        nut1 = st.file_uploader(
            "Total Nutrient Day 1 (.XPT)" if is_en else "总营养素 Day 1 (.XPT)", type=["xpt", "XPT"],
            key=f"mped_nut1_{index_key}",
            help="drxtot.xpt / drxtot_b.xpt"
        )
        nutind1 = st.file_uploader(
            "Individual Nutrient Day 1 (.XPT)" if is_en else "个体营养素 Day 1 (.XPT)", type=["xpt", "XPT"],
            key=f"mped_nutind1_{index_key}",
            help="drxiff.xpt"
        )
        if index_key == "DII":
            other1 = st.file_uploader(
                "Other Components Day 1 (.csv) — Optional" if is_en else "其他成分 Day 1 (.csv) — 可选", type=["csv"],
                key=f"mped_other1_{index_key}",
                help="Garlic, ginger, onion, pepper, saffron, thyme, turmeric, rosemary, tea, flavonoids, etc." if is_en else "含大蒜、生姜、洋葱、胡椒、藏红花、百里香、姜黄、迷迭香、茶、类黄酮等"
            )
        else:
            other1 = None
        demo = st.file_uploader(
            "Demographics DEMO (.XPT)" if is_en else "人口数据 DEMO (.XPT)", type=["xpt", "XPT"],
            key=f"mped_demo_{index_key}",
            help="demo.xpt / demo_b.xpt"
        )

        st.markdown("**Day 2 — Optional**" if is_en else "**第2天（Day 2）\u2014 可选**")
        nut2 = st.file_uploader(
            "Total Nutrient Day 2 (.XPT)" if is_en else "总营养素 Day 2 (.XPT)", type=["xpt", "XPT"],
            key=f"mped_nut2_{index_key}",
            help="dr2tot_c.xpt (Optional)" if is_en else "dr2tot_c.xpt (可选)"
        )
        nutind2 = st.file_uploader(
            "Individual Nutrient Day 2 (.XPT)" if is_en else "个体营养素 Day 2 (.XPT)", type=["xpt", "XPT"],
            key=f"mped_nutind2_{index_key}",
            help="dr2iff_c.xpt (Optional)" if is_en else "dr2iff_c.xpt (可选)"
        )

        from config.templates import _nhanes_mped_reference_excel
        st.download_button(
            "📥 Download NHANES MPED Reference (.xlsx)" if is_en else "\U0001f4e5 下载 NHANES MPED 文件结构参考 (.xlsx)",
            data=_nhanes_mped_reference_excel(),
            file_name="NHANES_MPED_文件结构参考.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            help="1999-2004 cycle file list, bilingual reference" if is_en else "1999-2004周期文件清单，中英文对照",
        )

        compute_title = cfg["title_en"] if is_en else cfg["title"]
        if st.button(f"\U0001f680 Compute {compute_title} (NHANES MPED)" if is_en else f"\U0001f680 开始计算 {compute_title} (NHANES MPED)", type="primary", use_container_width=True,
                     key=f"compute_{index_key}_mped"):
            if nut1 is None:
                st.error("Please upload at least the Total Nutrient Day 1 file (.XPT)" if is_en else "请至少上传「总营养素 Day 1」文件 (.XPT)")
                return

            with st.spinner(f"Computing {compute_title} (NHANES MPED)..." if is_en else f"正在计算 {compute_title} (NHANES MPED)..."):
                try:
                    def _save_to_temp(f):
                        if f is None:
                            return None
                        suffix = "." + f.name.rsplit(".", 1)[-1]
                        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
                        tmp.write(f.read())
                        tmp.close()
                        return tmp.name

                    ep = _save_to_temp(equiv_file)
                    np1 = _save_to_temp(nut1)
                    ni1 = _save_to_temp(nutind1)
                    dp = _save_to_temp(demo)
                    np2 = _save_to_temp(nut2)
                    ni2 = _save_to_temp(nutind2)
                    o1 = _save_to_temp(other1) if index_key == "DII" else None

                    if index_key == "DII":
                        h = _lazy_import_heavy()
                        result = h["compute_dii_nhanes_mped"](
                            mped_per_100_gram_path=ep,
                            nutrient_path=np1,
                            nutrient_ind_path=ni1,
                            demo_path=dp,
                            nutrient_path2=np2,
                            nutrient_ind_path2=ni2,
                            other_ingredients1=o1,
                        )
                    elif index_key == "DASHI":
                        adapter = _resolve_adapter(MPED_ADAPTER_KEYS, index_key)
                        result = adapter(
                            nutrient_path=np1,
                            nutrient_path2=np2,
                            demo_path=dp,
                        )
                    else:
                        adapter = _resolve_adapter(MPED_ADAPTER_KEYS, index_key)
                        if index_key in ["MEDI_V1", "MEDI_V2"]:
                            result = adapter(
                                mped_per_100_gram_path=ep,
                                nutrient_path=np1,
                                nutrient_ind_path=ni1,
                                demo_path=dp,
                                nutrient_path2=np2,
                                nutrient_ind_path2=ni2,
                                version="v1" if index_key == "MEDI_V1" else "v2"
                            )
                        else:
                            result = adapter(
                                mped_per_100_gram_path=ep,
                                nutrient_path=np1,
                                nutrient_ind_path=ni1,
                                demo_path=dp,
                                nutrient_path2=np2,
                                nutrient_ind_path2=ni2,
                            )

                    for f in [ep, np1, ni1, dp, np2, ni2, o1]:
                        if f:
                            os.unlink(f)

                    if result is not None:
                        st.session_state[f"result_{index_key}"] = {
                            "data": result,
                            "mode": "nhanes_mped",
                            "file_dep": (
                                equiv_file.name if equiv_file else None, 
                                nut1.name if nut1 else None, 
                                nutind1.name if nutind1 else None, 
                                demo.name if demo else None, 
                                nut2.name if nut2 else None, 
                                nutind2.name if nutind2 else None,
                                other1.name if (index_key == "DII" and other1) else None
                            ),
                            "hash": get_inputs_hash(index_key)
                        }
                        st.session_state[f"scroll_to_result_{index_key}"] = True
                        st.rerun()

                except Exception as e:
                    st.error(f"计算出错: {type(e).__name__}: {e}")
                    st.exception(e)

    return (
        equiv_file.name if equiv_file else None, 
        nut1.name if nut1 else None, 
        nutind1.name if nutind1 else None, 
        demo.name if demo else None, 
        nut2.name if nut2 else None, 
        nutind2.name if nutind2 else None,
        other1.name if (index_key == "DII" and other1) else None
    )


def _render_asa24_mode(index_key, cfg):
    """ASA24 上传模式 — 对标 DII"""
    lang = get_lang()
    is_en = lang == "en"
    label, _ = _mode_label("asa24")
    st.subheader(f"\U0001f4e6 {label}")

    col_info, col_upload = st.columns([2, 3])

    with col_info:
        asa_info = ASA24_INDEX_INFO.get(index_key, {})
        if is_en:
            st.markdown(f"""### \U0001f4cb File Format Info

**ASA24 (Automated Self-Administered 24-hour Dietary Assessment Tool)**

**File Requirements:**
| File | Format | Description |
|------|------|------|
| Totals.csv | CSV | Daily nutrient and food group totals exported from ASA24 |

{asa_info.get('adapter_note_en', 'System auto-recognizes column names and computes.')}

**Recall Summarize**:
- **On** (default): Average all recall records per person per day
- **Off**: Preserve each recall record individually""")
        else:
            st.markdown(f"""### \U0001f4cb 文件格式说明

**ASA24 (Automated Self-Administered 24-hour Dietary Assessment Tool)**

**文件要求：**
| 文件 | 格式 | 说明 |
|------|------|------|
| Totals.csv | CSV | ASA24 系统导出的每日营养素和食物组总量 |

{asa_info.get('adapter_note', '系统自动识别列名并计算。')}

**回忆汇总 (Recall Summarize)**：
- **开启**（默认）：按每人每天平均所有回忆记录
- **关闭**：保留每次回忆的原始记录""")

    with col_upload:
        st.markdown("### \U0001f4e4 Upload Files" if is_en else "### \U0001f4e4 上传文件")
        asa24_file = st.file_uploader(
            "ASA24 Totals.csv", type=["csv"],
            key=f"asa24_{index_key}",
            help="ASA24 Totals.csv — exported from ASA24 system" if is_en else "从 ASA24 系统导出的 Totals.csv 文件"
        )
        summarize = st.checkbox(
            "Recall Summarize (average all recalls per person per day)" if is_en else "回忆汇总（按每人每天平均所有回忆记录）", value=True,
            key=f"asa24_summarize_{index_key}",
        )

        from config.templates import _asa24_reference_excel
        st.download_button(
            "\U0001f4e5 Download ASA24 Column Reference (.xlsx)" if is_en else "\U0001f4e5 下载 ASA24 标准列名对照表 (.xlsx)",
            data=_asa24_reference_excel(),
            file_name="ASA24_标准列名对照表.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            help="ASA24 Totals.csv standard column names, bilingual reference" if is_en else "ASA24 Totals.csv 标准列名、中英文说明",
        )

        compute_title = cfg["title_en"] if is_en else cfg["title"]
        if st.button(f"\U0001f680 Compute {compute_title} (ASA24)" if is_en else f"\U0001f680 开始计算 {compute_title} (ASA24)", type="primary", use_container_width=True,
                     key=f"compute_{index_key}_asa24"):
            if asa24_file is None:
                st.error("Please upload ASA24 Totals.csv" if is_en else "请上传 ASA24 Totals.csv 文件")
                return

            with st.spinner(f"正在处理 ASA24 数据并计算 {cfg['title']}..."):
                try:
                    # Use the generic ASA24 adapter (DII's) for DII, or the generic computation for others
                    if index_key == "DII":
                        suffix = ".csv"
                        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
                        tmp.write(asa24_file.read())
                        tmp.close()
                        h = _lazy_import_heavy()
                        result = h["compute_dii_asa24"](tmp.name, recall_summarize=summarize)
                        os.unlink(tmp.name)
                    else:
                        # Load ASA24 data, do recall summarize, then call generic computation
                        asa24_file.seek(0)
                        df = pd.read_csv(asa24_file)
                        result = _compute_from_asa24_data(index_key, cfg, df, summarize)

                    if result is not None:
                        st.session_state[f"result_{index_key}"] = {
                            "data": result,
                            "mode": "asa24",
                            "file_dep": asa24_file.name if asa24_file else None,
                            "hash": get_inputs_hash(index_key)
                        }
                        st.session_state[f"scroll_to_result_{index_key}"] = True
                        st.rerun()

                except Exception as e:
                    st.error(f"计算出错: {type(e).__name__}: {e}")
                    st.exception(e)

    return asa24_file.name if asa24_file else None


def _render_dhq3_mode(index_key, cfg):
    """DHQ3 上传模式 — 对标 DII"""
    lang = get_lang()
    is_en = lang == "en"
    label, _ = _mode_label("dhq3")
    st.subheader(f"\U0001f4e6 {label}")

    col_info, col_upload = st.columns([2, 3])

    with col_info:
        dhq_info = DHQ3_INDEX_INFO.get(index_key, {})
        if is_en:
            if index_key == "AHEI":
                file_desc = """**DHQ3 (Diet History Questionnaire III)**

**File Requirements:**
| File | Format | Description |
|------|------|------|
| detail.csv | CSV | DHQ3 detailed food records (with Food ID column), not Total Daily Results |
"""
            else:
                file_desc = """**DHQ3 (Diet History Questionnaire III)**

**File Requirements:**
| File | Format | Description |
|------|------|------|
| results.csv | CSV | DHQ3 exported Total Daily Results |
"""
            st.markdown(f"""### \U0001f4cb File Format Info

{file_desc}
{dhq_info.get('adapter_note_en', 'System auto-recognizes column names and computes.')}

**Data structure**: One row per participant, with Respondent ID and nutrient columns.""")
        else:
            if index_key == "AHEI":
                file_desc = """**DHQ3 (Diet History Questionnaire III)**

**文件要求：**
| 文件 | 格式 | 说明 |
|------|------|------|
| detail.csv | CSV | DHQ3 的详细食物记录文件（含 Food ID 列），非 Total Daily Results |
"""
            else:
                file_desc = """**DHQ3 (Diet History Questionnaire III)**

**文件要求：**
| 文件 | 格式 | 说明 |
|------|------|------|
| results.csv | CSV | DHQ3 导出的 Total Daily Results 文件 |
"""
            st.markdown(f"""### \U0001f4cb 文件格式说明

{file_desc}
{dhq_info.get('adapter_note', '系统自动识别列名并计算。')}

**文件结构**：每行为一个参与者，包含 Respondent ID 和各营养素列。""")

    with col_upload:
        st.markdown("### \U0001f4e4 Upload Files" if is_en else "### \U0001f4e4 上传文件")
        if index_key == "AHEI":
            dhq3_label = "DHQ3 Detail File (.csv)" if is_en else "DHQ3 Detail 文件 (.csv)"
            dhq3_help = "DHQ3 detail.csv (with Food ID column), not Total Daily Results" if is_en else "DHQ3 的 detail.csv 文件（含 Food ID 列），非 Total Daily Results"
        else:
            dhq3_label = "DHQ3 Total Daily Results (.csv)"
            dhq3_help = "DHQ3 exported results.csv" if is_en else "从 DHQ3 系统导出的 results.csv 文件"
        dhq3_file = st.file_uploader(
            dhq3_label, type=["csv"],
            key=f"dhq3_{index_key}",
            help=dhq3_help
        )

        from config.templates import _dhq3_reference_excel
        st.download_button(
            "\U0001f4e5 Download DHQ3 Column Reference (.xlsx)" if is_en else "\U0001f4e5 下载 DHQ3 标准列名对照表 (.xlsx)",
            data=_dhq3_reference_excel(),
            file_name="DHQ3_标准列名对照表.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            help="DHQ3 Total Daily Results standard columns, bilingual reference" if is_en else "DHQ3 Total Daily Results 标准列名、中英文说明",
        )

        compute_title = cfg["title_en"] if is_en else cfg["title"]
        if st.button(f"\U0001f680 Compute {compute_title} (DHQ3)" if is_en else f"\U0001f680 开始计算 {compute_title} (DHQ3)", type="primary", use_container_width=True,
                     key=f"compute_{index_key}_dhq3"):
            if dhq3_file is None:
                if index_key == "AHEI":
                    st.error("Please upload DHQ3 detail.csv" if is_en else "请上传 DHQ3 detail.csv 文件")
                else:
                    st.error("Please upload DHQ3 Total Daily Results CSV" if is_en else "请上传 DHQ3 Total Daily Results CSV 文件")
                return

            with st.spinner(f"Processing DHQ3 data and computing {compute_title}..." if is_en else f"正在处理 DHQ3 数据并计算 {compute_title}..."):
                try:
                    if index_key == "DII":
                        suffix = ".csv"
                        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
                        tmp.write(dhq3_file.read())
                        tmp.close()
                        h = _lazy_import_heavy()
                        result = h["compute_dii_dhq3"](tmp.name)
                        os.unlink(tmp.name)
                    elif index_key == "AHEI":
                        suffix = ".csv"
                        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
                        tmp.write(dhq3_file.read())
                        tmp.close()
                        h = _lazy_import_heavy()
                        result = h["compute_ahei_dhq3"](tmp.name)
                        os.unlink(tmp.name)
                    else:
                        dhq3_file.seek(0)
                        df = pd.read_csv(dhq3_file)
                        result = _compute_from_generic_data(index_key, cfg, df, "DHQ3")

                    if result is not None:
                        st.session_state[f"result_{index_key}"] = {
                            "data": result,
                            "mode": "dhq3",
                            "file_dep": dhq3_file.name if dhq3_file else None,
                            "hash": get_inputs_hash(index_key)
                        }
                        st.session_state[f"scroll_to_result_{index_key}"] = True
                        st.rerun()

                except Exception as e:
                    st.error(f"计算出错: {type(e).__name__}: {e}")
                    st.exception(e)

    return dhq3_file.name if dhq3_file else None


def _render_block_mode(index_key, cfg):
    """BLOCK FFQ 上传模式 — 对标 DII"""
    lang = get_lang()
    is_en = lang == "en"
    label, _ = _mode_label("block")
    st.subheader(f"\U0001f4e6 {label}")

    col_info, col_upload = st.columns([2, 3])

    with col_info:
        blk_info = BLOCK_INDEX_INFO.get(index_key, {})
        if is_en:
            st.markdown(f"""### \U0001f4cb File Format Info

**BLOCK (Block Food Frequency Questionnaire)**

**File Requirements:**
| File | Format | Description |
|------|------|------|
| Raw Data | CSV / Excel | BLOCK FFQ exported dietary assessment results |

{blk_info.get('adapter_note_en', 'System auto-recognizes common BLOCK column names (KCAL, PROTEIN, CARB, FIBER, etc.) and computes.')}

**Data structure**: One row per participant, with daily nutrient and food group estimates.""")
        else:
            st.markdown(f"""### \U0001f4cb 文件格式说明

**BLOCK (Block Food Frequency Questionnaire)**

**文件要求：**
| 文件 | 格式 | 说明 |
|------|------|------|
| 原始数据 | CSV / Excel | BLOCK FFQ 导出的膳食评估结果数据 |

{blk_info.get('adapter_note', '系统自动识别常见 BLOCK 列名（KCAL, PROTEIN, CARB, FIBER 等）并计算。')}

**文件结构**：每行为一个参与者，包含每日营养素和食物组估计值。""")

    with col_upload:
        st.markdown("### \U0001f4e4 Upload Files" if is_en else "### \U0001f4e4 上传文件")
        block_file = st.file_uploader(
            "BLOCK FFQ data file" if is_en else "BLOCK FFQ 数据文件", type=["csv", "xlsx", "xls"],
            key=f"block_{index_key}",
            help="BLOCK Food Frequency Questionnaire exported data" if is_en else "BLOCK 食物频率问卷导出数据"
        )

        from config.templates import _block_reference_excel
        st.download_button(
            "\U0001f4e5 Download BLOCK FFQ Column Reference (.xlsx)" if is_en else "\U0001f4e5 下载 BLOCK FFQ 标准列名对照表 (.xlsx)",
            data=_block_reference_excel(),
            file_name="BLOCK_FFQ_标准列名对照表.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            help="BLOCK FFQ standard columns, bilingual reference" if is_en else "BLOCK FFQ 标准列名、中英文说明",
        )

        compute_title = cfg["title_en"] if is_en else cfg["title"]
        if st.button(f"\U0001f680 Compute {compute_title} (BLOCK)" if is_en else f"\U0001f680 开始计算 {compute_title} (BLOCK)", type="primary", use_container_width=True,
                     key=f"compute_{index_key}_block"):
            if block_file is None:
                st.error("Please upload BLOCK FFQ data file" if is_en else "请上传 BLOCK FFQ 数据文件")
                return

            with st.spinner(f"Processing BLOCK data and computing {compute_title}..." if is_en else f"正在处理 BLOCK 数据并计算 {compute_title}..."):
                try:
                    h = _lazy_import_heavy()
                    df = h["load_data"](block_file)
                    if df is None:
                        return

                    if index_key == "DII":
                        result = h["compute_dii_block"](df)
                    elif index_key == "AHEI":
                        result = h["compute_ahei_block"](df)
                    elif index_key == "AHEIP":
                        result = h["compute_aheip_block"](df)
                    else:
                        result = _compute_from_generic_data(index_key, cfg, df, "BLOCK")

                    if result is not None:
                        st.session_state[f"result_{index_key}"] = {
                            "data": result,
                            "mode": "block",
                            "file_dep": block_file.name if block_file else None,
                            "hash": get_inputs_hash(index_key)
                        }
                        st.session_state[f"scroll_to_result_{index_key}"] = True
                        st.rerun()

                except Exception as e:
                    st.error(f"计算出错: {type(e).__name__}: {e}")
                    st.exception(e)

    return block_file.name if block_file else None


# ═══════════════════════════════════════════════════════════════════════════════
# ASA24 / DHQ3 / BLOCK 非DII 通用适配器
# ═══════════════════════════════════════════════════════════════════════════════

def _compute_from_asa24_data(index_key, cfg, df, summarize):
    """从 ASA24 Totals.csv 数据计算非 DII 指数。

    识别 ASA24 标准列名，映射到指数参数，调用核心计算函数。
    """
    from utils import _run_asa24_for_index
    return _run_asa24_for_index(index_key, cfg, df, summarize)


def _compute_from_generic_data(index_key, cfg, df, source_label):
    """从通用数据源（DHQ3/BLOCK）计算非 DII 指数。

    尝试自动识别列名并映射到指数参数。
    如果自动映射失败，引导用户切换到「通用版（列名映射）」模式。
    """
    # Build auto-mapping from recognized column names
    auto_mapping = _auto_map_columns(df, index_key, cfg)
    unmapped = sum(1 for v in auto_mapping.values() if v is None)

    if unmapped > len(auto_mapping) * 0.5:
        st.warning(
            f"**自动列名识别不完整**（{unmapped}/{len(auto_mapping)} 个参数未匹配）。\n\n"
            f"请切换到 **通用版（列名映射）** 模式手动映射列名。"
        )
        return

    col_mapping = {k: v for k, v in auto_mapping.items() if v is not None}
    try:
        return _run_computation_direct(index_key, cfg, df, col_mapping)
    except Exception as e:
        st.error(f"自动计算失败: {e}。请切换到「通用版（列名映射）」模式手动操作。")
        st.exception(e)
        return None


def _auto_map_columns(df, index_key, cfg):
    """尝试自动识别 DataFrame 列名并映射到指数参数。"""
    from utils import FUNCTION_MAP

    col_lower = [c.lower().strip().replace(" ", "_").replace("-", "_") for c in df.columns]
    col_orig = list(df.columns)

    mapping = {}

    # Map ID column
    id_candidates = ["respondent_id", "respondentid", "id", "seqn", "username", "user_name",
                     "participant_id", "participantid", "subject_id", "subjectid"]
    for cid in id_candidates:
        if cid in col_lower:
            idx = col_lower.index(cid)
            mapping["respondent_id"] = col_orig[idx]
            break
    if "respondent_id" not in mapping and "SEQN" in df.columns:
        mapping["respondent_id"] = "SEQN"

    # Map extra params
    for ep in cfg.get("extra_params", []):
        if ep["name"] == "respondent_id":
            continue
        candidates = _get_column_candidates(ep["name"])
        for c in candidates:
            if c in col_lower:
                idx = col_lower.index(c)
                mapping[ep["name"]] = col_orig[idx]
                break

    # Map groups/params
    for group in cfg.get("groups", []):
        for p in group["params"]:
            candidates = _get_column_candidates(p["name"])
            for c in candidates:
                if c in col_lower:
                    idx = col_lower.index(c)
                    mapping[p["name"]] = col_orig[idx]
                    break
            if p["name"] not in mapping:
                mapping[p["name"]] = None

    return mapping


def _get_column_candidates(param_name):
    """获取参数名可能的列名候选列表。"""
    name_lower = param_name.lower().replace("_", "")
    candidates = [
        name_lower,
        param_name.lower(),
        param_name.upper(),
        param_name,
        param_name.lower().replace("_", ""),
    ]
    known_synonyms = {
        "respondent_id": ["id", "seqn", "respondent_id", "participant_id", "subject_id", "编号", "参与者id", "参与者编号", "用户id", "id", "seqn"],
        "gender": ["gender", "sex", "性别", "男女"],
        "age": ["age", "年龄", "岁"],
        "total_kcal": ["kcal", "energy", "total_energy", "totalenergy", "totalkcal",
                       "dr1tkcals", "dr1tkcals", "热量", "能量", "总能量", "卡路里"],
        "kcal": ["kcal", "energy", "total_energy", "totalenergy", "totalkcal", "热量", "能量", "总能量", "卡路里"],
        "total_fruit": ["fruit_total", "f_total", "totalfruit", "totalfruits", "水果", "总水果", "水果类"],
        "fruit": ["fruit", "total_fruit", "fruit_total", "f_total", "totalfruit", "totalfruits", "水果", "总水果", "水果类", "完整水果"],
        "whole_fruit": ["whole_fruit", "wholefrt", "wholefruit", "wholefruits", "完整水果", "新鲜水果"],
        "total_vegetable": ["vegetable_total", "v_total", "totalvegetable", "totalvegetables", "veg_total", "蔬菜", "总蔬菜", "蔬菜类"],
        "vegetable": ["vegetable", "total_vegetable", "vegetable_total", "v_total", "totalvegetable", "totalvegetables", "veg_total", "蔬菜", "总蔬菜", "蔬菜类"],
        "whole_grain": ["whole_grain", "wholegrain", "whole_grains", "wholegrains", "全谷物", "全谷类", "全麦"],
        "refined_grain": ["refined_grain", "refinedgrain", "refined_grains", "refinedgrains", "精制谷物", "精谷物", "精面"],
        "dairy": ["dairy", "dairy_total", "milk", "乳制品", "奶类", "乳类", "牛奶"],
        "nut_legume": ["nut_legume", "nuts_legumes", "nut", "nuts", "legume", "legumes", "坚果", "豆类", "坚果和豆类", "坚果豆类", "坚果与豆类"],
        "nuts": ["nuts", "nut", "坚果", "坚果类"],
        "legumes": ["legumes", "legume", "豆类", "豆类食物"],
        "sodium": ["sodium_mg", "na", "sodi", "sodium", "dr1tsodi", "dr1tsodium", "钠", "盐"],
        "fiber": ["dietary_fiber", "fibre", "dietaryfiber", "totalfiber", "dr1tfibe", "dr1tfiber", "纤维", "膳食纤维", "纤维素"],
        "alcohol": ["alcohol_g", "alc", "dr1talco", "dr1talcohol", "酒精", "乙醇", "酒精量", "酒"],
        "protein": ["protein_g", "prot", "totalprotein", "dr1tprot", "蛋白质", "蛋白"],
        "carb": ["carbohydrate", "carbo", "totalcarb", "dr1tcarb", "碳水化合物", "碳水"],
        "totalfat": ["total_fat", "fat", "totalfat", "tfat", "total_fat_g", "总脂肪", "脂肪"],
        "satfat": ["saturated_fat", "saturatedfat", "sat_fat", "sfa", "satfat_g", "饱和脂肪", "饱和脂肪酸"],
        "pufa": ["pufa", "poly_fat", "polyunsaturated", "多不饱和脂肪", "多不饱和脂肪酸"],
        "mufa": ["mufa", "mono_fat", "monounsaturated", "单不饱和脂肪", "单不饱和脂肪酸"],
        "trans_fat": ["transfat", "trans_fat", "trans_fatty_acids", "反式脂肪", "反式脂肪酸"],
        "transfat": ["transfat", "trans_fat", "trans_fatty_acids", "反式脂肪", "反式脂肪酸"],
        "n3_fat": ["n3fat", "omega3", "omega_3", "omega-3脂肪酸", "omega3脂肪酸", "n3脂肪酸"],
        "n3fat": ["n3fat", "omega3", "omega_3", "omega-3脂肪酸", "omega3脂肪酸", "n3脂肪酸"],
        "ssb_fruit_juice": ["ssb", "ssb_juice", "sweetened_beverage", "含糖饮料", "甜饮料", "果汁", "含糖饮料和果汁", "含糖饮料+果汁"],
        "red_processed_meat": ["red_meat", "processed_meat", "red_processed_meat", "红肉", "加工肉", "红肉和加工肉", "红肉与加工肉", "红肉加工肉", "红肉+加工肉"],
        "added_sugar": ["added_sugar", "added_sugars", "sugar", "添加糖", "糖"],
        "hpf_rg_ratio": ["hpf_rg_ratio", "hpf_ratio", "hpfrg_ratio", "hpfrg_ratio_serv_acs2020", "高加工食品", "精制谷物比值", "高加工食品比值"],
        "hpf_servings": ["hpf_servings", "hpf_serv", "hpfrg_serv", "hpfrg_serv_acs2020", "高加工食品份数", "高加工食品摄入量"],
        "vegetable_items": ["veg_items", "vegetable_items", "veg_items_serv_acs2020", "蔬菜种类", "蔬菜种类数"],
        "fruit_items": ["frt_items", "fruit_items", "frt_items_serv_acs2020", "水果种类", "水果种类数"],
    }
    for key, syns in known_synonyms.items():
        if param_name.lower() == key.lower():
            candidates.extend(syns)
    return list(set(candidates))


def _run_computation_direct(index_key, cfg, df, col_mapping):
    """直接运行计算（不使用 Streamlit widget）。"""
    from utils import FUNCTION_MAP

    func = FUNCTION_MAP()[cfg["function"]]
    import inspect
    sig = inspect.signature(func)

    args = {}
    for param_name in sig.parameters:
        if param_name == "data":
            args["data"] = df
        elif param_name in col_mapping:
            args[param_name] = df[col_mapping[param_name]].values
        elif param_name == "respondent_id":
            if "respondent_id" in col_mapping:
                args["respondent_id"] = df[col_mapping["respondent_id"]].values
            else:
                args["respondent_id"] = np.arange(1, len(df) + 1)

    result = func(**args)
    return result
