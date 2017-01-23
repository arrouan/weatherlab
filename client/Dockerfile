FROM node:6-alpine

ENV APPDIR /app

WORKDIR $APPDIR

RUN npm install -g webpack

ADD ./package.json $APPDIR/package.json

RUN \
    rm -rf node_modules && \
    npm install

ADD ./ $APPDIR

RUN \
    rm -rf dist

CMD ["webpack", "--config", "./webpack_config.js", "--progress", "--colors", "--display-error-details", "--output-pathinfo"]
