# Use official Node.js LTS version
FROM node:18-alpine AS build

# Set working directory
WORKDIR /usr/src/app

# Copy package.json and lock file first
COPY package*.json ./

# Install all dependencies (including devDependencies)
RUN npm install

# Copy the rest of the app source
COPY . .

# Build the TypeScript code
RUN npm run build

# ---- Production image ----
FROM node:18-alpine

WORKDIR /usr/src/app

# Copy only necessary files from build stage
COPY --from=build /usr/src/app/package*.json ./
COPY --from=build /usr/src/app/node_modules ./node_modules
COPY --from=build /usr/src/app/dist ./dist

# Use non-root user for security (optional but good practice)
RUN addgroup app && adduser -S -G app app
USER app

# Expose the port your app listens on
EXPOSE 5003

# Start the app
CMD ["node", "dist/server.js"]
