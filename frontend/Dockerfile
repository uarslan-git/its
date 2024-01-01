# Stage 1
FROM node:18.17.1 as node
WORKDIR /app
COPY its_ui/ .
RUN npm install
RUN npm run build -- --configuration staging
#RUN npm run build -- --configuration production
# Stage 2
FROM nginx:latest
COPY --from=node /app/dist/its_ui /usr/share/nginx/html