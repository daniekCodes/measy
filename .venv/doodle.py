from datetime import date, time

def collect_user_dates(
        date_start = date(2020,2,22),
        date_end = date(2020,2,22),
        time_start = time(11,30),
        time_end = time(16,0),
        ):
    user_date = (date_start, date_end)
    return user_date


def poll_dates(dates):
    polled_dates = []

    for date in set(dates):
        dates_to_poll = {
            "frequency": dates.count(date),
            "date": date
        }
        polled_dates.append(dates_to_poll)
    return polled_dates


user_dates = []

# Todo:
# Frontend Daten abgreifen
# if [Daten Input]:
user_dates.append(collect_user_dates())
user_dates.append(collect_user_dates())
user_dates.append(collect_user_dates())
user_dates.append(collect_user_dates(date_start=date(2020,2,20),date_end=date(2020,2,20)))


countedDates = poll_dates(user_dates)
countedDates.sort(key=lambda x: x["frequency"], reverse=True)

print(countedDates)
