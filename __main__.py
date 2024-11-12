"""Automation to send polls for GDT"""

from datetime import datetime, timedelta
import locale
from os import environ
from requests import get
import holidays

# Replace with your bot token and channel ID
TOKEN = environ.get("BOT_TOKEN")
CHAT_ID = environ.get("CHANNEL_ID")
BASE_URL = f"https://api.telegram.org/bot{TOKEN}/"


# Set the locale to Italian for date formatting
try:
    locale.setlocale(locale.LC_TIME, "it_IT")
except locale.Error:
    print(
        "Locale 'it_IT' not found on this system. Please ensure Italian locale is installed."
    )

bavaria_holidays = holidays.country_holidays(country="DE", subdiv="BY")


def get_upcoming_week_dates():
    """GETS THE CORRECT DATES FOR THE UPCOMING WEEK"""
    # Starting from Monday of the current week
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday())

    # Generate a list of formatted dates for each day of the week
    days = []
    for i in range(7):
        date = start_of_week + timedelta(
            days=i + 7
        )  # Adding 7 days to start on next week
        is_bavarian_holiday = date in bavaria_holidays
        formatted_date = date.strftime(
            "%A %d.%m"
        )  # Format as "<day of week> <day>.<month>"

        formatted_date = (
            f'{"🎉🎉" if is_bavarian_holiday else ""} {formatted_date}'  # Add holiday
        )

        # add time of meetup
        formatted_date = (
            f'{formatted_date} - {"tbd" if i >= 5 or is_bavarian_holiday else "18.30"}'
        )

        days.append(formatted_date)

    return days


def pin_message(message_id) -> dict | None:
    """Pin a message given the message_id"""
    if message_id is None:
        return None

    pinned_message = get(
        f"{BASE_URL}pinChatMessage",
        json={
            "chat_id": CHAT_ID,
            "message_id": message_id,
            "disable_notification": True,
        },
        timeout=10,
    )

    return pinned_message.json().get("result", None)


def unpin_message(message_id) -> dict | None:
    """Unpin a message given the message_id"""
    if message_id is None:
        return None

    unpinned_message = get(
        f"{BASE_URL}unpinChatMessage",
        json={
            "chat_id": CHAT_ID,
            "message_id": message_id,
        },
        timeout=10,
    )

    return unpinned_message.json().get("result", None)


def get_last_pinned_message_id() -> int | None:
    """Get the full chat response"""
    response = get(f"{BASE_URL}getChat", json={"chat_id": CHAT_ID}, timeout=10)
    pinned_message = response.json().get("result", {}).get("pinned_message", {})
    message_id = pinned_message.get("message_id", None)

    return message_id if pinned_message.get("poll", None) is not None else None


def send_poll():
    """SENDS THE POLL"""
    # Poll details
    question = "Questa settimana ci sono per giocare al Motorama:"
    options = get_upcoming_week_dates()
    options.append("Mai 🩵🩵")
    options.append("Forse 🥩🥩")

    # Data to send the poll
    data = {
        "chat_id": CHAT_ID,
        "question": question,
        "options": options,
        "is_anonymous": False,  # Set to True if you want anonymous polls
        "type": "regular",
        "allows_multiple_answers": True,  # Set to True if you want multiple answers
    }

    # Make the request
    response = get(f"{BASE_URL}sendPoll", json=data, timeout=10)

    # Check for errors
    if response.status_code == 200:
        return response.json()["result"]

    return None


# Run the function
def main():
    """MAIN FUNCTION"""
    last_pinned_message = get_last_pinned_message_id()
    poll = send_poll()

    if last_pinned_message is not None:
        unpin_message(last_pinned_message)

    pin_message(poll.get("message_id", None))


if __name__ == "__main__":
    main()
