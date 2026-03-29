# Spotify CSV MP3 Downloader

Загружает все треки из плейлиста Spotify в формате MP3, используя экспорт плейлиста в CSV (через [exportify.app](https://exportify.app/)) и загрузку с YouTube через `yt-dlp`. Работает без премиум-подписки Spotify, обходит ограничения API.

## Возможности

-  Загрузка MP3 192 kbps (настраивается)
-  Пропуск уже загруженных треков (возобновление загрузки)
-  Многопоточная загрузка (ускоряет процесс)
-  Работает на основе CSV, экспортированного из любого плейлиста
-  Не требует Spotify Premium, не использует Spotify API для скачивания

## Требования

- Python 3.8+
- [ffmpeg](https://ffmpeg.org/download.html) (должен быть в PATH)
- Установленные пакеты: `yt-dlp`, `pandas`

## Установка

```bash
pip install yt-dlp pandas
