import datetime
import math
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib as mpl
import numpy as np
import pandas as pd

# Following https://en.wikipedia.org/wiki/Sunrise_equation


def calc_day_hours(lon_degrees, lat_degrees, date):
    n = (date - datetime.date(2000, 1, 1)) / datetime.timedelta(1)

    # Mean solar time
    J = n - lon_degrees / 360

    # Solar mean anomaly
    M = (357.5291 + 0.98560028 * J) % 360

    # Equation of the center
    def sin_degrees(theta_degrees):
        return math.sin(theta_degrees * 2 * math.pi / 360)

    def cos_degrees(theta_degrees):
        return math.cos(theta_degrees * 2 * math.pi / 360)

    C = (
        1.9148 * sin_degrees(M)
        + 0.0200 * sin_degrees(2 * M)
        + 0.0003 * sin_degrees(3 * M)
    )

    # Ecliptic longitude
    lambda_ = (M + C + 180 + 102.9273) % 360

    # Solar transit
    J_transit = (
        2451545
        + J
        + 0.0053 * sin_degrees(M)
        - 0.0069 * sin_degrees(2 * lambda_)
    )

    # Declination of the sun
    sin_delta = sin_degrees(lambda_) * sin_degrees(23.44)
    delta = math.asin(sin_delta)
    cos_delta = math.cos(delta)

    # Hour angle
    cos_omega_0 = (
        sin_degrees(-0.83) - sin_degrees(lat_degrees) * sin_delta
    ) / (cos_degrees(lat_degrees) * cos_delta)
    omega_0 = math.acos(cos_omega_0)

    # Sunrise and sunset
    J_rise = J_transit - omega_0 / (2 * math.pi)
    J_set = J_transit + omega_0 / (2 * math.pi)

    # Day length
    l = J_set - J_rise

    return l * 24


year = 2021
lon_degrees = 12
lat_degrees = 59

days = range(1, 365 + 1 + 1)
day_hours = [
    calc_day_hours(lon_degrees, lat_degrees, year, day_of_year)
    for day_of_year in days
]

minutes_change = np.diff(np.array(day_hours) * 60)

days = days[:-1]
day_hours = day_hours[:-1]

fig, axs = plt.subplots(nrows=2, ncols=1, sharex=True)
axs[0].plot(days, day_hours)
axs[1].plot(days, minutes_change)
fig.savefig("fig.png")
