FROM node:22-alpine AS base
WORKDIR /app
COPY package*.json ./

FROM base AS prod
RUN npm ci
COPY . .
RUN npm run build

FROM base AS dev
CMD ["npm", "run", "dev"]
