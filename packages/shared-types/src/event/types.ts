export interface EventCard {
  id: string
  title: string
  layerId: number
  layerCode: string
  sourceClass: string
  trustTier: string
  summaryEn: string | null
  sourcePublishedAt: string | null
  countryCode: string | null
  primarySourceUrl: string
  primarySourceName: string
}
