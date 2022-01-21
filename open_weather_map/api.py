"""
File to write a wrapper for an external API
"""
import json
import re
import requests
import pandas as pd
from typing import List
from utils.config_parser import configuration_parser
from utils.database_connection import SetupDB
from exceptions import CityNotFoundException
from open_weather_map import DATA_DIR


class WeatherNotification:
    keys_map = {
        'temp': ['main', 'temp'],
        'humidity': ['main', 'humidity'],
        'windspeed': ['wind', 'speed'],
    }
    def __init__(self) -> None:
        self.db = SetupDB()
        self.api_key = configuration_parser()['WEATHER_API']['key']
        self.file_name = DATA_DIR.joinpath("log_subscriptions.txt")

    def get_data(self) -> None:
        query = Query.get_all_subscriptions
        return self.db.recieve(query)

    def get_request(self, url) -> requests.Response:
        try:
            response = requests.get(url)
            if response:
                return response
            raise CityNotFoundException
        except Exception as e:
            raise e
    
    def check_if_conditions_meet(self, conditions: List[str], response: requests.Response) -> bool:
        body = json.loads(response.text)
        
        all_conditions = []
        for condition in conditions:
            key, cond = condition.split(':')
            keys = self.keys_map[key]
            value = body[keys[0]][keys[1]]
            all_conditions.append(eval(f'{value}{cond}'))
        
        return all(all_conditions)
    
    def log_subscription(self, row: pd.Series):
        """File format
            city_id, state_id, country_id, email, conditions
        """
        with open(self.file_name, 'a') as file:
            values = ", ".join([v if v else '' for v in list(row.values)])
            line = f'{values}\n'
            file.write(line)

    def process_subscription(self, row: pd.Series) -> None:
        city_id = row['city_id']
        conditions = eval(row['conditions'])
        url = Query.city_url.format(city_id=city_id, key=self.api_key)
        response = self.get_request(url)
        if_conditions_meet = self.check_if_conditions_meet(conditions, response)
        if if_conditions_meet:
            self.log_subscription(row)
        return row

    def run(self) -> None:
        df = self.get_data()
        for _, row in df.iterrows():
            self.process_subscription(row)



class Query:
    """
    city ids
    Example 833,2960,3245
    """
    city_url = "http://api.openweathermap.org/data/2.5/weather?id={city_id}&appid={key}"

    get_all_subscriptions = """
        select city_id, state_id, country_id, email, conditions
        from public.subscription
        where is_active=True
    """

if __name__ == "__main__":
    notification = WeatherNotification()
    notification.run()