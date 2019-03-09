from django.core.management.base import BaseCommand
from forum.models import Topic
import requests
import json
from .secrets import nyt_api_key
import datetime

class Command(BaseCommand):
    def handle(*args, **options):
        url = "https://api.nytimes.com/svc/mostpopular/v2/viewed/7.json?api-key=" + nyt_api_key
        r = requests.get(url)
        data = json.loads(r.text) 
        topics = data['results']
        print(len(topics))
        i = 0
        for item in topics:
            print(str(round(i/len(topics)*100,2))+'%')
            i += 1
            if not Topic.objects.filter(title=item['title']).exists():
                topic = Topic()
                topic.title = item['title']
                topic.url = item['url']
                topic.published_date = datetime.datetime.strptime(item['published_date'], '%Y-%m-%d')
                topic.byline = item['byline']
                topic.abstract = item['abstract']
                topic.save()




