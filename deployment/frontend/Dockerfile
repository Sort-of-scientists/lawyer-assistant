FROM node:22.9.0
WORKDIR /app

COPY package.json package-lock.json ./

RUN npm install --silent

COPY . .

RUN npm run build

EXPOSE 3000
CMD npm run start
ENTRYPOINT ["top", "-b"]