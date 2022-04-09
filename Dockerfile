
FROM node:gallium

ENV PORT 8080
ENV HOST 0.0.0.0

# Create app directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Install app dependencies
# A wildcard is used to ensure both package.json AND package-lock.json are copied
# where available (npm@5+)
COPY package*.json /usr/src/app/
RUN npm install
# If you are building your code for production
# RUN npm ci --only=production

# Bundle app source
COPY . /usr/src/app
RUN npm run build

EXPOSE 8080

CMD [ "npm", "start" ]