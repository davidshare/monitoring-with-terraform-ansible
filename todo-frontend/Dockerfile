# Stage 1: Build
FROM node:20-alpine AS builder

# Set working directory
WORKDIR /app

# Install dependencies
COPY package.json package-lock.json* ./
RUN npm install --legacy-peer-deps --frozen-lockfile

# Copy source code and build the Next.js app
COPY . ./
RUN npm run build

# Stage 2: Run the Next.js app
FROM node:20-alpine AS runner

# Set environment variables for production
ENV NODE_ENV=production
ENV PORT=3000

# Set working directory
WORKDIR /app

# Copy only the necessary build output and dependencies
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json
COPY --from=builder /app/public ./public

# Expose the port the app runs on
EXPOSE 3000

# Start the Next.js app
CMD ["npm", "start"]
