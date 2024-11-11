"""Automation to send polls for GDT"""

from datetime import datetime, timedelta
import locale
from os import environ
import requests
import holidays

# Replace with your bot token and channel ID
BOT_TOKEN = environ.get("BOT_TOKEN")
CHANNEL_ID = environ.get("CHANNEL_ID")


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
            f"{"🎉🎉" if is_bavarian_holiday else ""} {formatted_date}"  # Add holiday
        )

        # add time of meetup
        formatted_date = (
            f"{formatted_date} - {"tbd" if i >= 5 or is_bavarian_holiday else "18.30"}"
        )

        days.append(formatted_date)

    return days


def send_poll():
    """SENDS THE POLL"""
    # Poll details
    question = "Questa settimana ci sono per giocare al Motorama:"
    options = get_upcoming_week_dates()
    options.append("Mai 🩵🩵")
    options.append("Forse 🥩🥩")
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPoll"

    # Data to send the poll
    data = {
        "chat_id": CHANNEL_ID,
        "question": question,
        "options": options,
        "is_anonymous": False,  # Set to True if you want anonymous polls
        "type": "regular",
        "allows_multiple_answers": True,  # Set to True if you want multiple answers
    }

    # Make the request
    response = requests.post(url, json=data)

    # Check for errors
    if response.status_code == 200:
        print("Poll sent successfully!")
    else:
        print("Failed to send poll:", response.text)


# Run the function
def main():
    """MAIN FUNCTION"""
    send_poll()


if __name__ == "__main__":
    main()
