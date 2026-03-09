# Phase 1 assumptions

- **Database driver:** Sync SQLAlchemy with `psycopg2` is used in Phase 1 so that Alembic migrations and the seed script run without async setup. The API uses sync `get_db`. Async (asyncpg) can be introduced in a later phase if needed.
- **Region presets:** The seven presets (World, Americas, MENA, Europe, Asia, Africa, Oceania) are seeded as rows in the `jurisdictions` table with `jurisdiction_type = 'region'` (World = `'global'`) for backend/filter use. The frontend may also keep a static list.
- **PostGIS:** The initial migration enables the PostGIS extension and creates geography columns as specified in the schema document.
