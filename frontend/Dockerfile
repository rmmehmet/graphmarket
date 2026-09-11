FROM node:22-slim AS build

WORKDIR /app

# Build context is the repo root (see docker-compose.yml) so the npm workspace
# (frontend + packages/api-client) resolves the same way it does locally.
# package-lock.json is deliberately NOT copied — it was generated on Windows and
# pins platform-specific optional deps (e.g. rolldown's win32 binary), which
# breaks a Linux install. A fresh `npm install` resolves the right binaries.
COPY package.json ./
COPY frontend/package.json frontend/
COPY packages/api-client/package.json packages/api-client/
RUN npm install

COPY frontend/ frontend/
COPY packages/api-client/ packages/api-client/

ARG VITE_API_BASE_URL
ENV VITE_API_BASE_URL=${VITE_API_BASE_URL}

WORKDIR /app/frontend
RUN npm run build

FROM nginx:1.27-alpine

COPY --from=build /app/frontend/dist /usr/share/nginx/html
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
