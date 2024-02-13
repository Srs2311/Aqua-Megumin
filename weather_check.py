import requests
import json

alerts_url = "https://api.weather.gov/alerts/active?area=CO"

latitude = 39.7392
longitude = -104.9903


def get_weather_forecasts(latitude = 39.7392, longitude = -104.9903):
    area_url = f"https://api.weather.gov/points/{latitude},{longitude}"
    r = requests.get(area_url)
    forecasts = r.json()
    forecasts = forecasts["properties"]["forecast"]
    weather_forecast = requests.get(forecasts)
    weather_forecast = weather_forecast.json()
    periods = weather_forecast["properties"]["periods"]
    return(periods)
    
def get_daily_forecast(latitude = 39.7392, longitude = -104.9903):
    periods = get_weather_forecasts(latitude,longitude)
    today = periods[0]
    return(today)

def get_weekly_forecast():
    periods = get_weather_forecasts(latitude,longitude)
    return(periods)
