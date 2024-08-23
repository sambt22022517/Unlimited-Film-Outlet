from django.core.management.base import BaseCommand
from app.models import Film
import random
import csv
from django.core.files import File

def import_films_from_csv(csv_file_path):
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        i = 0
        for idx, row in enumerate(reader):
            # Lấy hoặc tạo các thể loại
            genre_names = [name.strip() for name in row['genre'].split(',')]

            # Tạo đối tượng Film mà không có cover
            film = Film(
                id=row['film_id'],
                film_name=row['film_name'],
                author=row['author'],
                actor=row['actors'],
                genre=genre_names,
                release_date=row['release_year'],
                story=row['summary'],
                rating=float(row['rating']),
                price=random.randint(100, 1000) * 1000,
            )
            film.save()

            # Thêm ảnh bìa (cover) nếu có
            cover_path = f'covers/cover{idx}.jpg'
            if cover_path:
                with open(cover_path, 'rb') as cover_file:
                    film.cover.save(f"cover{idx}.jpg", File(cover_file))

            film.save()
            
            if (idx+1)%1000 == 0:
                print("Saved 1000 film.")
            i += 1
            if i == 13000:
                break

        print("Import hoàn tất!")

class Command(BaseCommand):
    help = 'Import films from a CSV file'
    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The CSV file path')

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_file']
        import_films_from_csv(csv_file_path)
