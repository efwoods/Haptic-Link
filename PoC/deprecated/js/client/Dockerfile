# client/Dockerfile

FROM node:18

WORKDIR /app

# Copy application files
COPY . .

# Install dependencies
RUN npm install

# Expose port 3000 for the client (React app)
EXPOSE 3000

# Start React development server
CMD ["npm", "start"]
