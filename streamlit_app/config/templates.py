"""
数据模板生成 — 输出 Excel(.xlsx) 格式，多 Sheet 结构

解决 CSV 中文乱码问题，提供中/英文独立版本。
"""

import pandas as pd
from io import StringIO, BytesIO

from dietaryindex.reference.dii_global import DII_REFERENCE, DII_VARIABLE_ORDER


# ============================================================
# DII 通用版 — 标准列名参考 Excel（中文版）
# ============================================================

def _dii_template_excel_cn():
    """
    中文版：2个Sheet
    - Sheet1 "数据整理模板": 第1行=列名(46列)，第2行=全局均值示例值
    - Sheet2 "参数说明": 45参数完整表（列名|中文名|单位|分组|炎症分数|全局均值|标准差）
    """
    # Sheet1: 数据整理模板
    template_cols = ["参与者ID"]
    template_vals = [1]
    reference_rows = []

    for var_name in DII_VARIABLE_ORDER:
        ref = DII_REFERENCE[var_name]
        template_cols.append(ref["label_zh"])
        template_vals.append(ref["global_mean"])
        group_cn = {
            "macronutrients": "宏量营养素与能量",
            "vitamins": "维生素",
            "minerals": "矿物质",
            "flavonoids": "类黄酮",
            "spices": "香料与草本",
            "other": "其他",
        }
        reference_rows.append({
            "变量名(代码中)": var_name,
            "中文名称": ref["label_zh"],
            "英文名称": ref["label_en"],
            "单位": ref["unit"],
            "分类": group_cn.get(ref["group"], ref["group"]),
            "炎症效应分数": ref["inflammatory_score"],
            "全球日均摄入量": ref["global_mean"],
            "全球标准差": ref["sd"],
        })

    df_template = pd.DataFrame([template_vals], columns=template_cols)
    df_ref = pd.DataFrame(reference_rows)

    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df_template.to_excel(writer, sheet_name="数据整理模板", index=False)
        df_ref.to_excel(writer, sheet_name="参数说明", index=False)
    output.seek(0)
    return output


# ============================================================
# DII 通用版 — 标准列名参考 Excel（英文版）
# ============================================================

def _dii_template_excel_en():
    """
    English version: 2 Sheets
    - "Data Template": Row1=column names (46 cols), Row2=global mean examples
    - "Parameter Reference": 45 params (Variable|Name|Unit|Group|Inflammatory Score|Mean|SD)
    """
    template_cols = ["ParticipantID"]
    template_vals = [1]
    reference_rows = []

    for var_name in DII_VARIABLE_ORDER:
        ref = DII_REFERENCE[var_name]
        template_cols.append(var_name)
        template_vals.append(ref["global_mean"])
        reference_rows.append({
            "Variable": var_name,
            "Name": ref["label_en"],
            "Unit": ref["unit"],
            "Group": ref["group"],
            "Inflammatory Score": ref["inflammatory_score"],
            "Global Mean": ref["global_mean"],
            "Global SD": ref["sd"],
        })

    df_template = pd.DataFrame([template_vals], columns=template_cols)
    df_ref = pd.DataFrame(reference_rows)

    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df_template.to_excel(writer, sheet_name="Data Template", index=False)
        df_ref.to_excel(writer, sheet_name="Parameter Reference", index=False)
    output.seek(0)
    return output


# ============================================================
# ASA24 — 列名对照 Excel（中英双语）
# ============================================================

def _asa24_reference_excel():
    """
    1 Sheet "标准列名对照"：ASA24 期望列名 + 中文说明 + 英文说明 + 类型
    """
    data = [
        ("UserName", "参与者标识", "Participant ID", "string"),
        ("KCAL", "能量 (kcal)", "Energy", "numeric"),
        ("PROT", "蛋白质 (g)", "Protein", "numeric"),
        ("CARB", "碳水化合物 (g)", "Carbohydrate", "numeric"),
        ("TFIBE", "膳食纤维 (g)", "Dietary Fiber", "numeric"),
        ("TFAT", "总脂肪 (g)", "Total Fat", "numeric"),
        ("SFAT", "饱和脂肪 (g)", "Saturated Fat", "numeric"),
        ("MFAT", "单不饱和脂肪 (g)", "MUFA", "numeric"),
        ("PFAT", "多不饱和脂肪 (g)", "PUFA", "numeric"),
        ("CHOLE", "胆固醇 (mg)", "Cholesterol", "numeric"),
        ("ALCO", "酒精 (g)", "Alcohol", "numeric"),
        ("CAFF", "咖啡因 (mg)", "Caffeine", "numeric"),
        ("FOLA", "叶酸 (mcg)", "Folic Acid", "numeric"),
        ("NIA", "烟酸 (mg)", "Niacin", "numeric"),
        ("MG", "镁 (mg)", "Magnesium", "numeric"),
        ("IRON", "铁 (mg)", "Iron", "numeric"),
        ("ZINC", "锌 (mg)", "Zinc", "numeric"),
        ("SELE", "硒 (mcg)", "Selenium", "numeric"),
        ("THIA", "硫胺素 (mg)", "Thiamin", "numeric"),
        ("RIBO", "核黄素 (mg)", "Riboflavin", "numeric"),
        ("VITB6", "维生素B6 (mg)", "Vitamin B6", "numeric"),
        ("VITB12", "维生素B12 (mcg)", "Vitamin B12", "numeric"),
        ("VITC", "维生素C (mg)", "Vitamin C", "numeric"),
        ("VITD", "维生素D (mcg)", "Vitamin D", "numeric"),
        ("VITA", "维生素A (mcg RAE)", "Vitamin A", "numeric"),
        ("ATOC", "维生素E (mg)", "Vitamin E", "numeric"),
        ("N3FAT", "Omega-3 (g)", "Omega-3 Fatty Acids", "numeric"),
        ("N6FAT", "Omega-6 (g)", "Omega-6 Fatty Acids", "numeric"),
    ]
    df = pd.DataFrame(data, columns=["标准列名", "中文说明", "English Description", "数据类型"])
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="标准列名对照", index=False)
    output.seek(0)
    return output


# ============================================================
# DHQ3 — 列名对照 Excel（中英双语）
# ============================================================

def _dhq3_reference_excel():
    data = [
        ("Respondent ID", "参与者标识", "Participant ID", "string"),
        ("KCAL", "能量 (kcal)", "Energy", "numeric"),
        ("PROTEIN", "蛋白质 (g)", "Protein", "numeric"),
        ("CARBOHYDRATE", "碳水化合物 (g)", "Carbohydrate", "numeric"),
        ("FIBER", "膳食纤维 (g)", "Dietary Fiber", "numeric"),
        ("TOTAL_FAT", "总脂肪 (g)", "Total Fat", "numeric"),
        ("SAT_FAT", "饱和脂肪 (g)", "Saturated Fat", "numeric"),
        ("MONO_FAT", "单不饱和脂肪 (g)", "MUFA", "numeric"),
        ("POLY_FAT", "多不饱和脂肪 (g)", "PUFA", "numeric"),
        ("CHOLESTEROL", "胆固醇 (mg)", "Cholesterol", "numeric"),
        ("ALCOHOL", "酒精 (g)", "Alcohol", "numeric"),
        ("CAFFEINE", "咖啡因 (mg)", "Caffeine", "numeric"),
        ("FOLIC_ACID", "叶酸 (mcg)", "Folic Acid", "numeric"),
        ("NIACIN", "烟酸 (mg)", "Niacin", "numeric"),
        ("MAGNESIUM", "镁 (mg)", "Magnesium", "numeric"),
        ("IRON", "铁 (mg)", "Iron", "numeric"),
        ("ZINC", "锌 (mg)", "Zinc", "numeric"),
        ("SELENIUM", "硒 (mcg)", "Selenium", "numeric"),
        ("THIAMIN", "硫胺素 (mg)", "Thiamin", "numeric"),
        ("RIBOFLAVIN", "核黄素 (mg)", "Riboflavin", "numeric"),
        ("VITAMIN_B6", "维生素B6 (mg)", "Vitamin B6", "numeric"),
        ("VITAMIN_B12", "维生素B12 (mcg)", "Vitamin B12", "numeric"),
        ("VITAMIN_C", "维生素C (mg)", "Vitamin C", "numeric"),
        ("VITAMIN_D", "维生素D (mcg)", "Vitamin D", "numeric"),
        ("VITAMIN_A", "维生素A (mcg RAE)", "Vitamin A", "numeric"),
        ("VITAMIN_E", "维生素E (mg)", "Vitamin E", "numeric"),
        ("N3_FAT", "Omega-3 (g)", "Omega-3 Fatty Acids", "numeric"),
        ("N6_FAT", "Omega-6 (g)", "Omega-6 Fatty Acids", "numeric"),
        ("TRANS_FAT", "反式脂肪 (g)", "Trans Fat", "numeric"),
        ("BETA_CAROTENE", "β-胡萝卜素 (mcg)", "Beta-Carotene", "numeric"),
    ]
    df = pd.DataFrame(data, columns=["标准列名", "中文说明", "English Description", "数据类型"])
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="标准列名对照", index=False)
    output.seek(0)
    return output


# ============================================================
# BLOCK FFQ — 列名对照 Excel（中英双语）
# ============================================================

def _block_reference_excel():
    data = [
        ("RESPONDENTID", "参与者标识", "Participant ID (also: ID, SUBJECTID)", "string"),
        ("KCAL", "能量 (kcal)", "Energy", "numeric"),
        ("PROTEIN", "蛋白质 (g)", "Protein", "numeric"),
        ("CARB", "碳水化合物 (g)", "Carbohydrate", "numeric"),
        ("FIBER", "膳食纤维 (g)", "Dietary Fiber", "numeric"),
        ("TOTALFAT", "总脂肪 (g)", "Total Fat", "numeric"),
        ("SATFAT", "饱和脂肪 (g)", "Saturated Fat", "numeric"),
        ("MONOFAT", "单不饱和脂肪 (g)", "MUFA", "numeric"),
        ("POLYFAT", "多不饱和脂肪 (g)", "PUFA", "numeric"),
        ("CHOLESTEROL", "胆固醇 (mg)", "Cholesterol", "numeric"),
        ("ALCOHOL", "酒精 (g)", "Alcohol", "numeric"),
        ("CAFFEINE", "咖啡因 (mg)", "Caffeine", "numeric"),
        ("FOLATE", "叶酸 (mcg)", "Folic Acid", "numeric"),
        ("NIACIN", "烟酸 (mg)", "Niacin", "numeric"),
        ("MAGNESIUM", "镁 (mg)", "Magnesium", "numeric"),
        ("IRON", "铁 (mg)", "Iron", "numeric"),
        ("ZINC", "锌 (mg)", "Zinc", "numeric"),
        ("SELENIUM", "硒 (mcg)", "Selenium", "numeric"),
        ("THIAMIN", "硫胺素 (mg)", "Thiamin", "numeric"),
        ("RIBOFLAVIN", "核黄素 (mg)", "Riboflavin", "numeric"),
        ("VITAMINB6", "维生素B6 (mg)", "Vitamin B6", "numeric"),
        ("VITAMINB12", "维生素B12 (mcg)", "Vitamin B12", "numeric"),
        ("VITAMINC", "维生素C (mg)", "Vitamin C", "numeric"),
        ("VITAMIND", "维生素D (mcg)", "Vitamin D", "numeric"),
        ("VITAMINA", "维生素A (IU)", "Vitamin A", "numeric"),
        ("VITAMINE", "维生素E (mg)", "Vitamin E", "numeric"),
        ("TRANSFAT", "反式脂肪 (g)", "Trans Fat", "numeric"),
        ("BETACAROTENE", "β-胡萝卜素 (mcg)", "Beta-Carotene", "numeric"),
        ("OMEGA3", "Omega-3 (g)", "Omega-3 Fatty Acids", "numeric"),
        ("OMEGA6", "Omega-6 (g)", "Omega-6 Fatty Acids", "numeric"),
    ]
    df = pd.DataFrame(data, columns=["标准列名", "中文说明", "English Description", "数据类型"])
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="标准列名对照", index=False)
    output.seek(0)
    return output


# ============================================================
# NHANES FPED — 文件结构参考 Excel（中英双语）
# ============================================================

def _nhanes_fped_reference_excel():
    # Sheet1: 文件清单
    files_data = [
        ("Day 1", "fpre_dr1tot_1718.sas7bdat", "FPED 数据 (SAS)", "食物模式等价数据库", "Food Patterns Equivalents Database"),
        ("Day 1", "DR1TOT_J.XPT", "总营养素 (XPT)", "Day 1 总营养素摄入 (168列)", "Day 1 Total Nutrient Intake"),
        ("Day 1", "other_ingredients.csv", "其他成分 (CSV)", "可选：大蒜/生姜/类黄酮等", "Optional: garlic/ginger/flavonoids etc."),
        ("Day 2", "fpre_dr2tot_1718.sas7bdat", "FPED 数据 (SAS)", "Day 2 食物模式等价数据库", "Day 2 Food Patterns Equivalents Database"),
        ("Day 2", "DR2TOT_J.XPT", "总营养素 (XPT)", "Day 2 总营养素摄入 (可选)", "Day 2 Total Nutrient Intake (optional)"),
        ("Day 2", "other_ingredients_day2.csv", "其他成分 (CSV)", "Day 2 其他成分 (可选)", "Day 2 other ingredients (optional)"),
    ]
    df_files = pd.DataFrame(files_data, columns=["日期", "文件名", "格式", "中文说明", "English Description"])

    # Sheet2: NHANES列名 → DII参数 对照
    nutrient_data = []
    from dietaryindex.adapters.nhanes_fped import NHANES_NUTRIENT_TO_DII
    for nh_col, dii_name in NHANES_NUTRIENT_TO_DII.items():
        ref = DII_REFERENCE.get(dii_name, {})
        nutrient_data.append({
            "NHANES 列名": nh_col,
            "DII 参数": dii_name,
            "中文名称": ref.get("label_zh", ""),
            "English Name": ref.get("label_en", ""),
            "单位": ref.get("unit", ""),
        })
    df_nutrients = pd.DataFrame(nutrient_data)

    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df_files.to_excel(writer, sheet_name="文件清单", index=False)
        df_nutrients.to_excel(writer, sheet_name="列名对照", index=False)
    output.seek(0)
    return output


# ============================================================
# NHANES MPED — 文件结构参考 Excel
# ============================================================

def _nhanes_mped_reference_excel():
    data = [
        ("Day 1", "pyr_tot_d1.sas7bdat", "MPED 每100克 (SAS)", "MyPyramid等价DB per 100g", "MyPyramid Equivalents DB"),
        ("Day 1", "wjfrt.sas7bdat", "WJFRT 表 (SAS)", "全果汁水果比率表", "Whole Juice Fruit Ratio Table"),
        ("Day 1", "DR1TOT_J.XPT", "总营养素 (XPT)", "Day 1 总营养素摄入", "Day 1 Total Nutrient Intake"),
        ("Day 1", "DR1IFF_J.XPT", "个体营养素 (XPT)", "Day 1 个体食物营养素", "Day 1 Individual Food Nutrients"),
        ("Day 1", "DEMO_J.XPT", "人口数据 (XPT)", "人口统计学信息", "Demographics"),
        ("Day 2", "DR2TOT_J.XPT", "总营养素 (XPT)", "Day 2 总营养素 (可选)", "Day 2 Total Nutrient (optional)"),
        ("Day 2", "DR2IFF_J.XPT", "个体营养素 (XPT)", "Day 2 个体营养素 (可选)", "Day 2 Individual Nutrients (optional)"),
    ]
    df = pd.DataFrame(data, columns=["日期", "文件名", "格式", "中文说明", "English Description"])
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="文件清单", index=False)
    output.seek(0)
    return output


# ============================================================
# 旧版兼容（保持向后兼容，输出 CSV utf-8-sig）
# ============================================================

def generate_dii_template():
    """旧版 DII 模板（兼容原有调用，返回 CSV 字符串 utf-8-sig）"""
    from dietaryindex.adapters.nhanes_fped import NHANES_NUTRIENT_TO_DII
    template_cols = ["ID"]
    for var_name in DII_VARIABLE_ORDER:
        template_cols.append(var_name)
    df = pd.DataFrame([], columns=template_cols)
    buf = StringIO()
    df.to_csv(buf, index=False, encoding="utf-8-sig")
    return buf.getvalue()


def generate_generic_template(param_names):
    """根据参数列表生成通用模板（兼容原有调用）"""
    row = {}
    for name, label in param_names:
        row[name] = 0
    df = pd.DataFrame([row, row])
    df.iloc[0, 0] = 1
    df.iloc[1, 0] = 2
    buf = StringIO()
    df.to_csv(buf, index=False)
    return buf.getvalue()
