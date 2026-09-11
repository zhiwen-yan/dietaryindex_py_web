# DietaryIndex-Py index and input-mode support

This document is software interface documentation, not a scientific validation result.
It describes the 32 base index keys exposed by DietaryIndex-Py v0.3.0. Eight explicit
input variants (`HEI2020_V1/V2`, `MEDI_V1/V2`, `ACS2020_V1/V2`, and `PHDI_V1/V2`)
bring the API and CLI catalog to 40 calculator entries.

`Yes` means that the mode is exposed by the service layer. Some modes use a dedicated
adapter; others use the standard field-mapping workflow. Scientific equivalence is
tracked separately in the sibling `dietaryindex_validation` project.

| Key | Display name | Score scale | General | FPED | MPED | ASA24 | DHQ3 | Block |
|---|---|---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `DII` | DII | approximately -13.152 to +13.152 with all 45 components | Yes | Yes | Yes | Yes | Yes | Yes |
| `FISI` | FII/FISI | continuous with no fixed bounds | Yes | Yes | Yes | Yes | Yes | Yes |
| `HEI2020` | HEI-2020 | 0-100 | Yes | Yes | Yes | Yes | - | - |
| `HEI2015` | HEI-2015 | 0-100 | Yes | Yes | Yes | Yes | - | - |
| `AHEI` | AHEI | 0-110 | Yes | Yes | Yes | Yes | Yes | Yes |
| `AHEIP` | AHEI-P | 0-90 | Yes | - | - | - | - | Yes |
| `DASH` | DASH | 8-40 | Yes | Yes | Yes | Yes | Yes | Yes |
| `DASHI` | DASHI | 0-9 | Yes | Yes | Yes | Yes | - | - |
| `MED` | MED | 0-9 | Yes | Yes | Yes | Yes | Yes | Yes |
| `MEDI` | MEDI / MEDAS | 0-11; MEDI V2 is 0-55 | Yes | Yes | Yes | - | - | - |
| `ACS2020` | ACS2020 | 0-12 | Yes | - | - | - | - | - |
| `PHDI` | PHDI | 0-140 | Yes | Yes | Yes | Yes | Yes | Yes |
| `DI_GM` | DI-GM | 0-14 | Yes | Yes | Yes | - | - | - |
| `PDI` | PDI | 18-90 (sample-quintile dependent) | Yes | - | - | - | - | - |
| `HPDI` | hPDI | 18-90 (sample-quintile dependent) | Yes | - | - | - | - | - |
| `UPDI` | uPDI | 18-90 (sample-quintile dependent) | Yes | - | - | - | - | - |
| `MIND` | MIND | 0-15 | Yes | - | - | - | - | - |
| `DQI_I` | DQI-I | 0-100 | Yes | - | - | - | - | - |
| `CHEI` | CHEI | 0-100 | Yes | - | - | - | - | - |
| `DBI` | DBI | DQD 0-84; signed TS and HBS/LBS are auxiliary | Yes | - | - | - | - | - |
| `GDQS` | GDQS | 0-49 | Yes | - | - | - | - | - |
| `WISH` | WISH | 0-130 | Yes | - | - | - | - | - |
| `NRF` | NRF9.3 | -300 to 900 (default capped-LIM profile) | Yes | - | - | Yes | Yes | Yes |
| `NAR` | NAR | 0-1 per nutrient / capped adequacy ratio | Yes | - | - | Yes | Yes | Yes |
| `MAR` | MAR | 0-100 | Yes | - | - | Yes | Yes | Yes |
| `INQ` | INQ | >=0 with no fixed upper bound | Yes | - | - | Yes | Yes | Yes |
| `PRAL` | PRAL | continuous with no fixed bounds | Yes | - | - | Yes | Yes | Yes |
| `NEAP` | NEAP | >=-10.2 for nonnegative valid inputs; no fixed upper bound | Yes | - | - | Yes | Yes | Yes |
| `E_DII` | EDII (empirical; compatibility key `E_DII`) | continuous with no fixed bounds | Yes | - | - | - | - | - |
| `CHINA_DII` | CHINA-DII | approximately -5.871 to +5.871 (23 components) | Yes | - | - | - | - | - |
| `CDAI` | modified six-z CDAI | standardized sum with no fixed bounds | Yes | - | - | Yes | Yes | Yes |
| `OBS` | OBS | 0-40 | Yes | - | - | - | - | - |
