"""
综合测试所有 12 个膳食指数算法
"""
import pandas as pd
import numpy as np
import traceback

def case(name):
    def decorator(fn):
        fn.case_name = name
        return fn
    return decorator

# 共享测试数据
n = 5
df = pd.DataFrame({
    'id': range(1, n + 1),
    'gender': [1, 2, 1, 2, 1],
    'age': [30, 25, 45, 2, 1],
    'kcal': [2200, 1800, 2500, 1200, 900],
    'total_fruit': [1.5, 2.0, 0.5, 0.8, 0.3],
    'whole_fruit': [0.8, 1.2, 0.2, 0.4, 0.1],
    'total_veg': [2.0, 2.5, 1.0, 0.6, 0.3],
    'green_bean': [0.3, 0.4, 0.1, 0.05, 0.02],
    'total_protein': [6.0, 5.0, 7.0, 3.0, 2.0],
    'seafood_plant': [1.5, 2.0, 0.5, 0.8, 0.3],
    'whole_grain': [2.0, 2.5, 1.0, 1.5, 0.5],
    'dairy': [1.5, 2.0, 0.8, 2.0, 0.5],
    'fatty_acid': [2.0, 2.5, 1.5, 1.0, 1.2],
    'refined_grain': [3.0, 2.5, 4.0, 1.5, 2.0],
    'sodium': [3000, 2500, 3500, 1800, 1200],
    'added_sugar': [40, 30, 50, 15, 10],
    'saturated_fat': [30, 25, 35, 15, 12],
    'alcohol': [0.5, 0.2, 1.5, 0, 0],
    'avocado': [0.5, 1.0, 0, 0.3, 0.5],
    'broccoli': [0.5, 1.0, 0.3, 0.5, 0.2],
    'chickpea': [0.3, 0.5, 0, 0.2, 0.1],
    'coffee': [2.0, 1.0, 3.0, 0, 0.5],
    'cranberry': [0.1, 0.2, 0, 0.1, 0.05],
    'fermented_dairy': [1.0, 1.5, 0.5, 1.0, 0.5],
    'fiber': [25, 30, 15, 20, 10],
    'green_tea': [0.5, 1.0, 0, 0.3, 0],
    'soybean': [0.3, 0.5, 0, 0.2, 0.1],
    'total_fat_pct': [30, 25, 35, 28, 32],
    'processed_meat': [1.0, 0.5, 1.5, 0.3, 0.8],
    'red_meat': [2.0, 1.0, 2.5, 0.5, 1.0],
    'ssb': [1.5, 1.0, 2.0, 0.3, 0.5],
    'nuts': [1.0, 1.5, 0.5, 0.3, 0.5],
    'legumes': [0.5, 1.0, 0.2, 0.3, 0.2],
    'fish': [0.5, 1.0, 0.2, 0.3, 0],
    'vegetable_items': [5, 7, 3, 4, 2],
    'fruit_items': [3, 4, 2, 2, 1],
    'hpf_rg_ratio': [35, 25, 45, 20, 30],
    'white_red_ratio': [1.5, 2.0, 0.5, 1.0, 0.8],
    'poly_sat_ratio': [0.5, 0.8, 0.2, 0.4, 0.3],
    'calcium': [800, 1000, 600, 900, 500],
    'folate': [400, 500, 300, 350, 200],
    'iron': [15, 20, 10, 18, 8],
    'olive_oil': [3, 6, 2, 4, 1],
    'sweets': [1.0, 0.5, 1.5, 0.3, 0.5],
    'discret_fat': [1.5, 1.0, 2.0, 0.5, 1.0],
    'starchy_veg': [100, 150, 80, 200, 50],
    'poultry': [50, 40, 60, 30, 20],
    'egg': [30, 20, 40, 25, 15],
    'soy_phdi': [20, 30, 10, 25, 5],
    'added_fat_unsat': [15, 20, 10, 12, 8],
    'added_fat_sat_trans': [8, 6, 10, 5, 7],
    'added_sugar_phdi': [20, 15, 25, 10, 12],
})

###############################################################################
@case("DII - 基本功能")
def test_dii():
    from dietaryindex import compute_dii
    r = compute_dii(
        data=df,
        respondent_id=df['id'],
        ALCOHOL=df['alcohol'],
        VITB12=df['calcium'] / 100,
        VITB6=df['iron'] / 10,
    )
    assert 'DII_ALL' in r.columns
    assert 'DII_NOETOH' in r.columns
    assert len(r) == n

@case("HEI2015 - 基本功能")
def test_hei2015():
    from dietaryindex import compute_hei2015
    r = compute_hei2015(
        data=df,
        respondent_id=df['id'],
        total_kcal=df['kcal'],
        total_fruit=df['total_fruit'],
        whole_fruit=df['whole_fruit'],
        total_vegetable=df['total_veg'],
        green_and_bean=df['green_bean'],
        total_protein=df['total_protein'],
        seafood_plant_protein=df['seafood_plant'],
        whole_grain=df['whole_grain'],
        dairy=df['dairy'],
        fatty_acid=df['fatty_acid'],
        refined_grain=df['refined_grain'],
        sodium=df['sodium'],
        added_sugar=df['added_sugar'],
        saturated_fat=df['saturated_fat'],
    )
    assert 'HEI2015_ALL' in r.columns
    assert len(r) == n
    assert r['HEI2015_ALL'].between(0, 100).all()

@case("HEI2020 - 基本功能")
def test_hei2020():
    from dietaryindex import compute_hei2020
    r = compute_hei2020(
        data=df,
        respondent_id=df['id'],
        age=df['age'],
        total_kcal=df['kcal'],
        total_fruit=df['total_fruit'],
        whole_fruit=df['whole_fruit'],
        total_vegetable=df['total_veg'],
        green_and_bean=df['green_bean'],
        total_protein=df['total_protein'],
        seafood_plant_protein=df['seafood_plant'],
        whole_grain=df['whole_grain'],
        dairy=df['dairy'],
        fatty_acid=df['fatty_acid'],
        refined_grain=df['refined_grain'],
        sodium=df['sodium'] / 1000,
        added_sugar=df['added_sugar'] / 10,
        saturated_fat=df['saturated_fat'] / 10,
    )
    assert 'HEI2020_ALL' in r.columns
    assert len(r) == n
    assert r['HEI2020_ALL'].between(0, 100).all()

@case("HEI2020_V2 - 基本功能")
def test_hei2020_v2():
    from dietaryindex import compute_hei2020_v2
    r = compute_hei2020_v2(
        data=df,
        respondent_id=df['id'],
        age=df['age'],
        total_kcal=df['kcal'],
        total_fruit=df['total_fruit'],
        whole_fruit=df['whole_fruit'],
        total_vegetable=df['total_veg'],
        green_and_bean=df['green_bean'],
        total_protein=df['total_protein'],
        seafood_plant_protein=df['seafood_plant'],
        whole_grain=df['whole_grain'],
        dairy=df['dairy'],
        fatty_acid=df['fatty_acid'],
        refined_grain=df['refined_grain'],
        sodium=df['sodium'],
        added_sugar=df['added_sugar'] / 4,
        saturated_fat=df['saturated_fat'],
    )
    assert 'HEI2020_ALL' in r.columns

@case("AHEI - 基本功能")
def test_ahei():
    from dietaryindex import compute_ahei
    r = compute_ahei(
        data=df,
        respondent_id=df['id'],
        gender=df['gender'],
        total_kcal=df['kcal'],
        vegetable=df['total_veg'],
        fruit=df['whole_fruit'],
        whole_grain=df['whole_grain'] * 30,
        nut_legume=df['nuts'],
        n3_fat=df['fish'] * 100,
        pufa=df['fatty_acid'] * 2,
        ssb_fruit_juice=df['ssb'],
        red_processed_meat=df['red_meat'] / 2,
        trans_fat=df['saturated_fat'] / 15,
        sodium=df['sodium'],
        alcohol=df['alcohol'],
    )
    assert 'AHEI_ALL' in r.columns
    assert 'AHEI_NOETOH' in r.columns
    assert len(r) == n

@case("AHEIP - 基本功能")
def test_aheip():
    from dietaryindex import compute_aheip
    r = compute_aheip(
        data=df,
        respondent_id=df['id'],
        vegetable=df['total_veg'],
        fruit=df['whole_fruit'],
        white_red_ratio=df['white_red_ratio'],
        fiber=df['fiber'],
        trans_fat=df['saturated_fat'] / 15,
        poly_sat_ratio=df['poly_sat_ratio'],
        calcium=df['calcium'],
        folate=df['folate'],
        iron=df['iron'],
    )
    assert 'AHEIP_ALL' in r.columns

@case("DASH - 基本功能")
def test_dash():
    from dietaryindex import compute_dash
    r = compute_dash(
        data=df,
        respondent_id=df['id'],
        total_kcal=df['kcal'],
        fruit_fruit_juice=df['total_fruit'],
        vegetable=df['total_veg'],
        nut_legume=df['nuts'],
        whole_grain=df['whole_grain'],
        low_fat_dairy=df['dairy'],
        sodium=df['sodium'],
        red_processed_meat=df['red_meat'],
        ssb_fruit_juice=df['ssb'],
    )
    assert 'DASH_ALL' in r.columns
    assert r['DASH_ALL'].between(8, 40).all()

@case("DASHI - 基本功能")
def test_dashi():
    from dietaryindex import compute_dashi
    r = compute_dashi(
        data=df,
        respondent_id=df['id'],
        total_kcal=df['kcal'],
        total_fat_pct=np.ones(n) * 30,
        sat_fat_pct=np.ones(n) * 10,
        protein_pct=np.ones(n) * 16,
        cholesterol=df['kcal'] / 10,
        fiber=df['fiber'],
        potassium=df['calcium'] * 3,
        magnesium=df['calcium'],
        calcium=df['calcium'],
        sodium=df['sodium'],
    )
    assert 'DASHI_ALL' in r.columns

@case("MED - 基本功能")
def test_med():
    from dietaryindex import compute_med
    r = compute_med(
        data=df,
        respondent_id=df['id'],
        fruit_fruit_juice=df['total_fruit'],
        vegetable=df['total_veg'],
        whole_grain=df['whole_grain'],
        legumes=df['legumes'],
        nuts=df['nuts'],
        fish=df['fish'],
        red_processed_meat=df['red_meat'],
        mon_sat_fat_ratio=df['fatty_acid'],
        alcohol=df['alcohol'],
    )
    assert 'MED_ALL' in r.columns
    assert 'MED_NOETOH' in r.columns

@case("MEDI - 基本功能")
def test_medi():
    from dietaryindex import compute_medi
    r = compute_medi(
        data=df,
        respondent_id=df['id'],
        olive_oil=df['olive_oil'],
        fruit=df['whole_fruit'] * 4,
        vegetable=df['total_veg'] * 2,
        legumes=df['legumes'],
        nuts=df['nuts'],
        fish_seafood=df['fish'],
        alcohol=df['alcohol'] * 2,
        ssb=df['ssb'],
        sweets=df['sweets'],
        discret_fat=df['discret_fat'],
        red_processed_meat=df['red_meat'],
    )
    assert 'MEDI_ALL' in r.columns

@case("MEDI_V2 - 基本功能")
def test_medi_v2():
    from dietaryindex import compute_medi_v2
    r = compute_medi_v2(
        data=df,
        respondent_id=df['id'],
        olive_oil=df['olive_oil'],
        fruit=df['whole_fruit'] * 4,
        vegetable=df['total_veg'] * 2,
        legumes=df['legumes'],
        nuts=df['nuts'],
        fish_seafood=df['fish'],
        alcohol=df['alcohol'] * 2,
        ssb=df['ssb'],
        sweets=df['sweets'],
        discret_fat=df['discret_fat'],
        red_processed_meat=df['red_meat'],
    )
    assert 'MEDI_V2_ALL' in r.columns

@case("ACS2020_V1 - 基本功能")
def test_acs2020_v1():
    from dietaryindex import compute_acs2020_v1
    r = compute_acs2020_v1(
        data=df,
        respondent_id=df['id'],
        gender=df['gender'],
        vegetable=df['total_veg'],
        vegetable_items=df['vegetable_items'],
        fruit=df['whole_fruit'],
        fruit_items=df['fruit_items'],
        whole_grain=df['whole_grain'],
        red_processed_meat=df['red_meat'],
        hpf_rg_ratio=df['hpf_rg_ratio'],
        ssb_fruit_juice=df['ssb'],
    )
    assert 'ACS2020_V1_ALL' in r.columns

@case("ACS2020_V2 - 基本功能")
def test_acs2020_v2():
    from dietaryindex import compute_acs2020_v2
    r = compute_acs2020_v2(
        data=df,
        respondent_id=df['id'],
        gender=df['gender'],
        total_kcal=df['kcal'],
        vegetable=df['total_veg'],
        vegetable_items=df['vegetable_items'],
        fruit=df['whole_fruit'],
        fruit_items=df['fruit_items'],
        whole_grain=df['whole_grain'],
        red_processed_meat=df['red_meat'],
        hpf_servings=df['hpf_rg_ratio'] / 10.0,
        ssb_fruit_juice=df['ssb'],
    )
    assert 'ACS2020_V2_ALL' in r.columns
    assert 'TOTALKCAL_ACS2020' in r.columns

@case("PHDI - 基本功能")
def test_phdi():
    from dietaryindex import compute_phdi
    r = compute_phdi(
        data=df,
        respondent_id=df['id'],
        gender=df['gender'],
        total_kcal=df['kcal'],
        whole_grain=df['whole_grain'] * 30,
        starchy_veg=df['starchy_veg'],
        vegetable=df['total_veg'] * 50,
        fruit=df['whole_fruit'] * 50,
        dairy=df['dairy'] * 100,
        red_processed_meat=df['red_meat'] * 50,
        poultry=df['poultry'],
        egg=df['egg'],
        fish=df['fish'] * 10,
        nuts=df['nuts'] * 10,
        legumes=df['legumes'] * 20,
        soy=df['soy_phdi'],
        added_fat_unsat=df['added_fat_unsat'],
        added_fat_sat_trans=df['added_fat_sat_trans'],
        added_sugar=df['added_sugar_phdi'],
    )
    assert 'PHDI_ALL' in r.columns

@case("PHDI_V2 - 基本功能")
def test_phdi_v2():
    from dietaryindex import compute_phdi_v2
    r = compute_phdi_v2(
        data=df,
        respondent_id=df['id'],
        gender=df['gender'],
        total_kcal=df['kcal'],
        whole_grain=df['whole_grain'] * 30,
        starchy_veg=df['starchy_veg'],
        vegetable=df['total_veg'] * 50,
        fruit=df['whole_fruit'] * 50,
        dairy=df['dairy'] * 100,
        red_processed_meat=df['red_meat'] * 50,
        poultry=df['poultry'],
        egg=df['egg'],
        fish=df['fish'] * 10,
        nuts=df['nuts'] * 10,
        legumes=df['legumes'] * 20,
        soy=df['soy_phdi'],
        added_fat_unsat=df['added_fat_unsat'] * 2,
        added_fat_sat_trans=df['added_fat_sat_trans'] / 2,
        added_sugar=df['added_sugar_phdi'] / 2,
    )
    assert 'PHDI_ALL' in r.columns

@case("DI_GM - 基本功能")
def test_di_gm():
    from dietaryindex import compute_di_gm
    r = compute_di_gm(
        data=df,
        respondent_id=df['id'],
        gender=df['gender'],
        avocado=df['avocado'],
        broccoli=df['broccoli'],
        chickpea=df['chickpea'],
        coffee=df['coffee'],
        cranberry=df['cranberry'],
        fermented_dairy=df['fermented_dairy'],
        fiber=df['fiber'],
        green_tea=df['green_tea'],
        soybean=df['soybean'],
        whole_grain=df['whole_grain'],
        total_fat_pct=df['total_fat_pct'],
        processed_meat=df['processed_meat'],
        red_meat=df['red_meat'],
        refined_grain=df['refined_grain'],
    )
    assert 'DI_GM_TOTAL' in r.columns
    assert r['DI_GM_TOTAL'].between(0, 14).all()

@case("导入测试 - 检查所有公开API")
def test_imports():
    import dietaryindex
    expected = [
        'compute_dii', 'compute_hei2015', 'compute_hei2020', 'compute_hei2020_v2',
        'compute_ahei', 'compute_aheip', 'compute_dash', 'compute_dashi',
        'compute_med', 'compute_medi', 'compute_acs2020_v1', 'compute_acs2020_v2',
        'compute_phdi', 'compute_phdi_v2', 'compute_phdi_nhanes_fped', 'compute_phdi_nhanes_mped',
        'compute_phdi_asa24', 'compute_phdi_dhq3', 'compute_phdi_block', 'compute_di_gm',
    ]
    for name in expected:
        fn = getattr(dietaryindex, name)
        assert callable(fn), f"{name} is not callable"
