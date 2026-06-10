"""
所有膳食指数参数定义

参考 dietaryindex R 包各函数签名。
"""

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
                    {"name": "sodium", "label": "钠 (g/1000kcal)", "label_en": "Sodium (g/1000kcal)", "unit": "g/1000kcal", "required": True},
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
        "description": "根据每日消耗的食物和营养素分量，计算 HEI2020 膳食指数（健康饮食指数 2020 及 HEI-Toddlers-2020）。此版本使用原始 HEI2020 算法，其中添加糖和饱和脂肪使用占总能量的百分比（% energy）输入，钠以克（g，在计算分量时系统会以 g/1000kcal 换算）为单位输入。总分 0-100。",
        "description_en": "Calculate the HEI-2020 dietary index (Healthy Eating Index 2020 and HEI-Toddlers-2020) based on daily food and nutrient intake. This version uses the original HEI-2020 algorithm with added sugar and saturated fat entered as percentage of total energy (% energy), and sodium in grams (g, converted by the system to g/1000kcal). Total score 0-100.",
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
                    {"name": "sodium", "label": "钠 (g/1000kcal)", "label_en": "Sodium (g/1000kcal)", "unit": "g/1000kcal", "required": True},
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
        "description": "基于 EAT-Lancet 报告，含 15 个组分。支持性别差异（全谷物）。总分 0-150。",
        "description_en": "Based on the EAT-Lancet report with 15 components. Supports sex-specific handling (whole grains). Total score 0-150.",
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
        "max_score": 150,
    },

    "PHDI_V1": {
        "title": "行星健康饮食指数 V1 (PHDI V1)",
        "title_en": "Planetary Health Diet Index V1",
        "description": "根据每日消耗的食物和营养素分量计算行星健康饮食指数（PHDI），用于评估对 EAT-Lancet 报告中参考膳食的依从性。在此版本（V1）中，添加不饱和脂肪、添加饱和与反式脂肪、添加糖三个组分以占每日总能量的百分比（% kcal）直接输入。总分 0-150。",
        "description_en": "Calculate the Planetary Health Diet Index (PHDI) based on daily food and nutrient intake to assess adherence to the EAT-Lancet reference diet. In V1, added unsaturated fats, added saturated & trans fats, and added sugars are entered as percentage of daily energy (% kcal). Total score 0-150.",
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
        "max_score": 150,
    },

    "PHDI_V2": {
        "title": "行星健康饮食指数 V2 (PHDI V2)",
        "title_en": "Planetary Health Diet Index V2",
        "description": "根据每日消耗的食物和营养素分量计算行星健康饮食指数（PHDI），该指数可量化对 EAT-Lancet 报告中参考膳食的依从性。与 V1 不同，此版本（V2）中所有的添加不饱和脂肪、添加饱和及反式脂肪、添加糖变量均直接以每日摄入克数（g/day）为单位进行输入，系统会自动根据每日总能量（TOTALKCAL_PHDI）将其换算为能量占比百分比（% kcal）。总分 0-150。",
        "description_en": "Calculate the Planetary Health Diet Index (PHDI) quantifying adherence to the EAT-Lancet reference diet. Unlike V1, V2 accepts added unsaturated fats, added saturated & trans fats, and added sugars directly in grams/day (g/day). The system auto-converts to energy percentage (% kcal) based on total energy (TOTALKCAL_PHDI). Total score 0-150.",
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
        "max_score": 150,
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
        "description": "8 个组分，性别分层四等分评分。总分 0-15。",
        "description_en": "8 components, sex-stratified quartile scoring. Total score 0-15.",
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
        "max_score": 15,
    },

    "ACS2020_V1": {
        "title": "ACS 2020 癌症协会饮食指数 V1",
        "title_en": "ACS 2020 Cancer Society Index V1",
        "description": "根据每日消耗的食物肉类及能量比例，计算美国癌症协会 2020 膳食指数（ACS 2020），评估蔬菜、水果、全谷物、红肉及加工肉类、含糖饮料组分。此版本使用高加工食品和精制谷物占每日总能量的百分比（% kcal）来计算该组分评分，是官方推荐首选的 ACS 2020 膳食评分计算方法。总分 0-15。",
        "description_en": "Calculate the ACS 2020 Dietary Index based on daily food and energy intake, assessing vegetables, fruits, whole grains, red & processed meat, and SSBs. This version uses highly processed foods and refined grains as percentage of daily energy (% kcal) — the officially recommended ACS 2020 scoring method. Total score 0-15.",
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
        "max_score": 15,
    },

    "ACS2020_V2": {
        "title": "ACS 2020 癌症协会饮食指数 V2",
        "title_en": "ACS 2020 Cancer Society Index V2",
        "description": "根据每日消耗的食物和营养素分量，计算美国癌症协会 2020 膳食指数版本 2（ACS 2020 V2）。与 V1 使用能量占比不同，此版本的高加工食品和精制谷物组分使用每 1000 kcal 每日消耗的份数（servings/d per 1000 kcal）进行计算，并使用总热量进行标准化。总分 0-15。",
        "description_en": "Calculate the ACS 2020 Dietary Index V2 based on daily food and nutrient intake. Unlike V1 which uses energy percentage, V2 computes highly processed foods and refined grains as servings per 1000 kcal, standardized by total energy. Total score 0-15.",
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
        "max_score": 15,
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
}
