import datetime

year = 2021
noon_first_day_of_year = datetime.datetime(year, 1, 1, 12)
day_of_year = 1
days_elapsed = day_of_year - 1
noon = noon_first_day_of_year + datetime.timedelta(days_elapsed)


def julian_date(t: datetime.datetime) -> float:
    # Implemented following https://en.wikipedia.org/wiki/Julian_day
    Y = t.year
    M = t.month
    D = t.day

    def div(a, b):
        return int(a / b)

    JDN = (  # julian day number
        div((1461 * (Y + 4800 + div((M - 14), 12))), 4)
        + div((367 * (M - 2 - 12 * (div((M - 14), 12)))), 12)
        - div((3 * (div((Y + 4900 + div((M - 14), 12)), 100))), 4)
        + D
        - 32075
    )
    JD = JDN + (t.hour - 12) / 24 + t.minute / 1440 + t.second / 86400
    return JD


n = julian_date(datetime.datetime(2021, 1, 1)) - 2451545 + 0.0008
print(n)

n2 = (datetime.datetime(2021, 1, 1) - datetime.datetime(2000, 1, 1, 12)) / datetime.timedelta(1)
print(n2)
