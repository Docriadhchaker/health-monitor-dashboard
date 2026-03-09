export interface EventListItem {
  id: string
  title: string
  layer_id: number
  layer_code: string
  layer_name: string
  source_class_id: number
  source_class_name: string
  trust_tier_id: number
  trust_tier_name: string
  evidence_status_id: number
  evidence_status_name: string
  source_name: string
  source_url: string | null
  source_published_at: string | null
  country_code: string | null
  region_code: string | null
  location_name: string | null
  lat: number | null
  lon: number | null
  summary_en: string | null
  geographic_scope: string
}

export interface EventTranslationOut {
  language_code: string
  translated_summary: string
  is_machine_translated: boolean
}

export interface EventDetail {
  id: string
  title: string
  layer_id: number
  layer_code: string
  layer_name: string
  source_class_id: number
  source_class_name: string
  trust_tier_id: number
  trust_tier_name: string
  evidence_status_id: number
  evidence_status_name: string
  source_name: string
  source_url: string | null
  source_published_at: string | null
  event_occurred_at: string | null
  country_code: string | null
  region_code: string | null
  location_name: string | null
  geographic_scope: string
  summary_en: string | null
  relevance_label: string | null
  specialty_names: string[]
  topic_names: string[]
  translations: EventTranslationOut[]
}

export interface EventsFilters {
  layer_ids: number[] | null
  region_code: string | null
  time_window: string | null
  country_code: string | null
}

export interface EventsListResponse {
  items: EventListItem[]
  total: number
}
