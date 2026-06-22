FROM node:20-alpine AS builder
WORKDIR /app

ARG VITE_API_URL=
ENV VITE_API_URL=${VITE_API_URL}
ARG VITE_REGISTRATION_ENABLED=true
ENV VITE_REGISTRATION_ENABLED=${VITE_REGISTRATION_ENABLED}

COPY package.json package-lock.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:1.27-alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
