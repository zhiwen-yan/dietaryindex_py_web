"""Update utils.py to add iff-level NHANES FPED adapter support."""
import sys
sys.path.insert(0, r'e:\BaiduSyncdisk\yanzhiwen\R shiny 网站\网站设计\dietaryindex_py')

path = r'e:\BaiduSyncdisk\yanzhiwen\R shiny 网站\网站设计\dietaryindex_py\streamlit_app\utils.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

print("File length:", len(content))

# 1. Add new imports after compute_dashi_nhanes_fped
old_import_block = '    compute_dashi_nhanes_fped,\n)'
new_import_block = '''    compute_dashi_nhanes_fped,
    compute_dash_nhanes_fped,
    compute_ahei_nhanes_fped,
    compute_medi_nhanes_fped,
    compute_di_gm_nhanes_fped,
)'''
if old_import_block in content:
    content = content.replace(old_import_block, new_import_block)
    print('OK: imports updated')
else:
    print('FAIL: import block not found')
    for line in content.split('\n'):
        if 'compute_dashi' in line:
            print('  FOUND:', line.strip())

# 2. Update NHANES_ADAPTER_MAP
old_map = '''NHANES_ADAPTER_MAP = {
    "HEI2015": compute_hei2015_nhanes_fped,
    "HEI2020": compute_hei2020_nhanes_fped,
    "MED": compute_med_nhanes_fped,
    "DASHI": compute_dashi_nhanes_fped,
}'''
new_map = '''NHANES_ADAPTER_MAP = {
    "HEI2015": compute_hei2015_nhanes_fped,
    "HEI2020": compute_hei2020_nhanes_fped,
    "MED": compute_med_nhanes_fped,
    "DASHI": compute_dashi_nhanes_fped,
    "DASH": compute_dash_nhanes_fped,
    "AHEI": compute_ahei_nhanes_fped,
    "MEDI": compute_medi_nhanes_fped,
    "DI_GM": compute_di_gm_nhanes_fped,
}'''
if old_map in content:
    content = content.replace(old_map, new_map)
    print('OK: NHANES_ADAPTER_MAP updated')
else:
    print('FAIL: old NHANES_ADAPTER_MAP not found')
    idx = content.find('NHANES_ADAPTER_MAP')
    if idx >= 0:
        print('  Found at pos:', idx)
        print(content[idx:idx+300])

# 3. Update NHANES_ADAPTER_FILES
old_files = '''NHANES_ADAPTER_FILES = {
    "HEI2015": "FPED tot 文件 (fped_dr1tot*.sas7bdat) + 营养 tot 文件 (DR1TOT*.XPT) + 人口学文件 (DEMO*.XPT)",
    "HEI2020": "FPED tot 文件 (fped_dr1tot*.sas7bdat) + 营养 tot 文件 (DR1TOT*.XPT) + 人口学文件 (DEMO*.XPT, 需含 RIDAGEYR 年龄)",
    "MED": "FPED tot 文件 (fpre_dr1tot*.sas7bdat) + 营养 tot 文件 (DR1TOT*.XPT) + 人口学文件 (DEMO*.XPT)",
    "DASHI": "仅需营养 tot 文件 (DR1TOT*.XPT) + 人口学文件 (DEMO*.XPT)",
}'''
new_files = '''NHANES_ADAPTER_FILES = {
    "HEI2015": "FPED tot 文件 (fped_dr1tot*.sas7bdat) + 营养 tot 文件 (DR1TOT*.XPT) + 人口学文件 (DEMO*.XPT)",
    "HEI2020": "FPED tot 文件 (fped_dr1tot*.sas7bdat) + 营养 tot 文件 (DR1TOT*.XPT) + 人口学文件 (DEMO*.XPT, 需含 RIDAGEYR 年龄)",
    "MED": "FPED tot 文件 (fpre_dr1tot*.sas7bdat) + 营养 tot 文件 (DR1TOT*.XPT) + 人口学文件 (DEMO*.XPT)",
    "DASHI": "仅需营养 tot 文件 (DR1TOT*.XPT) + 人口学文件 (DEMO*.XPT)",
    "DASH": "FPED iff 文件 (fped_dr1iff*.s