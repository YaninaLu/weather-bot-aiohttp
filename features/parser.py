from datetime import datetime

from bs4 import BeautifulSoup
from features.weather import Weather


class Parser:
    def __init__(self, html_data):
        self.html_data = html_data
        self.parsed_data = {}
        self.parse()

    def parse(self):
        for html in self.html_data.items():
            try:
                url = html[0]
                page_data = html[1]
                soup = BeautifulSoup(page_data, 'html.parser')
                if url.startswith("https://sinoptik.ua"):
                    self.parse_sinoptik(soup)
                elif url.startswith("https://www.meteoblue.com"):
                    self.parse_meteo(soup)
                else:
                    return "I don't know how to parse this site."
            except Exception as err:
                return err

    def parse_sinoptik(self, soup):
        weather = []
        for i in range(1, 9):
            time = soup.select(f".p{i}")[0].getText()
            degrees = soup.select(f".p{i}")[2].getText()
            precipitation = soup.select(f".p{i}")[7].getText()
            curr_weather = Weather(time=time, degrees=degrees, precipitation=precipitation)
            weather.append(curr_weather)

        self.parsed_data["Sinoptik"] = weather

    def parse_meteo(self, soup):
        weather = []
        times = []
        times_html = soup.select("div.cell time")
        temperatures_html = soup.select("tr.temperatures td div.cell")
        temperatures = []
        precipitation_html = soup.select("span.precip-prob.wet")
        precipitation = []
        times_html.pop(0)

        for t in times_html:
            raw_time = datetime.fromisoformat(t["datetime"])
            times.append(raw_time)

        for temp in temperatures_html:
            temperatures.append(temp.text)

        for i in range(8, 16):
            precipitation.append(precipitation_html[i].text)

        for w in list(zip(times, temperatures, precipitation)):
            curr_weather = Weather(time=datetime.strftime(w[0], "%H:%M"), degrees=w[1], precipitation=w[2])
            weather.append(curr_weather)

        self.parsed_data["Meteoblue"] = weather
