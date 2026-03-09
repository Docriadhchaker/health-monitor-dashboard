# Deployment

MVP targets (per Technology Stack):

- **Frontend:** Vercel (static build from apps/web)
- **API & Worker:** Railway (or equivalent)
- **Database:** Railway PostgreSQL with PostGIS, or managed Postgres 16 + PostGIS
- **Redis:** Railway or managed Redis
- **Secrets:** Environment variables (OPENAI_API_KEY, DEEPL_API_KEY, DATABASE_URL, REDIS_URL, SENTRY_DSN)

Place deployment configs in `infra/deployment/` per service.
