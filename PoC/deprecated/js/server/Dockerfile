# server/Dockerfile

FROM node:18

WORKDIR /app

# Copy application files
COPY . .

# Install dependencies
RUN npm install

# Expose port 5000 for server communication
EXPOSE 5000

# Start server
CMD ["npm", "run", "start"]
