# Решение команды "Своего рода ученые" для хакатона от ZAVODit

## Инструкция по установке
1. Убедиться, что на запускаемой машине установлены:```python```, ```pip```, ```docker```, ```docker-compose```, ```git```
3. Склонировать репозиторий:
   - ```git clone https://github.com/vkimbris/lawyer-assistant.git```
4. Перейти в папку с проектом и создать виртуальное окружение:
   - ```cd lawyer-assistant```
   - ```python -m venv env```
   - ```source env/bin/activate``` (для Linux и MacOS)
5. Установить ```dvc``` для загрузки моделей с нашего S3:
   ```pip install dvc dvc-s3```
6. Установить ключ и токен от нашего S3:
   - ```dvc remote modify --local storage access_key_id YCAJEk1Dap7upINca7OgHQ2MM```
   - ```dvc remote modify --local storage secret_access_key YCMEeVSyCwieGkX2JfbJWRnrnhzpHjsmej4OqUXb```
7. Скачать модели:
   - ```dvc pull```
8. Перейти в папку deployment и собрать приложение:
   - ```cd deployment```
   - ```docker-compose up --build```
