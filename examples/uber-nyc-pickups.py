# This example is based on a streamlit app: https://github.com/streamlit/demo-uber-nyc-pickups
import justpy as jp

import pandas as pd
import numpy as np
import pydeck as pdk

try:
    import altair as alt

    _has_altair = True
except:
    _has_altair = False


DATE_TIME = "date/time"
DATA_URL = (
    "http://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz"
)


def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    data[DATE_TIME] = pd.to_datetime(data[DATE_TIME])
    return data


data = load_data(100000)
lowercase = lambda x: str(x).lower()
data.rename(lowercase, axis="columns", inplace=True)
data[DATE_TIME] = pd.to_datetime(data[DATE_TIME])


def map_deck(data, lat, lon, zoom):
    deck = pdk.Deck(
        # https://docs.mapbox.com/help/getting-started/access-tokens/
        api_keys={"mapbox": "Insert your mapbox api token here"},
        map_provider="mapbox",
        map_style="light",
        initial_view_state={
            "latitude": lat,
            "longitude": lon,
            "zoom": zoom,
            "pitch": 50,
        },
        layers=[
            pdk.Layer(
                "HexagonLayer",
                data=data,
                get_position=["lon", "lat"],
                radius=100,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
            ),
        ],
    )
    return deck


airports = {
    "La Guardia": [40.7900, -73.8700],
    "JFK": [40.6650, -73.7821],
    "Newark": [40.7090, -74.1805],
}

zoom_level_airports = 12
zoom_level_main = 11
midpoint = (np.average(data["lat"]), np.average(data["lon"]))


def create_histogram(hour_selected):
    filtered = data[
        (data[DATE_TIME].dt.hour >= hour_selected)
        & (data[DATE_TIME].dt.hour < (hour_selected + 1))
    ]
    hist = np.histogram(filtered[DATE_TIME].dt.minute, bins=60, range=(0, 60))[0]
    chart_data = pd.DataFrame({"minute": range(60), "pickups": hist})
    chart = (
        alt.Chart(chart_data)
        .mark_area(
            interpolate="step-after",
        )
        .encode(
            x=alt.X("minute:Q", scale=alt.Scale(nice=False)),
            y=alt.Y("pickups:Q"),
            tooltip=["minute", "pickups"],
        )
        .configure_mark(opacity=0.5, color="red")
        .properties(width="container", height=200)
    )
    return chart


async def slider_change(self, msg):
    wp = msg.page
    hour = int(self.value)
    wp.all_caption.text = f"All New York City from {hour}:00 to {hour+1}:00"
    hour_data = data[data[DATE_TIME].dt.hour == hour]
    wp.decks["main"].deck = map_deck(
        hour_data, midpoint[0], midpoint[1], zoom_level_main
    )
    for airport, coords in airports.items():
        wp.decks[airport].deck = map_deck(
            hour_data, coords[0], coords[1], zoom_level_airports
        )
    if _has_altair:
        wp.histogram.chart = create_histogram(self.value)
        wp.histogram_caption.text = (
            f"Breakdown of rides per minute between {hour}:00 and {hour+1}:00"
        )


def pydeck_demo(request):
    wp = jp.QuasarPage(tailwind=True, title="Uber NYC Pickups")
    wp.decks = {}
    slider_div = jp.Div(a=wp, classes="flex ml-4", style="width: 50%; margin-top: 20px")
    jp.Div(
        text="Select hour of pickup:", a=slider_div, classes="pt-3 text-xl font-bold "
    )
    s1 = jp.Span(classes="ml-6 mt-1", style="width: 50%", a=slider_div)
    jp.QSlider(
        classes="w-64",
        min=0,
        max=23,
        a=s1,
        label=True,
        label_always=True,
        markers=True,
        step=1,
        snap=True,
        color="red",
        change=slider_change,
    )
    deck_div = jp.Div(classes="flex ml-2", a=wp)
    hour_data = data[data[DATE_TIME].dt.hour == int(0)]
    deck = map_deck(hour_data, midpoint[0], midpoint[1], zoom_level_main)
    all_div = jp.Div(a=deck_div)
    wp.all_caption = jp.Div(
        text="All New York City from 0:00 to 1:00",
        a=all_div,
        style="margin: 10px;",
        classes="text-xl font-bold",
    )
    wp.decks["main"] = jp.PyDeckFrame(
        a=all_div,
        deck=deck,
        style="margin: 10px; height: 400px; width: 450px",
        transition_duration=0.5,
    )
    for airport, coords in airports.items():
        airport_deck = map_deck(hour_data, coords[0], coords[1], zoom_level_airports)
        airport_div = jp.Div(a=deck_div)
        jp.Div(
            text=f"{airport} Airport",
            a=airport_div,
            style="margin: 10px;",
            classes="text-xl font-bold",
        )
        wp.decks[airport] = jp.PyDeckFrame(
            a=airport_div,
            deck=airport_deck,
            style="margin: 10px; height: 400px; width: 250px",
            transition_duration=0.5,
        )
    if _has_altair:
        chart = create_histogram(0)
        wp.histogram_caption = jp.Div(
            text="Breakdown of rides per minute between 0:00 and 1:00",
            a=wp,
            style="margin-left: 30px;",
            classes="text-xl font-bold",
        )
        wp.histogram = jp.AltairChart(
            chart=chart, a=wp, style="padding: 10px; width: 100%;"
        )
    return wp


from examples.basedemo import Demo

Demo("uber pydeck demo", pydeck_demo, VEGA=True)
