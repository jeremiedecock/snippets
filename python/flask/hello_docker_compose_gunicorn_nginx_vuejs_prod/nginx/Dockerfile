FROM node:lts-alpine as builder

WORKDIR /app
COPY vuejs ./
RUN npm install && npm run build

FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf