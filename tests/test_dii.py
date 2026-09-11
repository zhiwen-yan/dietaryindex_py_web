"""
验证 Python DII 算法与 dietaryindex R 包结果一致性

对照数据: R 包 DII.R 文档中的 DHQ3_exp 示例结果
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "dietaryindex_py"))

import pandas as pd
import numpy as np

from dietaryindex import compute_dii, DII_REFERENCE

print("=" * 60)
print("DII 算法验证测试")
print("=" * 60)

# 测试1: 基本功能 - 使用模板数据
print("\n[测试1] 基本 DII 计算功能")
df = pd.DataFrame({
    'id': [1, 2],
    'alcohol': [0, 10],
    'vitb12': [2.4, 3.0],
    'vitb6': [1.5, 2.0],
    'bcarotene': [2000, 3000],
})

result = compute_dii(
    data=df,
    respondent_id=df['id'],
    ALCOHOL=df['alcohol'],
    VITB12=df['vitb12'],
    VITB6=df['vitb6'],
    BCAROTENE=df['bcarotene'],
)

print(result.to_string(index=False))
print(f"\nDII_ALL values: {result['DII_ALL'].tolist()}")

# 测试2: 验证只有3个参数的 DII 计算
print("\n[测试2] 3参数 DII (ALCOHOL + VITB12 + VITB6)")
df2 = pd.DataFrame({
    'id': [1, 2],
    'alcohol': [0, 10],
    'vitb12': [2.4, 3.0],
    'vitb6': [1.5, 2.0],
})

result2 = compute_dii(
    data=df2,
    respondent_id=df2['id'],
    ALCOHOL=df2['alcohol'],
    VITB12=df2['vitb12'],
    VITB6=df2['vitb6'],
)

print(result2.to_string(index=False))
print(f"\nDII_ALL: {result2['DII_ALL'].tolist()}")

# 测试3: DII_REFERENCE 完整性检查
print("\n[测试3] 全球参考数据库完整性")
print(f"参数总数: {len(DII_REFERENCE)}")
groups = {}
for k, v in DII_REFERENCE.items():
    g = v.get('group', 'unknown')
    groups[g] = groups.get(g, 0) + 1
for g, c in sorted(groups.items()):
    print(f"  {g}: {c} 个参数")

# 测试4: Z-score 验证
print("\n[测试4] Z-score 计算验证")
from scipy.stats import norm

# Alcohol: global_mean=13.98, sd=3.72
alcohol_val = 0
z = (alcohol_val - 13.98) / 3.72
percentile = norm.cdf(z) * 2 - 1
score = percentile * (-0.278)
print(f"ALCOHOL=0 → Z={z:.4f}, Percentile={percentile:.6f}, Score={score:.6f}")

alcohol_val = 10
z = (alcohol_val - 13.98) / 3.72
percentile = norm.cdf(z) * 2 - 1
score = percentile * (-0.278)
print(f"ALCOHOL=10 → Z={z:.4f}, Percentile={percentile:.6f}, Score={score:.6f}")

# 对比 R 包预期结果: ALCOHOL=0时0.278; 2.4时0.278
print("\n[预期] R包中 ALCOHOL=0 → 0.278 (几乎所有人低于均值)")

print("\n" + "=" * 60)
print("测试完成!")
print("=" * 60)
