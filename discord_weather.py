import discord
import weather_check as wc

async def weather_message(weather,message):
    embed = discord.Embed(title=weather["name"],description=f"{weather["detailedForecast"]}")
    embed.set_author(name="Your Local Weatherman",icon_url = str(weather["icon"]))
    embed.add_field(name="Precipitation:",value=f"{weather["probabilityOfPrecipitation"]["value"] if weather["probabilityOfPrecipitation"]["value"] != None else "0"}%")
    await message.channel.send(embed=embed)

async def get_current_weather(message):
    weather = wc.get_daily_forecast()
    await weather_message(weather,message)


async def get_weekly_weather(message):
    weather = wc.get_weekly_forecast()
    for period in weather:
        await weather_message(period,message)