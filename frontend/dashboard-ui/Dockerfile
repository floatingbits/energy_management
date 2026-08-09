FROM node:22-bookworm-slim

WORKDIR /app

COPY package*.json ./



RUN npm install && chown -R 1000:1000 /app/node_modules

COPY . .

RUN chown -R 1000:1000 /app/dist

EXPOSE 5173

USER 1000:1000

CMD ["npm","run","dev","--","--host"]