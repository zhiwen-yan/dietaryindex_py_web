/**
 * Index selector scoping — mirrors the sidebar navigation.
 *
 * A calculator page may switch between indices that the sidebar presents as a
 * SINGLE combined entry (for example "PRAL / NEAP", "MIND / DQI-I",
 * "NRF / NAR / MAR / INQ"). Indices the sidebar lists as SEPARATE entries
 * (DII, FII/FISI and E-DII each own a link; HEI-2020 and HEI-2015 likewise)
 * must stay independent and never appear in one another's selector.
 *
 * Explicit version variants (`_V1` / `_V2`) are handled by a dedicated
 * control, not by this list.
 */

export const INDEX_GROUPS: readonly (readonly string[])[] = [
  ["DII"],
  ["FISI"],
  ["E_DII"],
  ["HEI2020"],
  ["HEI2015"],
  ["AHEI"],
  ["AHEIP"],
  ["DASH"],
  ["DASHI"],
  ["ACS2020"],
  ["MED"],
  ["MEDI"],
  ["PDI", "HPDI", "UPDI"],
  ["PHDI"],
  ["MIND", "DQI_I"],
  ["CHEI", "DBI", "CHINA_DII"],
  ["GDQS", "WISH"],
  ["NRF", "NAR", "MAR", "INQ"],
  ["PRAL", "NEAP"],
  ["CDAI", "OBS"],
  ["DI_GM"],
];

/** Explicit service variants exposed through the calculator version control. */
export const VERSIONED_INDEX_KEYS: readonly string[] = [
  "HEI2020_V1",
  "HEI2020_V2",
  "MEDI_V1",
  "MEDI_V2",
  "ACS2020_V1",
  "ACS2020_V2",
  "PHDI_V1",
  "PHDI_V2",
];

const VERSION_SUFFIX = /_V\d+$/;

/** Strip a trailing version marker from a service key. */
export function baseIndexKey(indexKey: string): string {
  return indexKey.replace(VERSION_SUFFIX, "");
}

/** Indices the current page may switch between (sidebar-combined siblings). */
export function groupForIndex(indexKey: string): string[] {
  const base = baseIndexKey(indexKey);
  const group = INDEX_GROUPS.find((items) => items.includes(base));
  return group ? [...group] : [base];
}

/**
 * Candidate keys for the version control: the base key plus its explicit
 * `_V1` / `_V2` variants. Callers filter these against the catalog, so
 * variants that do not exist are simply dropped.
 */
export function versionKeysForIndex(base: string): string[] {
  return [base, `${base}_V1`, `${base}_V2`];
}
