import requests
import datetime
from google.transit import gtfs_realtime_pb2

def get_time():
    return datetime.datetime.now()

def get_stockholm_temperature():
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": "Stockholm",
        "appid": "9cb45218b85f9b65bdec634d9872a67e",  # Replace with your OpenWeatherMap API key
        "units": "metric"
    }
    response = requests.get(url, params=params)
    data = response.json()
    temperature = data["main"]["temp"]
    return temperature

#Gets a color depending on how much time (minutes) == value, High value == green
def get_color(value):
    # Map the value to a color gradient from red to yellow to green
    if value <= 3:
        red = 255
        green = 0
        blue = 0
    elif value <= 5:
        red = 255
        green = 255
        blue = 0
    else:
        red = 0
        green = 255
        blue = 0
    return f'rgb({red},{green},{blue})'


def fetch_data(url):

    """
    Using request lib to get live data from url (in GTRF format)
    """

    feed = gtfs_realtime_pb2.FeedMessage()
    response = requests.get(url)
    assert response.status_code == 200, f'failed to get data from {url}'
    feed.ParseFromString(response.content)

    return feed


def get_trip_data(feed, stop_id):

    """
    using feed(data of all stops) and a stop id to get the realtime data on those.

    returns: a list with all stop time in minutes (int)
    """

    list_of_all_arrival_times = []

    for entity in feed.entity:
        if entity.HasField('trip_update'):
            for stop_time_update in entity.trip_update.stop_time_update:

                if stop_time_update.stop_id == stop_id:
                    # gets the stop id arrival time and changes it to how many minutes until it arriaves
                    arrival_time_minutes = int((datetime.datetime.fromtimestamp \
                                            (stop_time_update.arrival.time) - get_time()).total_seconds() // 60)
                    list_of_all_arrival_times.append(arrival_time_minutes)

    return list_of_all_arrival_times

def get_next_ride(list_rides):
    """
    takes a list of rides for a specific stop and returns the next on that is positive
    """
    try:
        if list_rides[0] < 0:
            return list_rides[1]
        else:
            return list_rides[0]
    except IndexError:
        raise ValueError(f"Invalid index: list only have: {len(list_rides)} objects inside it")