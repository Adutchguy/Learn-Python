from datetime import datetime, timedelta


def days_until(today, target):
    return (target - today).days


def format_date(d):
    return d.strftime("%d %B %Y")


def parse_date(text):
    return datetime.strptime(text, "%Y-%m-%d").date()


def add_business_days(start, n):
    current = start
    while n > 0:
        current += timedelta(days=1)
        if current.weekday() < 5:
            n -= 1
    return current
