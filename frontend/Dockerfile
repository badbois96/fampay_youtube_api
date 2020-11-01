FROM node:14.15.0-alpine3.12 as node
WORKDIR /app
COPY package*.json /app/
RUN npm install
COPY ./ /app/
RUN npm run build

FROM nginx:stable-alpine
COPY --from=node /app/build/ /usr/share/nginx/html/
COPY --from=node /app/nginx.conf /etc/nginx/nginx.conf