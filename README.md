# Bản hướng dẫn cho anh em trong nhóm
### Hướng dẫn chạy project
1. Mở `cmd`
2. Chạy
```bash
docker compose build
```
3. Chạy
```bash
docker compose up
```
4. Chạy
```bash
docker compose exec backend python manage.py import_films film_vietnamese.csv
```

5. Mở link [localhost:8000](http://localhost:8000/)