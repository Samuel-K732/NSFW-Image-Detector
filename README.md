# NSFW Image Detector (FastAPI + Sightengine)  

Backend-приложение на FastAPI, которое принимает изображение в формате .jpg или .png, отправляет его в сервис Sightengine для анализа и возвращает результат — содержит ли изображение нежелательный (NSFW) контент.  
NSFW параметры: nudity, gore, drugs.

## Требования для запуска:
- Python 3.10+
- Sightengine api_user и api_secret. Для получения ключей нужно создать аккаунт по адресу: https://sightengine.com/ (Данные банковской карты не требуются!). 

## Запуск:
- Клонировать репозиторий ``git clone https://github.com/Samuel-K732/NSFW-Image-Detector``
- Установить зависимости ``pip install -r requirements.txt``
- Cоздать .env файл со следующим содержимым:  
``SIGHTENGINE_API_USER=ваш_user_id ``   
``SIGHTENGINE_API_SECRET=ваш_secret_key``
- Запуск сервера:  ``uvicorn main:app``  или ``python main.py``  
 http://localhost:5000/docs - Swagger документация.


### Пример запроса через cURL:
curl -X POST -F "file=@example.jpg" http://localhost:5000/moderate   
ИЛИ (для Windows 10, 11)  
curl.exe -X POST -F "file=@example.jpg" http://localhost:5000/moderate

Возможные ответы:
{ "status": "OK" } — изображение безопасно;  
{ "status": "REJECTED", "reason": "NSFW content" } — найден нежелательный контент.
