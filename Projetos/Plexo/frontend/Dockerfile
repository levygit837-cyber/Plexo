# Frontend Dockerfile for development
# FEATURE: Docker
FROM node:18-alpine

# Install pnpm
RUN npm install -g pnpm

WORKDIR /app

# Copy package files and pnpm lockfile
COPY package*.json pnpm-lock.yaml ./

# Install dependencies using pnpm
RUN pnpm install

COPY . .

EXPOSE 5173

CMD ["pnpm", "dev", "--host"]
