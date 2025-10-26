install: pip install -r requirements.txt
migrate: python manage.py migrate
server: WEATHER_API_KEY=xxx python manage.py runserver 0.0.0.0:8000
bot: TELEGRAM_BOT_TOKEN=xxx python bot.py
example: curl "http://localhost:8000/api/weather/?city=Berlin"
