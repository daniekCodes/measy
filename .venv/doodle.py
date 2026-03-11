from datetime import date, time

def create_attendence():
    attendence = False
    # if button = "attend":
    #   attendence = True
    return attendence


def collect_dates(
        date_start # = date(2020,2,22),
        #date_end = date(2020,2,22),
        #time_start = time(11,30),
        #time_end = time(16,0),
        ):
    user_date = (date_start)
    doodle_dates.append(user_date)
    return user_date


def poll_date(dates):
    polled_dates = []

    for date in set(dates):
        dates_to_poll = {
            "frequency": dates.count(date),
            "date": date
        }
        polled_dates.append(dates_to_poll)
    return polled_dates


doodle_dates = []

# Todo:
# Frontend Daten abgreifen
# if [Daten Input]:
doodle_dates.append(collect_dates())
doodle_dates.append(collect_dates())
doodle_dates.append(collect_dates())
doodle_dates.append(collect_dates(date_start=date(2020,2,20),date_end=date(2020,2,20)))


countedDates = poll_date(doodle_dates)
countedDates.sort(key=lambda x: x["frequency"], reverse=True)

#for date in countedDates:
#    print(date)