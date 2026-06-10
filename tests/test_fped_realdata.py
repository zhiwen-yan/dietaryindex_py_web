"""测试 NHANES 2017-2018 FPED 真实数据"""
import sys
sys.path.insert(0, r"E:\BaiduSyncdisk\yanzhiwen\R shiny 网站\网站设计\dietaryindex_py")

import os
import time

DATA_DIR = r"E:\BaiduSyncdisk\yanzhiwen\R shiny 网站\网站设计\NHANES\2017-2018"

FPED_PATH = os.path.join(DATA_DIR, "Dietary", "fped_dr1tot_1718.sas7bdat")
FPED_PATH2 = os.path.join(DATA_DIR, "Dietary", "fped_dr2tot_1718.sas7bdat")
NUTRIENT_PATH = os.path.join(DATA_DIR, "Dietary", "dr1tot_j.xpt")
NUTRIENT_PATH2 = os.path.join(DATA_DIR, "Dietary", "dr2tot_j.xpt")
DEMO_PATH = os.path.join(DATA_DIR, "Demographics", "demo_j.xpt")

print("=" * 70)
print("NHANES 2017-2018 FPED DII 计算测试")
print("=" * 70)

print(f"\n[检查] 数据文件:")
for name, path in [
    ("FPED Day1   ", FPED_PATH),
    ("FPED Day2   ", FPED_PATH2),
    ("Nutrient D1 ", NUTRIENT_PATH),
    ("Nutrient D2 ", NUTRIENT_PATH2),
    ("Demo        ", DEMO_PATH),
]:
    exists = "OK" if os.path.exists(path) else "MISSING!"
    print(f"  {name}: {exists}  {path}")

from dietaryindex.adapters.nhanes_fped import compute_dii_nhanes_fped

print("\n[计算] 正在计算 DII (Day1+Day2, 含DEMO)...")
start = time.time()

try:
    result = compute_dii_nhanes_fped(
        fped_path=FPED_PATH,
        nutrient_path=NUTRIENT_PATH,
        demo_path=DEMO_PATH,
        fped_path2=FPED_PATH2,
        nutrient_path2=NUTRIENT_PATH2,
    )
    elapsed = time.time() - start
    print(f"  OK 计算完成! 耗时: {elapsed:.1f} 秒")
    print(f"  结果形状: {result.shape[0]} 行 * {result.shape[1]} 列")

    print(f"\n[验证] 结果列名:")
    key_cols = ["SEQN", "RESPONDENTID", "DII_ALL", "DII_NOETOH", "REPEATNUM"]
    for col in key_cols:
        present = "OK" if col in result.columns else "MISSING!"
        print(f"  {col}: {present}")

    print(f"\n[统计] DII 核心指标:")
    for col in ["DII_ALL", "DII_NOETOH"]:
        if col in result.columns:
            vals = result[col].dropna()
            print(f"  {col}:")
            print(f"    mean={vals.mean():.4f}, std={vals.std():.4f}")
            print(f"    min={vals.min():.4f}, max={vals.max():.4f}")
            print(f"    count={len(vals)}")

    print(f"\n[样例] 前 10 行:")
    print(result.head(10))
except Exception as e:
    print(f"  FAILED: {e}")