"""Authoritative literature attached to each public dietary-index page.

The registry intentionally stores structured citation data instead of rendered
HTML so that the API, Next.js frontend, Python clients, and future exports all
use the same source of truth.
"""

from __future__ import annotations

from copy import deepcopy


def _reference(
    authors: str,
    title: str,
    journal: str,
    year: int,
    *,
    volume_pages: str = "",
    doi: str = "",
    pmid: str = "",
    url: str = "",
    role_zh: str = "指标开发与评分依据",
    role_en: str = "Index development and scoring basis",
) -> dict:
    if not url:
        if doi:
            url = f"https://doi.org/{doi}"
        elif pmid:
            url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
    return {
        "authors": authors,
        "title": title,
        "journal": journal,
        "year": year,
        "volume_pages": volume_pages,
        "doi": doi,
        "pmid": pmid,
        "url": url,
        "role_zh": role_zh,
        "role_en": role_en,
    }


INDEX_LITERATURE: dict[str, list[dict]] = {
    "DII": [
        _reference(
            "Shivappa N, Steck SE, Hurley TG, Hussey JR, Hébert JR",
            "Designing and developing a literature-derived, population-based dietary inflammatory index",
            "Public Health Nutrition",
            2014,
            volume_pages="17(8):1689–1696",
            doi="10.1017/S1368980013002115",
            pmid="23941862",
        )
    ],
    "HEI2020": [
        _reference(
            "Shams-White MM, et al.",
            "Healthy Eating Index-2020: Review and Update Process to Reflect the Dietary Guidelines for Americans, 2020–2025",
            "Journal of the Academy of Nutrition and Dietetics",
            2023,
            volume_pages="123(9):1280–1288",
            doi="10.1016/j.jand.2023.05.015",
            role_zh="HEI-2020 官方更新与评分依据",
            role_en="Official HEI-2020 update and scoring basis",
        )
    ],
    "HEI2015": [
        _reference(
            "Krebs-Smith SM, Pannucci TE, Subar AF, et al.",
            "Update of the Healthy Eating Index: HEI-2015",
            "Journal of the Academy of Nutrition and Dietetics",
            2018,
            volume_pages="118(9):1591–1602",
            doi="10.1016/j.jand.2018.05.021",
            pmid="30146071",
        )
    ],
    "AHEI": [
        _reference(
            "Chiuve SE, Fung TT, Rimm EB, et al.",
            "Alternative Dietary Indices Both Strongly Predict Risk of Chronic Disease",
            "The Journal of Nutrition",
            2012,
            volume_pages="142(6):1009–1018",
            doi="10.3945/jn.111.157222",
            pmid="22513989",
            role_zh="AHEI-2010 评分定义与验证",
            role_en="AHEI-2010 scoring definition and validation",
        ),
        _reference(
            "McCullough ML, Feskanich D, Stampfer MJ, et al.",
            "Diet quality and major chronic disease risk in men and women: moving toward improved dietary guidance",
            "The American Journal of Clinical Nutrition",
            2002,
            volume_pages="76(6):1261–1271",
            doi="10.1093/ajcn/76.6.1261",
            role_zh="原始 AHEI 开发论文",
            role_en="Original AHEI development paper",
        ),
    ],
    "AHEIP": [
        _reference(
            "Rifas-Shiman SL, Rich-Edwards JW, Kleinman KP, Oken E, Gillman MW",
            "Dietary quality during pregnancy varies by maternal characteristics in Project Viva",
            "Journal of the American Dietetic Association",
            2009,
            volume_pages="109(6):1004–1011",
            doi="10.1016/j.jada.2009.03.001",
            role_zh="孕期替代健康饮食指数（AHEI-P）定义",
            role_en="Alternate Healthy Eating Index for Pregnancy definition",
        )
    ],
    "PHDI": [
        _reference(
            "Cacau LT, De Carli E, de Carvalho AM, et al.",
            "Development and Validation of an Index Based on EAT-Lancet Recommendations: The Planetary Health Diet Index",
            "Nutrients",
            2021,
            volume_pages="13(5):1698",
            doi="10.3390/nu13051698",
            pmid="34069840",
        ),
        _reference(
            "Willett W, Rockström J, Loken B, et al.",
            "Food in the Anthropocene: the EAT-Lancet Commission on healthy diets from sustainable food systems",
            "The Lancet",
            2019,
            volume_pages="393(10170):447–492",
            doi="10.1016/S0140-6736(18)31788-4",
            role_zh="EAT-Lancet 参考膳食",
            role_en="EAT-Lancet reference diet",
        ),
    ],
    "DASH": [
        _reference(
            "Fung TT, Chiuve SE, McCullough ML, Rexrode KM, Logroscino G, Hu FB",
            "Adherence to a DASH-Style Diet and Risk of Coronary Heart Disease and Stroke in Women",
            "Archives of Internal Medicine",
            2008,
            volume_pages="168(7):713–720",
            doi="10.1001/archinte.168.7.713",
            role_zh="流行病学 DASH 评分定义",
            role_en="Epidemiologic DASH score definition",
        ),
        _reference(
            "Appel LJ, Moore TJ, Obarzanek E, et al.",
            "A Clinical Trial of the Effects of Dietary Patterns on Blood Pressure",
            "New England Journal of Medicine",
            1997,
            volume_pages="336(16):1117–1124",
            doi="10.1056/NEJM199704173361601",
            role_zh="DASH 原始临床试验",
            role_en="Original DASH clinical trial",
        ),
    ],
    "DASHI": [
        _reference(
            "Mellen PB, Gao SK, Vitolins MZ, Goff DC Jr",
            "Deteriorating Dietary Habits Among Adults With Hypertension: DASH Dietary Accordance, NHANES 1988–1994 and 1999–2004",
            "Archives of Internal Medicine",
            2008,
            volume_pages="168(3):308–314",
            doi="10.1001/archinternmed.2007.119",
        )
    ],
    "MED": [
        _reference(
            "Trichopoulou A, Kouris-Blazos A, Wahlqvist ML, et al.",
            "Diet and overall survival in elderly people",
            "BMJ",
            1995,
            volume_pages="311(7018):1457–1460",
            doi="10.1136/bmj.311.7018.1457",
            role_zh="原始地中海膳食评分",
            role_en="Original Mediterranean Diet Score",
        ),
        _reference(
            "Fung TT, Rexrode KM, Mantzoros CS, Manson JE, Willett WC, Hu FB",
            "Mediterranean Diet and Incidence of and Mortality From Coronary Heart Disease and Stroke in Women",
            "Circulation",
            2009,
            volume_pages="119(8):1093–1100",
            doi="10.1161/CIRCULATIONAHA.108.816736",
            role_zh="替代地中海膳食评分（aMED）",
            role_en="Alternate Mediterranean Diet Score (aMED)",
        ),
    ],
    "MEDI": [
        _reference(
            "Schröder H, Fitó M, Estruch R, et al.",
            "A Short Screener Is Valid for Assessing Mediterranean Diet Adherence among Older Spanish Men and Women",
            "The Journal of Nutrition",
            2011,
            volume_pages="141(6):1140–1145",
            doi="10.3945/jn.110.135566",
            pmid="21508208",
            role_zh="14 项 MEDAS 评分与验证",
            role_en="14-item MEDAS scoring and validation",
        ),
        _reference(
            "Estruch R, Ros E, Salas-Salvadó J, et al.",
            "Primary Prevention of Cardiovascular Disease with a Mediterranean Diet Supplemented with Extra-Virgin Olive Oil or Nuts",
            "New England Journal of Medicine",
            2018,
            volume_pages="378:e34",
            doi="10.1056/NEJMoa1800389",
            role_zh="PREDIMED 临床试验",
            role_en="PREDIMED clinical trial",
        ),
    ],
    "ACS2020": [
        _reference(
            "Rock CL, Thomson C, Gansler T, et al.",
            "American Cancer Society guideline for diet and physical activity for cancer prevention",
            "CA: A Cancer Journal for Clinicians",
            2020,
            volume_pages="70(4):245–271",
            doi="10.3322/caac.21591",
            pmid="32515406",
            role_zh="ACS 2020 癌症预防指南",
            role_en="ACS 2020 cancer prevention guideline",
        ),
        _reference(
            "McCullough ML, Patel AV, Kushi LH, et al.",
            "Association Between Adherence to the American Cancer Society Nutrition and Physical Activity Guidelines and Cancer Mortality",
            "JAMA Network Open",
            2022,
            volume_pages="5(5):e2211618",
            doi="10.1001/jamanetworkopen.2022.11618",
            role_zh="ACS 指南依从性评分应用与验证",
            role_en="ACS guideline adherence score application and validation",
        ),
    ],
    "DI_GM": [
        _reference(
            "Kase BE, Liese AD, Zhang J, Murphy EA, Zhao L, Steck SE",
            "The Development and Evaluation of a Literature-Based Dietary Index for Gut Microbiota",
            "Nutrients",
            2024,
            volume_pages="16(7):1045",
            doi="10.3390/nu16071045",
            pmid="38613077",
        )
    ],
    "PDI": [
        _reference(
            "Satija A, Bhupathiraju SN, Rimm EB, et al.",
            "Plant-Based Dietary Patterns and Incidence of Type 2 Diabetes in US Men and Women",
            "PLoS Medicine",
            2016,
            volume_pages="13(6):e1002039",
            doi="10.1371/journal.pmed.1002039",
            role_zh="PDI、hPDI 与 uPDI 开发论文",
            role_en="PDI, hPDI, and uPDI development paper",
        ),
        _reference(
            "Satija A, Bhupathiraju SN, Spiegelman D, et al.",
            "Healthful and Unhealthful Plant-Based Diets and the Risk of Coronary Heart Disease in U.S. Adults",
            "Journal of the American College of Cardiology",
            2017,
            volume_pages="70(4):411–422",
            doi="10.1016/j.jacc.2017.05.047",
            role_zh="健康与不健康植物性膳食评分验证",
            role_en="Healthful and unhealthful PDI validation",
        ),
    ],
    "FISI": [
        _reference(
            "Wang Z, Yuan C, Zhang Y, et al.",
            "Food inflammation index reveals the key inflammatory components in foods and heterogeneity within food groups",
            "Journal of Advanced Research",
            2025,
            volume_pages="74:87-98",
            doi="10.1016/j.jare.2024.10.010",
            pmid="39401693",
            role_zh="FII/FISI 原始开发与食物炎症数据库",
            role_en="Original FII/FISI development and food inflammation database",
        ),
        _reference(
            "Li T, Liu Y, Li J, Zhang J, Zhao H, Luo K, Gao Y, Mu J, Yang Q, Yan Z.",
            "From nutrient-based to food-based assessment: the evolution of inflammatory indices and their significance for metabolic syndrome and type 3 diabetes mellitus",
            "Frontiers in Nutrition",
            2026,
            volume_pages="",
            doi="10.3389/fnut.2026.1818219",
            role_zh="炎症指数从营养素到食物层面的综述与 FISI 应用框架",
            role_en="Review of the evolution from nutrient- to food-based inflammatory indices and the FISI application framework",
        ),
        _reference(
            "Yan Z, Luo K, Yang Q, Liu X, Zhao H, Gao Y, Zhang Q, Mu J.",
            "Investigating the association between the food inflammation scores of individuals and stroke in adults: an extreme gradient boosting machine learning model interpreted with shapley additive explanations",
            "Journal of Health, Population and Nutrition",
            2026,
            volume_pages="45:170",
            doi="10.1186/s41043-026-01342-6",
            role_zh="FISI 与成人卒中关联的 NHANES 验证研究",
            role_en="NHANES validation study of FISI and stroke in adults",
        ),
        _reference(
            "Li T, Yang Q, Zeng X, Yu H, Mu J, Yan Z, Tang Y.",
            "Association between food inflammation scores of individuals and sarcopenia in U.S. adults: a cross-sectional study from NHANES 2011–2018",
            "Experimental Gerontology",
            2026,
            volume_pages="213:113004",
            doi="10.1016/j.exger.2025.113004",
            role_zh="FISI34、FISI26-USDA 与 FISI26-CHINA 的 NHANES 验证研究",
            role_en="NHANES validation of FISI34, FISI26-USDA, and FISI26-CHINA",
        ),
    ],
    "MIND": [
        _reference(
            "Morris MC, Tangney CC, Wang Y, et al.",
            "MIND diet slows cognitive decline with aging",
            "Alzheimer's & Dementia",
            2015,
            volume_pages="11(9):1015–1022",
            doi="10.1016/j.jalz.2015.04.011",
            pmid="26086182",
            role_zh="MIND 膳食评分定义与认知验证",
            role_en="MIND diet scoring definition and cognitive validation",
        )
    ],
    "DQI_I": [
        _reference(
            "Kim S, Haines PS, Siega-Riz AM, Popkin BM",
            "The Diet Quality Index-International (DQI-I) provides an effective tool for cross-national comparison of diet quality as illustrated by China and the United States",
            "The Journal of Nutrition",
            2003,
            volume_pages="133(11):3476–3484",
            doi="10.1093/jn/133.11.3476",
            pmid="14608061",
        )
    ],
    "CHEI": [
        _reference(
            "Yuan YQ, Li F, Wu H, et al.",
            "Evaluation of the Validity and Reliability of the Chinese Healthy Eating Index",
            "Nutrients",
            2018,
            volume_pages="10(2):114",
            doi="10.3390/nu10020114",
            pmid="29364173",
        )
    ],
    "DBI": [
        _reference(
            "He YN, Zhai FY, Ge KY",
            "Measuring diet quality of Chinese 18–59 years adults using Chinese Diet Balance Index",
            "Wei Sheng Yan Jiu (Journal of Hygiene Research)",
            2005,
            volume_pages="34(4):442–444",
            pmid="16229271",
            role_zh="中国膳食平衡指数原始方法与效度研究",
            role_en="Original Chinese Diet Balance Index method and validity study",
        ),
        _reference(
            "Xu X, Hall J, Byles J, Shi Z",
            "Assessing dietary quality of older Chinese people using the Chinese Diet Balance Index (DBI)",
            "PLoS ONE",
            2015,
            volume_pages="10(3):e0121618",
            doi="10.1371/journal.pone.0121618",
            pmid="25811834",
            role_zh="DBI-07 应用与方法说明",
            role_en="DBI-07 application and methodological description",
        ),
    ],
    "GDQS": [
        _reference(
            "Bromage S, Batis C, Bhupathiraju SN, et al.",
            "Development and Validation of a Novel Food-Based Global Diet Quality Score (GDQS)",
            "The Journal of Nutrition",
            2021,
            volume_pages="151(Suppl 2):75S–92S",
            doi="10.1093/jn/nxab244",
            role_zh="GDQS 原始开发与跨国验证",
            role_en="Original GDQS development and multinational validation",
        )
    ],
    "WISH": [
        _reference(
            "Trijsburg L, Talsma EF, Crispim SP, Garrett J, Kennedy G, de Vries JHM, Brouwer ID",
            "Method for the Development of WISH, a Globally Applicable Index for Healthy Diets from Sustainable Food Systems",
            "Nutrients",
            2021,
            volume_pages="13(1):93",
            doi="10.3390/nu13010093",
        )
    ],
    "NRF": [
        _reference(
            "Drewnowski A",
            "Defining Nutrient Density: Development and Validation of the Nutrient Rich Foods Index",
            "Journal of the American College of Nutrition",
            2009,
            volume_pages="28(4 Suppl):421S–426S",
            doi="10.1080/07315724.2009.10718106",
            pmid="20368382",
        )
    ],
    "NAR": [
        _reference(
            "Madden JP, Yoder MD",
            "Program Evaluation: Food Stamps and Commodity Distribution in Rural Areas of Central Pennsylvania",
            "Pennsylvania State University Agricultural Experiment Station Bulletin 780",
            1972,
            url="https://eric.ed.gov/?id=ED053857",
            role_zh="NAR/MAR 原始方法来源",
            role_en="Foundational NAR/MAR method source",
        ),
        _reference(
            "Institute of Medicine",
            "Dietary Reference Intakes: Applications in Dietary Assessment",
            "National Academies Press",
            2000,
            doi="10.17226/9956",
            role_zh="营养素充足率参考摄入量与膳食评估标准",
            role_en="Reference intake and dietary assessment standard",
        ),
    ],
    "MAR": [
        _reference(
            "Madden JP, Yoder MD",
            "Program Evaluation: Food Stamps and Commodity Distribution in Rural Areas of Central Pennsylvania",
            "Pennsylvania State University Agricultural Experiment Station Bulletin 780",
            1972,
            url="https://eric.ed.gov/?id=ED053857",
            role_zh="NAR/MAR 原始方法来源",
            role_en="Foundational NAR/MAR method source",
        ),
        _reference(
            "Institute of Medicine",
            "Dietary Reference Intakes: Applications in Dietary Assessment",
            "National Academies Press",
            2000,
            doi="10.17226/9956",
            role_zh="营养素充足率参考摄入量与膳食评估标准",
            role_en="Reference intake and dietary assessment standard",
        ),
    ],
    "INQ": [
        _reference(
            "Sorenson AW, Wyse BW, Wittwer AJ, Hansen RG",
            "An Index of Nutritional Quality for a balanced diet. New help for an old problem",
            "Journal of the American Dietetic Association",
            1976,
            volume_pages="68(3):236–242",
            pmid="55430",
        )
    ],
    "PRAL": [
        _reference(
            "Remer T, Manz F",
            "Potential renal acid load of foods and its influence on urine pH",
            "Journal of the American Dietetic Association",
            1995,
            volume_pages="95(7):791–797",
            doi="10.1016/S0002-8223(95)00219-7",
            pmid="7797810",
            role_zh="PRAL 公式原始论文",
            role_en="Original PRAL formula paper",
        )
    ],
    "NEAP": [
        _reference(
            "Frassetto LA, Todd KM, Morris RC Jr, Sebastian A",
            "Estimation of net endogenous noncarbonic acid production in humans from diet potassium and protein contents",
            "The American Journal of Clinical Nutrition",
            1998,
            volume_pages="68(3):576–583",
            doi="10.1093/ajcn/68.3.576",
            pmid="9734733",
            role_zh="NEAP 公式原始论文",
            role_en="Original NEAP formula paper",
        )
    ],
    "CDAI": [
        _reference(
            "Wright ME, Mayne ST, Stolzenberg-Solomon RZ, et al.",
            "Development of a comprehensive dietary antioxidant index and application to lung cancer risk in a cohort of male smokers",
            "American Journal of Epidemiology",
            2004,
            volume_pages="160(1):68–76",
            doi="10.1093/aje/kwh173",
            pmid="15229119",
        )
    ],
    "OBS": [
        _reference(
            "Chen X, Wu Z, Hou X, et al.",
            "Association of the oxidative balance score and chronic kidney disease: insights from the national health and nutrition examination survey 2009-2018",
            "Frontiers in Nutrition",
            2024,
            volume_pages="11:1429191",
            doi="10.3389/fnut.2024.1429191",
            pmid="39399530",
            role_zh="本项目 20 组分 OBS 评分依据",
            role_en="Basis for the 20-component OBS implemented here",
        ),
        _reference(
            "Hernández-Ruiz Á, García-Villanova B, Guerra-Hernández EJ, et al.",
            "Oxidative Balance Scores Integrating Nutrient, Food and Lifestyle Dimensions: Development of the NutrientL-OBS and FoodL-OBS",
            "Antioxidants",
            2022,
            volume_pages="11(2):300",
            doi="10.3390/antiox11020300",
            pmid="35204183",
            role_zh="OBS 方法学开发与生物标志物验证",
            role_en="OBS methodological development and biomarker validation",
        ),
    ],
    "E_DII": [
        _reference(
            "Tabung FK, Smith-Warner SA, Chavarro JE, et al.",
            "Development and Validation of an Empirical Dietary Inflammatory Index",
            "The Journal of Nutrition",
            2016,
            volume_pages="146(8):1560–1570",
            doi="10.3945/jn.115.228718",
            pmid="27358416",
        )
    ],
    "CHINA_DII": [
        _reference(
            "Chen Y, Luo Z, Cheng L, et al.",
            "Development and Validation of the China Dietary Inflammatory Index (CHINA-DII)",
            "Nutrients",
            2025,
            volume_pages="17(10):1687",
            doi="10.3390/nu17101687",
            pmid="40431426",
        )
    ],
}


REFERENCE_ALIASES = {
    "HEI2020_V1": "HEI2020",
    "HEI2020_V2": "HEI2020",
    "PHDI_V1": "PHDI",
    "PHDI_V2": "PHDI",
    "MEDI_V1": "MEDI",
    "MEDI_V2": "MEDI",
    "ACS2020_V1": "ACS2020",
    "ACS2020_V2": "ACS2020",
    "HPDI": "PDI",
    "UPDI": "PDI",
}


def get_index_literature(index_key: str) -> list[dict]:
    """Return a safe copy of the literature for one public index key."""

    canonical_key = REFERENCE_ALIASES.get(index_key, index_key)
    return deepcopy(INDEX_LITERATURE.get(canonical_key, []))


def missing_literature(index_keys) -> list[str]:
    """Return public index keys that have no registered references."""

    return [key for key in index_keys if not get_index_literature(key)]
