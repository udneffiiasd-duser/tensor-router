# tensor-router

**Маршрутизатор запросов к ИИ** — распределяет запросы между несколькими
моделями/бэкендами по правилам: приоритет, лимиты и spring fallback.

## Возможности

- Несколько бэкендов (моделей) с весами
- Лимиты по частоте и параллелизму
- Автоматический fallback при ошибке 5xx/таймауте
- Метрики по каждому бэкенду

## Установка

```bash
pip install -r requirements.txt
```

## Пример

```python
from router import Router, Backend

r = Router()
r.add(Backend("gpt-a", weight=3))
r.add(Backend("gpt-b", weight=1))

resp = r.request({"prompt": "привет"})
print(resp.backend, resp.data)
```

## Лицензия

MIT
