type NhanesFileGuide = {
  filename: string;
  source: "cdc" | "usda" | "user";
  naming: "fixed" | "recommended";
  unavailable?: boolean;
};

export type NhanesCycleOption = { value: string; suffix: string };

const FPED_CYCLES: NhanesCycleOption[] = [
  { value: "2017-2018", suffix: "J" },
  { value: "2015-2016", suffix: "I" },
  { value: "2013-2014", suffix: "H" },
  { value: "2011-2012", suffix: "G" },
  { value: "2009-2010", suffix: "F" },
  { value: "2007-2008", suffix: "E" },
  { value: "2005-2006", suffix: "D" },
];

const MPED_CYCLES: NhanesCycleOption[] = [
  { value: "2003-2004", suffix: "C" },
  { value: "2001-2002", suffix: "B" },
  { value: "1999-2000", suffix: "" },
];

export function nhanesCycleOptions(mode: string): NhanesCycleOption[] {
  return mode === "nhanes_mped" ? MPED_CYCLES : FPED_CYCLES;
}

const CDC_DATA_PAGE = "https://wwwn.cdc.gov/nchs/nhanes/Search/DataPage.aspx?Component=Dietary&Cycle=";
const CDC_DEMO_PAGE = "https://wwwn.cdc.gov/nchs/nhanes/Search/DataPage.aspx?Cycle=";
const USDA_FPED_PAGE = "https://www.ars.usda.gov/northeast-area/beltsville-md-bhnrc/beltsville-human-nutrition-research-center/food-surveys-research-group/docs/fped-databases/";

export function nhanesFileGuide(key: string, cycle: string, mode: string): (NhanesFileGuide & { url: string }) | null {
  const day = key.endsWith("2") ? 2 : 1;
  if (mode === "nhanes_mped") {
    const option = MPED_CYCLES.find((item) => item.value === cycle) ?? MPED_CYCLES[0];
    const suffix = option.suffix ? `_${option.suffix}` : "";
    const noDay2 = day === 2 && option.value !== "2003-2004";
    if (noDay2 && ["nutrient_path2", "nutrient_ind_path2", "pyramid_path2"].includes(key)) {
      return {
        filename: "无独立 Day 2 文件（建议留空）",
        source: "user",
        naming: "recommended",
        unavailable: true,
        url: "",
      };
    }
    if (key === "nutrient_path" || key === "nutrient_path2") {
      const filename = option.value === "2003-2004"
        ? `DR${day}TOT${suffix}.XPT`
        : `DRXTOT${suffix}.XPT`;
      return { filename, source: "cdc", naming: "fixed", url: `${CDC_DATA_PAGE}${encodeURIComponent(cycle)}` };
    }
    if (key === "nutrient_ind_path" || key === "nutrient_ind_path2") {
      const filename = option.value === "2003-2004"
        ? `DR${day}IFF${suffix}.XPT`
        : `DRXIFF${suffix}.XPT`;
      return { filename, source: "cdc", naming: "fixed", url: `${CDC_DATA_PAGE}${encodeURIComponent(cycle)}` };
    }
    if (key === "demo_path") {
      return { filename: `DEMO${suffix}.XPT`, source: "cdc", naming: "fixed", url: `${CDC_DEMO_PAGE}${encodeURIComponent(cycle)}` };
    }
    if (key === "pyramid_path" || key === "pyramid_path2") {
      const filename = option.value === "2003-2004" ? `pyr_tot_d${day}.sas7bdat` : "pyr_tot.sas7bdat";
      return { filename, source: "user", naming: "recommended", url: "" };
    }
    if (key === "mped_per_100_gram_path") {
      return { filename: "MPED_EQUIV_0102.TXT", source: "user", naming: "recommended", url: "" };
    }
    if (key === "wjfrt") {
      return { filename: "WJFRT.csv", source: "user", naming: "recommended", url: "" };
    }
    if (key === "other_ingredients1" || key === "other_ingredients2") {
      return { filename: `other_ingredients_day${day}.csv`, source: "user", naming: "recommended", url: "" };
    }
    return null;
  }
  if (mode !== "nhanes_fped") return null;
  const option = FPED_CYCLES.find((item) => item.value === cycle) ?? FPED_CYCLES[0];
  const [start, end] = option.value.split("-");
  const fpedYear = `${start.slice(-2)}${end.slice(-2)}`;
  const suffix = option.suffix ? `_${option.suffix}` : "";
  if (key === "nutrient_path" || key === "nutrient_path2") return { filename: `DR${day}TOT${suffix}.XPT`, source: "cdc", naming: "fixed", url: `${CDC_DATA_PAGE}${encodeURIComponent(cycle)}` };
  if (key === "nutrient_ind_path" || key === "nutrient_ind_path2") return { filename: `DR${day}IFF${suffix}.XPT`, source: "cdc", naming: "fixed", url: `${CDC_DATA_PAGE}${encodeURIComponent(cycle)}` };
  if (key === "demo_path") return { filename: `DEMO${suffix}.XPT`, source: "cdc", naming: "fixed", url: `${CDC_DEMO_PAGE}${encodeURIComponent(cycle)}` };
  if (key === "fped_path" || key === "fped_path2") return { filename: `fped_dr${day}tot_${fpedYear}.sas7bdat`, source: "usda", naming: "fixed", url: USDA_FPED_PAGE };
  if (key === "fped_ind_path" || key === "fped_ind_path2") return { filename: `fped_dr${day}iff_${fpedYear}.sas7bdat`, source: "usda", naming: "fixed", url: USDA_FPED_PAGE };
  if (key === "other_ingredients1" || key === "other_ingredients2") return { filename: `other_ingredients_day${day}.csv`, source: "user", naming: "recommended", url: "" };
  return null;
}
