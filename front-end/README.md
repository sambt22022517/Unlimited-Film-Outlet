# React + Vite

# Prerequirest: Đã cài đặt NodeJS (cài bản LTS 20.16.x)
## Hướng dẫn chạy trên local
```bash
# Step 1
cd front-end

# Step 2
npm install

# Step 2.5
# Run server on localhost:8000 to fetch data

# See the formal data in file front-end/src/pages/Home.jsx

# Step 3
npm run dev
```

## Hướng dẫn chạy trên Docker
```bash
# Step 1
cd front-end

# Step 2
docker build -t movie-app:v1.0 .

# Step 2.5
# Run server on localhost:8000 to fetch data


# Step 3
docker run -p 3000:3000 movie-app:v1.0
```