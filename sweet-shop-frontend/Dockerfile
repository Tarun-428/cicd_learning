FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install && npm run build

COPY . .

RUN npm run build

EXPOSE 3000
CMD ["npm", "run", "start"]
