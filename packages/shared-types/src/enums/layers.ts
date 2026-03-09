export const LAYER_CODES = [
  'PUB_HEALTH',
  'GUIDELINES',
  'LITERATURE',
  'PREPRINTS',
  'PHARMACOVIGILANCE',
] as const
export type LayerCode = (typeof LAYER_CODES)[number]
