# api_yamdb
# Описание:  

Проект YaMDb (REST API) собирает отзывы пользователей на различные произведения.  
Реализовано на `Djangorestframework 3.12.4` Аутентификация на основе `JWT`. Читать контент могут все, вносить и изменять только аутентифицированные пользователи.  
Предоставляет ответы от сервера в формате JSON для последующей сериалиализации на стороне фронта.  
Это первый совместный проект, было сложно но интересно. 

  
# Установка:

Клонировать репозиторий и перейти в него в командной строке:  
`git clone https://github.com/mark-rom/api_yamdb.git`  
`cd api_yamdb`  
  
Cоздать и активировать виртуальное окружение:  
`python3.9 -m venv env`  
`source env/bin/activate` - для Mac OS  
`source venv/Scripts/activate` - для Windows OS  
  
Установить зависимости из файла requirements.txt:  
  
`python3 -m pip install --upgrade pip`  
`pip install -r requirements.txt`  
  
Выполнить миграции:  
  
`python3 manage.py makemigrations`  
`python3 manage.py migrate`  
  
 Залить базу данных из csv файлов:  
  
`python3 manage.py unpackingcsv`
  
Запустить проект:  
  
`python3 manage.py runserver`  
  
# Алгоритм регистрации пользователей
  
1. Пользователь отправляет POST-запрос на добавление нового пользователя с параметрами `email` и `username` на эндпоинт `/api/v1/auth/signup/`.  
2. YaMDB отправляет письмо с кодом подтверждения `confirmation_code` на адрес `email`. В проекте реализован бэкенд почтового сервиса, папка - `sent_emails`.  
3. Пользователь отправляет POST-запрос с параметрами `username` и `confirmation_code` на эндпоинт `/api/v1/auth/token/`, в ответе на запрос ему приходит token (JWT-токен).  
4. При желании пользователь отправляет PATCH-запрос на эндпоинт `/api/v1/users/me/` и заполняет поля в своём профайле.  
