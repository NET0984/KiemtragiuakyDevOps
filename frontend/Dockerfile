FROM node:18-alpine

WORKDIR /app

# Copy frontend files
COPY . .

# Install a simple HTTP server to serve static files
RUN npm install -g http-server

EXPOSE 8080

CMD ["http-server", "-p", "8080", "-c-1"]
