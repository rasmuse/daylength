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
lon = 12
latitudes = [
    52,
    58,
    64,
]

latitude_colors = dict(zip(latitudes, mpl.cm.tab10.colors))
latitude_labels = {
    52: "Potsdam",
    58: "Gothenburg",
    64: "Umeå",
}

dates = [
    datetime.date(year, 1, 1) + datetime.timedelta(days_elapsed)
    for days_elapsed in range(366)
]

day_hours = pd.DataFrame(
    index=dates,
    data={
        lat: [calc_day_hours(lon, lat, date) for date in dates]
        for lat in latitudes
    },
)

minutes_change = day_hours.diff() * 60
mark_days = [datetime.date(year, 1, 26)]


def make_fig(latitudes):
    fig, axs = plt.subplots(
        nrows=2,
        ncols=1,
        sharex=True,
        figsize=(6, 6),
    )
    for latitude in latitudes:
        axs[0].plot(
            day_hours[latitude],
            label=f"{latitude}° N ({latitude_labels[latitude]})",
            color=latitude_colors[latitude],
        )
        axs[1].plot(
            dates,
            minutes_change[latitude],
            label=f"{latitude}° N ({latitude_labels[latitude]})",
            color=latitude_colors[latitude],
        )
    axs[0].set_title("Day length [hours]")
    axs[1].set_title("Day length change rate [minutes/day]")
    axs[0].set_ylim(0, 24)
    axs[1].set_ylim(-7, 7)

    axs[0].legend(bbox_to_anchor=(1, 1), loc="upper right")

    for ax in axs:
        ax.grid(True)
        ax.axvline(mark_days, color="k")

    axs[-1].set_xticks(
        [datetime.date(year, month, 1) for month in range(1, 12 + 1)]
    )
    axs[-1].xaxis.set_major_formatter(mdates.DateFormatter("%b"))

    fig.savefig(f"fig-{'-'.join(map(str, sorted(latitudes)))}.png", dpi=300)


make_fig([58])
make_fig([58, 52])
make_fig([64, 58, 52])
