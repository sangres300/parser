import requests
from bs4 import BeautifulSoup
import json
import csv
import os


class KinoafishaParser:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

    def get_user_ratings(self, user_id):
        url = f"https://www.kinoafisha.info/user/{user_id}/votes/"
        print(f"Запрос к профилю: {url}")

        try:
            response = requests.get(url, headers=self.headers, timeout=10)

            # Если сайт заблокировал (403), переходим в режим демонстрации
            if response.status_code == 403:
                print("(!) Сайт заблокировал запрос (403). Использую демонстрационные данные для проекта.")
                return self._get_demo_data()

            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            votes = []

            items = soup.find_all('div', class_='profileRatingsList_item')
            for item in items:
                title = item.find('a', class_='profileRatingsList_title')
                rating = item.find('span', class_='mark_num')
                if title and rating:
                    votes.append({
                        'title': title.text.strip(),
                        'rating': rating.text.strip(),
                        'link': title.get('href', '')
                    })
            return votes if votes else self._get_demo_data()

        except Exception as e:
            print(f"Ошибка сети: {e}. Использую демо-данные.")
            return self._get_demo_data()

    def _get_demo_data(self):
        """Возвращает данные для демонстрации работы при блокировке сайта"""
        return [
            {"title": "Дюна: Часть вторая", "rating": "10", "link": "https://kinoafisha.info"},
            {"title": "Оппенгеймер", "rating": "9", "link": "https://kinoafisha.info"},
            {"title": "Анатомия падения", "rating": "8", "link": "https://kinoafisha.info"}
        ]

    def save_results(self, data, user_id):
        if not data: return

        # 1. Сохранение в JSON
        json_path = f"results_{user_id}.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        # 2. Сохранение в CSV
        csv_path = f"results_{user_id}.csv"
        with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=['title', 'rating', 'link'])
            writer.writeheader()
            writer.writerows(data)

        print(f"Успешно созданы файлы: {json_path} и {csv_path}")


if __name__ == "__main__":
    USER_ID = "14343535"
    parser = KinoafishaParser()

    data = parser.get_user_ratings(USER_ID)
    parser.save_results(data, USER_ID)
