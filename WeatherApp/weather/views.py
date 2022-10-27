from django.shortcuts import render
from django.http import HttpResponse
import requests
from .models import City
from .forms import CityForm
from django.views.generic import DeleteView, DetailView, ListView

appid = '937718b1123af2e9f2f0c69f567d1f06'
url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=" + appid

def get_data(city, res):
    return {
            'id': city.id,
            'city': res['name'],
            'country': res["sys"]["country"],
            'temp': res["main"]["temp"],
            'icon': "http://openweathermap.org/img/w/{}.png".format(res["weather"][0]["icon"]),
            'pressure': res["main"]["pressure"],
            'humidity': res["main"]["humidity"],
            'temp_min': res["main"]["temp_min"],
            'temp_max': res["main"]["temp_max"],
            'visibility': res["visibility"],
            'wind_speed': res["wind"]["speed"],
        }

def index(request):
    cities = City.objects.all()
    form = CityForm(request.POST)
    name = form['name'].value()
    current_city = requests.get(url.format(name)).json()
    name = current_city['name']
    array_with_existing_city = list(filter(lambda obj: obj.name == name, cities))
    is_existing = len(array_with_existing_city)


    if request.method == 'POST' and not len(array_with_existing_city):
        database_city = City(name=name)
        database_city.save()

    cities = City.objects.all()
    form = CityForm()
    all_cities = []
    for city in cities:
        res = requests.get(url.format(city.name)).json()
        city_info = get_data(city, res)

        if city_info not in all_cities:
            all_cities.append(city_info)
        else:
            form = CityForm()

    context = {
        'all_info': all_cities,
        'form': form,
        'error': 'This city is already exists' if is_existing else ''
    }

    return render(request, 'index.html', context)


class DeleteCity(DeleteView):
    model = City
    success_url = 'index.html'
    template_name = 'index.html'


class DetailCity(DetailView):
    model = City
    template_name = 'detail_city.html'
    context_object_name = 'el'

    def get(self, request, pk):
        city = City.objects.get(pk=pk)
        res = requests.get(url.format(city.name)).json()

        city_info = get_data(city, res)
        return render(request, 'detail_city.html', {'info': city_info})
