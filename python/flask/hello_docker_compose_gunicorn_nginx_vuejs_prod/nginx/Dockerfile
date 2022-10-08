FROM node:lts-alpine as builder

COPY --chown=node:node vuejs /app
USER node
WORKDIR /app

# If by mistake "node_modules" have been kept in the vuejs directory, remove it as it may prevent "npm run build" to run properly
RUN rm -rf node_modules

RUN npm install && npm run build

FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf