from features.scraper import WebScraper
from features.parser import Parser

from yaml import safe_load, YAMLError
import asyncio
import sys
import telegram_send


def get_config():
    urls = []
    with open("config/config.yaml", "r") as config_file:
        try:
            config = safe_load(config_file)
            for url in config["APP"]["urls"]:
                urls.append(url)
        except YAMLError as err:
            return f"{err}"
    return urls


def get_forecasts():
    urls = get_config()
    scraper = WebScraper(urls=urls)
    parser = Parser(scraper.data_per_page)
    weather = parser.parsed_data
    sinoptik_forecast = weather.get("Sinoptik")
    message_sinoptik = "Sinoptik forecast:\n" + "\n".join([str(w) for w in sinoptik_forecast])
    meteoblue_forecast = weather.get("Meteoblue")
    message_meteoblue = "Meteoblue forecast:\n" + "\n".join([str(w) for w in meteoblue_forecast])
    return message_sinoptik, message_meteoblue


def app_run():
    message_one, message_two = get_forecasts()
    telegram_send.send(messages=[message_one, message_two])


if __name__ == '__main__':
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    app_run()
