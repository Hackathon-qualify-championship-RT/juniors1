# Askly
## Система опросов для школьных мероприятий
### Запуск проекта
Все команды вводятся в терминале</br>
***Необходимо иметь установленный pip и python для терминала***

#### Клонируем проект

```commandline
git clone https://github.com/Hackathon-qualify-championship-RT/juniors1
```

#### Переходим в папку juniors1

```commandline
cd juniors1
```

#### Создаём и активируем виртуальное окружение
Рекомендуется использовать виртуальное окружение для изоляции зависимостей:<br>
Для Windows:
```commandline
python -m venv venv
venv\Scripts\activate
```

Для MacOS/Linux:
```commandline
python3 -m venv venv
source venv/bin/activate
```

#### Устанавливаем зависимости

```commandline
pip install -r requirements.txt
```

#### Переходим в папку с manage.py

```commandline
cd askly
```

#### Настраиваем миграции

```commandline
python manage.py migrate
```

#### Запускаем сервер 

```commandline
python manage.py runserver
```

#### Переходим на сайт

<a href="http://127.0.0.1:8000/">http://127.0.0.1:8000/</a>

***Терминал не закрываем!***

### Видеодемонстрация проекта
[Скачать видеодемонстрацию проекта](https://github.com/Hackathon-qualify-championship-RT/juniors1/raw/main/Askly_video.mp4)

## Если у вас возникли проблемы с запуском проекта, свяжитесь с нами!