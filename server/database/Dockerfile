FROM node:18.12.1-bullseye-slim

# Keep npm consistent with the lab
RUN npm install -g npm@9.1.3

WORKDIR /app

# Copy only package files first for better layer caching
COPY package.json /app/package.json
# If package-lock.json exists, copy it too (safe even if it doesn't exist in some labs)
COPY package-lock.json /app/package-lock.json

# Install deps
RUN npm install --omit=dev

# Copy app source
COPY app.js /app/app.js
COPY review.js /app/review.js
COPY dealership.js /app/dealership.js

# Seed data: app.js expects these files to exist in the working directory OR read them explicitly
# We'll place them where your app.js expects them (best practice: keep them in /app/data)
COPY data/dealerships.json /app/data/dealerships.json
COPY data/reviews.json /app/data/reviews.json


COPY data/dealerships.json /app/dealerships.json
COPY data/reviews.json /app/reviews.json

EXPOSE 3030

CMD ["node", "app.js"]
