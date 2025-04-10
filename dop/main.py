import requests
from bs4 import BeautifulSoup

def get_movie_info(movie_title):
    # URL для поиска фильма на Kinopoisk
    search_url = f"https://www.kinopoisk.ru/index.php?kp_query={movie_title}"
    
    # Заголовки для имитации браузера
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    # Получаем результаты поиска
    response = requests.get(search_url, headers=headers)
    if response.status_code != 200:
        print("Ошибка при получении данных с Kinopoisk.")
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Находим первую ссылку на фильм в результатах поиска
    movie_link = soup.select_one(".search_results .selection_film-item > a")
    if not movie_link:
        print("Фильм не найден.")
        return None
    
    # Переходим на страницу фильма
    movie_page_url = "https://www.kinopoisk.ru" + movie_link['href']
    movie_page_response = requests.get(movie_page_url, headers=headers)
    if movie_page_response.status_code != 200:
        print("Ошибка при получении страницы фильма.")
        return None
    
    movie_soup = BeautifulSoup(movie_page_response.text, 'html.parser')
    
    # Извлекаем название фильма
    title = movie_soup.select_one('h1.headline__title')
    if not title:
        print("Не удалось найти название фильма.")
        return None
    title = title.get_text(strip=True)
    
    # Извлекаем оценку IMDb
    imdb_rating = movie_soup.select_one('.film-synopsis-characteristics [data-test-id="block-imdb-rating"] span.rating__value')
    if imdb_rating:
        imdb_rating = imdb_rating.get_text(strip=True)
    else:
        imdb_rating = "Оценка IMDb отсутствует."
    
    # Извлекаем ссылку на постер
    poster = movie_soup.select_one('.film-poster .film-poster__image img')
    if poster:
        poster_url = poster['src']
    else:
        poster_url = "Постер отсутствует."
    
    # Возвращаем информацию
    return {
        "Название": title,
        "Оценка IMDb": imdb_rating,
        "Постер": poster_url
    }

# Пример использования
if __name__ == "__main__":
    movie_title = input("Введите название фильма/сериала: ")
    movie_info = get_movie_info(movie_title)
    if movie_info:
        print("\nИнформация о фильме:")
        for key, value in movie_info.items():
            print(f"{key}: {value}")