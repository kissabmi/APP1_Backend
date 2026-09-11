# Запуск Backend 05

Учебное Flask-приложение «Крестики-нолики». Требуются Python 3.11+ и Docker с Compose.
Команды ниже — для Bash (Linux/macOS). Из Fish сначала выполни `bash`.
Все команды выполняются из папки `project05`.

## 1. Зависимости

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r src/requirements.txt
```

## 2. Собственные настройки

Выполни один раз: команда создаст `.env` с новым случайным паролем БД и ключом JWT.
Существующий файл не перезаписывается. `.env` не нужно отправлять в Git.
`.env.example` показывает состав настроек, но сам по себе не готов для запуска.

```bash
python - <<'PY'
import os, secrets
password = secrets.token_hex(24)
lines = [f"POSTGRES_PASSWORD={password}"]
lines.append(f"DATABASE_URL=postgresql://school21:{password}@127.0.0.1:55405/school21")
lines.append("JWT_SECRET_KEY=" + secrets.token_hex(32))
fd = os.open(".env", os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
with os.fdopen(fd, "w") as f:
    f.write("\n".join(lines) + "\n")
print("Created local .env; values are not printed")
PY
```

## 3. PostgreSQL и приложение

```bash
docker compose up -d --wait
set -a
source .env
set +a
python src/main.py
```

Открой **http://127.0.0.1:5000/**, зарегистрируй тестового пользователя и войди.
Можно сыграть против компьютера; для двух игроков нужны разные профили браузера
или обычное и приватное окно — вкладки делят localStorage.

Для повторного запуска достаточно активировать `.venv`, запустить БД и загрузить `.env`.
Другие Flask-проекты тоже используют порт 5000: демонстрируй их по очереди.
При собственной PostgreSQL задай `DATABASE_URL` для отдельной тестовой БД вместо Compose;
схему приложение создаёт само. Не указывай рабочую БД с ценными данными.

## Остановка

Приложение: Ctrl+C. База: `docker compose down`.
Данные остаются в именованном Docker volume. Не меняй пароль в `.env` после инициализации
БД без соответствующего изменения пароля в самой БД.

## Ограничения

Это учебная локальная демонстрация, не готовый публичный сервис.
Не используй настоящие личные пароли и не выставляй Flask development server в интернет.
Условия заданий сохранены в [README_RUS.md](README_RUS.md), исходная лицензия — в [LICENSE](LICENSE).
