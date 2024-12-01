FROM node:22.9.0 as build

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm install --silent

COPY . .

RUN npm run build

# Set CMD for running your application
# CMD ["npm", "run", "start"]


FROM nginx:alpine

COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]