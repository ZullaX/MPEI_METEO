from abc import ABC
import time
import requests
from datetime import datetime

class Post(ABC):
    host = "http://127.0.0.1:8000/"
    host = "Site"

    # интервал отправки данных на сервер в минутах
    def __init__(self,post_path, interval_min):
        self.last_post = None
        self.path = post_path
        self.interval=interval_min
        self.DB_fields=tuple()

    def send(self,values):
        now = datetime.now()
        if not self.last_post  or (now - self.last_post).seconds >= 60*self.interval:
            dict_kv = dict(zip(self.DB_fields, [now, ] + values))
            try:
                response = requests.post(self.host+self.path, data=dict_kv)
                self.last_post = now
                print( f"POST request Status Code: {response.status_code}. Text: {response.text}")
            except Exception as e1:
                print(f"POST request to {self.host + self.path}: {e1.__class__.__name__}")
                print(e1)

class Wind(Post):
    def __init__(self, post_path="meteo/post_wind/", interval_min=10):
        super(Wind, self).__init__(post_path, interval_min)
        self.DB_fields = (
        'DATE', 'WS1AVG', 'WD1AVG', 'WS1MIN2', 'WS1AVG2', 'WS1MAX2', 'WD1MIN2', 'WD1AVG2', 'WD1MAX2', 'WS1MIN10', 'WS1AVG10', 'WS1MAX10', 'WD1MIN10', 'WD1AVG10',
        'WD1MAX10',)


class Meteo(Post):
    def __init__(self, post_path="meteo/post_meteo/", interval_min=10):
        super(Meteo, self).__init__(post_path, interval_min)
        self.DB_fields = (
        'DATE', 'TA', 'DP', 'WC', 'RH', 'PA', 'PR', 'PR1H', 'PR24h', 'SR_1M', 'SR_1D', 'SR_45_1M', 'SR_45_1D', 'SD_1H',
        'SD_1D', 'SD_45_1H', 'SD_45_1D')


if __name__ == "__main__":
    pass

    #Add to Script
    meteo=Meteo(interval_min=2)
    wind=Wind(interval_min=1)

    values_meteo = [-20, -100, -20.4, 74, 738.1, 0, 0, 0, 0, 13, -1, 15, -168, 239982, -314, 258735]

    values_wind = [  0.9, 144, 0.4, 1, 2.3, 26, 104, 155, 0.3, 1.3, 3.4, 26, 122, 216]

    while True:

        # Add to Script
        meteo.send(values_meteo)
        wind.send(values_wind)

        time.sleep(60 * min((wind.interval,meteo.interval)) - 5)
