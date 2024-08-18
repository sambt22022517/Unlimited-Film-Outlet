import pandas as pd
import numpy as np

genres_vietnamese = [
    "Chính kịch", "Âm nhạc", "Nhạc kịch", "Giả tưởng", "Hành động", "Phiêu lưu", 
    "Hài kịch", "Bí ẩn", "Khoa học viễn tưởng", "Phim ngắn", "Kinh dị tâm lý", 
    "Kinh dị", "Tiểu sử", "Thể thao", "Lãng mạn", "Gia đình", "Lịch sử", 
    "Hoạt hình", "Tài liệu", "Hình sự", "Chiến tranh", "Miền Tây hoang dã", 
    "Trực tiếp", "Trò chơi truyền hình", "Thoại mục", "Tin tức", "Phim người lớn"
]

def update_genres(row):
    genres = row['genre'].split(',')
    for genre in genres:
        if genre in genres_vietnamese:
            row[genre] = 1
    return row

def calculate_rec_score(row, watched_genres_count):
    genre_vector = row[genres_vietnamese].values.astype(int)
    watched_genres_count_array = np.array(watched_genres_count)
    rec_score = np.sum(genre_vector * watched_genres_count_array) / np.sum(watched_genres_count_array)
    return rec_score


def apply_penalty(row, watched_films, penalty_factor):
    if row['film_id'] in watched_films:
        row['rec_score'] = row['rec_score'] * (1-penalty_factor)
    return row

def rec_films(df, watched_films, watched_genres_count):
    '''
    Function to get 20 highest recommended film_id
    Input:
    df: Film dataframe (original from the database or not) containing at least 3 columns 'film_id', 'rating', 'genre'
    watched_films: A list of film_id of the films that user watched in the user history
    watched_genres_count: An array showing how many times user have watched for every genres

    Output: A list with 20 film_ids of the 20 highest recommended film by this really simple method. 
    '''
    df1 = df[['film_id','film_name','rating','genre']]
    for genre in genres_vietnamese:
        df1[genre] = 0
    
    df1 = df1.apply(update_genres, axis=1)
    df1['rec_score'] = df1.apply(calculate_rec_score, watched_genres_count=watched_genres_count, axis=1)
    df1 = df1.apply(apply_penalty, watched_films=watched_films, penalty_factor=0.25, axis=1)
    df1 = df1.sort_values(by=['rec_score', 'rating'], ascending=[False, False])

    return df1.head(20)['film_id'].tolist()

    