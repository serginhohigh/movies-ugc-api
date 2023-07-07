# Сервис пользовательского контента

Сервис пользовательского контента для онлайн кинотеатра. Позволяет осуществлять следующие действия:

- Добавить кинопроизведение в закладки
- Удалить кинопроизведение из закладок
- Получить полный список закладок с пагинацией

- Оставить или удалить рецензию
- Поставить лайки рецензии
- Получить полный список рецензий с количеством лайков и дизлайков по определенному фильму

- Поставить или удалить оценку кинопроизведению
  > Для оценки фильмов используется 10-бальная шкала (от 1 до 10)
- Получить рейтинг кинопроизведения

---

Контракты API по пути `/api/v1/swagger#/`. Сгенерировать JWT можно с помощью следующего сниппета:

> Не забудьте предварительно установить python-jose

```
import uuid

from datetime import UTC, datetime, timedelta
from jose import jwt


token_data = {
    "sub": str(uuid.uuid4()),
    "role": "Admin",
    "exp": datetime.now(tz=UTC) + timedelta(hours=1),
    "iat": datetime.now(tz=UTC),
    "type": "access",
}

print(jwt.encode(token_data, "123qwe", algorithm="HS256"))
```

## Что используется в проекте

- FastAPI + [Dependency Injector](https://python-dependency-injector.ets-labs.org/)
- Кластер MongoDB
- Sentry
- python-jose для проверки JWT токенов
- pytest + pytest-asyncio + aiohttp для функционального тестирования

## Как запуститься

- Выполнить команду `make install`
- При необходимости изменить переменные `.env` файлов в каталогах `./`, `./ugc`, `./tests/functional/.env`
- Выполнить команду `make up`
- Выполнить инициализацию монго кластера вручную с помощью указанных ниже команд
  > Не забудьте дождаться полного старта кластера
  >
  > Для корректной инициализации сделайте небольшую паузу между каждой командой

```
docker exec -i mongocfg1 mongosh < mongo/init_config.js
docker exec -i mongors1n1 mongosh < mongo/init_shard1.js
docker exec -i mongors2n1 mongosh < mongo/init_shard2.js
docker exec -i mongos1 mongosh < mongo/add_shards.js
docker exec -i mongos1 mongosh < mongo/init_database.js
docker exec -i mongos1 mongosh < mongo/enable_sharding.js
```

## Как запустить тестирование

- Выполнить команду `make test`
  > При необходимости выполните `make install`
  >
  > Обратите внимание, что все `.env` файлы в каталогах `./`, `./ugc` и `./tests/functional` должны быть идентичными, то есть иметь одинаковые значения у одинаковых переменных

## TODO

- [ ] Poetry или PDM
- [ ] SQLAlchemy mongodb
- [ ] Репликация данных в ClickHouse для аналитиков
