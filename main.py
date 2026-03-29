import os
import time
import pandas as pd
import yt_dlp
from concurrent.futures import ThreadPoolExecutor, as_completed

# ========== НАСТРОЙКИ ==========
CSV_FILE = "playlist.csv"          # ваш CSV от exportify.app
COL_TRACK = "Track Name"           # название колонки с треком
COL_ARTIST = "Artist Name(s)"      # название колонки с исполнителем
DOWNLOAD_DIR = "downloads"         # папка для MP3
MAX_WORKERS = 4                    # сколько загрузок одновременно
DELAY_BETWEEN = 2                  # задержка между поисками (сек)
# ================================

def sanitize_filename(name):
    """Удаляет недопустимые символы из имени файла"""
    return "".join(c for c in name if c not in r'\/:*?"<>|')

def download_track(artist, title, download_dir, delay):
    """Скачивает трек с YouTube, сохраняет MP3"""
    base_name = sanitize_filename(f"{artist} - {title}")
    final_path = os.path.join(download_dir, f"{base_name}.mp3")

    if os.path.exists(final_path):
        print(f"[ ] Пропускаем (уже есть): {artist} - {title}")
        return True

    # Шаблон: yt-dlp сам добавит .mp3 после конвертации
    outtmpl = os.path.join(download_dir, f"{base_name}.%(ext)s")

    query = f"{artist} {title} audio"
    print(f"[•] Ищем: {query}")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': outtmpl,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'keepvideo': False,        # удалять исходный файл после конвертации
        'quiet': True,
        'no_warnings': True,
        'default_search': 'ytsearch',
        'noplaylist': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([query])
        time.sleep(delay)
        print(f"[✓] Загружено: {artist} - {title}")
        return True
    except Exception as e:
        print(f"[✗] Ошибка {artist} - {title}: {e}")
        return False

def main():
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    df = pd.read_csv(CSV_FILE)
    print(f"Загружено треков из CSV: {len(df)}")

    df = df.dropna(subset=[COL_TRACK, COL_ARTIST])
    tracks = list(zip(df[COL_ARTIST], df[COL_TRACK]))

    print(f"Будем загружать: {len(tracks)} треков")

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {
            executor.submit(download_track, artist, title, DOWNLOAD_DIR, DELAY_BETWEEN): (artist, title)
            for artist, title in tracks
        }

        for future in as_completed(futures):
            artist, title = futures[future]
            try:
                future.result()
            except Exception as e:
                print(f"[!] Необработанная ошибка для {artist} - {title}: {e}")

    print("Загрузка завершена.")

if __name__ == "__main__":
    main()