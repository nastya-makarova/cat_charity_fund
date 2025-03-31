Generic single-database configuration with an async dbapi.
## Основные команды
* Инициализация Alembic в проекте:
  ```
  alembic init --template async alembic 
  ```
```--template async``` - использование асинхронного шаблона

```alembic``` - директория, где нужно создать файлы Alembic
* Создание файла миграции:
  ```
  alembic revision
  ```
Ключ ```--autogenerate``` запускает автогенерацию миграций.

После ключа ```-m``` (или в полной форме — ```--message```) указывают название миграции.
* Применение миграций:
  ```
  alembic upgrade
  ```
  Выполнение всех неприменённых миграций:
  ```
  alembic upgrade head 
  ```
* Отмена миграций:
  ```
  alembic downgrade
  ```
  Отмена всех миграций, которые были в проекте:
  ```
  alembic downgrade base
  ```
* Показать все миграции в хронологическом порядке:
  ```
  alembic history 
  ```
* Посмотреть последнюю применённую миграцию:
  ```
  alembic current
  ```