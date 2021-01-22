import datetime

year = 2021
noon_first_day_of_year = datetime.datetime(year, 1, 1, 12)
day_of_year = 1
days_elapsed = day_of_year - 1
noon = noon_first_day_of_year + datetime.timedelta(days_elapsed)

current_day = datetime.datetime(year, 1, 1) + datetime.timedelta(days_elapsed)
n = (current_day - datetime.datetime(2000, 1, 1, 12)) / datetime.timedelta(1)
print(n)
