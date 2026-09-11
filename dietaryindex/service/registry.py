"""Registry helpers for API-facing index metadata."""

from __future__ import annotations

from copy import deepcopy

from dietaryindex.reference.index_registry import INDEX_SPEC_REGISTRY
from dietaryindex.reference.index_params import INDEX_PARAMS
from dietaryindex.reference.literature import get_index_literature


_BASE_SCORE_SCALES = {item["index_key"]: item["score_scale"] for item in INDEX_SPEC_REGISTRY}
_VERSION_SCORE_SCALES = {
    "HEI2020_V1": "0-100",
    "HEI2020_V2": "0-100",
    "MEDI_V1": "0-11",
    "MEDI_V2": "0-55",
    "ACS2020_V1": "0-12",
    "ACS2020_V2": "0-12",
    "PHDI_V1": "0-140",
    "PHDI_V2": "0-140",
}


def _score_scale(index_key: str) -> str:
    if index_key in _VERSION_SCORE_SCALES:
        return _VERSION_SCORE_SCALES[index_key]
    return _BASE_SCORE_SCALES[index_key]


def _clean_zh(value, fallback: str | None = None):
    if isinstance(value, str) and value.strip():
        return value
    return fallback or value


MODE_DEFINITIONS = {
    "general": {
        "label_en": "General (Column Mapping)",
        "label_zh": "通用模式（列名映射）",
        "description_en": "Upload a prepared CSV or Excel file and map columns manually or semi-automatically.",
        "description_zh": "上传整理好的 CSV 或 Excel 文件，并手动或半自动完成列名映射。",
        "kind": "tabular",
    },
    "nhanes_fped": {
        "label_en": "NHANES FPED (Post-2005)",
        "label_zh": "NHANES FPED（2005年后）",
        "description_en": "Direct upload of NHANES 2005+ dietary recall files.",
        "description_zh": "直接上传 NHANES 2005 年后的膳食回顾文件。",
        "kind": "multi-file",
    },
    "nhanes_mped": {
        "label_en": "NHANES MPED (1999-2004)",
        "label_zh": "NHANES MPED（1999-2004）",
        "description_en": "For early NHANES MPED or Pyramid data structures.",
        "description_zh": "适用于早期 NHANES MPED / Pyramid 数据结构。",
        "kind": "multi-file",
    },
    "asa24": {
        "label_en": "ASA24",
        "label_zh": "ASA24",
        "description_en": "Upload an ASA24 Totals.csv export.",
        "description_zh": "上传 ASA24 的 Totals.csv 导出文件。",
        "kind": "tabular",
    },
    "dhq3": {
        "label_en": "DHQ3",
        "label_zh": "DHQ3",
        "description_en": "Upload a DHQ3 export for questionnaire-style dietary workflows.",
        "description_zh": "上传 DHQ3 导出文件，用于问卷型膳食数据流程。",
        "kind": "tabular",
    },
    "block": {
        "label_en": "BLOCK FFQ",
        "label_zh": "BLOCK FFQ",
        "description_en": "Upload a BLOCK FFQ export for food frequency workflows.",
        "description_zh": "上传 BLOCK FFQ 导出文件，用于食物频率问卷流程。",
        "kind": "tabular",
    },
}


MODE_FILE_SPECS = {
    "general": [
        {
            "key": "input",
            "label_en": "Input data file",
            "label_zh": "输入数据文件",
            "required": True,
            "accepted_extensions": [".csv", ".xlsx", ".xls", ".sas7bdat", ".xpt"],
            "description_en": "Prepared tabular data for column mapping.",
            "description_zh": "用于列名映射的整理后表格数据。",
        }
    ],
    "asa24": [
        {
            "key": "input",
            "label_en": "ASA24 Totals export",
            "label_zh": "ASA24 Totals 导出文件",
            "required": True,
            "accepted_extensions": [".csv"],
            "description_en": "Usually Totals.csv exported from ASA24.",
            "description_zh": "通常为 ASA24 导出的 Totals.csv。",
        }
    ],
    "dhq3": [
        {
            "key": "input",
            "label_en": "DHQ3 export",
            "label_zh": "DHQ3 导出文件",
            "required": True,
            "accepted_extensions": [".csv", ".xlsx", ".xls"],
            "description_en": "Use Total Daily Results for DII/PHDI; use detail.csv for AHEI.",
            "description_zh": "DII/PHDI 通常使用 Total Daily Results；AHEI 需要 detail.csv。",
        }
    ],
    "block": [
        {
            "key": "input",
            "label_en": "BLOCK FFQ export",
            "label_zh": "BLOCK FFQ 导出文件",
            "required": True,
            "accepted_extensions": [".csv", ".xlsx", ".xls"],
            "description_en": "BLOCK FFQ raw export used by the one-step adapters.",
            "description_zh": "BLOCK FFQ 原始导出文件，可直接用于一步式适配器。",
        }
    ],
    "nhanes_fped": [
        {
            "key": "fped_path",
            "label_en": "FPED totals day 1",
            "label_zh": "FPED 总表 Day 1",
            "required": False,
            "accepted_extensions": [".sas7bdat", ".xpt"],
            "description_en": "Needed by FPED total-based scores such as HEI, MED, and PHDI.",
            "description_zh": "HEI、MED、PHDI 等基于 FPED total 的指标需要此文件。",
        },
        {
            "key": "nutrient_path",
            "label_en": "Nutrient totals day 1",
            "label_zh": "营养素总表 Day 1",
            "required": True,
            "accepted_extensions": [".sas7bdat", ".xpt"],
            "description_en": "Required by nearly all NHANES FPED workflows.",
            "description_zh": "几乎所有 NHANES FPED 工作流都需要此文件。",
        },
        {
            "key": "demo_path",
            "label_en": "DEMO file",
            "label_zh": "DEMO 文件",
            "required": False,
            "accepted_extensions": [".xpt"],
            "description_en": "Often required for age / sex filters or merge-back metadata.",
            "description_zh": "常用于年龄、性别筛选或结果回并。",
        },
        {
            "key": "fped_path2",
            "label_en": "FPED totals day 2",
            "label_zh": "FPED 总表 Day 2",
            "required": False,
            "accepted_extensions": [".sas7bdat", ".xpt"],
            "description_en": "Optional second recall day for total-based scores.",
            "description_zh": "total 类指标可选的第二天回顾文件。",
        },
        {
            "key": "nutrient_path2",
            "label_en": "Nutrient totals day 2",
            "label_zh": "营养素总表 Day 2",
            "required": False,
            "accepted_extensions": [".sas7bdat", ".xpt"],
            "description_en": "Optional second recall day nutrient totals.",
            "description_zh": "可选的第二天营养素总表。",
        },
        {
            "key": "fped_ind_path",
            "label_en": "FPED individual foods day 1",
            "label_zh": "FPED 个体食物表 Day 1",
            "required": False,
            "accepted_extensions": [".sas7bdat", ".xpt"],
            "description_en": "Needed by individual-food based scores such as DASH, AHEI, MEDI, and DI-GM.",
            "description_zh": "DASH、AHEI、MEDI、DI-GM 等基于个体食物的指标需要此文件。",
        },
        {
            "key": "nutrient_ind_path",
            "label_en": "Nutrient individual foods day 1",
            "label_zh": "营养素个体食物表 Day 1",
            "required": False,
            "accepted_extensions": [".sas7bdat", ".xpt"],
            "description_en": "Needed by individual-food based scores.",
            "description_zh": "基于个体食物的指标需要此文件。",
        },
        {
            "key": "fped_ind_path2",
            "label_en": "FPED individual foods day 2",
            "label_zh": "FPED 个体食物表 Day 2",
            "required": False,
            "accepted_extensions": [".sas7bdat", ".xpt"],
            "description_en": "Optional second recall day for individual-food scores.",
            "description_zh": "个体食物类指标可选的第二天文件。",
        },
        {
            "key": "nutrient_ind_path2",
            "label_en": "Nutrient individual foods day 2",
            "label_zh": "营养素个体食物表 Day 2",
            "required": False,
            "accepted_extensions": [".sas7bdat", ".xpt"],
            "description_en": "Optional second recall day for individual-food scores.",
            "description_zh": "个体食物类指标可选的第二天文件。",
        },
        {
            "key": "other_ingredients1",
            "label_en": "Other ingredients day 1",
            "label_zh": "其他成分 Day 1",
            "required": False,
            "accepted_extensions": [".csv"],
            "description_en": "Optional DII enhancement table for garlic, ginger, flavonoids, and related variables.",
            "description_zh": "DII 可选增强表，用于大蒜、生姜、黄酮等额外成分。",
        },
        {
            "key": "other_ingredients2",
            "label_en": "Other ingredients day 2",
            "label_zh": "其他成分 Day 2",
            "required": False,
            "accepted_extensions": [".csv"],
            "description_en": "Optional day 2 enhancement table.",
            "description_zh": "可选的 Day 2 增强表。",
        },
    ],
    "nhanes_mped": [
        {
            "key": "pyramid_path",
            "label_en": "Pyramid totals day 1",
            "label_zh": "Pyramid 总表 Day 1",
            "required": False,
            "accepted_extensions": [".sas7bdat", ".xpt", ".txt", ".csv"],
            "description_en": "Needed by MPED/Pyramid total-based PHDI workflows.",
            "description_zh": "MPED/Pyramid total 型 PHDI 工作流需要此文件。",
        },
        {
            "key": "nutrient_path",
            "label_en": "Nutrient totals day 1",
            "label_zh": "营养素总表 Day 1",
            "required": True,
            "accepted_extensions": [".xpt"],
            "description_en": "Required by most MPED workflows.",
            "description_zh": "大多数 MPED 工作流都需要此文件。",
        },
        {
            "key": "demo_path",
            "label_en": "DEMO file",
            "label_zh": "DEMO 文件",
            "required": False,
            "accepted_extensions": [".xpt"],
            "description_en": "Often required for age / sex filters or merge-back metadata.",
            "description_zh": "常用于年龄、性别筛选或结果回并。",
        },
        {
            "key": "pyramid_path2",
            "label_en": "Pyramid totals day 2",
            "label_zh": "Pyramid 总表 Day 2",
            "required": False,
            "accepted_extensions": [".sas7bdat", ".xpt", ".txt", ".csv"],
            "description_en": "Optional second recall day for PHDI workflows.",
            "description_zh": "PHDI 工作流可选的第二天文件。",
        },
        {
            "key": "nutrient_path2",
            "label_en": "Nutrient totals day 2",
            "label_zh": "营养素总表 Day 2",
            "required": False,
            "accepted_extensions": [".xpt"],
            "description_en": "Optional second recall day nutrient totals.",
            "description_zh": "可选的第二天营养素总表。",
        },
        {
            "key": "mped_per_100_gram_path",
            "label_en": "MPED equiv.txt",
            "label_zh": "MPED equiv.txt",
            "required": False,
            "accepted_extensions": [".txt", ".csv"],
            "description_en": "Used by several MPED individual-food workflows.",
            "description_zh": "多个 MPED 个体食物工作流会用到这个 equiv.txt。",
        },
        {
            "key": "wjfrt",
            "label_en": "WJFRT table",
            "label_zh": "WJFRT 表",
            "required": False,
            "accepted_extensions": [".csv"],
            "description_en": "Optional override for the built-in whole juice fruit ratio table.",
            "description_zh": "可选覆盖内置的 whole juice fruit ratio 表。",
        },
        {
            "key": "nutrient_ind_path",
            "label_en": "Nutrient individual foods day 1",
            "label_zh": "营养素个体食物表 Day 1",
            "required": False,
            "accepted_extensions": [".xpt"],
            "description_en": "Needed by AHEI, DASH, MEDI, and DI-GM MPED workflows.",
            "description_zh": "AHEI、DASH、MEDI、DI-GM 等 MPED 工作流需要此文件。",
        },
        {
            "key": "nutrient_ind_path2",
            "label_en": "Nutrient individual foods day 2",
            "label_zh": "营养素个体食物表 Day 2",
            "required": False,
            "accepted_extensions": [".xpt"],
            "description_en": "Optional second recall day for individual-food workflows.",
            "description_zh": "个体食物工作流可选的第二天文件。",
        },
        {
            "key": "other_ingredients1",
            "label_en": "Other ingredients day 1",
            "label_zh": "其他成分 Day 1",
            "required": False,
            "accepted_extensions": [".csv"],
            "description_en": "Optional DII enhancement table.",
            "description_zh": "DII 可选增强表。",
        },
        {
            "key": "other_ingredients2",
            "label_en": "Other ingredients day 2",
            "label_zh": "其他成分 Day 2",
            "required": False,
            "accepted_extensions": [".csv"],
            "description_en": "Optional day 2 DII enhancement table.",
            "description_zh": "可选的 Day 2 DII 增强表。",
        },
    ],
}


INDEX_MODE_CONFIG = {
    "DII": ["general", "nhanes_fped", "nhanes_mped", "asa24", "dhq3", "block"],
    "HEI2015": ["general", "nhanes_fped", "nhanes_mped", "asa24"],
    "HEI2020": ["general", "nhanes_fped", "nhanes_mped", "asa24"],
    "AHEI": ["general", "nhanes_fped", "nhanes_mped", "asa24", "dhq3", "block"],
    "AHEIP": ["general", "block"],
    "DASH": ["general", "nhanes_fped", "nhanes_mped", "asa24", "dhq3", "block"],
    "DASHI": ["general", "nhanes_fped", "nhanes_mped", "asa24"],
    "MED": ["general", "nhanes_fped", "nhanes_mped", "asa24", "dhq3", "block"],
    "MEDI": ["general", "nhanes_fped", "nhanes_mped"],
    "ACS2020": ["general"],
    "PHDI": ["general", "nhanes_fped", "nhanes_mped", "asa24", "dhq3", "block"],
    "DI_GM": ["general", "nhanes_fped", "nhanes_mped"],
    "FISI": ["general", "nhanes_fped", "nhanes_mped", "asa24", "dhq3", "block"],
    "PDI": ["general"],
    "HPDI": ["general"],
    "UPDI": ["general"],
    "MIND": ["general"],
    "DQI_I": ["general"],
    "CHEI": ["general"],
    "DBI": ["general"],
    "GDQS": ["general"],
    "WISH": ["general"],
    "OBS": ["general"],
    "E_DII": ["general"],
    "CHINA_DII": ["general"],
    "NRF": ["general", "asa24", "dhq3", "block"],
    "NAR": ["general", "asa24", "dhq3", "block"],
    "MAR": ["general", "asa24", "dhq3", "block"],
    "INQ": ["general", "asa24", "dhq3", "block"],
    "PRAL": ["general", "asa24", "dhq3", "block"],
    "NEAP": ["general", "asa24", "dhq3", "block"],
    "CDAI": ["general", "asa24", "dhq3", "block"],
}


MODE_REQUIREMENTS = {
    ("DII", "general"): {"single_file": True, "required_file_keys": ["input"]},
    ("HEI2015", "general"): {"single_file": True, "required_file_keys": ["input"]},
    ("HEI2020", "general"): {"single_file": True, "required_file_keys": ["input"]},
    ("AHEI", "general"): {"single_file": True, "required_file_keys": ["input"]},
    ("AHEIP", "general"): {"single_file": True, "required_file_keys": ["input"]},
    ("DASH", "general"): {"single_file": True, "required_file_keys": ["input"]},
    ("DASHI", "general"): {"single_file": True, "required_file_keys": ["input"]},
    ("MED", "general"): {"single_file": True, "required_file_keys": ["input"]},
    ("MEDI", "general"): {"single_file": True, "required_file_keys": ["input"]},
    ("ACS2020", "general"): {"single_file": True, "required_file_keys": ["input"]},
    ("PHDI", "general"): {"single_file": True, "required_file_keys": ["input"]},
    ("DI_GM", "general"): {"single_file": True, "required_file_keys": ["input"]},
    ("FISI", "general"): {"single_file": True, "required_file_keys": ["input"]},
    ("PDI", "general"): {"single_file": True, "required_file_keys": ["input"]},
    ("HPDI", "general"): {"single_file": True, "required_file_keys": ["input"]},
    ("UPDI", "general"): {"single_file": True, "required_file_keys": ["input"]},
    ("MIND", "general"): {"single_file": True, "required_file_keys": ["input"]},
    ("DQI_I", "general"): {"single_file": True, "required_file_keys": ["input"]},
    ("CHEI", "general"): {"single_file": True, "required_file_keys": ["input"]},
    ("DBI", "general"): {"single_file": True, "required_file_keys": ["input"]},
    ("GDQS", "general"): {"single_file": True, "required_file_keys": ["input"]},
    ("WISH", "general"): {"single_file": True, "required_file_keys": ["input"]},
    ("OBS", "general"): {"single_file": True, "required_file_keys": ["input"]},
    ("E_DII", "general"): {"single_file": True, "required_file_keys": ["input"]},
    ("CHINA_DII", "general"): {"single_file": True, "required_file_keys": ["input"]},
    ("NRF", "general"): {"single_file": True, "required_file_keys": ["input"]},
    ("NAR", "general"): {"single_file": True, "required_file_keys": ["input"]},
    ("MAR", "general"): {"single_file": True, "required_file_keys": ["input"]},
    ("INQ", "general"): {"single_file": True, "required_file_keys": ["input"]},
    ("PRAL", "general"): {"single_file": True, "required_file_keys": ["input"]},
    ("NEAP", "general"): {"single_file": True, "required_file_keys": ["input"]},
    ("CDAI", "general"): {"single_file": True, "required_file_keys": ["input"]},
    ("DII", "asa24"): {"single_file": True, "required_file_keys": ["input"], "notes_en": "Upload ASA24 Totals.csv.", "notes_zh": "请上传 ASA24 Totals.csv。"},
    ("PHDI", "asa24"): {"single_file": True, "required_file_keys": ["input"], "notes_en": "Upload ASA24 Totals.csv.", "notes_zh": "请上传 ASA24 Totals.csv。"},
    ("HEI2015", "asa24"): {"single_file": True, "required_file_keys": ["input"], "notes_en": "Prepared ASA24 exports will be auto-mapped.", "notes_zh": "系统会自动识别整理后的 ASA24 导出字段。"},
    ("HEI2020", "asa24"): {"single_file": True, "required_file_keys": ["input"], "notes_en": "Prepared ASA24 exports will be auto-mapped.", "notes_zh": "系统会自动识别整理后的 ASA24 导出字段。"},
    ("AHEI", "asa24"): {"single_file": True, "required_file_keys": ["input"], "notes_en": "Prepared ASA24 exports will be auto-mapped.", "notes_zh": "系统会自动识别整理后的 ASA24 导出字段。"},
    ("DASH", "asa24"): {"single_file": True, "required_file_keys": ["input"], "notes_en": "Prepared ASA24 exports will be auto-mapped.", "notes_zh": "系统会自动识别整理后的 ASA24 导出字段。"},
    ("DASHI", "asa24"): {"single_file": True, "required_file_keys": ["input"], "notes_en": "Prepared ASA24 exports will be auto-mapped.", "notes_zh": "系统会自动识别整理后的 ASA24 导出字段。"},
    ("MED", "asa24"): {"single_file": True, "required_file_keys": ["input"], "notes_en": "Prepared ASA24 exports will be auto-mapped.", "notes_zh": "系统会自动识别整理后的 ASA24 导出字段。"},
    ("DII", "dhq3"): {"single_file": True, "required_file_keys": ["input"], "notes_en": "Use Total Daily Results for DII.", "notes_zh": "DII 通常使用 Total Daily Results。"},
    ("AHEI", "dhq3"): {"single_file": True, "required_file_keys": ["input"], "notes_en": "AHEI requires DHQ3 detail.csv with Food ID.", "notes_zh": "AHEI 需要带 Food ID 的 DHQ3 detail.csv。"},
    ("PHDI", "dhq3"): {"single_file": True, "required_file_keys": ["input"], "notes_en": "Use DHQ3 exports with food-group and nutrient fields.", "notes_zh": "请上传包含食物组和营养字段的 DHQ3 导出文件。"},
    ("DASH", "dhq3"): {"single_file": True, "required_file_keys": ["input"], "notes_en": "Prepared DHQ3 exports will be auto-mapped.", "notes_zh": "系统会自动识别整理后的 DHQ3 导出字段。"},
    ("MED", "dhq3"): {"single_file": True, "required_file_keys": ["input"], "notes_en": "Prepared DHQ3 exports will be auto-mapped.", "notes_zh": "系统会自动识别整理后的 DHQ3 导出字段。"},
    ("DII", "block"): {"single_file": True, "required_file_keys": ["input"], "notes_en": "Upload one BLOCK FFQ export file.", "notes_zh": "请上传一个 BLOCK FFQ 导出文件。"},
    ("AHEI", "block"): {"single_file": True, "required_file_keys": ["input"], "notes_en": "Upload one BLOCK FFQ export file.", "notes_zh": "请上传一个 BLOCK FFQ 导出文件。"},
    ("AHEIP", "block"): {"single_file": True, "required_file_keys": ["input"], "notes_en": "Upload one BLOCK FFQ export file.", "notes_zh": "请上传一个 BLOCK FFQ 导出文件。"},
    ("PHDI", "block"): {"single_file": True, "required_file_keys": ["input"], "notes_en": "Upload one BLOCK FFQ export file.", "notes_zh": "请上传一个 BLOCK FFQ 导出文件。"},
    ("DASH", "block"): {"single_file": True, "required_file_keys": ["input"], "notes_en": "Prepared BLOCK exports will be auto-mapped.", "notes_zh": "系统会自动识别整理后的 BLOCK 导出字段。"},
    ("MED", "block"): {"single_file": True, "required_file_keys": ["input"], "notes_en": "Prepared BLOCK exports will be auto-mapped.", "notes_zh": "系统会自动识别整理后的 BLOCK 导出字段。"},
    ("DII", "nhanes_fped"): {
        "required_file_keys": ["nutrient_path"],
        "visible_file_keys": ["nutrient_path", "other_ingredients1", "nutrient_path2", "other_ingredients2", "demo_path"],
        "notes_en": "Day 1 nutrient totals are required. Day 2, demographics, and extra ingredients are optional.",
        "notes_zh": "Day 1 营养素总表为必需文件；Day 2、人口学和额外成分文件均为可选。",
    },
    ("HEI2015", "nhanes_fped"): {"required_file_keys": ["fped_path", "nutrient_path"], "notes_en": "Use FPED total + nutrient total files.", "notes_zh": "请上传 FPED 总表和营养素总表。"},
    ("HEI2020", "nhanes_fped"): {"required_file_keys": ["fped_path", "nutrient_path"], "notes_en": "Use FPED total + nutrient total files.", "notes_zh": "请上传 FPED 总表和营养素总表。"},
    ("MED", "nhanes_fped"): {"required_file_keys": ["fped_path", "nutrient_path"], "notes_en": "Use FPED total + nutrient total files.", "notes_zh": "请上传 FPED 总表和营养素总表。"},
    ("DASHI", "nhanes_fped"): {"required_file_keys": ["nutrient_path"], "notes_en": "Use nutrient total files.", "notes_zh": "请上传营养素总表。"},
    ("PHDI", "nhanes_fped"): {"required_file_keys": ["fped_path", "nutrient_path", "demo_path"], "notes_en": "PHDI requires FPED total, nutrient total, and DEMO.", "notes_zh": "PHDI 必须提供 FPED 总表、营养素总表和 DEMO 文件。"},
    ("DASH", "nhanes_fped"): {"required_file_keys": ["fped_ind_path", "nutrient_ind_path"], "notes_en": "Use FPED individual-food + nutrient individual-food files.", "notes_zh": "请上传 FPED 个体食物表和营养素个体食物表。"},
    ("AHEI", "nhanes_fped"): {"required_file_keys": ["fped_ind_path", "nutrient_ind_path"], "notes_en": "Use FPED individual-food + nutrient individual-food files.", "notes_zh": "请上传 FPED 个体食物表和营养素个体食物表。"},
    ("MEDI", "nhanes_fped"): {"required_file_keys": ["fped_ind_path", "nutrient_ind_path"], "notes_en": "Use FPED individual-food + nutrient individual-food files.", "notes_zh": "请上传 FPED 个体食物表和营养素个体食物表。"},
    ("DI_GM", "nhanes_fped"): {"required_file_keys": ["fped_ind_path", "nutrient_ind_path"], "notes_en": "Use FPED individual-food + nutrient individual-food files.", "notes_zh": "请上传 FPED 个体食物表和营养素个体食物表。"},
    ("FISI", "nhanes_fped"): {
        "required_file_keys": ["nutrient_path"],
        "visible_file_keys": ["nutrient_path", "nutrient_ind_path", "nutrient_path2", "nutrient_ind_path2", "demo_path"],
        "notes_en": "Nutrient variants require Day 1 totals. FISI1 also requires Day 1 individual foods; Day 2 total and individual files must be supplied together.",
        "notes_zh": "营养素版本必须提供 Day 1 总表；FISI1 还必须提供 Day 1 个体食物表，Day 2 总表与个体食物表必须成对提供。",
    },
    ("DII", "nhanes_mped"): {
        "required_file_keys": ["nutrient_path"],
        "visible_file_keys": ["nutrient_path", "other_ingredients1", "nutrient_path2", "other_ingredients2", "demo_path"],
        "notes_en": "Day 1 nutrient totals are required. Day 2, demographics, and extra ingredients are optional.",
        "notes_zh": "Day 1 营养素总表为必需文件；Day 2、人口学和额外成分文件均为可选。",
    },
    ("HEI2015", "nhanes_mped"): {"required_file_keys": ["nutrient_path", "nutrient_ind_path"], "notes_en": "Use day 1 nutrient total + individual-food nutrient files.", "notes_zh": "请上传 Day 1 营养素总表和个体食物营养素表。"},
    ("HEI2020", "nhanes_mped"): {"required_file_keys": ["nutrient_path", "nutrient_ind_path"], "notes_en": "Use day 1 nutrient total + individual-food nutrient files.", "notes_zh": "请上传 Day 1 营养素总表和个体食物营养素表。"},
    ("MED", "nhanes_mped"): {"required_file_keys": ["nutrient_path", "nutrient_ind_path"], "notes_en": "Use day 1 nutrient total + individual-food nutrient files.", "notes_zh": "请上传 Day 1 营养素总表和个体食物营养素表。"},
    ("AHEI", "nhanes_mped"): {"required_file_keys": ["nutrient_path", "nutrient_ind_path"], "notes_en": "Use day 1 nutrient total + individual-food nutrient files.", "notes_zh": "请上传 Day 1 营养素总表和个体食物营养素表。"},
    ("MEDI", "nhanes_mped"): {"required_file_keys": ["nutrient_path", "nutrient_ind_path"], "notes_en": "Use day 1 nutrient total + individual-food nutrient files.", "notes_zh": "请上传 Day 1 营养素总表和个体食物营养素表。"},
    ("DASH", "nhanes_mped"): {"required_file_keys": ["nutrient_path", "nutrient_ind_path"], "notes_en": "Use day 1 nutrient total + individual-food nutrient files.", "notes_zh": "请上传 Day 1 营养素总表和个体食物营养素表。"},
    ("DI_GM", "nhanes_mped"): {"required_file_keys": ["nutrient_path", "nutrient_ind_path"], "notes_en": "Use day 1 nutrient total + individual-food nutrient files.", "notes_zh": "请上传 Day 1 营养素总表和个体食物营养素表。"},
    ("DASHI", "nhanes_mped"): {"required_file_keys": ["nutrient_path"], "notes_en": "Use nutrient total files.", "notes_zh": "请上传营养素总表。"},
    ("PHDI", "nhanes_mped"): {"required_file_keys": ["pyramid_path", "nutrient_path", "demo_path"], "notes_en": "PHDI requires Pyramid total, nutrient total, and DEMO.", "notes_zh": "PHDI 必须提供 Pyramid 总表、营养素总表和 DEMO 文件。"},
    ("FISI", "nhanes_mped"): {
        "required_file_keys": ["nutrient_path"],
        "visible_file_keys": ["nutrient_path", "nutrient_ind_path", "nutrient_path2", "nutrient_ind_path2", "demo_path"],
        "notes_en": "Nutrient variants require Day 1 totals. FISI1 also requires Day 1 individual foods; Day 2 total and individual files must be supplied together.",
        "notes_zh": "营养素版本必须提供 Day 1 总表；FISI1 还必须提供 Day 1 个体食物表，Day 2 总表与个体食物表必须成对提供。",
    },
}


def _field_meta(item: dict) -> dict:
    label_en = item.get("label_en", item["name"])
    return {
        "name": item["name"],
        "label_en": label_en,
        "label_zh": _clean_zh(item.get("label", label_en), fallback=label_en),
        "required": bool(item.get("required")),
        "unit": item.get("unit"),
        "default": item.get("default"),
    }


def _flatten_fields(cfg: dict) -> list[dict]:
    fields: list[dict] = []
    for item in cfg.get("extra_params", []):
        fields.append({**_field_meta(item), "field_type": "extra"})
    for group in cfg.get("groups", []):
        group_name_en = group.get("name_en", group.get("name", "Group"))
        group_name_zh = _clean_zh(group.get("name", group_name_en), fallback=group_name_en)
        for item in group.get("params", []):
            fields.append(
                {
                    **_field_meta(item),
                    "field_type": "input",
                    "group_en": group_name_en,
                    "group_zh": group_name_zh,
                }
            )
    return fields


def get_mode_definitions() -> dict[str, dict]:
    return deepcopy(MODE_DEFINITIONS)


def get_mode_file_specs(mode: str) -> list[dict]:
    return deepcopy(MODE_FILE_SPECS.get(mode, []))


def get_mode_requirements(index_key: str, mode: str) -> dict:
    default = {
        "single_file": mode in {"general", "asa24", "dhq3", "block"},
        "required_file_keys": ["input"] if mode in {"general", "asa24", "dhq3", "block"} else [],
        "notes_en": "",
        "notes_zh": "",
    }
    return {**default, **deepcopy(MODE_REQUIREMENTS.get((index_key, mode), {}))}


def get_index_catalog() -> list[dict]:
    catalog = []
    for index_key, cfg in INDEX_PARAMS.items():
        title_en = cfg.get("title_en", index_key)
        supported_modes = list(INDEX_MODE_CONFIG.get(index_key, ["general"]))
        catalog.append(
            {
                "index_key": index_key,
                "title_en": title_en,
                "title_zh": _clean_zh(cfg.get("title", title_en), fallback=title_en),
                "description_en": cfg.get("description_en", ""),
                "description_zh": _clean_zh(cfg.get("description", title_en), fallback=cfg.get("description_en", title_en)),
                "function_name": cfg.get("function"),
                "score_scale": _score_scale(index_key),
                "max_score": cfg.get("max_score"),
                "output_cols": list(cfg.get("output_cols", [])),
                "supported_modes": supported_modes,
                "mode_specs": {mode: get_mode_file_specs(mode) for mode in supported_modes},
                "mode_requirements": {mode: get_mode_requirements(index_key, mode) for mode in supported_modes},
                "references": get_index_literature(index_key),
            }
        )
    return catalog


def get_index_detail(index_key: str) -> dict:
    if index_key not in INDEX_PARAMS:
        raise KeyError(f"Unknown index key: {index_key}")

    cfg = INDEX_PARAMS[index_key]
    title_en = cfg.get("title_en", index_key)
    supported_modes = list(INDEX_MODE_CONFIG.get(index_key, ["general"]))
    return {
        "index_key": index_key,
        "title_en": title_en,
        "title_zh": _clean_zh(cfg.get("title", title_en), fallback=title_en),
        "description_en": cfg.get("description_en", ""),
        "description_zh": _clean_zh(cfg.get("description", title_en), fallback=cfg.get("description_en", title_en)),
        "function_name": cfg.get("function"),
        "score_scale": _score_scale(index_key),
        "max_score": cfg.get("max_score"),
        "output_cols": list(cfg.get("output_cols", [])),
        "supported_modes": supported_modes,
        "mode_specs": {mode: get_mode_file_specs(mode) for mode in supported_modes},
        "mode_requirements": {mode: get_mode_requirements(index_key, mode) for mode in supported_modes},
        "references": get_index_literature(index_key),
        "fields": _flatten_fields(cfg),
    }
