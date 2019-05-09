"""
  project2
  Project 2 - finding the best route
  Program: best_route.py
  Author: Aghared Alyousif
  Last date modified: 5/8/19
"""
import requests
import json
from itertools import permutations


API_KEY = ""
WS_URL = "https://api.openweathermap.org/data/2.5/forecast"


class City:
    """ Representing a city including the forecast max temps"""
    def __init__(self, name, temperatures):
        self.name = name
        self.temps = temperatures

    def get_temperature(self, day):
        return self.temps[day]

    def __str__(self):
        return self.name


class Route:
    """ A route represents a sequence of cities according to permutation_list"""
    avg_route = []
    minimum = 0.0

    def __init__(self, cities1, permutation_list):
        self.cities = cities1
        self.permutation_list = permutation_list

    def avg_temp(self):
        """find the best order of 5 cities that has the lowest average temp on 5 days"""
        lis_avg_temp = [sum([self.cities[item].get_temperature(j) for item, j in zip(sublist, range(5))])
                        / len(self.cities) for sublist in self.permutation_list]

        self.minimum = min(lis_avg_temp)

        index = lis_avg_temp.index(self.minimum)
        self.avg_route = self.permutation_list[index]
        return self.avg_route

    def __str__(self):
        final_string = "The lowest average temperature high of {:.2f} is forecast for this route: "
        city_list = [str(self.cities[self.avg_route[city]]) for city in range(len(self.avg_route))]
        final_string += ":".join(city_list)
        return final_string.format(self.minimum)


def fetch_weather(id_fetch):
    # get 5 gson files from openweathermap.org to get temp_max for each 5 city
    # for each 5 days
    query_string = "?id={}&units=imperial&APIKEY={}".format(id_fetch, API_KEY)
    request_url = WS_URL + query_string
    # print("Request URL: ", request_url)
    response = requests.get(request_url)
    if response.status_code == 200:
        d = response.json()
        city_name = d["city"]['name']
        # list of all 40 record 8 rec each day for 5 days
        lst = d['list']
        # loop for 5 days
        # li is the list of index for 8 rec in a day
        # the max of this 8 rec in i day
        tmp_list = [max([lst[j]["main"]["temp_max"] for j in [x for x in range(len(lst)) if x // 8 == i]])
                    for i in range(len(lst) // 8)]
        return City(city_name, tmp_list)
    else:
        print("How should I know?")
        return None


if __name__ == "__main__":
    id_list = json.loads(open("cities.json").read())
    # list to instantiate 5 objects for 5 cities and their highest temperatures over 5 days.
    cities = [fetch_weather(id_index) for id_index in id_list]

    # to get the order of permutations
    p = list(permutations(range(5)))

    print()
    # instantiate an instance of Route class
    r = Route(cities, p)

    # to get the order of the best route
    r.avg_temp()
    print(r.__str__())
"""
output
The lowest average temperature high of 68.03 is forecast for this route: Sedona:Flagstaff:Lake Havasu City:Tucson:Phoenix
"""
