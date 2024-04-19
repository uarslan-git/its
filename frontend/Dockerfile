# Stage 1
FROM node:18.17.1 as node
WORKDIR /app
COPY its_ui/ .
RUN npm install

ARG ITS_ENV
#ENV ITS_ENV=$ITS_ENV
RUN echo ${ITS_ENV}
RUN npm run build -- --configuration development-docker

# Stage 2
FROM nginx:latest
COPY --from=node /app/dist/its_ui /usr/share/nginx/html