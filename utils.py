
from datetime import datetime, timedelta, date
from typing import Dict

def month_report_time(months_ago: int) -> Dict[str, str]:
    today = date.today();
    old = today - timedelta(days=months_ago * 30)
    correct_old = date(old.year, old.month, 1)
    correct_today = date(today.year, today.month, 1)

    return {"startDate": str(correct_old), "endDate": str(correct_today)}

