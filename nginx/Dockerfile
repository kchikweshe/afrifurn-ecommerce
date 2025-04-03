# syntax = docker/dockerfile:experimental
FROM nginx:1.19.2-alpine

# tzdata = to be able to set the correct timezone
ARG rundeps="tzdata"

# Install apk dependencies
RUN --mount=type=cache,target=/var/cache/apk \
    apk update \
    && apk --progress add $rundeps

# Copy nginx config to expose frontend and api
# this is a template file that is processed upon startup via envsubst
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
