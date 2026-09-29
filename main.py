import os
import calendar
from datetime import date
import requests

BOT_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def get_message() -> str:
    today = date.today()

    last_day = calendar.monthrange(today.year, today.month)[1]
    end_of_month = date(today.year, today.month, last_day)
    days_to_month_end = (end_of_month - today).days

    end_of_year = date(today.year, 12, 31)
    days_to_year_end = (end_of_year - today).days

    day_of_year = today.timetuple().tm_yday
    total_days = 366 if calendar.isleap(today.year) else 365
    year_percent = round(day_of_year / total_days * 100, 1)

    bar_len = 20
    filled = int(bar_len * day_of_year / total_days)
    bar = "█" * filled + "░" * (bar_len - filled)

    return (
        f"<b>Доброе утро!</b>\n"
        f"{today.strftime('%d.%m.%Y')}\n\n"
        f"До конца месяца: <b>{days_to_month_end}</b> дн.\n"
        f"До конца года: <b>{days_to_year_end}</b> дн.\n\n"
        f"Прогресс года: {year_percent}%\n"
        f"<code>{bar}</code>\n\n"
        f"<i>Хорошего дня!</i>"
    )

def send_telegram(text: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    print("Сообщение отправлено!")

if __name__ == "__main__":
    send_telegram(get_message())