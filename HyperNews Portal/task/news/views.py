import itertools
import json
import random
from datetime import datetime
from django.shortcuts import render, redirect
from django.conf import settings


# Create your views here.
def index(request):
    return redirect('/news/')


def news_home(request):

    with open(settings.NEWS_JSON_PATH, 'r') as file:
        news_list = json.load(file)

        news_to_show = []
        search_word = request.GET.get('q')

        if search_word is not None:
            for news_post_dict in news_list:
                if search_word in news_post_dict['title']:
                    news_to_show.append(news_post_dict)
        else:
            news_to_show = news_list

        sorted_news = sorted(news_to_show, reverse=True,
                             key=lambda x: datetime.strptime(x['created'], '%Y-%m-%d %H:%M:%S'))
        grouped_news = itertools.groupby(sorted_news, lambda y: y['created'].split(' ')[0])
        data = {key: [x for x in value] for key, value in grouped_news}
        return render(request, 'news_home.html', {'data': data})


def post_view(request, news_id):
    target_dict = {}
    with open(settings.NEWS_JSON_PATH, 'r') as file:
        news_dict = json.load(file)
        for news in news_dict:
            if news['link'] == news_id:
                target_dict = news
    return render(request, 'news_page.html', target_dict)


def create_post(request):

    if request.method == 'POST':

        with open(settings.NEWS_JSON_PATH, 'r') as file:

            my_json = json.load(file)

            # generating a random link number

            link_ist = []

            for i in range(len(my_json)):
                link_ist.append(my_json[i]['link'])

            while True:
                random_number = random.randint(100, 10000000000)
                if random_number not in link_ist:
                    link_ist.append(random_number)
                    new_link = random_number
                    break

            new_post = {
                'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'text': request.POST.get('text'),
                'title': request.POST.get('title'),
                'link': new_link
            }

        with open(settings.NEWS_JSON_PATH, 'w') as file:
            my_json.append(new_post)
            json.dump(my_json, file)

        return redirect('/news/')

    return render(request, 'create.html')
