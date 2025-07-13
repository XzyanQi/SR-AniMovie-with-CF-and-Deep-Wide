import requests
import pandas as pd
import time
from tqdm import tqdm

API_KEY = 'xxxxxxxxxxxxxxxxxxx'


base_url = 'https://api.themoviedb.org/3'
all_data = []

# Film Populer
def get_popular_movies(pages):
    print("\nMengambil data Film Populer...")
    movie_data_list = []
    for page_num in tqdm(range(1, pages + 1), desc="Halaman Film"):
        url = f"{base_url}/movie/popular?api_key={API_KEY}&language=en-US&page={page_num}"
        try:
            response = requests.get(url).json()['results']
            for movie in response:
                detail_url = f"{base_url}/movie/{movie['id']}?api_key={API_KEY}&append_to_response=credits"
                movie_detail = requests.get(detail_url).json()
                
                director = next((p['name'] for p in movie_detail.get('credits', {}).get('crew', []) if p['job'] == 'Director'), 'N/A')
                runtime_m = movie_detail.get('runtime', 0)
                
                movie_data_list.append({
                    'Judul': movie_detail.get('title'),
                    'Tanggal_Rilis': movie_detail.get('release_date'),
                    'Tipe': 'Movie',
                    'Rating': f"{movie_detail.get('vote_average', 0) * 10:.0f}",
                    'Genre': ', '.join([g['name'] for g in movie_detail.get('genres', [])]),
                    'Durasi': f"{runtime_m // 60}h {runtime_m % 60}m" if runtime_m else 'N/A',
                    'Overview': movie_detail.get('overview'),
                    'Kreator_Sutradara': director
                })
                time.sleep(0.05)
        except Exception as e:
            print(f"Error di halaman film {page_num}: {e}")
    return movie_data_list

# Japan
def get_japanese_anime(pages):
    print("\nMengambil data Animasi TV Jepang...")
    anime_data_list = []
    for page_num in tqdm(range(1, pages + 1), desc="Halaman Anime"):
        url = f"{base_url}/discover/tv?api_key={API_KEY}&with_origin_country=JP&with_genres=16&sort_by=popularity.desc&page={page_num}"
        try:
            response = requests.get(url).json()['results']
            for tv in response:
                detail_url = f"{base_url}/tv/{tv['id']}?api_key={API_KEY}&append_to_response=credits"
                tv_detail = requests.get(detail_url).json()

                creator = ', '.join([p['name'] for p in tv_detail.get('created_by', [])]) if tv_detail.get('created_by') else 'N/A'
                runtime_ep = tv_detail.get('episode_run_time', [0])

                anime_data_list.append({
                    'Judul': tv_detail.get('name'),
                    'Tanggal_Rilis': tv_detail.get('first_air_date'),
                    'Tipe': 'Anime TV Show',
                    'Rating': f"{tv_detail.get('vote_average', 0) * 10:.0f}",
                    'Genre': ', '.join([g['name'] for g in tv_detail.get('genres', [])]),
                    'Durasi': f"{runtime_ep[0]}m per episode" if runtime_ep else 'N/A',
                    'Overview': tv_detail.get('overview'),
                    'Kreator_Sutradara': creator
                })
                time.sleep(0.05)
        except Exception as e:
            print(f"Error di halaman anime {page_num}: {e}")
    return anime_data_list


# 125 halaman film (2500 film kalau full)
movies = get_popular_movies(125)
all_data.extend(movies)

# 125 halaman (2500 anime kalau full)
anime = get_japanese_anime(125)
all_data.extend(anime)

# dataframe > Excel
print("\nMenyimpan data gabungan ke file Excel...")
df = pd.DataFrame(all_data)
df.index = df.index + 1
df.to_excel('dataset_gabungan_fa.xlsx', index_label='No.')

print(f"Selesai! Dataset gabungan telah disimpan sebagai 'dataset_gabungan_fa.xlsx' dengan total {len(df)} data.")
