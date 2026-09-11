# 膳食指数分类方案（Proposed Taxonomy v1）

> 目的：为 DietaryIndex-Py 的 32 个基础指数 + 8 个显式版本提供一套**科学自洽、可扩展、可落地**的分类体系。
> 现状问题：现行 `INDEX_FAMILY_REGISTRY`（13 个 family）在同一层级混用了 4 种互不兼容的划分标准（机制/结局、模式/地域、谱系/方法、时序/成熟度）；且该元数据**当前并未被任何活跃代码或前端消费**，前端导航使用独立的硬编码分组。本方案用一个"5 域 + 16 家族 + 横切标签"的结构替换它。

---

## 1. 设计原则

| 编号 | 原则 | 说明 |
|---|---|---|
| P1 | **单一主轴** | 一级分类只用一个维度：该指数"回答膳食的哪一类科学问题（主题域）"。不再混入发布机构、地域、时序。 |
| P2 | **地域/机制/输入层级降为标签** | 地域会横切所有主题（CHEI 既是质量也是中国），因此 `region`、`mechanism`、`input_level`、`scoring_basis` 一律作为 **tag**，不占分类层。 |
| P3 | **家族 = 同源谱系** | 同一家族内的指标应来自同一文献谱系或同一方法学，可同页并列比较（如 HEI-2015/2020、PDI/hPDI/uPDI）。 |
| P4 | **MECE** | 每个指标恰好属于一个主题域，无重叠、无遗漏。 |
| P5 | **可扩展** | 新增指数时只需落到已有域下的某家族，或新增一个小家族，不需要重排导航。 |
| P6 | **二维导航** | 一级按主题域（稳定），二级按家族（可增长）；地域/机制通过筛选器（tag filter）呈现。 |

---

## 2. 方案总览：5 域 / 16 家族 / 32 指标

| 域 | domain_key | 家族（family） | 成员 | 数 |
|---|---|---|---|---:|
| **① 膳食质量与指南依从** | `diet_quality` | HEI 系列 | HEI-2015, HEI-2020 | 2 |
| | | AHEI 系列 | AHEI, AHEI-P | 2 |
| | | 综合评价 | DQI-I, CHEI | 2 |
| | | 指南依从 / 人群监测 | ACS2020, GDQS | 2 |
| **② 膳食模式** | `dietary_pattern` | 地中海模式 | MED, MEDI | 2 |
| | | 植物性模式 | PDI, hPDI, uPDI | 3 |
| | | DASH 模式 | DASH, DASHI | 2 |
| | | 神经保护模式 | MIND | 1 |
| | | 膳食平衡 | DBI | 1 |
| **③ 膳食-生理机制** | `diet_mechanism` | 炎症 | DII, E-DII, FISI, CHINA-DII | 4 |
| | | 氧化应激与抗氧化 | CDAI, OBS | 2 |
| | | 酸碱负荷 | PRAL, NEAP | 2 |
| | | 肠道微生物 | DI-GM | 1 |
| **④ 营养素充足与密度** | `nutrient` | 营养素密度 | NRF9.3, INQ | 2 |
| | | 营养素充足比 | NAR, MAR | 2 |
| **⑤ 可持续与行星健康** | `sustainability` | 行星健康 | PHDI | 1 |
| | | 可持续健康 | WISH | 1 |

合计：8 + 9 + 9 + 4 + 2 = **32** ✓

> 与旧方案相比的主要变化：`emerging`（仅 DI-GM）取消；`china_localized`（CHEI/DBI/CHINA-DII）拆解按主题归位，地域改为标签；`plant_based` 中的 PHDI 移入域⑤；`sustainable_global` 中的 GDQS 移入域①。

---

## 3. 完整映射（含标签）

标签取值：`region` = 通用 / CN / 地中海 / 全球 · `input` = 营养素 / 食物组 / 食物项 / 混合 · `scoring` = 固定阈值 / 固定权重 / 样本分位 / 样本中位 / 公式 / 复合

| index_key | 显示名 | 域 | 家族 | region | input | scoring |
|---|---|---|---|---|---|---|
| `HEI2020` | HEI-2020 | ① | HEI 系列 | 通用 | 食物组 | 固定阈值 |
| `HEI2015` | HEI-2015 | ① | HEI 系列 | 通用 | 食物组 | 固定阈值 |
| `AHEI` | AHEI | ① | AHEI 系列 | 通用 | 混合 | 固定阈值+十分位 |
| `AHEIP` | AHEI-P | ① | AHEI 系列 | 通用 | 混合 | 固定阈值 |
| `DQI_I` | DQI-I | ① | 综合评价 | 通用 | 混合 | 复合（多域） |
| `CHEI` | CHEI | ① | 综合评价 | **CN** | 食物组 | 固定阈值（中国） |
| `ACS2020` | ACS2020 | ① | 指南依从/人群监测 | 通用 | 食物组 | 四分位/连续 |
| `GDQS` | GDQS | ① | 指南依从/人群监测 | **全球** | 食物组 | 固定规则 |
| `MED` | MED | ② | 地中海模式 | **地中海** | 食物组 | 样本中位 |
| `MEDI` | MEDI / MEDAS | ② | 地中海模式 | **地中海** | 食物组 | 固定规则 |
| `PDI` | PDI | ② | 植物性模式 | 通用 | 食物组 | 样本五分位 |
| `HPDI` | hPDI | ② | 植物性模式 | 通用 | 食物组 | 样本五分位 |
| `UPDI` | uPDI | ② | 植物性模式 | 通用 | 食物组 | 样本五分位 |
| `DASH` | DASH | ② | DASH 模式 | 通用 | 食物组 | 样本五分位 |
| `DASHI` | DASHI | ② | DASH 模式 | 通用 | 营养素 | 样本五分位 |
| `MIND` | MIND | ② | 神经保护模式 | 通用 | 食物组 | 固定规则 |
| `DBI` | DBI | ② | 膳食平衡 | **CN** | 食物组 | 固定规则（平衡） |
| `DII` | DII | ③ | 炎症 | 通用 | 混合 | 全球参考库 |
| `FISI` | FII / FISI | ③ | 炎症 | 通用 | 混合 | NRV / 食物 FII 库 |
| `E_DII` | EDII（经验型） | ③ | 炎症 | 通用 | 食物组 | 固定权重（18 组） |
| `CHINA_DII` | CHINA-DII | ③ | 炎症 | **CN** | 营养素 | 中国参考均值/SD |
| `CDAI` | 改良六 z CDAI | ③ | 氧化应激与抗氧化 | 通用 | 营养素 | 标准化和 |
| `OBS` | OBS | ③ | 氧化应激与抗氧化 | 通用 | 膳食+生活方式 | 复合评分 |
| `PRAL` | PRAL | ③ | 酸碱负荷 | 通用 | 营养素 | 公式 |
| `NEAP` | NEAP | ③ | 酸碱负荷 | 通用 | 营养素 | 公式 |
| `DI_GM` | DI-GM | ③ | 肠道微生物 | 通用 | 食物项 | 固定规则 |
| `NRF` | NRF9.3 | ④ | 营养素密度 | 通用 | 营养素 | 固定基准（NRF9.3） |
| `INQ` | INQ | ④ | 营养素密度 | 通用 | 营养素 | 能量调整比 |
| `NAR` | NAR | ④ | 营养素充足比 | 通用 | 营养素 | NRV 比 |
| `MAR` | MAR | ④ | 营养素充足比 | 通用 | 营养素 | NAR 均值 |
| `PHDI` | PHDI | ⑤ | 行星健康 | **全球** | 食物组 | 固定目标区间 |
| `WISH` | WISH | ⑤ | 可持续健康 | **全球** | 食物组 | 固定目标 |

---

## 4. 迁移映射（旧 family → 新归属）

| 旧 family | 受影响指标 | 新归属 | 是否移动 |
|---|---|---|---|
| `inflammatory` | DII, FISI, E_DII | ③ 炎症 | 不变 |
| `hei_series` | HEI2015, HEI2020 | ① HEI 系列 | 不变 |
| `alternative_healthy` | AHEI, AHEIP | ① AHEI 系列 | 不变 |
| `nutrient_density` | NRF, NAR, MAR, INQ | ④（拆为"密度""充足比"两家族） | 域内重排 |
| `antioxidant_balance` | CDAI, OBS | ③ 氧化应激与抗氧化 | 域变更 |
| `acid_load` | PRAL, NEAP | ③ 酸碱负荷 | 域变更 |
| `disease_prevention` | DASH, DASHI | ② DASH 模式 | 域变更 |
| `disease_prevention` | ACS2020 | ① 指南依从/人群监测 | 域变更 |
| `dietary_pattern` | MED, MEDI | ② 地中海模式 | 域变更（改名） |
| `plant_based` | PDI, HPDI, UPDI | ② 植物性模式 | 域变更 |
| `plant_based` | **PHDI** | ⑤ 行星健康 | **★ 关键修正** |
| `emerging` | **DI_GM** | ③ 肠道微生物 | **★ 取消伪类别** |
| `classic_quality` | MIND | ② 神经保护模式 | 域变更 |
| `classic_quality` | DQI_I | ① 综合评价 | 域变更 |
| `sustainable_global` | **GDQS** | ① 指南依从/人群监测 | **★ 关键修正** |
| `sustainable_global` | WISH | ⑤ 可持续健康 | 域变更 |
| `china_localized` | CHEI / DBI / CHINA_DII | ① / ② / ③（region=CN） | **★ 拆解，地域降为标签** |

---

## 5. 数据模型建议

将"单层 family"升级为"域 + 家族 + 标签"，并保持向后兼容（保留 `family_key` 字段，新增 `domain_key` 与 `tags`）。

```python
# dietaryindex/reference/index_registry.py

INDEX_DOMAIN_REGISTRY = [
    {"domain_key": "diet_quality",    "label_zh": "膳食质量与指南依从", "label_en": "Diet Quality & Guideline Adherence", "order": 1},
    {"domain_key": "dietary_pattern", "label_zh": "膳食模式",           "label_en": "Dietary Patterns",                  "order": 2},
    {"domain_key": "diet_mechanism",  "label_zh": "膳食-生理机制",      "label_en": "Diet and Mechanism",                "order": 3},
    {"domain_key": "nutrient",        "label_zh": "营养素充足与密度",   "label_en": "Nutrient Adequacy & Density",       "order": 4},
    {"domain_key": "sustainability",  "label_zh": "可持续与行星健康",   "label_en": "Sustainability & Planetary Health", "order": 5},
]

# 每个 INDEX_SPEC_REGISTRY 条目新增：
#   "domain_key": "diet_mechanism",
#   "family_key": "inflammation",        # 二级家族（原字段保留，值收敛到 16 个）
#   "tags": {
#       "region": "CN",                  # 通用 / CN / 地中海 / 全球
#       "input": "nutrient",             # nutrient / food_group / food_item / mixed
#       "scoring": "fixed_weight",       # fixed_threshold / fixed_weight / quantile / median / formula / composite
#   },
```

导出函数建议同步扩展：

- `get_index_spec_table()` 增加 `domain_label_zh/en`、`tags` 列；
- `get_family_blueprint_table()` 改为按 `domain_key` 分组；
- 新增 `get_domain_blueprint_table()`：域 → 家族 → 成员 三级结构，供前端直接渲染导航。

再在服务层目录接口暴露分类字段：

```python
# dietaryindex/service/registry.py -> get_index_catalog()
{
    "index_key": ...,
    "domain_key": "diet_mechanism",
    "domain_title_zh": "膳食-生理机制",
    "family_key": "inflammation",
    "family_title_zh": "炎症",
    "tags": {...},
    ...
}
```

## 6. 前端导航建议

- **侧边栏**：5 个域作为可折叠一级分组；域内家族作为二级小标题；成员指标为叶子链接。原 13 组收敛为 5 组，认知负担显著下降。
- **计算页指标选择器**：`index-groups.ts` 从"hardcode 13 数组"改为**按 `domain_key` 生成**，同域指标可同页切换（保留现有"防止误切到无关算法"的设计意图）。
- **标签筛选器**：新增 `region`（通用 / 中国本土 / 地中海 / 全球）、`input`、`scoring` 三个筛选 chip，满足"我想看中国本土指数""我只想用固定阈值类"等查询，而无需为地域单开分类。

---

## 7. 落地影响面（已核查）

| 文件 | 需要改动 | 风险 |
|---|---|---|
| `dietaryindex/reference/index_registry.py` | 新增 `INDEX_DOMAIN_REGISTRY`；每个 spec 加 `domain_key`/`tags`；`family_key` 值收敛 | 低（**该文件当前无任何活跃引用**） |
| `dietaryindex/service/registry.py` | `get_index_catalog()`/`get_index_detail()` 输出分类字段 | 低 |
| `web_frontend/lib/index-groups.ts` | 由硬编码改为按域生成 | 中（影响计算页选择器） |
| `web_frontend/components/site-sidebar.tsx` | 13 组 → 5 域 + 家族二级 | 中（纯展示） |
| `docs/INDEX_SUPPORT_MATRIX.md`、`README.md` | 表格按域重排 | 低 |
| `tests/` | 已核查：**无测试引用 `family_key`**，无需同步（新增分类测试建议另行补） | 低 |

> 说明：经全仓检索，`INDEX_FAMILY_REGISTRY` / `family_key` 仅定义于 `dietaryindex/reference/index_registry.py`，除 `archive/` 旧版快照外**无其他引用**；前端分类来自独立的 `web_frontend/lib/index-groups.ts`。因此本方案的代码改动面小、且不触碰任何计算逻辑（`index_key` 与算法完全不变）。

---

## 8. 可选的下一步

1. 按本方案改写 `INDEX_FAMILY_REGISTRY` → `INDEX_DOMAIN_REGISTRY` + 家族 + tags（保持 32 个 `index_key` 不变）；
2. 服务层目录接口暴露分类字段；
3. 前端侧边栏与选择器切换为按域渲染；
4. 补一个分类一致性测试：断言每个 `index_key` 恰有一个域、域内家族非空、标签取值合法。
