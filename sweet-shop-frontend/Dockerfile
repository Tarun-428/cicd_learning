FROM node:22-bookworm

WORKDIR /usr/src/app

COPY package*.json ./
RUN npm install && npm run build

COPY . .

EXPOSE 3000
CMD ["npm", "run", "start"]
