# Askly
## Система опросов для школьных мероприятий
### Запуск проекта
Все команды вводятся в терминале</br>
***Необходимо иметь установленный pip и python для терминала***

#### Клонируем проект

```
git clone https://github.com/Hackathon-qualify-championship-RT/juniors1
```

#### Переходим в папку juniors1

```
cd juniors1
```

#### Устанавливаем зависимости

```
pip install -r requirements.txt
```

#### Переходим в папку с manage.py

```
cd askly
```

#### Настраиваем миграции

```
python manage.py migrate
```

#### Запускаем сервер 

```
python manage.py runserver
```

#### Переходим на сайт

```
http://127.0.0.1:8000/
```
