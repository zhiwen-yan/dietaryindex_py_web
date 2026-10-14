export type FileSpec = {
  key: string;
  label_en: string;
  label_zh: string;
  required: boolean;
  accepted_extensions: string[];
  description_en: string;
  description_zh: string;
};

export type IndexField = {
  name: string;
  label_en: string;
  label_zh: string;
  required: boolean;
  unit?: string | null;
  default?: string | number | null;
  field_type: "input" | "extra";
  group_en?: string;
  group_zh?: string;
};

export type ModeDefinition = {
  label_en: string;
  label_zh: string;
  description_en: string;
  description_zh: string;
  kind: string;
};

export type ModeRequirement = {
  single_file: boolean;
  required_file_keys: string[];
  visible_file_keys?: string[];
  notes_en?: string;
  notes_zh?: string;
};

export type IndexReference = {
  authors: string;
  title: string;
  journal: string;
  year: number;
  volume_pages: string;
  doi: string;
  pmid: string;
  url: string;
  role_zh: string;
  role_en: string;
};

export type IndexCatalogItem = {
  index_key: string;
  title_en: string;
  title_zh: string;
  description_en: string;
  description_zh: string;
  score_scale: string;
  max_score?: number | null;
  output_cols: string[];
  supported_modes: string[];
  mode_specs: Record<string, FileSpec[]>;
  mode_requirements: Record<string, ModeRequirement>;
  references: IndexReference[];
};

export type IndexDetail = IndexCatalogItem & {
  function_name: string;
  fields: IndexField[];
};

export type CatalogResponse = {
  items: IndexCatalogItem[];
  modes: Record<string, ModeDefinition>;
};

export type Preview = {
  rows: number;
  columns: string[];
  dtypes: Record<string, string>;
  preview: Record<string, unknown>[];
  error?: { type: string; message: string };
};

export type UploadResponse = {
  upload_id: string;
  filename: string;
  size: number;
  preview: Preview;
};

export type MappingSuggestion = {
  column: string | null;
  confidence: number;
  required: boolean;
  label_en: string;
  label_zh: string;
};

export type MappingResponse = {
  index_key: string;
  suggestions: Record<string, MappingSuggestion>;
  missing_required: string[];
};

export type ResultPayload = {
  index_key: string;
  mode: string;
  rows: number;
  columns: string[];
  primary_output_column?: string | null;
  summary_stats?: Record<string, number | null> | null;
  mapping_used: Record<string, unknown>;
  preview: Record<string, unknown>[];
  downloads?: { csv: string; xlsx: string };
};

export type Job = {
  job_id: string;
  status: "queued" | "running" | "succeeded" | "failed";
  created_at: string;
  started_at?: string;
  finished_at?: string;
  index_key: string;
  mode: string;
  result?: ResultPayload | null;
  error?: { type: string; message: string } | null;
};

export type FiiSummary = { foods: number; groups: number; group_names: string[]; anti: number; pro: number };
export type FiiFood = {
  fdcd: number;
  food: string;
  fii: number;
  fii_score: number | null;
  food_group: string;
  source: string;
  direction: "anti" | "pro" | "neutral";
};

export type FiiPeers = { food_group: string; anti: FiiFood[]; pro: FiiFood[] };
