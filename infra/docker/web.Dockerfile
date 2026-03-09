FROM node:20-alpine AS builder

WORKDIR /app
RUN corepack enable && corepack prepare pnpm@latest --activate
COPY pnpm-workspace.yaml package.json ./
COPY apps/web/package.json apps/web/
COPY packages/shared-types/package.json packages/shared-types/
COPY packages/shared-config/package.json packages/shared-config/
RUN pnpm install --frozen-lockfile

COPY apps/web/ apps/web/
COPY packages/ packages/
RUN pnpm -C apps/web build

FROM nginx:alpine
COPY --from=builder /app/apps/web/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
