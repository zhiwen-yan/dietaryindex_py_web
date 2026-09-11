"""
所有膳食指数参数定义

参考 dietaryindex R 包各函数签名。
"""

__all__ = ["INDEX_PARAMS"]


INDEX_PARAMS = {
    "DII": {
        "title": "膳食炎症指数 (DII)",
        "title_en": "Dietary Inflammatory Index",
        "description": "基于 45 种食物/营养素的全球参考数据库，计算膳食炎症指数。提供越多参数，结果越完整。",
        "description_en": "Calculates the Dietary Inflammatory Index based on a global reference database of 45 foods/nutrients. The more parameters provided, the more complete the result.",
        "function": "compute_dii",
        "extra_params": [
            {"name": "respondent_id", "label": "参与者ID", "label_en": "Respondent ID", "required": True},
            {"name": "repeat_num", "label": "重复编号 (REPEATNUM)", "label_en": "Repeat Number", "required": False, "default": 1},
        ],
        "groups": [
            {
                "name": "宏量营养素与能量",
                "name_en": "Macronutrients & Energy",
                "params": [
                    {"name": "ALCOHOL", "label": "酒精 (g)", "label_en": "Alcohol (g)", "unit": "g", "required": False},
                    {"name": "CARB", "label": "碳水化合物 (g)", "label_en": "Carbohydrate (g)", "unit": "g", "required": False},
                    {"name": "TOTALFAT", "label": "总脂肪 (g)", "label_en": "Total Fat (g)", "unit": "g", "required": False},
                    {"name": "PROTEIN", "label": "蛋白质 (g)", "label_en": "Protein (g)", "unit": "g", "required": False},
                    {"name": "FIBER", "label": "膳食纤维 (g)", "label_en": "Fiber (g)", "unit": "g", "required": False},
                    {"name": "SATFAT", "label": "饱和脂肪 (g)", "label_en": "Saturated Fat (g)", "unit": "g", "required": False},
                    {"name": "MUFA", "label": "单不饱和脂肪酸 (g)", "label_en": "MUFA (g)", "unit": "g", "required": False},
                    {"name": "PUFA", "label": "多不饱和脂肪酸 (g)", "label_en": "PUFA (g)", "unit": "g", "required": False},
                    {"name": "TRANSFAT", "label": "反式脂肪 (g)", "label_en": "Trans Fat (g)", "unit": "g", "required": False},
                    {"name": "CHOLES", "label": "胆固醇 (mg)", "label_en": "Cholesterol (mg)", "unit": "mg", "required": False},
                    {"name": "N3FAT", "label": "Omega-3脂肪酸 (g)", "label_en": "Omega-3 Fatty Acids (g)", "unit": "g", "required": False},
                    {"name": "N6FAT", "label": "Omega-6脂肪酸 (g)", "label_en": "Omega-6 Fatty Acids (g)", "unit": "g", "required": False},
                    {"name": "KCAL", "label": "能量 (kcal)", "label_en": "Energy (kcal)", "unit": "kcal", "required": False},
                ]
            },
            {
                "name": "维生素",
                "name_en": "Vitamins",
                "params": [
                    {"name": "VITA", "label": "维生素A (RE)", "label_en": "Vitamin A (RE)", "unit": "RE", "required": False},
                    {"name": "VITB6", "label": "维生素B6 (mg)", "label_en": "Vitamin B6 (mg)", "unit": "mg", "required": False},
                    {"name": "VITB12", "label": "维生素B12 (μg)", "label_en": "Vitamin B12 (μg)", "unit": "μg", "required": False},
                    {"name": "VITC", "label": "维生素C (mg)", "label_en": "Vitamin C (mg)", "unit": "mg", "required": False},
                    {"name": "VITD", "label": "维生素D (μg)", "label_en": "Vitamin D (μg)", "unit": "μg", "required": False},
                    {"name": "VITE", "label": "维生素E (mg)", "label_en": "Vitamin E (mg)", "unit": "mg", "required": False},
                    {"name": "THIAMIN", "label": "硫胺素/B1 (mg)", "label_en": "Thiamin (mg)", "unit": "mg", "required": False},
                    {"name": "RIBOFLAVIN", "label": "核黄素/B2 (mg)", "label_en": "Riboflavin (mg)", "unit": "mg", "required": False},
                    {"name": "NIACIN", "label": "烟酸 (mg)", "label_en": "Niacin (mg)", "unit": "mg", "required": False},
                    {"name": "FOLICACID", "label": "叶酸 (μg)", "label_en": "Folic Acid (μg)", "unit": "μg", "required": False},
                    {"name": "BCAROTENE", "label": "β-胡萝卜素 (μg)", "label_en": "Beta-Carotene (μg)", "unit": "μg", "required": False},
                ]
            },
            {
                "name": "矿物质",
                "name_en": "Minerals",
                "params": [
                    {"name": "IRON", "label": "铁 (mg)", "label_en": "Iron (mg)", "unit": "mg", "required": False},
                    {"name": "MG", "label": "镁 (mg)", "label_en": "Magnesium (mg)", "unit": "mg", "required": False},
                    {"name": "SE", "label": "硒 (μg)", "label_en": "Selenium (μg)", "unit": "μg", "required": False},
                    {"name": "ZN", "label": "锌 (mg)", "label_en": "Zinc (mg)", "unit": "mg", "required": False},
                ]
            },
            {
                "name": "类黄酮",
                "name_en": "Flavonoids",
                "params": [
                    {"name": "FLA3OL", "label": "黄烷-3-醇 (mg)", "label_en": "Flavan-3-ol (mg)", "unit": "mg", "required": False},
                    {"name": "FLAVONES", "label": "黄酮 (mg)", "label_en": "Flavones (mg)", "unit": "mg", "required": False},
                    {"name": "FLAVONOLS", "label": "黄酮醇 (mg)", "label_en": "Flavonols (mg)", "unit": "mg", "required": False},
                    {"name": "FLAVONONES", "label": "黄烷酮 (mg)", "label_en": "Flavanones (mg)", "unit": "mg", "required": False},
                    {"name": "ANTHOC", "label": "花青素 (mg)", "label_en": "Anthocyanidins (mg)", "unit": "mg", "required": False},
                    {"name": "ISOFLAVONES", "label": "异黄酮 (mg)", "label_en": "Isoflavones (mg)", "unit": "mg", "required": False},
                ]
            },
            {
                "name": "香料草本",
                "name_en": "Spices & Herbs",
                "params": [
                    {"name": "GARLIC", "label": "大蒜 (g)", "label_en": "Garlic (g)", "unit": "g", "required": False},
                    {"name": "GINGER", "label": "生姜 (mg)", "label_en": "Ginger (mg)", "unit": "mg", "required": False},
                    {"name": "ONION", "label": "洋葱 (g)", "label_en": "Onion (g)", "unit": "g", "required": False},
                    {"name": "PEPPER", "label": "胡椒 (g)", "label_en": "Pepper (g)", "unit": "g", "required": False},
                    {"name": "SAFFRON", "label": "藏红花 (g)", "label_en": "Saffron (g)", "unit": "g", "required": False},
                    {"name": "THYME_OREGANO", "label": "百里香/牛至 (mg)", "label_en": "Thyme/Oregano (mg)", "unit": "mg", "required": False},
                    {"name": "TURMERIC", "label": "姜黄 (mg)", "label_en": "Turmeric (mg)", "unit": "mg", "required": False},
                    {"name": "ROSEMARY", "label": "迷迭香 (mg)", "label_en": "Rosemary (mg)", "unit": "mg", "required": False},
                ]
            },
            {
                "name": "其他",
                "name_en": "Other",
                "params": [
                    {"name": "CAFFEINE", "label": "咖啡因 (g)", "label_en": "Caffeine (g)", "unit": "g", "required": False},
                    {"name": "EUGENOL", "label": "丁香酚 (mg)", "label_en": "Eugenol (mg)", "unit": "mg", "required": False},
                    {"name": "TEA", "label": "茶 (g)", "label_en": "Tea (g)", "unit": "g", "required": False},
                ]
            },
        ],
        "output_cols": ["DII_ALL", "DII_NOETOH"],
        "max_score": None,
    },

    "HEI2020": {
        "title": "健康饮食指数 2020 (HEI-2020)",
        "title_en": "Healthy Eating Index 2020",
        "description": "基于 13 个食物组分的密度法评分。支持成人 (≥2岁) 和幼儿 (1-2岁) 标准。总分 0-100。",
        "description_en": "13-component density-based scoring. Supports adult (≥2 yrs) and toddler (1-2 yrs) standards. Total score 0-100.",
        "function": "compute_hei2020",
        "extra_params": [
            {"name": "respondent_id", "label": "参与者ID", "label_en": "Respondent ID", "required": True},
            {"name": "age", "label": "年龄 (岁)", "label_en": "Age (years)", "required": True},
        ],
        "groups": [
            {
                "name": "必需参数",
                "name_en": "Required",
                "params": [
                    {"name": "total_kcal", "label": "总能量 (kcal)", "label_en": "Total Energy (kcal)", "unit": "kcal", "required": True},
                    {"name": "total_fruit", "label": "总水果 (cup eq.)", "label_en": "Total Fruit (cup eq.)", "unit": "cup eq.", "required": True},
                    {"name": "whole_fruit", "label": "完整水果 (cup eq.)", "label_en": "Whole Fruit (cup eq.)", "unit": "cup eq.", "required": True},
                    {"name": "total_vegetable", "label": "总蔬菜 (cup eq.)", "label_en": "Total Vegetable (cup eq.)", "unit": "cup eq.", "required": True},
                    {"name": "green_and_bean", "label": "深绿蔬菜+豆类 (cup eq.)", "label_en": "Green & Bean (cup eq.)", "unit": "cup eq.", "required": True},
                    {"name": "total_protein", "label": "总蛋白质 (oz eq.)", "label_en": "Total Protein (oz eq.)", "unit": "oz eq.", "required": True},
                    {"name": "seafood_plant_protein", "label": "海鲜+植物蛋白 (oz eq.)", "label_en": "Seafood & Plant Protein (oz eq.)", "unit": "oz eq.", "required": True},
                    {"name": "whole_grain", "label": "全谷物 (oz eq.)", "label_en": "Whole Grain (oz eq.)", "unit": "oz eq.", "required": True},
                    {"name": "dairy", "label": "乳制品 (cup eq.)", "label_en": "Dairy (cup eq.)", "unit": "cup eq.", "required": True},
                    {"name": "fatty_acid", "label": "脂肪酸比值 (MUFA+PUFA)/SFA", "label_en": "Fatty Acid Ratio", "unit": "ratio", "required": True},
                    {"name": "refined_grain", "label": "精制谷物 (oz eq.)", "label_en": "Refined Grain (oz eq.)", "unit": "oz eq.", "required": True},
                    {"name": "sodium", "label": "钠 (g/day)", "label_en": "Sodium (g/day)", "unit": "g/day", "required": True},
                    {"name": "added_sugar", "label": "添加糖 (%能量)", "label_en": "Added Sugar (% energy)", "unit": "% energy", "required": True},
                    {"name": "saturated_fat", "label": "饱和脂肪 (%能量)", "label_en": "Saturated Fat (% energy)", "unit": "% energy", "required": True},
                ]
            },
        ],
        "output_cols": ["HEI2020_ALL"],
        "max_score": 100,
    },

    "HEI2020_V1": {
        "title": "健康饮食指数 2020 V1 (HEI-2020 V1)",
        "title_en": "Healthy Eating Index 2020 V1",
        "description": "根据每日消耗的食物和营养素分量，计算 HEI2020 膳食指数（健康饮食指数 2020 及 HEI-Toddlers-2020）。此版本使用原始 HEI2020 算法，其中添加糖和饱和脂肪使用占总能量的百分比（% energy）输入，钠以 g/day 输入并在内部换算为 g/1000 kcal。总分 0-100。",
        "description_en": "Calculate the HEI-2020 dietary index (Healthy Eating Index 2020 and HEI-Toddlers-2020) based on daily food and nutrient intake. This version uses the original HEI-2020 algorithm with added sugar and saturated fat entered as percentage of total energy (% energy), and sodium in g/day converted internally to g/1000 kcal. Total score 0-100.",
        "function": "compute_hei2020",
        "extra_params": [
            {"name": "respondent_id", "label": "参与者ID", "label_en": "Respondent ID", "required": True},
            {"name": "age", "label": "年龄 (岁)", "label_en": "Age (years)", "required": True},
        ],
        "groups": [
            {
                "name": "必需参数",
                "name_en": "Required",
                "params": [
                    {"name": "total_kcal", "label": "总能量 (kcal)", "label_en": "Total Energy (kcal)", "unit": "kcal", "required": True},
                    {"name": "total_fruit", "label": "总水果 (cup eq.)", "label_en": "Total Fruit (cup eq.)", "unit": "cup eq.", "required": True},
                    {"name": "whole_fruit", "label": "完整水果 (cup eq.)", "label_en": "Whole Fruit (cup eq.)", "unit": "cup eq.", "required": True},
                    {"name": "total_vegetable", "label": "总蔬菜 (cup eq.)", "label_en": "Total Vegetable (cup eq.)", "unit": "cup eq.", "required": True},
                    {"name": "green_and_bean", "label": "深绿蔬菜+豆类 (cup eq.)", "label_en": "Green & Bean (cup eq.)", "unit": "cup eq.", "required": True},
                    {"name": "total_protein", "label": "总蛋白质 (oz eq.)", "label_en": "Total Protein (oz eq.)", "unit": "oz eq.", "required": True},
                    {"name": "seafood_plant_protein", "label": "海鲜+植物蛋白 (oz eq.)", "label_en": "Seafood & Plant Protein (oz eq.)", "unit": "oz eq.", "required": True},
                    {"name": "whole_grain", "label": "全谷物 (oz eq.)", "label_en": "Whole Grain (oz eq.)", "unit": "oz eq.", "required": True},
                    {"name": "dairy", "label": "乳制品 (cup eq.)", "label_en": "Dairy (cup eq.)", "unit": "cup eq.", "required": True},
                    {"name": "fatty_acid", "label": "脂肪酸比值 (MUFA+PUFA)/SFA", "label_en": "Fatty Acid Ratio", "unit": "ratio", "required": True},
                    {"name": "refined_grain", "label": "精制谷物 (oz eq.)", "label_en": "Refined Grain (oz eq.)", "unit": "oz eq.", "required": True},
                    {"name": "sodium", "label": "钠 (g/day)", "label_en": "Sodium (g/day)", "unit": "g/day", "required": True},
                    {"name": "added_sugar", "label": "添加糖 (%能量)", "label_en": "Added Sugar (% energy)", "unit": "% energy", "required": True},
                    {"name": "saturated_fat", "label": "饱和脂肪 (%能量)", "label_en": "Saturated Fat (% energy)", "unit": "% energy", "required": True},
                ]
            },
        ],
        "output_cols": ["HEI2020_ALL"],
        "max_score": 100,
    },

    "HEI2020_V2": {
        "title": "健康饮食指数 2020 V2 (HEI-2020 V2)",
        "title_en": "Healthy Eating Index 2020 V2",
        "description": "根据每日消耗的食物和营养素分量，计算 HEI2020 膳食指数（健康饮食指数 2020 及 HEI-Toddlers-2020）。与原始 HEI2020 相比，此版本的添加糖以茶匙（tsp）为单位输入，饱和脂肪以克（g）为单位输入，钠以毫克（mg）为单位输入，由系统基于每日总热量自动转换为对应的能量占比百分比，而不是直接使用占总能量的百分比。总分 0-100。",
        "description_en": "Calculate the HEI-2020 dietary index (Healthy Eating Index 2020 and HEI-Toddlers-2020). Unlike the original HEI-2020, added sugar is entered in teaspoons (tsp), saturated fat in grams (g), and sodium in milligrams (mg). The system auto-converts these to energy percentage based on daily total calories. Total score 0-100.",
        "function": "compute_hei2020_v2",
        "extra_params": [
            {"name": "respondent_id", "label": "参与者ID", "label_en": "Respondent ID", "required": True},
            {"name": "age", "label": "年龄 (岁)", "label_en": "Age (years)", "required": True},
        ],
        "groups": [
            {
                "name": "必需参数",
                "name_en": "Required",
                "params": [
                    {"name": "total_kcal", "label": "总能量 (kcal)", "label_en": "Total Energy (kcal)", "unit": "kcal", "required": True},
                    {"name": "total_fruit", "label": "总水果 (cup eq.)", "label_en": "Total Fruit (cup eq.)", "unit": "cup eq.", "required": True},
                    {"name": "whole_fruit", "label": "完整水果 (cup eq.)", "label_en": "Whole Fruit (cup eq.)", "unit": "cup eq.", "required": True},
                    {"name": "total_vegetable", "label": "总蔬菜 (cup eq.)", "label_en": "Total Vegetable (cup eq.)", "unit": "cup eq.", "required": True},
                    {"name": "green_and_bean", "label": "深绿蔬菜+豆类 (cup eq.)", "label_en": "Green & Bean (cup eq.)", "unit": "cup eq.", "required": True},
                    {"name": "total_protein", "label": "总蛋白质 (oz eq.)", "label_en": "Total Protein (oz eq.)", "unit": "oz eq.", "required": True},
                    {"name": "seafood_plant_protein", "label": "海鲜+植物蛋白 (oz eq.)", "label_en": "Seafood & Plant Protein (oz eq.)", "unit": "oz eq.", "required": True},
                    {"name": "whole_grain", "label": "全谷物 (oz eq.)", "label_en": "Whole Grain (oz eq.)", "unit": "oz eq.", "required": True},
                    {"name": "dairy", "label": "乳制品 (cup eq.)", "label_en": "Dairy (cup eq.)", "unit": "cup eq.", "required": True},
                    {"name": "fatty_acid", "label": "脂肪酸比值 (MUFA+PUFA)/SFA", "label_en": "Fatty Acid Ratio", "unit": "ratio", "required": True},
                    {"name": "refined_grain", "label": "精制谷物 (oz eq.)", "label_en": "Refined Grain (oz eq.)", "unit": "oz eq.", "required": True},
                    {"name": "sodium", "label": "钠 (mg)", "label_en": "Sodium (mg)", "unit": "mg", "required": True},
                    {"name": "added_sugar", "label": "添加糖 (tsp)", "label_en": "Added Sugar (tsp)", "unit": "tsp", "required": True},
                    {"name": "saturated_fat", "label": "饱和脂肪 (g)", "label_en": "Saturated Fat (g)", "unit": "g", "required": True},
                ]
            },
        ],
        "output_cols": ["HEI2020_ALL"],
        "max_score": 100,
    },

    "HEI2015": {
        "title": "健康饮食指数 2015 (HEI-2015)",
        "title_en": "Healthy Eating Index 2015",
        "description": "基于 13 个食物组分的密度法评分。添加糖以 tsp 输入，饱和脂肪以 g 输入。总分 0-100。",
        "description_en": "13-component density-based scoring. Added sugar entered as tsp, saturated fat as g. Total score 0-100.",
        "function": "compute_hei2015",
        "extra_params": [
            {"name": "respondent_id", "label": "参与者ID", "label_en": "Respondent ID", "required": True},
        ],
        "groups": [
            {
                "name": "必需参数",
                "name_en": "Required",
                "params": [
                    {"name": "total_kcal", "label": "总能量 (kcal)", "label_en": "Total Energy (kcal)", "unit": "kcal", "required": True},
                    {"name": "total_fruit", "label": "总水果 (cup eq.)", "label_en": "Total Fruit (cup eq.)", "unit": "cup eq.", "required": True},
                    {"name": "whole_fruit", "label": "完整水果 (cup eq.)", "label_en": "Whole Fruit (cup eq.)", "unit": "cup eq.", "required": True},
                    {"name": "total_vegetable", "label": "总蔬菜 (cup eq.)", "label_en": "Total Vegetable (cup eq.)", "unit": "cup eq.", "required": True},
                    {"name": "green_and_bean", "label": "深绿蔬菜+豆类 (cup eq.)", "label_en": "Green & Bean (cup eq.)", "unit": "cup eq.", "required": True},
                    {"name": "total_protein", "label": "总蛋白质 (oz eq.)", "label_en": "Total Protein (oz eq.)", "unit": "oz eq.", "required": True},
                    {"name": "seafood_plant_protein", "label": "海鲜+植物蛋白 (oz eq.)", "label_en": "Seafood & Plant Protein (oz eq.)", "unit": "oz eq.", "required": True},
                    {"name": "whole_grain", "label": "全谷物 (oz eq.)", "label_en": "Whole Grain (oz eq.)", "unit": "oz eq.", "required": True},
                    {"name": "dairy", "label": "乳制品 (cup eq.)", "label_en": "Dairy (cup eq.)", "unit": "cup eq.", "required": True},
                    {"name": "fatty_acid", "label": "脂肪酸比值 (MUFA+PUFA)/SFA", "label_en": "Fatty Acid Ratio", "unit": "ratio", "required": True},
                    {"name": "refined_grain", "label": "精制谷物 (oz eq.)", "label_en": "Refined Grain (oz eq.)", "unit": "oz eq.", "required": True},
                    {"name": "sodium", "label": "钠 (mg)", "label_en": "Sodium (mg)", "unit": "mg", "required": True},
                    {"name": "added_sugar", "label": "添加糖 (tsp)", "label_en": "Added Sugar (tsp)", "unit": "tsp", "required": True},
                    {"name": "saturated_fat", "label": "饱和脂肪 (g)", "label_en": "Saturated Fat (g)", "unit": "g", "required": True},
                ]
            },
        ],
        "output_cols": ["HEI2015_ALL"],
        "max_score": 100,
    },

    "AHEI": {
        "title": "替代健康饮食指数 (AHEI)",
        "title_en": "Alternative Healthy Eating Index",
        "description": "含 11 个组分，支持性别差异处理（全谷物和酒精）。总分 0-110。",
        "description_en": "11 components with sex-specific handling (whole grains and alcohol). Total score 0-110.",
        "function": "compute_ahei",
        "extra_params": [
            {"name": "respondent_id", "label": "参与者ID", "label_en": "Respondent ID", "required": True},
        ],
        "groups": [
            {
                "name": "必需参数",
                "name_en": "Required",
                "params": [
                    {"name": "gender", "label": "性别 (1=男, 2=女)", "label_en": "Gender (1=Male, 2=Female)", "unit": "", "required": True},
                    {"name": "total_kcal", "label": "总能量 (kcal)", "label_en": "Total Energy (kcal)", "unit": "kcal", "required": True},
                    {"name": "vegetable", "label": "蔬菜 (servings/day)", "label_en": "Vegetable (servings/day)", "unit": "servings/day", "required": True},
                    {"name": "fruit", "label": "完整水果 (servings/day)", "label_en": "Whole Fruit (servings/day)", "unit": "servings/day", "required": True},
                    {"name": "whole_grain", "label": "全谷物 (g/day)", "label_en": "Whole Grain (g/day)", "unit": "g/day", "required": True},
                    {"name": "nut_legume", "label": "坚果+豆类 (servings/day)", "label_en": "Nuts & Legumes (servings/day)", "unit": "servings/day", "required": True},
                    {"name": "n3_fat", "label": "Omega-3脂肪酸 (mg/day)", "label_en": "Omega-3 Fatty Acids (mg/day)", "unit": "mg/day", "required": True},
                    {"name": "pufa", "label": "PUFA (%能量)", "label_en": "PUFA (% energy)", "unit": "%", "required": True},
                    {"name": "ssb_fruit_juice", "label": "含糖饮料+果汁 (servings/day)", "label_en": "SSB & Fruit Juice (servings/day)", "unit": "servings/day", "required": True},
                    {"name": "red_processed_meat", "label": "红肉+加工肉 (servings/day)", "label_en": "Red & Processed Meat (servings/day)", "unit": "servings/day", "required": True},
                    {"name": "trans_fat", "label": "反式脂肪 (%能量)", "label_en": "Trans Fat (% energy)", "unit": "%", "required": True},
                    {"name": "sodium", "label": "钠 (mg/day)", "label_en": "Sodium (mg/day)", "unit": "mg/day", "required": True},
                    {"name": "alcohol", "label": "酒精 (drinks/day)", "label_en": "Alcohol (drinks/day)", "unit": "drinks/day", "required": True},
                ]
            },
        ],
        "output_cols": ["AHEI_ALL", "AHEI_NOETOH"],
        "max_score": 110,
    },

    "AHEIP": {
        "title": "替代健康饮食指数-怀孕版 (AHEIP)",
        "title_en": "AHEI for Pregnancy",
        "description": "专门针对孕妇的 9 组分膳食质量评分。总分 0-90。",
        "description_en": "9-component dietary quality score specifically for pregnant women. Total score 0-90.",
        "function": "compute_aheip",
        "extra_params": [
            {"name": "respondent_id", "label": "参与者ID", "label_en": "Respondent ID", "required": True},
        ],
        "groups": [
            {
                "name": "必需参数",
                "name_en": "Required",
                "params": [
                    {"name": "vegetable", "label": "蔬菜 (servings/day)", "label_en": "Vegetable (servings/day)", "unit": "servings/day", "required": True},
                    {"name": "fruit", "label": "完整水果 (servings/day)", "label_en": "Whole Fruit (servings/day)", "unit": "servings/day", "required": True},
                    {"name": "white_red_ratio", "label": "白肉/红肉比值", "label_en": "White/Red Meat Ratio", "unit": "ratio", "required": True},
                    {"name": "fiber", "label": "膳食纤维 (g/day)", "label_en": "Fiber (g/day)", "unit": "g/day", "required": True},
                    {"name": "trans_fat", "label": "反式脂肪 (%能量)", "label_en": "Trans Fat (% energy)", "unit": "%", "required": True},
                    {"name": "poly_sat_ratio", "label": "PUFA/SFA 比值", "label_en": "PUFA/SFA Ratio", "unit": "ratio", "required": True},
                    {"name": "calcium", "label": "钙 (mg/day)", "label_en": "Calcium (mg/day)", "unit": "mg/day", "required": True},
                    {"name": "folate", "label": "叶酸 (μg/day)", "label_en": "Folate (μg/day)", "unit": "μg/day", "required": True},
                    {"name": "iron", "label": "铁 (mg/day)", "label_en": "Iron (mg/day)", "unit": "mg/day", "required": True},
                ]
            },
        ],
        "output_cols": ["AHEIP_ALL"],
        "max_score": 90,
    },

    "PHDI": {
        "title": "行星健康饮食指数 (PHDI)",
        "title_en": "Planetary Health Diet Index",
        "description": "基于 EAT-Lancet 报告，含 15 个组分。支持性别差异（全谷物）。总分 0-140。",
        "description_en": "Based on the EAT-Lancet report with 15 components. Supports sex-specific handling (whole grains). Total score 0-140.",
        "function": "compute_phdi",
        "extra_params": [
            {"name": "respondent_id", "label": "参与者ID", "label_en": "Respondent ID", "required": True},
            {"name": "gender", "label": "性别 (1=男, 2=女)", "label_en": "Gender (1=Male, 2=Female)", "unit": "", "required": True},
            {"name": "total_kcal", "label": "总能量 (kcal)", "label_en": "Total Energy (kcal)", "unit": "kcal", "required": True},
        ],
        "groups": [
            {
                "name": "必需参数",
                "name_en": "Required",
                "params": [
                    {"name": "whole_grain", "label": "全谷物 (g/day)", "label_en": "Whole Grain (g/day)", "unit": "g/day", "required": True},
                    {"name": "starchy_veg", "label": "淀粉类蔬菜 (g/day)", "label_en": "Starchy Vegetable (g/day)", "unit": "g/day", "required": True},
                    {"name": "vegetable", "label": "蔬菜 (g/day)", "label_en": "Vegetable (g/day)", "unit": "g/day", "required": True},
                    {"name": "fruit", "label": "水果 (g/day)", "label_en": "Fruit (g/day)", "unit": "g/day", "required": True},
                    {"name": "dairy", "label": "乳制品 (g/day)", "label_en": "Dairy (g/day)", "unit": "g/day", "required": True},
                    {"name": "red_processed_meat", "label": "红肉+加工肉 (g/day)", "label_en": "Red & Processed Meat (g/day)", "unit": "g/day", "required": True},
                    {"name": "poultry", "label": "禽肉 (g/day)", "label_en": "Poultry (g/day)", "unit": "g/day", "required": True},
                    {"name": "egg", "label": "鸡蛋 (g/day)", "label_en": "Egg (g/day)", "unit": "g/day", "required": True},
                    {"name": "fish", "label": "鱼类 (g/day)", "label_en": "Fish (g/day)", "unit": "g/day", "required": True},
                    {"name": "nuts", "label": "坚果 (g/day)", "label_en": "Nuts (g/day)", "unit": "g/day", "required": True},
                    {"name": "legumes", "label": "豆类 (g/day)", "label_en": "Legumes (g/day)", "unit": "g/day", "required": True},
                    {"name": "soy", "label": "大豆制品 (g/day)", "label_en": "Soy Products (g/day)", "unit": "g/day", "required": True},
                    {"name": "added_fat_unsat", "label": "添加不饱和脂肪 (%kcal)", "label_en": "Added Unsaturated Fat (%kcal)", "unit": "%kcal", "required": True},
                    {"name": "added_fat_sat_trans", "label": "添加饱和+反式脂肪 (%kcal)", "label_en": "Added Saturated & Trans Fat (%kcal)", "unit": "%kcal", "required": True},
                    {"name": "added_sugar", "label": "添加糖 (%kcal)", "label_en": "Added Sugar (%kcal)", "unit": "%kcal", "required": True},
                ]
            },
        ],
        "output_cols": ["PHDI_ALL"],
        "max_score": 140,
    },

    "PHDI_V1": {
        "title": "行星健康饮食指数 V1 (PHDI V1)",
        "title_en": "Planetary Health Diet Index V1",
        "description": "根据每日消耗的食物和营养素分量计算行星健康饮食指数（PHDI），用于评估对 EAT-Lancet 报告中参考膳食的依从性。在此版本（V1）中，添加不饱和脂肪、添加饱和与反式脂肪、添加糖三个组分以占每日总能量的百分比（% kcal）直接输入。总分 0-140。",
        "description_en": "Calculate the Planetary Health Diet Index (PHDI) based on daily food and nutrient intake to assess adherence to the EAT-Lancet reference diet. In V1, added unsaturated fats, added saturated & trans fats, and added sugars are entered as percentage of daily energy (% kcal). Total score 0-140.",
        "function": "compute_phdi",
        "extra_params": [
            {"name": "respondent_id", "label": "参与者ID", "label_en": "Respondent ID", "required": True},
            {"name": "gender", "label": "性别 (1=男, 2=女)", "label_en": "Gender (1=Male, 2=Female)", "unit": "", "required": True},
            {"name": "total_kcal", "label": "总能量 (kcal)", "label_en": "Total Energy (kcal)", "unit": "kcal", "required": True},
        ],
        "groups": [
            {
                "name": "必需参数",
                "name_en": "Required",
                "params": [
                    {"name": "whole_grain", "label": "全谷物 (g/day)", "label_en": "Whole Grain (g/day)", "unit": "g/day", "required": True},
                    {"name": "starchy_veg", "label": "淀粉类蔬菜 (g/day)", "label_en": "Starchy Vegetable (g/day)", "unit": "g/day", "required": True},
                    {"name": "vegetable", "label": "蔬菜 (g/day)", "label_en": "Vegetable (g/day)", "unit": "g/day", "required": True},
                    {"name": "fruit", "label": "水果 (g/day)", "label_en": "Fruit (g/day)", "unit": "g/day", "required": True},
                    {"name": "dairy", "label": "乳制品 (g/day)", "label_en": "Dairy (g/day)", "unit": "g/day", "required": True},
                    {"name": "red_processed_meat", "label": "红肉+加工肉 (g/day)", "label_en": "Red & Processed Meat (g/day)", "unit": "g/day", "required": True},
                    {"name": "poultry", "label": "禽肉 (g/day)", "label_en": "Poultry (g/day)", "unit": "g/day", "required": True},
                    {"name": "egg", "label": "鸡蛋 (g/day)", "label_en": "Egg (g/day)", "unit": "g/day", "required": True},
                    {"name": "fish", "label": "鱼类 (g/day)", "label_en": "Fish (g/day)", "unit": "g/day", "required": True},
                    {"name": "nuts", "label": "坚果 (g/day)", "label_en": "Nuts (g/day)", "unit": "g/day", "required": True},
                    {"name": "legumes", "label": "豆类 (g/day)", "label_en": "Legumes (g/day)", "unit": "g/day", "required": True},
                    {"name": "soy", "label": "大豆制品 (g/day)", "label_en": "Soy Products (g/day)", "unit": "g/day", "required": True},
                    {"name": "added_fat_unsat", "label": "添加不饱和脂肪 (%kcal)", "label_en": "Added Unsaturated Fat (%kcal)", "unit": "%kcal", "required": True},
                    {"name": "added_fat_sat_trans", "label": "添加饱和+反式脂肪 (%kcal)", "label_en": "Added Saturated & Trans Fat (%kcal)", "unit": "%kcal", "required": True},
                    {"name": "added_sugar", "label": "添加糖 (%kcal)", "label_en": "Added Sugar (%kcal)", "unit": "%kcal", "required": True},
                ]
            },
        ],
        "output_cols": ["PHDI_ALL"],
        "max_score": 140,
    },

    "PHDI_V2": {
        "title": "行星健康饮食指数 V2 (PHDI V2)",
        "title_en": "Planetary Health Diet Index V2",
        "description": "根据每日消耗的食物和营养素分量计算行星健康饮食指数（PHDI），该指数可量化对 EAT-Lancet 报告中参考膳食的依从性。与 V1 不同，此版本（V2）中所有的添加不饱和脂肪、添加饱和及反式脂肪、添加糖变量均直接以每日摄入克数（g/day）为单位进行输入，系统会自动根据每日总能量（TOTALKCAL_PHDI）将其换算为能量占比百分比（% kcal）。总分 0-140。",
        "description_en": "Calculate the Planetary Health Diet Index (PHDI) quantifying adherence to the EAT-Lancet reference diet. Unlike V1, V2 accepts added unsaturated fats, added saturated & trans fats, and added sugars directly in grams/day (g/day). The system auto-converts to energy percentage (% kcal) based on total energy (TOTALKCAL_PHDI). Total score 0-140.",
        "function": "compute_phdi_v2",
        "extra_params": [
            {"name": "respondent_id", "label": "参与者ID", "label_en": "Respondent ID", "required": True},
            {"name": "gender", "label": "性别 (1=男, 2=女)", "label_en": "Gender (1=Male, 2=Female)", "unit": "", "required": True},
            {"name": "total_kcal", "label": "总能量 (kcal)", "label_en": "Total Energy (kcal)", "unit": "kcal", "required": True},
        ],
        "groups": [
            {
                "name": "必需参数",
                "name_en": "Required",
                "params": [
                    {"name": "whole_grain", "label": "全谷物 (g/day)", "label_en": "Whole Grain (g/day)", "unit": "g/day", "required": True},
                    {"name": "starchy_veg", "label": "淀粉类蔬菜 (g/day)", "label_en": "Starchy Vegetable (g/day)", "unit": "g/day", "required": True},
                    {"name": "vegetable", "label": "蔬菜 (g/day)", "label_en": "Vegetable (g/day)", "unit": "g/day", "required": True},
                    {"name": "fruit", "label": "水果 (g/day)", "label_en": "Fruit (g/day)", "unit": "g/day", "required": True},
                    {"name": "dairy", "label": "乳制品 (g/day)", "label_en": "Dairy (g/day)", "unit": "g/day", "required": True},
                    {"name": "red_processed_meat", "label": "红肉+加工肉 (g/day)", "label_en": "Red & Processed Meat (g/day)", "unit": "g/day", "required": True},
                    {"name": "poultry", "label": "禽肉 (g/day)", "label_en": "Poultry (g/day)", "unit": "g/day", "required": True},
                    {"name": "egg", "label": "鸡蛋 (g/day)", "label_en": "Egg (g/day)", "unit": "g/day", "required": True},
                    {"name": "fish", "label": "鱼类 (g/day)", "label_en": "Fish (g/day)", "unit": "g/day", "required": True},
                    {"name": "nuts", "label": "坚果 (g/day)", "label_en": "Nuts (g/day)", "unit": "g/day", "required": True},
                    {"name": "legumes", "label": "豆类 (g/day)", "label_en": "Legumes (g/day)", "unit": "g/day", "required": True},
                    {"name": "soy", "label": "大豆制品 (g/day)", "label_en": "Soy Products (g/day)", "unit": "g/day", "required": True},
                    {"name": "added_fat_unsat", "label": "添加不饱和脂肪 (g/day)", "label_en": "Added Unsaturated Fat (g/day)", "unit": "g/day", "required": True},
                    {"name": "added_fat_sat_trans", "label": "添加饱和+反式脂肪 (g/day)", "label_en": "Added Saturated & Trans Fat (g/day)", "unit": "g/day", "required": True},
                    {"name": "added_sugar", "label": "添加糖 (g/day)", "label_en": "Added Sugar (g/day)", "unit": "g/day", "required": True},
                ]
            },
        ],
        "output_cols": ["PHDI_ALL"],
        "max_score": 140,
    },

    "DASH": {
        "title": "DASH 饮食指数",
        "title_en": "DASH Diet Index",
        "description": "8 个组分，基于人群五等分排名评分。总分 8-40。",
        "description_en": "8 components, population-based quintile ranking. Total score 8-40.",
        "function": "compute_dash",
        "extra_params": [
            {"name": "respondent_id", "label": "参与者ID", "label_en": "Respondent ID", "required": True},
        ],
        "groups": [
            {
                "name": "必需参数",
                "name_en": "Required",
                "params": [
                    {"name": "total_kcal", "label": "总能量 (kcal)", "label_en": "Total Energy (kcal)", "unit": "kcal", "required": True},
                    {"name": "fruit_fruit_juice", "label": "水果+100%果汁 (servings/day)", "label_en": "Fruit & Juice (servings/day)", "unit": "servings/day", "required": True},
                    {"name": "vegetable", "label": "蔬菜 (servings/day)", "label_en": "Vegetable (servings/day)", "unit": "servings/day", "required": True},
                    {"name": "nut_legume", "label": "坚果+豆类 (servings/day)", "label_en": "Nuts & Legumes (servings/day)", "unit": "servings/day", "required": True},
                    {"name": "whole_grain", "label": "全谷物 (oz)", "label_en": "Whole Grain (oz)", "unit": "oz", "required": True},
                    {"name": "low_fat_dairy", "label": "低脂乳制品 (servings/day)", "label_en": "Low-fat Dairy (servings/day)", "unit": "servings/day", "required": True},
                    {"name": "sodium", "label": "钠 (mg/day)", "label_en": "Sodium (mg/day)", "unit": "mg/day", "required": True},
                    {"name": "red_processed_meat", "label": "红肉+加工肉 (servings/day)", "label_en": "Red & Processed Meat (servings/day)", "unit": "servings/day", "required": True},
                    {"name": "ssb_fruit_juice", "label": "含糖饮料 (servings/day)", "label_en": "SSB (servings/day)", "unit": "servings/day", "required": True},
                ]
            },
        ],
        "output_cols": ["DASH_ALL"],
        "max_score": 40,
    },

    "DASHI": {
        "title": "DASHI 饮食指数（营养密度版）",
        "title_en": "DASHI (Nutrient-based)",
        "description": "9 个营养素组分，线性评分。总分 0-9。",
        "description_en": "9 nutrient components, linear scoring. Total score 0-9.",
        "function": "compute_dashi",
        "extra_params": [
            {"name": "respondent_id", "label": "参与者ID", "label_en": "Respondent ID", "required": True},
        ],
        "groups": [
            {
                "name": "必需参数",
                "name_en": "Required",
                "params": [
                    {"name": "total_kcal", "label": "总能量 (kcal)", "label_en": "Total Energy (kcal)", "unit": "kcal", "required": True},
                    {"name": "total_fat_pct", "label": "总脂肪 (%kcal)", "label_en": "Total Fat (%kcal)", "unit": "%kcal", "required": True},
                    {"name": "sat_fat_pct", "label": "饱和脂肪 (%kcal)", "label_en": "Saturated Fat (%kcal)", "unit": "%kcal", "required": True},
                    {"name": "protein_pct", "label": "蛋白质 (%kcal)", "label_en": "Protein (%kcal)", "unit": "%kcal", "required": True},
                    {"name": "cholesterol", "label": "胆固醇 (mg/2000kcal)", "label_en": "Cholesterol (mg/2000kcal)", "unit": "mg/2000kcal", "required": True},
                    {"name": "fiber", "label": "纤维 (g/2000kcal)", "label_en": "Fiber (g/2000kcal)", "unit": "g/2000kcal", "required": True},
                    {"name": "potassium", "label": "钾 (mg/2000kcal)", "label_en": "Potassium (mg/2000kcal)", "unit": "mg/2000kcal", "required": True},
                    {"name": "magnesium", "label": "镁 (mg/2000kcal)", "label_en": "Magnesium (mg/2000kcal)", "unit": "mg/2000kcal", "required": True},
                    {"name": "calcium", "label": "钙 (mg/2000kcal)", "label_en": "Calcium (mg/2000kcal)", "unit": "mg/2000kcal", "required": True},
                    {"name": "sodium", "label": "钠 (mg/2000kcal)", "label_en": "Sodium (mg/2000kcal)", "unit": "mg/2000kcal", "required": True},
                ]
            },
        ],
        "output_cols": ["DASHI_ALL"],
        "max_score": 9,
    },

    "MED": {
        "title": "地中海饮食指数 (MED)",
        "title_en": "Mediterranean Diet Index",
        "description": "9 个组分，基于中位数排名评分。总分 0-9。",
        "description_en": "9 components, median-based ranking. Total score 0-9.",
        "function": "compute_med",
        "extra_params": [
            {"name": "respondent_id", "label": "参与者ID", "label_en": "Respondent ID", "required": True},
        ],
        "groups": [
            {
                "name": "必需参数",
                "name_en": "Required",
                "params": [
                    {"name": "fruit_fruit_juice", "label": "水果+果汁 (servings/day)", "label_en": "Fruit & Juice (servings/day)", "unit": "servings/day", "required": True},
                    {"name": "vegetable", "label": "蔬菜 (servings/day)", "label_en": "Vegetable (servings/day)", "unit": "servings/day", "required": True},
                    {"name": "whole_grain", "label": "全谷物 (oz)", "label_en": "Whole Grain (oz)", "unit": "oz", "required": True},
                    {"name": "legumes", "label": "豆类 (oz)", "label_en": "Legumes (oz)", "unit": "oz", "required": True},
                    {"name": "nuts", "label": "坚果 (oz)", "label_en": "Nuts (oz)", "unit": "oz", "required": True},
                    {"name": "fish", "label": "鱼类 (4oz)", "label_en": "Fish (4oz)", "unit": "4oz", "required": True},
                    {"name": "red_processed_meat", "label": "红肉+加工肉 (servings)", "label_en": "Red & Processed Meat (servings)", "unit": "servings", "required": True},
                    {"name": "mon_sat_fat_ratio", "label": "MUFA/SFA 比值", "label_en": "MUFA/SFA Ratio", "unit": "ratio", "required": True},
                    {"name": "alcohol", "label": "酒精 (13g)", "label_en": "Alcohol (13g)", "unit": "13g", "required": True},
                ]
            },
        ],
        "output_cols": ["MED_ALL", "MED_NOETOH"],
        "max_score": 9,
    },

    "MEDI": {
        "title": "MEDI 地中海饮食指数（改进版）",
        "title_en": "MEDI (PREDIMED-based)",
        "description": "基于 PREDIMED 试验的 11 个组分绝对阈值评分。总分 0-11。",
        "description_en": "11-component absolute threshold scoring based on the PREDIMED trial. Total score 0-11.",
        "function": "compute_medi",
        "extra_params": [
            {"name": "respondent_id", "label": "参与者ID", "label_en": "Respondent ID", "required": True},
        ],
        "groups": [
            {
                "name": "必需参数",
                "name_en": "Required",
                "params": [
                    {"name": "olive_oil", "label": "橄榄油 (10g/份)", "label_en": "Olive Oil (10g/serving)", "unit": "servings", "required": True},
                    {"name": "fruit", "label": "水果 (125g/份)", "label_en": "Fruit (125g/serving)", "unit": "servings", "required": True},
                    {"name": "vegetable", "label": "蔬菜 (125g/份)", "label_en": "Vegetable (125g/serving)", "unit": "servings", "required": True},
                    {"name": "legumes", "label": "豆类 (40g/份)", "label_en": "Legumes (40g/serving)", "unit": "servings", "required": True},
                    {"name": "nuts", "label": "坚果 (25g/份)", "label_en": "Nuts (25g/serving)", "unit": "servings", "required": True},
                    {"name": "fish_seafood", "label": "鱼类海鲜 (125g/份)", "label_en": "Fish & Seafood (125g/serving)", "unit": "servings", "required": True},
                    {"name": "alcohol", "label": "酒精 (14g/份)", "label_en": "Alcohol (14g/serving)", "unit": "servings", "required": True},
                    {"name": "ssb", "label": "含糖饮料 (240mL/份)", "label_en": "SSB (240mL/serving)", "unit": "servings", "required": True},
                    {"name": "sweets", "label": "甜食 (50g/份)", "label_en": "Sweets (50g/serving)", "unit": "servings", "required": True},
                    {"name": "discret_fat", "label": "添加脂肪 (10g/份)", "label_en": "Discretionary Fat (10g/serving)", "unit": "servings", "required": True},
                    {"name": "red_processed_meat", "label": "红肉+加工肉 (150g/份)", "label_en": "Red & Processed Meat (150g/serving)", "unit": "servings", "required": True},
                ]
            },
        ],
        "output_cols": ["MEDI_ALL", "MEDI_NOETOH"],
        "max_score": 11,
    },

    "MEDI_V1": {
        "title": "MEDI 地中海饮食指数 V1 (二分评分)",
        "title_en": "MEDI V1 (PREDIMED-based, Binary)",
        "description_en": "Calculate the MEDI (Mediterranean Diet Index) based on daily food and nutrient intake, using serving-based 0/1 binary scoring. Each of the 11 components receives 1 point if it meets the recommended threshold, 0 otherwise. Total score ranges from 0-11 (or 0-10 without alcohol).<br><br><b>Component serving sizes and thresholds:</b><br>1. Olive Oil: ≥5 servings/day (1 serving = 10 g or 0.8 tbsp)<br>2. Whole Fruit: ≥3 servings/day (1 serving = 125 g)<br>3. Vegetables (excluding potatoes & legumes): ≥2 servings/day (1 serving = 125 g)<br>4. Legumes: ≥3/7 servings/day (1 serving = 40 g)<br>5. Nuts & Seeds: ≥3/7 servings/day (1 serving = 25 g)<br>6. Fish & Seafood: ≥3/7 servings/day (1 serving = 125 g)<br>7. Alcohol: ≥1 serving/day (1 serving = 14 g pure alcohol)<br>8. SSBs (limit): <1 serving/day (1 serving = 240 mL/cup)<br>9. Sweets (limit): <2/7 servings/day (1 serving = 50 g)<br>10. Discretionary Fat (limit): <1 serving/day (1 serving = 10 g)<br>11. Red & Processed Meat (limit): <1 serving/day (1 serving = 150 g)",
        "description": "根据每日消耗的食物和营养素分量，计算 MEDI 地中海膳食指数（基于摄入分量和 0/1 二分评分）。每个组分（共11个）若达到设定的推荐阈值则得 1 分，否则得 0 分。总分范围 0-11 分（或不含酒精版 0-10 分）。<br><br><b>具体组分分量及推荐阈值：</b><br>1. 橄榄油：≥5 份/天 (1 份 = 10 g 或 0.8 汤匙)<br>2. 完整水果：≥3 份/天 (1 份 = 125 g)<br>3. 蔬菜（除土豆和豆类）：≥2 份/天 (1 份 = 125 g)<br>4. 豆类：≥3/7 份/天 (1 份 = 40 g)<br>5. 坚果和种子：≥3/7 份/天 (1 份 = 25 g)<br>6. 鱼类和海鲜：≥3/7 份/天 (1 份 = 125 g)<br>7. 酒精：≥1 份/天 (1 份 = 14 g 纯酒精)<br>8. 含糖饮料（限制）：&lt;1 份/天 (1 份 = 240 mL/杯)<br>9. 甜食（限制）：&lt;2/7 份/天 (1 份 = 50 g)<br>10. 添加脂肪（限制）：&lt;1 份/天 (1 份 = 10 g)<br>11. 红肉和加工肉（限制）：&lt;1 份/天 (1 份 = 150 g)",
        "function": "compute_medi",
        "extra_params": [
            {"name": "respondent_id", "label": "参与者ID", "label_en": "Respondent ID", "required": True},
        ],
        "groups": [
            {
                "name": "必需参数",
                "name_en": "Required",
                "params": [
                    {"name": "olive_oil", "label": "橄榄油 (10g/份)", "label_en": "Olive Oil (10g/serving)", "unit": "servings", "required": True},
                    {"name": "fruit", "label": "水果 (125g/份)", "label_en": "Fruit (125g/serving)", "unit": "servings", "required": True},
                    {"name": "vegetable", "label": "蔬菜 (125g/份)", "label_en": "Vegetable (125g/serving)", "unit": "servings", "required": True},
                    {"name": "legumes", "label": "豆类 (40g/份)", "label_en": "Legumes (40g/serving)", "unit": "servings", "required": True},
                    {"name": "nuts", "label": "坚果 (25g/份)", "label_en": "Nuts (25g/serving)", "unit": "servings", "required": True},
                    {"name": "fish_seafood", "label": "鱼类海鲜 (125g/份)", "label_en": "Fish & Seafood (125g/serving)", "unit": "servings", "required": True},
                    {"name": "alcohol", "label": "酒精 (14g/份)", "label_en": "Alcohol (14g/serving)", "unit": "servings", "required": True},
                    {"name": "ssb", "label": "含糖饮料 (240mL/份)", "label_en": "SSB (240mL/serving)", "unit": "servings", "required": True},
                    {"name": "sweets", "label": "甜食 (50g/份)", "label_en": "Sweets (50g/serving)", "unit": "servings", "required": True},
                    {"name": "discret_fat", "label": "添加脂肪 (10g/份)", "label_en": "Discretionary Fat (10g/serving)", "unit": "servings", "required": True},
                    {"name": "red_processed_meat", "label": "红肉+加工肉 (150g/份)", "label_en": "Red & Processed Meat (150g/serving)", "unit": "servings", "required": True},
                ]
            },
        ],
        "output_cols": ["MEDI_ALL", "MEDI_NOETOH"],
        "max_score": 11,
    },

    "MEDI_V2": {
        "title": "MEDI 地中海饮食指数 V2 (连续评分)",
        "title_en": "MEDI V2 (PREDIMED-based, Continuous)",
        "description": "根据每日消耗的食物和营养素分量，计算 MEDI_V2 地中海膳食指数（基于摄入分量和 0-5 分连续插值评分）。与 V1 的 0/1 二分评分不同，此版本每个组分的得分在最小和最大推荐阈值之间进行连续的线性插值计算，得分范围在 0 至 5 分之间。总分范围 0-55 分（或不含酒精版 0-50 分）。<br><br><b>具体组分分量及评分区间（最小 0 分 ~ 最大 5 分）：</b><br>1. 橄榄油：0 ~ 5 份/天 (1 份 = 10 g 或 0.8 汤匙)<br>2. 完整水果：0 ~ 3 份/天 (1 份 = 125 g)<br>3. 蔬菜（除土豆和豆类）：0 ~ 2 份/天 (1 份 = 125 g)<br>4. 豆类：0 ~ 3/7 份/天 (1 份 = 40 g)<br>5. 坚果和种子：0 ~ 3/7 份/天 (1 份 = 25 g)<br>6. 鱼类和海鲜：0 ~ 3/7 份/天 (1 份 = 125 g)<br>7. 酒精：0 ~ 1 份/天 (1 份 = 14 g 纯酒精)<br>8. 含糖饮料（反向评分）：1 ~ 0 份/天 (1 份 = 240 mL/杯)<br>9. 甜食（反向评分）：2/7 ~ 0 份/天 (1 份 = 50 g)<br>10. 添加脂肪（反向评分）：1 ~ 0 份/天 (1 份 = 10 g)<br>11. 红肉和加工肉（反向评分）：1 ~ 0 份/天 (1 份 = 150 g)",
        "description_en": "Calculate the MEDI V2 (Mediterranean Diet Index) using continuous 0-5 scoring with linear interpolation between minimum and maximum thresholds, based on daily food and nutrient intake. Unlike V1\'s 0/1 binary scoring, this version assigns scores from 0 to 5 per component via continuous linear interpolation. Total score ranges from 0-55 (or 0-50 without alcohol).<br><br><b>Component serving sizes and scoring ranges (Min 0 pts ~ Max 5 pts):</b><br>1. Olive Oil: 0 ~ 5 servings/day (1 serving = 10 g or 0.8 tbsp)<br>2. Whole Fruit: 0 ~ 3 servings/day (1 serving = 125 g)<br>3. Vegetables (excluding potatoes & legumes): 0 ~ 2 servings/day (1 serving = 125 g)<br>4. Legumes: 0 ~ 3/7 servings/day (1 serving = 40 g)<br>5. Nuts & Seeds: 0 ~ 3/7 servings/day (1 serving = 25 g)<br>6. Fish & Seafood: 0 ~ 3/7 servings/day (1 serving = 125 g)<br>7. Alcohol: 0 ~ 1 serving/day (1 serving = 14 g pure alcohol)<br>8. SSBs (reverse scored): 1 ~ 0 servings/day (1 serving = 240 mL/cup)<br>9. Sweets (reverse scored): 2/7 ~ 0 servings/day (1 serving = 50 g)<br>10. Discretionary Fat (reverse scored): 1 ~ 0 servings/day (1 serving = 10 g)<br>11. Red & Processed Meat (reverse scored): 1 ~ 0 servings/day (1 serving = 150 g)",
        "function": "compute_medi_v2",
        "extra_params": [
            {"name": "respondent_id", "label": "参与者ID", "label_en": "Respondent ID", "required": True},
        ],
        "groups": [
            {
                "name": "必需参数",
                "name_en": "Required",
                "params": [
                    {"name": "olive_oil", "label": "橄榄油 (10g/份)", "label_en": "Olive Oil (10g/serving)", "unit": "servings", "required": True},
                    {"name": "fruit", "label": "水果 (125g/份)", "label_en": "Fruit (125g/serving)", "unit": "servings", "required": True},
                    {"name": "vegetable", "label": "蔬菜 (125g/份)", "label_en": "Vegetable (125g/serving)", "unit": "servings", "required": True},
                    {"name": "legumes", "label": "豆类 (40g/份)", "label_en": "Legumes (40g/serving)", "unit": "servings", "required": True},
                    {"name": "nuts", "label": "坚果 (25g/份)", "label_en": "Nuts (25g/serving)", "unit": "servings", "required": True},
                    {"name": "fish_seafood", "label": "鱼类海鲜 (125g/份)", "label_en": "Fish & Seafood (125g/serving)", "unit": "servings", "required": True},
                    {"name": "alcohol", "label": "酒精 (14g/份)", "label_en": "Alcohol (14g/serving)", "unit": "servings", "required": True},
                    {"name": "ssb", "label": "含糖饮料 (240mL/份)", "label_en": "SSB (240mL/serving)", "unit": "servings", "required": True},
                    {"name": "sweets", "label": "甜食 (50g/份)", "label_en": "Sweets (50g/serving)", "unit": "servings", "required": True},
                    {"name": "discret_fat", "label": "添加脂肪 (10g/份)", "label_en": "Discretionary Fat (10g/serving)", "unit": "servings", "required": True},
                    {"name": "red_processed_meat", "label": "红肉+加工肉 (150g/份)", "label_en": "Red & Processed Meat (150g/serving)", "unit": "servings", "required": True},
                ]
            },
        ],
        "output_cols": ["MEDI_V2_ALL", "MEDI_V2_NOETOH"],
        "max_score": 55,
    },

    "ACS2020": {
        "title": "ACS 2020 癌症协会饮食指数",
        "title_en": "ACS 2020 Cancer Society Index",
        "description": "8 个组分，性别分层四等分评分。总分 0-12。",
        "description_en": "8 components, sex-stratified quartile scoring. Total score 0-12.",
        "function": "compute_acs2020_v1",
        "extra_params": [
            {"name": "respondent_id", "label": "参与者ID", "label_en": "Respondent ID", "required": True},
            {"name": "gender", "label": "性别 (1=男, 2=女)", "label_en": "Gender (1=Male, 2=Female)", "unit": "", "required": True},
        ],
        "groups": [
            {
                "name": "必需参数",
                "name_en": "Required",
                "params": [
                    {"name": "vegetable", "label": "蔬菜 (servings/day)", "label_en": "Vegetable (servings/day)", "unit": "servings/day", "required": True},
                    {"name": "vegetable_items", "label": "蔬菜种类数", "label_en": "Vegetable Variety (items)", "unit": "items", "required": True},
                    {"name": "fruit", "label": "完整水果 (servings/day)", "label_en": "Whole Fruit (servings/day)", "unit": "servings/day", "required": True},
                    {"name": "fruit_items", "label": "水果种类数", "label_en": "Fruit Variety (items)", "unit": "items", "required": True},
                    {"name": "whole_grain", "label": "全谷物 (g/day)", "label_en": "Whole Grain (g/day)", "unit": "g/day", "required": True},
                    {"name": "red_processed_meat", "label": "红肉+加工肉 (servings/day)", "label_en": "Red & Processed Meat (servings/day)", "unit": "servings/day", "required": True},
                    {"name": "hpf_rg_ratio", "label": "高加工食品+精制谷物 (%kcal)", "label_en": "HPF & Refined Grain (%kcal)", "unit": "%kcal", "required": True},
                    {"name": "ssb_fruit_juice", "label": "含糖饮料 (servings/day)", "label_en": "SSB (servings/day)", "unit": "servings/day", "required": True},
                ]
            },
        ],
        "output_cols": ["ACS2020_V1_ALL"],
        "max_score": 12,
    },

    "ACS2020_V1": {
        "title": "ACS 2020 癌症协会饮食指数 V1",
        "title_en": "ACS 2020 Cancer Society Index V1",
        "description": "根据每日消耗的食物肉类及能量比例，计算美国癌症协会 2020 膳食指数（ACS 2020），评估蔬菜、水果、全谷物、红肉及加工肉类、含糖饮料组分。此版本使用高加工食品和精制谷物占每日总能量的百分比（% kcal）来计算该组分评分，是官方推荐首选的 ACS 2020 膳食评分计算方法。总分 0-12。",
        "description_en": "Calculate the ACS 2020 Dietary Index based on daily food and energy intake, assessing vegetables, fruits, whole grains, red & processed meat, and SSBs. This version uses highly processed foods and refined grains as percentage of daily energy (% kcal) — the officially recommended ACS 2020 scoring method. Total score 0-12.",
        "function": "compute_acs2020_v1",
        "extra_params": [
            {"name": "respondent_id", "label": "参与者ID", "label_en": "Respondent ID", "required": True},
            {"name": "gender", "label": "性别 (1=男, 2=女)", "label_en": "Gender (1=Male, 2=Female)", "unit": "", "required": True},
        ],
        "groups": [
            {
                "name": "必需参数",
                "name_en": "Required",
                "params": [
                    {"name": "vegetable", "label": "蔬菜 (servings/day)", "label_en": "Vegetable (servings/day)", "unit": "servings/day", "required": True},
                    {"name": "vegetable_items", "label": "蔬菜种类数", "label_en": "Vegetable Variety (items)", "unit": "items", "required": True},
                    {"name": "fruit", "label": "完整水果 (servings/day)", "label_en": "Whole Fruit (servings/day)", "unit": "servings/day", "required": True},
                    {"name": "fruit_items", "label": "水果种类数", "label_en": "Fruit Variety (items)", "unit": "items", "required": True},
                    {"name": "whole_grain", "label": "全谷物 (g/day)", "label_en": "Whole Grain (g/day)", "unit": "g/day", "required": True},
                    {"name": "red_processed_meat", "label": "红肉+加工肉 (servings/day)", "label_en": "Red & Processed Meat (servings/day)", "unit": "servings/day", "required": True},
                    {"name": "hpf_rg_ratio", "label": "高加工食品+精制谷物 (%kcal)", "label_en": "HPF & Refined Grain (%kcal)", "unit": "%kcal", "required": True},
                    {"name": "ssb_fruit_juice", "label": "含糖饮料 (servings/day)", "label_en": "SSB (servings/day)", "unit": "servings/day", "required": True},
                ]
            },
        ],
        "output_cols": ["ACS2020_V1_ALL"],
        "max_score": 12,
    },

    "ACS2020_V2": {
        "title": "ACS 2020 癌症协会饮食指数 V2",
        "title_en": "ACS 2020 Cancer Society Index V2",
        "description": "根据每日消耗的食物和营养素分量，计算美国癌症协会 2020 膳食指数版本 2（ACS 2020 V2）。与 V1 使用能量占比不同，此版本的高加工食品和精制谷物组分使用每 1000 kcal 每日消耗的份数（servings/d per 1000 kcal）进行计算，并使用总热量进行标准化。总分 0-12。",
        "description_en": "Calculate the ACS 2020 Dietary Index V2 based on daily food and nutrient intake. Unlike V1 which uses energy percentage, V2 computes highly processed foods and refined grains as servings per 1000 kcal, standardized by total energy. Total score 0-12.",
        "function": "compute_acs2020_v2",
        "extra_params": [
            {"name": "respondent_id", "label": "参与者ID", "label_en": "Respondent ID", "required": True},
            {"name": "gender", "label": "性别 (1=男, 2=女)", "label_en": "Gender (1=Male, 2=Female)", "unit": "", "required": True},
            {"name": "total_kcal", "label": "总能量 (kcal/day)", "label_en": "Total Energy (kcal/day)", "required": True},
        ],
        "groups": [
            {
                "name": "必需参数",
                "name_en": "Required",
                "params": [
                    {"name": "vegetable", "label": "蔬菜 (servings/day)", "label_en": "Vegetable (servings/day)", "unit": "servings/day", "required": True},
                    {"name": "vegetable_items", "label": "蔬菜种类数", "label_en": "Vegetable Variety (items)", "unit": "items", "required": True},
                    {"name": "fruit", "label": "完整水果 (servings/day)", "label_en": "Whole Fruit (servings/day)", "unit": "servings/day", "required": True},
                    {"name": "fruit_items", "label": "水果种类数", "label_en": "Fruit Variety (items)", "unit": "items", "required": True},
                    {"name": "whole_grain", "label": "全谷物 (g/day)", "label_en": "Whole Grain (g/day)", "unit": "g/day", "required": True},
                    {"name": "red_processed_meat", "label": "红肉+加工肉 (servings/day)", "label_en": "Red & Processed Meat (servings/day)", "unit": "servings/day", "required": True},
                    {"name": "hpf_servings", "label": "高加工食品+精制谷物 (servings/day)", "label_en": "HPF & Refined Grain (servings/day)", "unit": "servings/day", "required": True},
                    {"name": "ssb_fruit_juice", "label": "含糖饮料 (servings/day)", "label_en": "SSB (servings/day)", "unit": "servings/day", "required": True},
                ]
            },
        ],
        "output_cols": ["ACS2020_V2_ALL"],
        "max_score": 12,
    },

    "DI_GM": {
        "title": "肠道微生物膳食指数 (DI-GM)",
        "title_en": "Dietary Index for Gut Microbiota",
        "description": "14 个食物组分，性别分层中位数评分。总分 0-14。",
        "description_en": "14 food components, sex-stratified median scoring. Total score 0-14.",
        "function": "compute_di_gm",
        "extra_params": [
            {"name": "respondent_id", "label": "参与者ID", "label_en": "Respondent ID", "required": True},
            {"name": "gender", "label": "性别 (1=男, 2=女)", "label_en": "Gender (1=Male, 2=Female)", "unit": "", "required": True},
        ],
        "groups": [
            {
                "name": "有益食物 (健康成分)",
                "name_en": "Beneficial Foods",
                "params": [
                    {"name": "avocado", "label": "牛油果", "label_en": "Avocado", "unit": "arbitrary", "required": True},
                    {"name": "broccoli", "label": "西兰花", "label_en": "Broccoli", "unit": "arbitrary", "required": True},
                    {"name": "chickpea", "label": "鹰嘴豆", "label_en": "Chickpea", "unit": "arbitrary", "required": True},
                    {"name": "coffee", "label": "咖啡", "label_en": "Coffee", "unit": "arbitrary", "required": True},
                    {"name": "cranberry", "label": "蔓越莓", "label_en": "Cranberry", "unit": "arbitrary", "required": True},
                    {"name": "fermented_dairy", "label": "发酵乳制品", "label_en": "Fermented Dairy", "unit": "arbitrary", "required": True},
                    {"name": "fiber", "label": "膳食纤维", "label_en": "Fiber", "unit": "arbitrary", "required": True},
                    {"name": "green_tea", "label": "绿茶", "label_en": "Green Tea", "unit": "arbitrary", "required": True},
                    {"name": "soybean", "label": "大豆", "label_en": "Soybean", "unit": "arbitrary", "required": True},
                    {"name": "whole_grain", "label": "全谷物", "label_en": "Whole Grain", "unit": "arbitrary", "required": True},
                ]
            },
            {
                "name": "限制食物 (不健康成分)",
                "name_en": "Foods to Limit",
                "params": [
                    {"name": "total_fat_pct", "label": "总脂肪 (%kcal)", "label_en": "Total Fat (%kcal)", "unit": "%kcal", "required": True},
                    {"name": "processed_meat", "label": "加工肉", "label_en": "Processed Meat", "unit": "arbitrary", "required": True},
                    {"name": "red_meat", "label": "红肉", "label_en": "Red Meat", "unit": "arbitrary", "required": True},
                    {"name": "refined_grain", "label": "精制谷物", "label_en": "Refined Grain", "unit": "arbitrary", "required": True},
                ]
            },
        ],
        "output_cols": ["DI_GM_TOTAL"],
        "max_score": 14,
    },

    "PDI": {
        "title": "植物性膳食指数 (PDI)",
        "title_en": "Plant-based Diet Index (PDI)",
        "description": "基于 18 个食物组的五分位数评分。健康植物性食物和不健康植物性食物均正向计分，动物性食物反向计分。建议输入经能量调整后的 servings/day，但只要单位在样本内一致，也可以直接用于排序计分。总分 18-90。",
        "description_en": "Quintile-based score across 18 food groups. Both healthy and less-healthy plant foods are positively scored, while animal foods are reverse scored. Energy-adjusted servings/day are recommended, but any internally consistent continuous intake unit can be ranked. Total score 18-90.",
        "function": "compute_pdi",
        "extra_params": [
            {"name": "respondent_id", "label": "参与者 ID", "label_en": "Respondent ID", "required": True},
        ],
        "groups": [
            {
                "name": "健康植物性食物",
                "name_en": "Healthy Plant Foods",
                "params": [
                    {"name": "whole_grain", "label": "全谷物", "label_en": "Whole Grains", "unit": "servings/day", "required": True},
                    {"name": "fruit", "label": "水果", "label_en": "Fruit", "unit": "servings/day", "required": True},
                    {"name": "vegetable", "label": "蔬菜", "label_en": "Vegetables", "unit": "servings/day", "required": True},
                    {"name": "nuts", "label": "坚果", "label_en": "Nuts", "unit": "servings/day", "required": True},
                    {"name": "legumes", "label": "豆类", "label_en": "Legumes", "unit": "servings/day", "required": True},
                    {"name": "vegetable_oil", "label": "植物油", "label_en": "Vegetable Oils", "unit": "servings/day", "required": True},
                    {"name": "tea_coffee", "label": "茶 / 咖啡", "label_en": "Tea / Coffee", "unit": "servings/day", "required": True},
                ],
            },
            {
                "name": "相对不健康植物性食物",
                "name_en": "Less-healthy Plant Foods",
                "params": [
                    {"name": "fruit_juice", "label": "果汁", "label_en": "Fruit Juices", "unit": "servings/day", "required": True},
                    {"name": "refined_grain", "label": "精制谷物", "label_en": "Refined Grains", "unit": "servings/day", "required": True},
                    {"name": "potatoes", "label": "土豆 / 淀粉类薯类", "label_en": "Potatoes", "unit": "servings/day", "required": True},
                    {"name": "ssb", "label": "含糖饮料", "label_en": "Sugar-sweetened Beverages", "unit": "servings/day", "required": True},
                    {"name": "sweets_desserts", "label": "甜食 / 甜点", "label_en": "Sweets / Desserts", "unit": "servings/day", "required": True},
                ],
            },
            {
                "name": "动物性食物",
                "name_en": "Animal Foods",
                "params": [
                    {"name": "animal_fat", "label": "动物脂肪", "label_en": "Animal Fat", "unit": "servings/day", "required": True},
                    {"name": "dairy", "label": "乳制品", "label_en": "Dairy", "unit": "servings/day", "required": True},
                    {"name": "eggs", "label": "鸡蛋", "label_en": "Eggs", "unit": "servings/day", "required": True},
                    {"name": "fish_seafood", "label": "鱼类 / 海鲜", "label_en": "Fish / Seafood", "unit": "servings/day", "required": True},
                    {"name": "meat", "label": "肉类", "label_en": "Meat", "unit": "servings/day", "required": True},
                    {"name": "misc_animal_based", "label": "其他动物来源食物", "label_en": "Miscellaneous Animal-based Foods", "unit": "servings/day", "required": True},
                ],
            },
        ],
        "output_cols": ["PDI_ALL"],
        "max_score": 90,
    },

    "HPDI": {
        "title": "健康植物性膳食指数 (hPDI)",
        "title_en": "Healthful Plant-based Diet Index (hPDI)",
        "description": "基于 18 个食物组的五分位数评分。仅健康植物性食物正向计分，相对不健康植物性食物和动物性食物反向计分。建议输入经能量调整后的 servings/day。总分 18-90。",
        "description_en": "Quintile-based score across 18 food groups. Only healthy plant foods are positively scored, while less-healthy plant foods and animal foods are reverse scored. Energy-adjusted servings/day are recommended. Total score 18-90.",
        "function": "compute_hpdi",
        "extra_params": [
            {"name": "respondent_id", "label": "参与者 ID", "label_en": "Respondent ID", "required": True},
        ],
        "groups": [
            {
                "name": "健康植物性食物",
                "name_en": "Healthy Plant Foods",
                "params": [
                    {"name": "whole_grain", "label": "全谷物", "label_en": "Whole Grains", "unit": "servings/day", "required": True},
                    {"name": "fruit", "label": "水果", "label_en": "Fruit", "unit": "servings/day", "required": True},
                    {"name": "vegetable", "label": "蔬菜", "label_en": "Vegetables", "unit": "servings/day", "required": True},
                    {"name": "nuts", "label": "坚果", "label_en": "Nuts", "unit": "servings/day", "required": True},
                    {"name": "legumes", "label": "豆类", "label_en": "Legumes", "unit": "servings/day", "required": True},
                    {"name": "vegetable_oil", "label": "植物油", "label_en": "Vegetable Oils", "unit": "servings/day", "required": True},
                    {"name": "tea_coffee", "label": "茶 / 咖啡", "label_en": "Tea / Coffee", "unit": "servings/day", "required": True},
                ],
            },
            {
                "name": "相对不健康植物性食物",
                "name_en": "Less-healthy Plant Foods",
                "params": [
                    {"name": "fruit_juice", "label": "果汁", "label_en": "Fruit Juices", "unit": "servings/day", "required": True},
                    {"name": "refined_grain", "label": "精制谷物", "label_en": "Refined Grains", "unit": "servings/day", "required": True},
                    {"name": "potatoes", "label": "土豆 / 淀粉类薯类", "label_en": "Potatoes", "unit": "servings/day", "required": True},
                    {"name": "ssb", "label": "含糖饮料", "label_en": "Sugar-sweetened Beverages", "unit": "servings/day", "required": True},
                    {"name": "sweets_desserts", "label": "甜食 / 甜点", "label_en": "Sweets / Desserts", "unit": "servings/day", "required": True},
                ],
            },
            {
                "name": "动物性食物",
                "name_en": "Animal Foods",
                "params": [
                    {"name": "animal_fat", "label": "动物脂肪", "label_en": "Animal Fat", "unit": "servings/day", "required": True},
                    {"name": "dairy", "label": "乳制品", "label_en": "Dairy", "unit": "servings/day", "required": True},
                    {"name": "eggs", "label": "鸡蛋", "label_en": "Eggs", "unit": "servings/day", "required": True},
                    {"name": "fish_seafood", "label": "鱼类 / 海鲜", "label_en": "Fish / Seafood", "unit": "servings/day", "required": True},
                    {"name": "meat", "label": "肉类", "label_en": "Meat", "unit": "servings/day", "required": True},
                    {"name": "misc_animal_based", "label": "其他动物来源食物", "label_en": "Miscellaneous Animal-based Foods", "unit": "servings/day", "required": True},
                ],
            },
        ],
        "output_cols": ["HPDI_ALL"],
        "max_score": 90,
    },

    "UPDI": {
        "title": "不健康植物性膳食指数 (uPDI)",
        "title_en": "Unhealthful Plant-based Diet Index (uPDI)",
        "description": "基于 18 个食物组的五分位数评分。相对不健康植物性食物正向计分，健康植物性食物和动物性食物反向计分。建议输入经能量调整后的 servings/day。总分 18-90。",
        "description_en": "Quintile-based score across 18 food groups. Less-healthy plant foods are positively scored, while healthy plant foods and animal foods are reverse scored. Energy-adjusted servings/day are recommended. Total score 18-90.",
        "function": "compute_updi",
        "extra_params": [
            {"name": "respondent_id", "label": "参与者 ID", "label_en": "Respondent ID", "required": True},
        ],
        "groups": [
            {
                "name": "健康植物性食物",
                "name_en": "Healthy Plant Foods",
                "params": [
                    {"name": "whole_grain", "label": "全谷物", "label_en": "Whole Grains", "unit": "servings/day", "required": True},
                    {"name": "fruit", "label": "水果", "label_en": "Fruit", "unit": "servings/day", "required": True},
                    {"name": "vegetable", "label": "蔬菜", "label_en": "Vegetables", "unit": "servings/day", "required": True},
                    {"name": "nuts", "label": "坚果", "label_en": "Nuts", "unit": "servings/day", "required": True},
                    {"name": "legumes", "label": "豆类", "label_en": "Legumes", "unit": "servings/day", "required": True},
                    {"name": "vegetable_oil", "label": "植物油", "label_en": "Vegetable Oils", "unit": "servings/day", "required": True},
                    {"name": "tea_coffee", "label": "茶 / 咖啡", "label_en": "Tea / Coffee", "unit": "servings/day", "required": True},
                ],
            },
            {
                "name": "相对不健康植物性食物",
                "name_en": "Less-healthy Plant Foods",
                "params": [
                    {"name": "fruit_juice", "label": "果汁", "label_en": "Fruit Juices", "unit": "servings/day", "required": True},
                    {"name": "refined_grain", "label": "精制谷物", "label_en": "Refined Grains", "unit": "servings/day", "required": True},
                    {"name": "potatoes", "label": "土豆 / 淀粉类薯类", "label_en": "Potatoes", "unit": "servings/day", "required": True},
                    {"name": "ssb", "label": "含糖饮料", "label_en": "Sugar-sweetened Beverages", "unit": "servings/day", "required": True},
                    {"name": "sweets_desserts", "label": "甜食 / 甜点", "label_en": "Sweets / Desserts", "unit": "servings/day", "required": True},
                ],
            },
            {
                "name": "动物性食物",
                "name_en": "Animal Foods",
                "params": [
                    {"name": "animal_fat", "label": "动物脂肪", "label_en": "Animal Fat", "unit": "servings/day", "required": True},
                    {"name": "dairy", "label": "乳制品", "label_en": "Dairy", "unit": "servings/day", "required": True},
                    {"name": "eggs", "label": "鸡蛋", "label_en": "Eggs", "unit": "servings/day", "required": True},
                    {"name": "fish_seafood", "label": "鱼类 / 海鲜", "label_en": "Fish / Seafood", "unit": "servings/day", "required": True},
                    {"name": "meat", "label": "肉类", "label_en": "Meat", "unit": "servings/day", "required": True},
                    {"name": "misc_animal_based", "label": "其他动物来源食物", "label_en": "Miscellaneous Animal-based Foods", "unit": "servings/day", "required": True},
                ],
            },
        ],
        "output_cols": ["UPDI_ALL"],
        "max_score": 90,
    },

    "FISI": {
        "title": "食物炎症指数 / 食物炎症评分指数 (FII/FISI)",
        "title_en": "Food Inflammatory Index / Food Inflammatory Score Index",
        "description": "基于营养素摄入量、总炎症评分 (TIS) 和营养素参考值 (NRV) 计算 FII/FISI。分数越负表示膳食炎症潜力越低。",
        "description_en": "Calculates FII/FISI from nutrient intake, total inflammatory scores (TIS), and nutrient reference values (NRVs). More negative scores indicate lower inflammatory potential.",
        "function": "compute_fisi",
        "extra_params": [
            {"name": "respondent_id", "label": "参与者ID", "label_en": "Respondent ID", "required": False},
        ],
        "groups": [
            {
                "name": "宏量营养素与能量",
                "name_en": "Macronutrients & Energy",
                "params": [
                    {"name": "Protein", "label": "蛋白质 (g)", "label_en": "Protein (g)", "unit": "g", "required": False},
                    {"name": "Total_fat", "label": "总脂肪 (g)", "label_en": "Total fat (g)", "unit": "g", "required": False},
                    {"name": "Carbohydrate", "label": "碳水化合物 (g)", "label_en": "Carbohydrate (g)", "unit": "g", "required": False},
                    {"name": "Energy", "label": "能量 (kcal)", "label_en": "Energy (kcal)", "unit": "kcal", "required": False},
                    {"name": "Alcohol", "label": "酒精 (g)", "label_en": "Alcohol (g)", "unit": "g", "required": False},
                    {"name": "Caffeine", "label": "咖啡因 (mg)", "label_en": "Caffeine (mg)", "unit": "mg", "required": False},
                    {"name": "Fiber", "label": "膳食纤维 (g)", "label_en": "Fiber (g)", "unit": "g", "required": False},
                ],
            },
            {
                "name": "矿物质",
                "name_en": "Minerals",
                "params": [
                    {"name": "Iron", "label": "铁 (mg)", "label_en": "Iron (mg)", "unit": "mg", "required": False},
                    {"name": "Magnesium", "label": "镁 (mg)", "label_en": "Magnesium (mg)", "unit": "mg", "required": False},
                    {"name": "Zinc", "label": "锌 (mg)", "label_en": "Zinc (mg)", "unit": "mg", "required": False},
                    {"name": "Selenium", "label": "硒 (μg)", "label_en": "Selenium (μg)", "unit": "μg", "required": False},
                ],
            },
            {
                "name": "维生素",
                "name_en": "Vitamins",
                "params": [
                    {"name": "Vitamin_A", "label": "维生素A (μg)", "label_en": "Vitamin A (μg)", "unit": "μg", "required": False},
                    {"name": "Carotene_alpha", "label": "α-胡萝卜素 (μg)", "label_en": "Alpha-carotene (μg)", "unit": "μg", "required": False},
                    {"name": "Vitamin_E", "label": "维生素E (mg)", "label_en": "Vitamin E (mg)", "unit": "mg", "required": False},
                    {"name": "Vitamin_D", "label": "维生素D (μg)", "label_en": "Vitamin D (μg)", "unit": "μg", "required": False},
                    {"name": "Vitamin_C", "label": "维生素C (mg)", "label_en": "Vitamin C (mg)", "unit": "mg", "required": False},
                    {"name": "Thiamin", "label": "硫胺素B1 (mg)", "label_en": "Thiamin (mg)", "unit": "mg", "required": False},
                    {"name": "Riboflavin", "label": "核黄素B2 (mg)", "label_en": "Riboflavin (mg)", "unit": "mg", "required": False},
                    {"name": "Niacin", "label": "烟酸 (mg)", "label_en": "Niacin (mg)", "unit": "mg", "required": False},
                    {"name": "Vitamin_B6", "label": "维生素B6 (mg)", "label_en": "Vitamin B6 (mg)", "unit": "mg", "required": False},
                    {"name": "Vitamin_B12", "label": "维生素B12 (μg)", "label_en": "Vitamin B12 (μg)", "unit": "μg", "required": False},
                    {"name": "Folic_acid", "label": "叶酸 (μg)", "label_en": "Folic acid (μg)", "unit": "μg", "required": False},
                    {"name": "Vitamin_E_added", "label": "补充维生素E (mg)", "label_en": "Added vitamin E (mg)", "unit": "mg", "required": False},
                    {"name": "Vitamin_B_12_added", "label": "补充维生素B12 (μg)", "label_en": "Added vitamin B12 (μg)", "unit": "μg", "required": False},
                ],
            },
            {
                "name": "脂类",
                "name_en": "Lipids",
                "params": [
                    {"name": "Cholesterol", "label": "胆固醇 (mg)", "label_en": "Cholesterol (mg)", "unit": "mg", "required": False},
                    {"name": "Saturated_fat", "label": "饱和脂肪 (g)", "label_en": "Saturated fat (g)", "unit": "g", "required": False},
                    {"name": "PUFA_18_2", "label": "PUFA 18:2 (g)", "label_en": "PUFA 18:2 (g)", "unit": "g", "required": False},
                    {"name": "PUFA_18_3", "label": "PUFA 18:3 (g)", "label_en": "PUFA 18:3 (g)", "unit": "g", "required": False},
                    {"name": "PUFA_20_4", "label": "PUFA 20:4 (g)", "label_en": "PUFA 20:4 (g)", "unit": "g", "required": False},
                    {"name": "DHA", "label": "DHA (g)", "label_en": "DHA (g)", "unit": "g", "required": False},
                    {"name": "EPA", "label": "EPA (g)", "label_en": "EPA (g)", "unit": "g", "required": False},
                    {"name": "DPA", "label": "DPA (g)", "label_en": "DPA (g)", "unit": "g", "required": False},
                    {"name": "total_monounsaturated", "label": "总单不饱和脂肪 (g)", "label_en": "Total monounsaturated fat (g)", "unit": "g", "required": False},
                    {"name": "total_polyunsaturated", "label": "总多不饱和脂肪 (g)", "label_en": "Total polyunsaturated fat (g)", "unit": "g", "required": False},
                ],
            },
        ],
        "output_cols": ["FISI_Total"],
        "max_score": None,
    },
    "MIND": {
        "title": "MIND 膳食指数",
        "title_en": "MIND Diet Score",
        "description": "基于 15 个组件的固定阈值评分，综合 Mediterranean 与 DASH 中与认知健康最相关的食物组。请按页面说明使用每天或每周的统一频率单位。",
        "description_en": "Fifteen-component fixed-threshold score combining the cognition-oriented parts of Mediterranean and DASH patterns. Use the expected daily or weekly units shown in the component labels.",
        "function": "compute_mind",
        "extra_params": [
            {"name": "respondent_id", "label": "参与者 ID", "label_en": "Respondent ID", "required": True}
        ],
        "groups": [
            {
                "name": "鼓励食物",
                "name_en": "Recommended Foods",
                "params": [
                    {"name": "green_leafy_vegetables", "label": "绿叶蔬菜 (servings/week)", "label_en": "Green Leafy Vegetables (servings/week)", "unit": "servings/week", "required": True},
                    {"name": "other_vegetables", "label": "其他蔬菜 (servings/day)", "label_en": "Other Vegetables (servings/day)", "unit": "servings/day", "required": True},
                    {"name": "nuts", "label": "坚果 (servings/week)", "label_en": "Nuts (servings/week)", "unit": "servings/week", "required": True},
                    {"name": "berries", "label": "莓果 (servings/week)", "label_en": "Berries (servings/week)", "unit": "servings/week", "required": True},
                    {"name": "beans", "label": "豆类 (servings/week)", "label_en": "Beans (servings/week)", "unit": "servings/week", "required": True},
                    {"name": "whole_grains", "label": "全谷物 (servings/day)", "label_en": "Whole Grains (servings/day)", "unit": "servings/day", "required": True},
                    {"name": "fish", "label": "鱼类 (servings/week)", "label_en": "Fish (servings/week)", "unit": "servings/week", "required": True},
                    {"name": "poultry", "label": "禽肉 (servings/week)", "label_en": "Poultry (servings/week)", "unit": "servings/week", "required": True},
                    {"name": "olive_oil_primary", "label": "橄榄油是否为主要用油 (0/1)", "label_en": "Olive Oil as Primary Oil (0/1)", "unit": "binary", "required": True},
                    {"name": "wine", "label": "葡萄酒 (glasses/day)", "label_en": "Wine (glasses/day)", "unit": "glasses/day", "required": True}
                ]
            },
            {
                "name": "限制食物",
                "name_en": "Foods to Limit",
                "params": [
                    {"name": "red_meats", "label": "红肉 (servings/week)", "label_en": "Red Meats (servings/week)", "unit": "servings/week", "required": True},
                    {"name": "butter_margarine", "label": "黄油/人造黄油 (tbsp/day)", "label_en": "Butter / Margarine (tbsp/day)", "unit": "tbsp/day", "required": True},
                    {"name": "cheese", "label": "奶酪 (servings/week)", "label_en": "Cheese (servings/week)", "unit": "servings/week", "required": True},
                    {"name": "pastries_sweets", "label": "甜点甜食 (servings/week)", "label_en": "Pastries / Sweets (servings/week)", "unit": "servings/week", "required": True},
                    {"name": "fried_fast_food", "label": "油炸/快餐 (servings/week)", "label_en": "Fried / Fast Food (servings/week)", "unit": "servings/week", "required": True}
                ]
            }
        ],
        "output_cols": ["MIND_ALL"],
        "max_score": 15,
    },
    "DQI_I": {
        "title": "国际膳食质量指数 (DQI-I)",
        "title_en": "Diet Quality Index-International (DQI-I)",
        "description": "DQI-I 将饮食质量拆成 Variety、Adequacy、Moderation、Balance 四个维度。当前网页版要求用户额外准备一列“空热量食物供能百分比”，其余变量可按通用模式直接映射。",
        "description_en": "DQI-I breaks diet quality into Variety, Adequacy, Moderation, and Balance. The current web release expects one precomputed column for percent energy from empty-calorie foods; all other inputs can be mapped directly in general mode.",
        "function": "compute_dqii",
        "extra_params": [
            {"name": "respondent_id", "label": "参与者 ID", "label_en": "Respondent ID", "required": True},
            {"name": "age", "label": "年龄 (years)", "label_en": "Age (years)", "required": True},
            {"name": "gender", "label": "性别 (1=Male, 2=Female)", "label_en": "Gender (1=Male, 2=Female)", "required": True}
        ],
        "groups": [
            {
                "name": "食物组与能量",
                "name_en": "Energy and Food Groups",
                "params": [
                    {"name": "total_kcal", "label": "总能量 (kcal/day)", "label_en": "Total Energy (kcal/day)", "unit": "kcal/day", "required": True},
                    {"name": "grain", "label": "谷类/谷物 (servings/day)", "label_en": "Grains (servings/day)", "unit": "servings/day", "required": True},
                    {"name": "vegetable", "label": "蔬菜 (servings/day)", "label_en": "Vegetables (servings/day)", "unit": "servings/day", "required": True},
                    {"name": "fruit", "label": "水果 (servings/day)", "label_en": "Fruits (servings/day)", "unit": "servings/day", "required": True},
                    {"name": "meat", "label": "肉类 (servings/day)", "label_en": "Meat (servings/day)", "unit": "servings/day", "required": True},
                    {"name": "poultry", "label": "禽肉 (servings/day)", "label_en": "Poultry (servings/day)", "unit": "servings/day", "required": True},
                    {"name": "fish", "label": "鱼类 (servings/day)", "label_en": "Fish (servings/day)", "unit": "servings/day", "required": True},
                    {"name": "dairy", "label": "乳制品 (servings/day)", "label_en": "Dairy (servings/day)", "unit": "servings/day", "required": True},
                    {"name": "legumes", "label": "豆类 (servings/day)", "label_en": "Legumes (servings/day)", "unit": "servings/day", "required": True},
                    {"name": "egg", "label": "蛋类 (servings/day)", "label_en": "Eggs (servings/day)", "unit": "servings/day", "required": True}
                ]
            },
            {
                "name": "充足性营养素",
                "name_en": "Adequacy Nutrients",
                "params": [
                    {"name": "fiber", "label": "膳食纤维 (g/day)", "label_en": "Fiber (g/day)", "unit": "g/day", "required": True},
                    {"name": "protein", "label": "蛋白质 (g/day)", "label_en": "Protein (g/day)", "unit": "g/day", "required": True},
                    {"name": "iron", "label": "铁 (mg/day)", "label_en": "Iron (mg/day)", "unit": "mg/day", "required": True},
                    {"name": "calcium", "label": "钙 (mg/day)", "label_en": "Calcium (mg/day)", "unit": "mg/day", "required": True},
                    {"name": "vitamin_c", "label": "维生素 C (mg/day)", "label_en": "Vitamin C (mg/day)", "unit": "mg/day", "required": True}
                ]
            },
            {
                "name": "节制与平衡",
                "name_en": "Moderation and Balance",
                "params": [
                    {"name": "carbohydrate", "label": "碳水化合物 (g/day)", "label_en": "Carbohydrate (g/day)", "unit": "g/day", "required": True},
                    {"name": "total_fat", "label": "总脂肪 (g/day)", "label_en": "Total Fat (g/day)", "unit": "g/day", "required": True},
                    {"name": "saturated_fat", "label": "饱和脂肪 (g/day)", "label_en": "Saturated Fat (g/day)", "unit": "g/day", "required": True},
                    {"name": "mufa", "label": "单不饱和脂肪酸 MUFA (g/day)", "label_en": "MUFA (g/day)", "unit": "g/day", "required": True},
                    {"name": "pufa", "label": "多不饱和脂肪酸 PUFA (g/day)", "label_en": "PUFA (g/day)", "unit": "g/day", "required": True},
                    {"name": "cholesterol", "label": "胆固醇 (mg/day)", "label_en": "Cholesterol (mg/day)", "unit": "mg/day", "required": True},
                    {"name": "sodium", "label": "钠 (mg/day)", "label_en": "Sodium (mg/day)", "unit": "mg/day", "required": True},
                    {"name": "empty_calorie_pct_energy", "label": "空热量食物供能百分比 (% energy)", "label_en": "% Energy from Empty-Calorie Foods", "unit": "% energy", "required": True}
                ]
            }
        ],
        "output_cols": ["DQII_ALL"],
        "max_score": 100,
    },
    "CHEI": {
        "title": "中国健康饮食指数 (CHEI)",
        "title_en": "Chinese Healthy Eating Index (CHEI)",
        "description": "基于 CHEI 17 组件固定评分规则。除酒精与添加糖外，请优先输入按每 1000 kcal 标准化后的标准份或密度值。",
        "description_en": "CHEI with 17 fixed-rule components. Except alcohol and added sugars, inputs are expected as standard portions or densities per 1000 kcal.",
        "function": "compute_chei",
        "extra_params": [
            {"name": "respondent_id", "label": "参与者 ID", "label_en": "Respondent ID", "required": True},
            {"name": "gender", "label": "性别 (1=男, 2=女)", "label_en": "Gender (1=Male, 2=Female)", "required": True}
        ],
        "groups": [
            {
                "name": "充足性组件",
                "name_en": "Adequacy Components",
                "params": [
                    {"name": "total_grains", "label": "总谷类 (SP/1000 kcal)", "label_en": "Total Grains (SP/1000 kcal)", "unit": "SP/1000 kcal", "required": True},
                    {"name": "whole_grains_mixed_beans", "label": "全谷杂豆 (SP/1000 kcal)", "label_en": "Whole Grains and Mixed Beans (SP/1000 kcal)", "unit": "SP/1000 kcal", "required": True},
                    {"name": "tubers", "label": "薯类 (SP/1000 kcal)", "label_en": "Tubers (SP/1000 kcal)", "unit": "SP/1000 kcal", "required": True},
                    {"name": "total_vegetables", "label": "总蔬菜 (SP/1000 kcal)", "label_en": "Total Vegetables (SP/1000 kcal)", "unit": "SP/1000 kcal", "required": True},
                    {"name": "dark_vegetables", "label": "深色蔬菜 (SP/1000 kcal)", "label_en": "Dark Vegetables (SP/1000 kcal)", "unit": "SP/1000 kcal", "required": True},
                    {"name": "fruits", "label": "水果 (SP/1000 kcal)", "label_en": "Fruits (SP/1000 kcal)", "unit": "SP/1000 kcal", "required": True},
                    {"name": "dairy", "label": "奶类 (SP/1000 kcal)", "label_en": "Dairy (SP/1000 kcal)", "unit": "SP/1000 kcal", "required": True},
                    {"name": "soybeans", "label": "大豆 (SP/1000 kcal)", "label_en": "Soybeans (SP/1000 kcal)", "unit": "SP/1000 kcal", "required": True},
                    {"name": "fish_seafood", "label": "鱼虾水产 (SP/1000 kcal)", "label_en": "Fish and Seafood (SP/1000 kcal)", "unit": "SP/1000 kcal", "required": True},
                    {"name": "poultry", "label": "禽肉 (SP/1000 kcal)", "label_en": "Poultry (SP/1000 kcal)", "unit": "SP/1000 kcal", "required": True},
                    {"name": "eggs", "label": "蛋类 (SP/1000 kcal)", "label_en": "Eggs (SP/1000 kcal)", "unit": "SP/1000 kcal", "required": True},
                    {"name": "seeds_nuts", "label": "坚果种子 (SP/1000 kcal)", "label_en": "Seeds and Nuts (SP/1000 kcal)", "unit": "SP/1000 kcal", "required": True}
                ]
            },
            {
                "name": "限制性组件",
                "name_en": "Moderation Components",
                "params": [
                    {"name": "red_meat", "label": "红肉 (SP/1000 kcal)", "label_en": "Red Meat (SP/1000 kcal)", "unit": "SP/1000 kcal", "required": True},
                    {"name": "cooking_oils", "label": "烹调油 (g/1000 kcal)", "label_en": "Cooking Oils (g/1000 kcal)", "unit": "g/1000 kcal", "required": True},
                    {"name": "sodium", "label": "钠 (mg/1000 kcal)", "label_en": "Sodium (mg/1000 kcal)", "unit": "mg/1000 kcal", "required": True},
                    {"name": "added_sugars_pct_energy", "label": "添加糖占能量百分比 (%)", "label_en": "Added Sugars (% energy)", "unit": "% energy", "required": True},
                    {"name": "alcohol", "label": "酒精 (g/day)", "label_en": "Alcohol (g/day)", "unit": "g/day", "required": True}
                ]
            }
        ],
        "output_cols": ["CHEI_ALL"],
        "max_score": 100,
    },
    "DBI": {
        "title": "膳食平衡指数 (DBI-07)",
        "title_en": "Diet Balance Index (DBI-07)",
        "description": "当前上线的是 DBI-07 成人通用版，按文献中 2000 kcal/天标准表示例进行评分。输入单位默认为每日摄入量：食物组 g/day、饮水 mL/day、酒精 g/day。",
        "description_en": "Current release: adult DBI-07 using the published 2000-kcal/day standard table. Inputs are daily intakes: food groups in g/day, water in mL/day, and alcohol in g/day.",
        "function": "compute_dbi",
        "extra_params": [
            {"name": "respondent_id", "label": "参与者 ID", "label_en": "Respondent ID", "required": True},
            {"name": "gender", "label": "性别 (1=男, 2=女)", "label_en": "Gender (1=Male, 2=Female)", "required": True}
        ],
        "groups": [
            {
                "name": "核心食物组",
                "name_en": "Core Food Groups",
                "params": [
                    {"name": "cereals", "label": "谷类总量 (g/day)", "label_en": "Total Cereals (g/day)", "unit": "g/day", "required": True},
                    {"name": "vegetables", "label": "蔬菜 (g/day)", "label_en": "Vegetables (g/day)", "unit": "g/day", "required": True},
                    {"name": "fruits", "label": "水果 (g/day)", "label_en": "Fruits (g/day)", "unit": "g/day", "required": True},
                    {"name": "dairy", "label": "乳类 (g/day)", "label_en": "Dairy (g/day)", "unit": "g/day", "required": True},
                    {"name": "soybean", "label": "大豆及制品 (g/day)", "label_en": "Soybean and Soy Products (g/day)", "unit": "g/day", "required": True}
                ]
            },
            {
                "name": "动物性食物、调味与饮水",
                "name_en": "Animal Foods, Condiments, and Water",
                "params": [
                    {"name": "meat", "label": "肉类 (g/day)", "label_en": "Meat (g/day)", "unit": "g/day", "required": True},
                    {"name": "fish_shrimp", "label": "鱼虾类 (g/day)", "label_en": "Fish and Shrimp (g/day)", "unit": "g/day", "required": True},
                    {"name": "egg", "label": "蛋类 (g/day)", "label_en": "Eggs (g/day)", "unit": "g/day", "required": True},
                    {"name": "oil", "label": "食用油 (g/day)", "label_en": "Cooking Oil (g/day)", "unit": "g/day", "required": True},
                    {"name": "salt", "label": "食盐 (g/day)", "label_en": "Salt (g/day)", "unit": "g/day", "required": True},
                    {"name": "alcohol", "label": "酒精 (g/day)", "label_en": "Alcohol (g/day)", "unit": "g/day", "required": True},
                    {"name": "water", "label": "饮水量 (mL/day)", "label_en": "Drinking Water (mL/day)", "unit": "mL/day", "required": True}
                ]
            },
            {
                "name": "膳食多样性子组",
                "name_en": "Diet Variety Subgroups",
                "params": [
                    {"name": "rice_products", "label": "米及米制品 (g/day)", "label_en": "Rice and Rice Products (g/day)", "unit": "g/day", "required": True},
                    {"name": "wheat_products", "label": "小麦及制品 (g/day)", "label_en": "Wheat and Wheat Products (g/day)", "unit": "g/day", "required": True},
                    {"name": "coarse_grains_tubers", "label": "粗杂粮与薯类 (g/day)", "label_en": "Coarse Grains and Tubers (g/day)", "unit": "g/day", "required": True},
                    {"name": "dark_vegetables", "label": "深色蔬菜 (g/day)", "label_en": "Dark Vegetables (g/day)", "unit": "g/day", "required": True},
                    {"name": "light_vegetables", "label": "浅色蔬菜 (g/day)", "label_en": "Light Vegetables (g/day)", "unit": "g/day", "required": True},
                    {"name": "red_meat_products", "label": "红肉及制品 (g/day)", "label_en": "Red Meat and Products (g/day)", "unit": "g/day", "required": True},
                    {"name": "poultry_game", "label": "禽肉与野味 (g/day)", "label_en": "Poultry and Game (g/day)", "unit": "g/day", "required": True}
                ]
            }
        ],
        "output_cols": ["DBI_DQD", "DBI_LBS", "DBI_HBS", "DBI_TS"],
        "max_score": 84,
    },
    "GDQS": {
        "title": "全球膳食质量评分 (GDQS)",
        "title_en": "Global Diet Quality Score (GDQS)",
        "description": "GDQS 基于 25 个全球可比食物组的固定阈值评分，适合公共营养、人群监测与跨国家队列比较。输入单位默认为各食物组 g/day。",
        "description_en": "GDQS uses fixed thresholds across 25 globally comparable food groups, making it well suited to public nutrition, surveillance, and cross-country cohort work. Inputs are expected in g/day.",
        "function": "compute_gdqs",
        "extra_params": [
            {"name": "respondent_id", "label": "参与者 ID", "label_en": "Respondent ID", "required": True}
        ],
        "groups": [
            {
                "name": "水果与蔬菜",
                "name_en": "Fruits and Vegetables",
                "params": [
                    {"name": "citrus_fruits", "label": "柑橘类水果 (g/day)", "label_en": "Citrus Fruits (g/day)", "unit": "g/day", "required": True},
                    {"name": "deep_orange_fruits", "label": "深橙色水果 (g/day)", "label_en": "Deep Orange Fruits (g/day)", "unit": "g/day", "required": True},
                    {"name": "other_fruits", "label": "其他水果 (g/day)", "label_en": "Other Fruits (g/day)", "unit": "g/day", "required": True},
                    {"name": "dark_green_leafy_vegetables", "label": "深绿色叶菜 (g/day)", "label_en": "Dark Green Leafy Vegetables (g/day)", "unit": "g/day", "required": True},
                    {"name": "cruciferous_vegetables", "label": "十字花科蔬菜 (g/day)", "label_en": "Cruciferous Vegetables (g/day)", "unit": "g/day", "required": True},
                    {"name": "deep_orange_vegetables", "label": "深橙色蔬菜 (g/day)", "label_en": "Deep Orange Vegetables (g/day)", "unit": "g/day", "required": True},
                    {"name": "other_vegetables", "label": "其他蔬菜 (g/day)", "label_en": "Other Vegetables (g/day)", "unit": "g/day", "required": True},
                    {"name": "deep_orange_tubers", "label": "深橙色块根块茎 (g/day)", "label_en": "Deep Orange Tubers (g/day)", "unit": "g/day", "required": True},
                    {"name": "white_roots_tubers", "label": "白色根茎薯类 (g/day)", "label_en": "White Roots and Tubers (g/day)", "unit": "g/day", "required": True}
                ]
            },
            {
                "name": "豆类、谷物与健康脂肪",
                "name_en": "Legumes, Grains, and Healthy Fats",
                "params": [
                    {"name": "legumes", "label": "豆类 (g/day)", "label_en": "Legumes (g/day)", "unit": "g/day", "required": True},
                    {"name": "nuts_seeds", "label": "坚果和种子 (g/day)", "label_en": "Nuts and Seeds (g/day)", "unit": "g/day", "required": True},
                    {"name": "whole_grains", "label": "全谷物 (g/day)", "label_en": "Whole Grains (g/day)", "unit": "g/day", "required": True},
                    {"name": "refined_grains_baked_goods", "label": "精制谷物与烘焙食品 (g/day)", "label_en": "Refined Grains and Baked Goods (g/day)", "unit": "g/day", "required": True},
                    {"name": "liquid_oils", "label": "液体油脂 (g/day)", "label_en": "Liquid Oils (g/day)", "unit": "g/day", "required": True}
                ]
            },
            {
                "name": "动物性食物与乳制品",
                "name_en": "Animal Foods and Dairy",
                "params": [
                    {"name": "fish_shellfish", "label": "鱼和贝类 (g/day)", "label_en": "Fish and Shellfish (g/day)", "unit": "g/day", "required": True},
                    {"name": "poultry_game_meat", "label": "禽肉和野味 (g/day)", "label_en": "Poultry and Game Meat (g/day)", "unit": "g/day", "required": True},
                    {"name": "low_fat_dairy", "label": "低脂乳制品 (g/day)", "label_en": "Low-Fat Dairy (g/day)", "unit": "g/day", "required": True},
                    {"name": "high_fat_dairy", "label": "高脂乳制品 (g/day)", "label_en": "High-Fat Dairy (g/day)", "unit": "g/day", "required": True},
                    {"name": "eggs", "label": "蛋类 (g/day)", "label_en": "Eggs (g/day)", "unit": "g/day", "required": True},
                    {"name": "red_meat", "label": "红肉 (g/day)", "label_en": "Red Meat (g/day)", "unit": "g/day", "required": True},
                    {"name": "processed_meat", "label": "加工肉类 (g/day)", "label_en": "Processed Meat (g/day)", "unit": "g/day", "required": True}
                ]
            },
            {
                "name": "限制性食物和饮料",
                "name_en": "Foods and Drinks to Limit",
                "params": [
                    {"name": "sweets_ice_cream", "label": "甜食与冰淇淋 (g/day)", "label_en": "Sweets and Ice Cream (g/day)", "unit": "g/day", "required": True},
                    {"name": "sugar_sweetened_beverages", "label": "含糖饮料 (g/day)", "label_en": "Sugar-Sweetened Beverages (g/day)", "unit": "g/day", "required": True},
                    {"name": "juice", "label": "果汁 (g/day)", "label_en": "Juice (g/day)", "unit": "g/day", "required": True},
                    {"name": "purchased_deep_fried_foods", "label": "购买的油炸食品 (g/day)", "label_en": "Purchased Deep-Fried Foods (g/day)", "unit": "g/day", "required": True}
                ]
            }
        ],
        "output_cols": ["GDQS_ALL", "GDQS_POS", "GDQS_NEG"],
        "max_score": 49,
    },
    "WISH": {
        "title": "可持续与健康饮食指数 (WISH)",
        "title_en": "World Index for Sustainability and Health (WISH)",
        "description": "WISH 基于 13 个食物组的固定目标值，兼顾健康导向与环境影响子分。输入单位默认为各食物组 g/day。",
        "description_en": "WISH uses fixed intake targets across 13 food groups and returns both health-oriented and environmental-impact subscores. Inputs are expected in g/day.",
        "function": "compute_wish",
        "extra_params": [
            {"name": "respondent_id", "label": "参与者 ID", "label_en": "Respondent ID", "required": True}
        ],
        "groups": [
            {
                "name": "保护性食物组",
                "name_en": "Protective Food Groups",
                "params": [
                    {"name": "whole_grains", "label": "全谷物 (g/day)", "label_en": "Whole Grains (g/day)", "unit": "g/day", "required": True},
                    {"name": "vegetables", "label": "蔬菜 (g/day)", "label_en": "Vegetables (g/day)", "unit": "g/day", "required": True},
                    {"name": "fruit", "label": "水果 (g/day)", "label_en": "Fruit (g/day)", "unit": "g/day", "required": True},
                    {"name": "legumes", "label": "豆类 (g/day)", "label_en": "Legumes (g/day)", "unit": "g/day", "required": True},
                    {"name": "unsaturated_oils", "label": "不饱和油脂 (g/day)", "label_en": "Unsaturated Oils (g/day)", "unit": "g/day", "required": True},
                    {"name": "fish", "label": "鱼类 (g/day)", "label_en": "Fish (g/day)", "unit": "g/day", "required": True},
                    {"name": "dairy", "label": "乳制品 (g/day)", "label_en": "Dairy (g/day)", "unit": "g/day", "required": True},
                    {"name": "nuts", "label": "坚果 (g/day)", "label_en": "Nuts (g/day)", "unit": "g/day", "required": True}
                ]
            },
            {
                "name": "中性食物组",
                "name_en": "Neutral Food Groups",
                "params": [
                    {"name": "poultry", "label": "禽肉 (g/day)", "label_en": "Poultry (g/day)", "unit": "g/day", "required": True},
                    {"name": "eggs", "label": "鸡蛋 (g/day)", "label_en": "Eggs (g/day)", "unit": "g/day", "required": True}
                ]
            },
            {
                "name": "限制性食物组",
                "name_en": "Limit Food Groups",
                "params": [
                    {"name": "red_meat", "label": "红肉 (g/day)", "label_en": "Red Meat (g/day)", "unit": "g/day", "required": True},
                    {"name": "saturated_oils", "label": "饱和油脂 (g/day)", "label_en": "Saturated Oils (g/day)", "unit": "g/day", "required": True},
                    {"name": "added_sugars", "label": "添加糖 (g/day)", "label_en": "Added Sugars (g/day)", "unit": "g/day", "required": True}
                ]
            }
        ],
        "output_cols": ["WISH_ALL", "WISH_HEALTHY", "WISH_LESS_HEALTHY", "WISH_LOW_ENV", "WISH_HIGH_ENV"],
        "max_score": 130,
    },
    "NRF": {
        "title": "营养丰富食物指数 (NRF9.3)",
        "title_en": "Nutrient Rich Foods Index (NRF9.3)",
        "description": "NRF9.3 的膳食层面 2000 kcal 适配版，使用 Fulgoni 等（2009）的固定 9+3 基准；0.2.1 默认对每个鼓励/限制营养素百分比封顶 100%（总分 -300–900），并保留显式 uncapped-LIM 敏感性版本。必须完整提供 12 项。",
        "description_en": "Diet-level 2,000-kcal adaptation of NRF9.3 using the fixed Fulgoni et al. (2009) 9+3 panel. Version 0.2.1 caps each qualifying and limiting percentage at 100% by default (total -300 to 900) and retains an explicitly named uncapped-LIM sensitivity variant. All 12 nutrients are required.",
        "function": "compute_nrf",
        "extra_params": [
            {"name": "respondent_id", "label": "参与者 ID", "label_en": "Respondent ID", "required": True},
            {"name": "reference_energy_kcal", "label": "参考能量 (kcal)", "label_en": "Reference Energy (kcal)", "required": False, "default": 2000}
        ],
        "groups": [
            {
                "name": "基础能量与鼓励营养素",
                "name_en": "Energy and Positive Nutrients",
                "params": [
                    {"name": "energy", "label": "能量 (kcal)", "label_en": "Energy (kcal)", "unit": "kcal", "required": True},
                    {"name": "protein", "label": "蛋白质 (g)", "label_en": "Protein (g)", "unit": "g", "required": True},
                    {"name": "fiber", "label": "膳食纤维 (g)", "label_en": "Fiber (g)", "unit": "g", "required": True},
                    {"name": "vitamin_a", "label": "维生素A (ug)", "label_en": "Vitamin A (ug)", "unit": "ug", "required": True},
                    {"name": "vitamin_c", "label": "维生素C (mg)", "label_en": "Vitamin C (mg)", "unit": "mg", "required": True},
                    {"name": "vitamin_e", "label": "维生素E (mg)", "label_en": "Vitamin E (mg)", "unit": "mg", "required": True},
                    {"name": "calcium", "label": "钙 (mg)", "label_en": "Calcium (mg)", "unit": "mg", "required": True},
                    {"name": "iron", "label": "铁 (mg)", "label_en": "Iron (mg)", "unit": "mg", "required": True},
                    {"name": "magnesium", "label": "镁 (mg)", "label_en": "Magnesium (mg)", "unit": "mg", "required": True},
                    {"name": "potassium", "label": "钾 (mg)", "label_en": "Potassium (mg)", "unit": "mg", "required": True}
                ]
            },
            {
                "name": "限制营养素",
                "name_en": "Nutrients to Limit",
                "params": [
                    {"name": "saturated_fat", "label": "饱和脂肪 (g)", "label_en": "Saturated Fat (g)", "unit": "g", "required": True},
                    {"name": "added_sugar", "label": "添加糖 (g)", "label_en": "Added Sugar (g)", "unit": "g", "required": True},
                    {"name": "sodium", "label": "钠 (mg)", "label_en": "Sodium (mg)", "unit": "mg", "required": True}
                ]
            }
        ],
        "output_cols": ["NRF_ALL"],
        "max_score": None,
    },
    "NAR": {
        "title": "营养素充足比 (NAR)",
        "title_en": "Nutrient Adequacy Ratio (NAR)",
        "description": "按参考摄入值计算多个营养素的充足比，并将每个营养素的比例封顶在 1。页面主分数显示所选营养素充足比的平均值。",
        "description_en": "Computes capped nutrient adequacy ratios against benchmark intakes. The page-level total is the mean capped adequacy across the selected nutrient panel.",
        "function": "compute_nar",
        "extra_params": [
            {"name": "respondent_id", "label": "参与者 ID", "label_en": "Respondent ID", "required": True}
        ],
        "groups": [
            {
                "name": "营养素面板",
                "name_en": "Nutrient Panel",
                "params": [
                    {"name": "protein", "label": "蛋白质 (g)", "label_en": "Protein (g)", "unit": "g", "required": True},
                    {"name": "fiber", "label": "膳食纤维 (g)", "label_en": "Fiber (g)", "unit": "g", "required": True},
                    {"name": "vitamin_a", "label": "维生素A (ug)", "label_en": "Vitamin A (ug)", "unit": "ug", "required": True},
                    {"name": "vitamin_c", "label": "维生素C (mg)", "label_en": "Vitamin C (mg)", "unit": "mg", "required": True},
                    {"name": "vitamin_e", "label": "维生素E (mg)", "label_en": "Vitamin E (mg)", "unit": "mg", "required": True},
                    {"name": "calcium", "label": "钙 (mg)", "label_en": "Calcium (mg)", "unit": "mg", "required": True},
                    {"name": "iron", "label": "铁 (mg)", "label_en": "Iron (mg)", "unit": "mg", "required": True},
                    {"name": "magnesium", "label": "镁 (mg)", "label_en": "Magnesium (mg)", "unit": "mg", "required": True},
                    {"name": "potassium", "label": "钾 (mg)", "label_en": "Potassium (mg)", "unit": "mg", "required": True}
                ]
            }
        ],
        "output_cols": ["NAR_ALL"],
        "max_score": 1,
    },
    "MAR": {
        "title": "平均营养素充足比 (MAR)",
        "title_en": "Mean Adequacy Ratio (MAR)",
        "description": "MAR 是多个封顶 NAR 的平均值。这里按百分制输出，100 表示该营养素面板全部达到或超过参考值。",
        "description_en": "MAR is the mean of capped NAR values. This implementation reports it on a 0-100 scale, where 100 means the full nutrient panel reached benchmark intake levels.",
        "function": "compute_mar",
        "extra_params": [
            {"name": "respondent_id", "label": "参与者 ID", "label_en": "Respondent ID", "required": True}
        ],
        "groups": [
            {
                "name": "营养素面板",
                "name_en": "Nutrient Panel",
                "params": [
                    {"name": "protein", "label": "蛋白质 (g)", "label_en": "Protein (g)", "unit": "g", "required": True},
                    {"name": "fiber", "label": "膳食纤维 (g)", "label_en": "Fiber (g)", "unit": "g", "required": True},
                    {"name": "vitamin_a", "label": "维生素A (ug)", "label_en": "Vitamin A (ug)", "unit": "ug", "required": True},
                    {"name": "vitamin_c", "label": "维生素C (mg)", "label_en": "Vitamin C (mg)", "unit": "mg", "required": True},
                    {"name": "vitamin_e", "label": "维生素E (mg)", "label_en": "Vitamin E (mg)", "unit": "mg", "required": True},
                    {"name": "calcium", "label": "钙 (mg)", "label_en": "Calcium (mg)", "unit": "mg", "required": True},
                    {"name": "iron", "label": "铁 (mg)", "label_en": "Iron (mg)", "unit": "mg", "required": True},
                    {"name": "magnesium", "label": "镁 (mg)", "label_en": "Magnesium (mg)", "unit": "mg", "required": True},
                    {"name": "potassium", "label": "钾 (mg)", "label_en": "Potassium (mg)", "unit": "mg", "required": True}
                ]
            }
        ],
        "output_cols": ["MAR_ALL"],
        "max_score": 100,
    },
    "INQ": {
        "title": "营养质量指数 (INQ)",
        "title_en": "Index of Nutritional Quality (INQ)",
        "description": "INQ 按单位能量的营养素密度与参考营养素密度进行比较。主分数为多个营养素 INQ 的平均值。",
        "description_en": "INQ compares nutrient density per unit energy with the benchmark nutrient density. The page-level total is the mean INQ across the selected nutrient panel.",
        "function": "compute_inq",
        "extra_params": [
            {"name": "respondent_id", "label": "参与者 ID", "label_en": "Respondent ID", "required": True},
            {"name": "reference_energy_kcal", "label": "参考能量 (kcal)", "label_en": "Reference Energy (kcal)", "required": False, "default": 2000}
        ],
        "groups": [
            {
                "name": "能量与营养素面板",
                "name_en": "Energy and Nutrient Panel",
                "params": [
                    {"name": "energy", "label": "能量 (kcal)", "label_en": "Energy (kcal)", "unit": "kcal", "required": True},
                    {"name": "protein", "label": "蛋白质 (g)", "label_en": "Protein (g)", "unit": "g", "required": True},
                    {"name": "fiber", "label": "膳食纤维 (g)", "label_en": "Fiber (g)", "unit": "g", "required": True},
                    {"name": "vitamin_a", "label": "维生素A (ug)", "label_en": "Vitamin A (ug)", "unit": "ug", "required": True},
                    {"name": "vitamin_c", "label": "维生素C (mg)", "label_en": "Vitamin C (mg)", "unit": "mg", "required": True},
                    {"name": "vitamin_e", "label": "维生素E (mg)", "label_en": "Vitamin E (mg)", "unit": "mg", "required": True},
                    {"name": "calcium", "label": "钙 (mg)", "label_en": "Calcium (mg)", "unit": "mg", "required": True},
                    {"name": "iron", "label": "铁 (mg)", "label_en": "Iron (mg)", "unit": "mg", "required": True},
                    {"name": "magnesium", "label": "镁 (mg)", "label_en": "Magnesium (mg)", "unit": "mg", "required": True},
                    {"name": "potassium", "label": "钾 (mg)", "label_en": "Potassium (mg)", "unit": "mg", "required": True}
                ]
            }
        ],
        "output_cols": ["INQ_ALL"],
        "max_score": None,
    },
    "PRAL": {
        "title": "潜在肾酸负荷 (PRAL)",
        "title_en": "Potential Renal Acid Load (PRAL)",
        "description": "根据蛋白质、磷、钾、镁、钙摄入量按经典 Remer-Manz 公式估计膳食酸负荷。正值通常表示更偏产酸。",
        "description_en": "Classic Remer-Manz PRAL formula based on protein, phosphorus, potassium, magnesium, and calcium intake. Positive values generally indicate a more acid-producing profile.",
        "function": "compute_pral",
        "extra_params": [
            {"name": "respondent_id", "label": "参与者 ID", "label_en": "Respondent ID", "required": True}
        ],
        "groups": [
            {
                "name": "公式输入",
                "name_en": "Formula Inputs",
                "params": [
                    {"name": "protein", "label": "蛋白质 (g/day)", "label_en": "Protein (g/day)", "unit": "g/day", "required": True},
                    {"name": "phosphorus", "label": "磷 (mg/day)", "label_en": "Phosphorus (mg/day)", "unit": "mg/day", "required": True},
                    {"name": "potassium", "label": "钾 (mg/day)", "label_en": "Potassium (mg/day)", "unit": "mg/day", "required": True},
                    {"name": "magnesium", "label": "镁 (mg/day)", "label_en": "Magnesium (mg/day)", "unit": "mg/day", "required": True},
                    {"name": "calcium", "label": "钙 (mg/day)", "label_en": "Calcium (mg/day)", "unit": "mg/day", "required": True}
                ]
            }
        ],
        "output_cols": ["PRAL_ALL"],
        "max_score": None,
    },
    "NEAP": {
        "title": "净内源性酸产生 (NEAP)",
        "title_en": "Net Endogenous Acid Production (NEAP)",
        "description": "根据蛋白质与钾的摄入比值按 Frassetto 公式估计内源性酸产生。这里的钾输入使用常见的 mg/day，系统会自动换算为公式所需的 mEq/day。",
        "description_en": "Frassetto NEAP formula based on the ratio of protein to potassium intake. Potassium can be entered in the usual mg/day form and is auto-converted to mEq/day internally.",
        "function": "compute_neap",
        "extra_params": [
            {"name": "respondent_id", "label": "参与者 ID", "label_en": "Respondent ID", "required": True}
        ],
        "groups": [
            {
                "name": "公式输入",
                "name_en": "Formula Inputs",
                "params": [
                    {"name": "protein", "label": "蛋白质 (g/day)", "label_en": "Protein (g/day)", "unit": "g/day", "required": True},
                    {"name": "potassium", "label": "钾 (mg/day，自动换算 mEq/day)", "label_en": "Potassium (mg/day, auto-converted to mEq/day)", "unit": "mg/day", "required": True}
                ]
            }
        ],
        "output_cols": ["NEAP_ALL"],
        "max_score": None,
    },
    "CDAI": {
        "title": "膳食抗氧化复合指数 (CDAI)",
        "title_en": "Composite Dietary Antioxidant Index (CDAI)",
        "description": "将锌、硒、总类胡萝卜素、维生素A、维生素C、维生素E 在样本内标准化后求和。该指标是样本相对分数，适合队列内部比较。",
        "description_en": "Sample-standardized sum of zinc, selenium, total carotenoids, vitamin A, vitamin C, and vitamin E. This is a sample-relative composite score designed for within-cohort comparison.",
        "function": "compute_cdai",
        "extra_params": [
            {"name": "respondent_id", "label": "参与者 ID", "label_en": "Respondent ID", "required": True}
        ],
        "groups": [
            {
                "name": "抗氧化营养素",
                "name_en": "Antioxidant Nutrients",
                "params": [
                    {"name": "zinc", "label": "锌 (mg)", "label_en": "Zinc (mg)", "unit": "mg", "required": True},
                    {"name": "selenium", "label": "硒 (ug)", "label_en": "Selenium (ug)", "unit": "ug", "required": True},
                    {"name": "total_carotenoids", "label": "总类胡萝卜素 (ug)", "label_en": "Total Carotenoids (ug)", "unit": "ug", "required": True},
                    {"name": "vitamin_a", "label": "维生素A (ug)", "label_en": "Vitamin A (ug)", "unit": "ug", "required": True},
                    {"name": "vitamin_c", "label": "维生素C (mg)", "label_en": "Vitamin C (mg)", "unit": "mg", "required": True},
                    {"name": "vitamin_e", "label": "维生素E (mg)", "label_en": "Vitamin E (mg)", "unit": "mg", "required": True}
                ]
            }
        ],
        "output_cols": ["CDAI_ALL"],
        "max_score": None,
    },
    "OBS": {
        "title": "氧化平衡评分 (OBS)",
        "title_en": "Oxidative Balance Score (OBS)",
        "description": "采用明确边界的 NHANES 风格 OBS：16 个饮食因子加 4 个生活方式因子。饮食成分、BMI 与 cotinine 按性别分层三分位评分，体力活动与饮酒按论文固定分类计分。",
        "description_en": "Implements an explicitly bounded NHANES-style OBS with 16 dietary factors plus 4 lifestyle factors. Dietary components, BMI, and cotinine use sex-specific tertiles, while physical activity and alcohol follow the paper's fixed categories.",
        "function": "compute_obs",
        "extra_params": [
            {"name": "respondent_id", "label": "参与者 ID", "label_en": "Respondent ID", "required": True},
            {"name": "gender", "label": "性别 (1=男, 2=女)", "label_en": "Gender (1=Male, 2=Female)", "required": True}
        ],
        "groups": [
            {
                "name": "饮食抗氧化因子",
                "name_en": "Dietary Antioxidant Factors",
                "params": [
                    {"name": "fiber", "label": "膳食纤维 (g/day)", "label_en": "Dietary Fiber (g/day)", "unit": "g/day", "required": True},
                    {"name": "carotene_re", "label": "胡萝卜素 RE (ug/day)", "label_en": "Carotene RE (ug/day)", "unit": "ug/day", "required": True},
                    {"name": "vitamin_b2", "label": "维生素 B2 / 核黄素 (mg/day)", "label_en": "Vitamin B2 / Riboflavin (mg/day)", "unit": "mg/day", "required": True},
                    {"name": "niacin", "label": "烟酸 (mg/day)", "label_en": "Niacin (mg/day)", "unit": "mg/day", "required": True},
                    {"name": "total_folate", "label": "总叶酸 (ug/day)", "label_en": "Total Folate (ug/day)", "unit": "ug/day", "required": True},
                    {"name": "calcium", "label": "钙 (mg/day)", "label_en": "Calcium (mg/day)", "unit": "mg/day", "required": True},
                    {"name": "zinc", "label": "锌 (mg/day)", "label_en": "Zinc (mg/day)", "unit": "mg/day", "required": True},
                    {"name": "magnesium", "label": "镁 (mg/day)", "label_en": "Magnesium (mg/day)", "unit": "mg/day", "required": True},
                    {"name": "copper", "label": "铜 (mg/day)", "label_en": "Copper (mg/day)", "unit": "mg/day", "required": True},
                    {"name": "selenium", "label": "硒 (ug/day)", "label_en": "Selenium (ug/day)", "unit": "ug/day", "required": True},
                    {"name": "vitamin_b6", "label": "维生素 B6 (mg/day)", "label_en": "Vitamin B6 (mg/day)", "unit": "mg/day", "required": True},
                    {"name": "vitamin_b12", "label": "维生素 B12 (ug/day)", "label_en": "Vitamin B12 (ug/day)", "unit": "ug/day", "required": True},
                    {"name": "vitamin_c", "label": "维生素 C (mg/day)", "label_en": "Vitamin C (mg/day)", "unit": "mg/day", "required": True},
                    {"name": "vitamin_e", "label": "维生素 E (mg/day)", "label_en": "Vitamin E (mg/day)", "unit": "mg/day", "required": True}
                ]
            },
            {
                "name": "促氧化与生活方式因子",
                "name_en": "Pro-oxidant and Lifestyle Factors",
                "params": [
                    {"name": "iron", "label": "铁 (mg/day)", "label_en": "Iron (mg/day)", "unit": "mg/day", "required": True},
                    {"name": "total_fat", "label": "总脂肪 (g/day)", "label_en": "Total Fat (g/day)", "unit": "g/day", "required": True},
                    {"name": "bmi", "label": "BMI (kg/m²)", "label_en": "BMI (kg/m²)", "unit": "kg/m²", "required": True},
                    {"name": "cotinine", "label": "Cotinine (ng/mL)", "label_en": "Cotinine (ng/mL)", "unit": "ng/mL", "required": True},
                    {"name": "physical_activity_met", "label": "体力活动 (MET-min/week)", "label_en": "Physical Activity (MET-min/week)", "unit": "MET-min/week", "required": True},
                    {"name": "alcohol_drinks_per_day", "label": "饮酒量 (drinks/day)", "label_en": "Alcohol (drinks/day)", "unit": "drinks/day", "required": True},
                    {"name": "alcohol_drinks_per_year", "label": "饮酒频率 (drinks/year)", "label_en": "Alcohol (drinks/year)", "unit": "drinks/year", "required": True}
                ]
            }
        ],
        "output_cols": ["OBS_ALL", "OBS_DIET", "OBS_LIFESTYLE"],
        "max_score": 40,
    },
    "E_DII": {
        "title": "经验型膳食炎症指数 (EDII)",
        "title_en": "Empirical Dietary Inflammatory Index (EDII)",
        "description": "基于 18 个食物组的论文固定权重，先将每个食物组摄入乘以权重，再求和并除以 1000。为了贴近原始论文，建议输入 servings/day。",
        "description_en": "Uses fixed paper-derived weights across 18 food groups, sums the weighted intakes, and divides by 1000. Servings/day aligned to the original paper are preferred.",
        "function": "compute_edii",
        "extra_params": [
            {"name": "respondent_id", "label": "参与者 ID", "label_en": "Respondent ID", "required": True}
        ],
        "groups": [
            {
                "name": "促炎食物组",
                "name_en": "Pro-inflammatory Food Groups",
                "params": [
                    {"name": "processed_meat", "label": "加工肉 (servings/day)", "label_en": "Processed Meat (servings/day)", "unit": "servings/day", "required": True},
                    {"name": "red_meat", "label": "红肉 (servings/day)", "label_en": "Red Meat (servings/day)", "unit": "servings/day", "required": True},
                    {"name": "organ_meat", "label": "动物内脏 (servings/day)", "label_en": "Organ Meat (servings/day)", "unit": "servings/day", "required": True},
                    {"name": "other_fish", "label": "其他鱼类 (servings/day)", "label_en": "Other Fish (servings/day)", "unit": "servings/day", "required": True},
                    {"name": "other_vegetables", "label": "其他蔬菜 (servings/day)", "label_en": "Other Vegetables (servings/day)", "unit": "servings/day", "required": True},
                    {"name": "refined_grains", "label": "精制谷物 (servings/day)", "label_en": "Refined Grains (servings/day)", "unit": "servings/day", "required": True},
                    {"name": "high_energy_beverages", "label": "高能量饮料 (servings/day)", "label_en": "High-energy Beverages (servings/day)", "unit": "servings/day", "required": True},
                    {"name": "low_energy_beverages", "label": "低能量饮料 (servings/day)", "label_en": "Low-energy Beverages (servings/day)", "unit": "servings/day", "required": True},
                    {"name": "tomatoes", "label": "番茄 (servings/day)", "label_en": "Tomatoes (servings/day)", "unit": "servings/day", "required": True}
                ]
            },
            {
                "name": "抗炎食物组",
                "name_en": "Anti-inflammatory Food Groups",
                "params": [
                    {"name": "beer", "label": "啤酒 (servings/day)", "label_en": "Beer (servings/day)", "unit": "servings/day", "required": True},
                    {"name": "wine", "label": "葡萄酒 (servings/day)", "label_en": "Wine (servings/day)", "unit": "servings/day", "required": True},
                    {"name": "tea", "label": "茶 (servings/day)", "label_en": "Tea (servings/day)", "unit": "servings/day", "required": True},
                    {"name": "coffee", "label": "咖啡 (servings/day)", "label_en": "Coffee (servings/day)", "unit": "servings/day", "required": True},
                    {"name": "dark_yellow_vegetables", "label": "深黄色蔬菜 (servings/day)", "label_en": "Dark Yellow Vegetables (servings/day)", "unit": "servings/day", "required": True},
                    {"name": "leafy_green_vegetables", "label": "绿叶蔬菜 (servings/day)", "label_en": "Leafy Green Vegetables (servings/day)", "unit": "servings/day", "required": True},
                    {"name": "snacks", "label": "零食 (servings/day)", "label_en": "Snacks (servings/day)", "unit": "servings/day", "required": True},
                    {"name": "fruit_juice", "label": "果汁 (servings/day)", "label_en": "Fruit Juice (servings/day)", "unit": "servings/day", "required": True},
                    {"name": "pizza", "label": "披萨 (servings/day)", "label_en": "Pizza (servings/day)", "unit": "servings/day", "required": True}
                ]
            }
        ],
        "output_cols": ["EDII_ALL"],
        "max_score": None,
    },
    "CHINA_DII": {
        "title": "中国膳食炎症指数 (CHINA-DII)",
        "title_en": "China Dietary Inflammatory Index (CHINA-DII)",
        "description": "沿用 DII 的中心百分位加权公式，但参考均值和标准差替换为中国成人参考表。当前实现严格按论文表 4 明确公布的 23 个参考成分复现。",
        "description_en": "Reuses the centered-percentile DII formula but substitutes the published Chinese adult reference means and SDs. The current implementation follows the 23 explicitly tabulated Table 4 components.",
        "function": "compute_china_dii",
        "extra_params": [
            {"name": "respondent_id", "label": "参与者 ID", "label_en": "Respondent ID", "required": True}
        ],
        "groups": [
            {
                "name": "能量与宏量营养素",
                "name_en": "Energy and Macronutrients",
                "params": [
                    {"name": "KCAL", "label": "能量 (kcal/day)", "label_en": "Energy (kcal/day)", "unit": "kcal", "required": False},
                    {"name": "PROTEIN", "label": "蛋白质 (g/day)", "label_en": "Protein (g/day)", "unit": "g/day", "required": False},
                    {"name": "CARB", "label": "碳水化合物 (g/day)", "label_en": "Carbohydrate (g/day)", "unit": "g/day", "required": False},
                    {"name": "TOTALFAT", "label": "总脂肪 (g/day)", "label_en": "Total Fat (g/day)", "unit": "g/day", "required": False},
                    {"name": "FIBER", "label": "膳食纤维 (g/day)", "label_en": "Dietary Fiber (g/day)", "unit": "g/day", "required": False},
                    {"name": "CHOLES", "label": "胆固醇 (mg/day)", "label_en": "Cholesterol (mg/day)", "unit": "mg/day", "required": False}
                ]
            },
            {
                "name": "脂肪酸组成",
                "name_en": "Fatty Acids",
                "params": [
                    {"name": "SATFAT", "label": "饱和脂肪 (g/day)", "label_en": "Saturated Fat (g/day)", "unit": "g/day", "required": False},
                    {"name": "MUFA", "label": "单不饱和脂肪酸 (g/day)", "label_en": "MUFA (g/day)", "unit": "g/day", "required": False},
                    {"name": "PUFA", "label": "多不饱和脂肪酸 (g/day)", "label_en": "PUFA (g/day)", "unit": "g/day", "required": False}
                ]
            },
            {
                "name": "维生素",
                "name_en": "Vitamins",
                "params": [
                    {"name": "FOLICACID", "label": "叶酸 (ug/day)", "label_en": "Folic Acid (ug/day)", "unit": "ug/day", "required": False},
                    {"name": "VITA", "label": "维生素 A (RE/day)", "label_en": "Vitamin A (RE/day)", "unit": "RE", "required": False},
                    {"name": "THIAMIN", "label": "维生素 B1 / 硫胺素 (mg/day)", "label_en": "Vitamin B1 / Thiamin (mg/day)", "unit": "mg/day", "required": False},
                    {"name": "RIBOFLAVIN", "label": "维生素 B2 / 核黄素 (mg/day)", "label_en": "Vitamin B2 / Riboflavin (mg/day)", "unit": "mg/day", "required": False},
                    {"name": "NIACIN", "label": "烟酸 (mg/day)", "label_en": "Niacin (mg/day)", "unit": "mg/day", "required": False},
                    {"name": "VITB6", "label": "维生素 B6 (mg/day)", "label_en": "Vitamin B6 (mg/day)", "unit": "mg/day", "required": False},
                    {"name": "VITB12", "label": "维生素 B12 (ug/day)", "label_en": "Vitamin B12 (ug/day)", "unit": "ug/day", "required": False},
                    {"name": "VITC", "label": "维生素 C (mg/day)", "label_en": "Vitamin C (mg/day)", "unit": "mg/day", "required": False},
                    {"name": "VITD", "label": "维生素 D (ug/day)", "label_en": "Vitamin D (ug/day)", "unit": "ug/day", "required": False},
                    {"name": "VITE", "label": "维生素 E (mg/day)", "label_en": "Vitamin E (mg/day)", "unit": "mg/day", "required": False}
                ]
            },
            {
                "name": "矿物质",
                "name_en": "Minerals",
                "params": [
                    {"name": "ZN", "label": "锌 (mg/day)", "label_en": "Zinc (mg/day)", "unit": "mg/day", "required": False},
                    {"name": "MG", "label": "镁 (mg/day)", "label_en": "Magnesium (mg/day)", "unit": "mg/day", "required": False},
                    {"name": "IRON", "label": "铁 (mg/day)", "label_en": "Iron (mg/day)", "unit": "mg/day", "required": False},
                    {"name": "SE", "label": "硒 (ug/day)", "label_en": "Selenium (ug/day)", "unit": "ug/day", "required": False}
                ]
            }
        ],
        "output_cols": ["CHINADII_ALL"],
        "max_score": None,
    },
}
