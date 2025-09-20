## tg-ai-gen

Автогенерация и публикация контента в Telegram-каналы с помощью DeepSeek и aiogram v3.

### Настройка
- Создайте бота в Telegram и добавьте его админом в нужные каналы
- Укажите токен бота и ключ DeepSeek в `.env`
- Пропишите промпты для каналов в `tg_config.py` в словаре `channel_id_to_prompt`

Пример `.env`:
```
[DeepSeek]
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_API_KEY=...  # ваш ключ
DEEPSEEK_MODEL=deepseek-chat

[Telegram]
TG_BOT_TOKEN=...      # токен бота
```

### Установка
```
python3 -m venv venv
./venv/bin/pip install -U pip
./venv/bin/pip install -r requirements.txt
```

### Запуск (одиночный постинг во все каналы)
```
./venv/bin/python3 main.py
```

### Примечания
- Скрипт выполняется один раз и завершает работу
- Если нужно параллелить постинг, можно заменить цикл на ограниченную конкурентность
