
from datetime import datetime, timedelta, date
from typing import Dict

def day_report_time(days_ago: int) -> Dict[str, str]:
    today = date.today()
    old_date = today - timedelta(days=days_ago)
    return {"startDate": str(old_date), "endDate": str(today)}


def month_report_time(months_ago: int) -> Dict[str, str]:
    today = date.today()
    old_date = today - timedelta(months_ago * 30)
    return {"startDate": str(old_date), "endDate": str(today)}


def year_report_time(years_ago: int) -> Dict[str, str]:
    if years_ago > 1:
        print("We cannot retrieve more than 1 year")
        return
    today = date.today()
    old_date = today - timedelta(days=years_ago * 365)
    return {"startDate": str(old_date), "endDate": str(today)}