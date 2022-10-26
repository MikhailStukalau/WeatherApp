from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm
from django.views.generic import DeleteView, DetailView


def index(request):
    appid = '937718b1123af2e9f2f0c69f567d1f06'
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=" + appid


    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()

    form = CityForm()

    cities = City.objects.all()
    all_cities = []
    for city in cities:
        res = requests.get(url.format(city.name)).json()
        city_info = {
            'city': city.name,
            'country': res["sys"]["country"],
            'temp': res["main"]["temp"],
            'icon': res["weather"][0]["icon"],
            'pressure': res["main"]["pressure"],
            'humidity': res["main"]["humidity"],
            'temp_min': res["main"]["temp_min"],
            'temp_max': res["main"]["temp_max"],
            'visibility': res["visibility"],
            'wind_speed': res["wind"]["speed"],
        }

        if city_info not in all_cities:
            all_cities.append(city_info)
        else:
            form = CityForm()


    context = {
        'all_info': all_cities,
        'form': form,
    }
    return render(request, 'index.html', context)


class DeleteCity(DeleteView):
    model = City
    success_url = 'index.html'
    template_name = 'index.html'

class DetailCity(DetailView):
    model = City
    template_name = 'detail_city.html'
    context_object_name = 'all_info'
