FROM node:23.7.0-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
# Make cache folder writable to fix EACCES error
RUN mkdir -p /app/node_modules/.cache && chmod -R 777 /app/node_modules/.cache
COPY . .
EXPOSE 3000
CMD ["npm", "start"]