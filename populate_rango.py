import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'Rango.settings')

import django

django.setup()

from rango.models import Category, Page

import random

def populate():
    python_pages = [
        {"title": "Official Python Tutorial",
         "url": "http://docs.python.org/2/tutorial/"},
        {"title": "How to Think like a Computer Scientist",
         "url": "http://www.greenteapress.com/thinkpython/"},
        {"title": "Learn Python in 10 Minutes",
         "url": "http://www.korokithakis.net/tutorials/python/"}]
    django_pages = [
        {"title": "Official Django Tutorial",
         "url": "https://docs.djangoproject.com/en/1.9/intro/tutorial01/"},
        {"title": "Django Rocks",
         "url": "http://www.djangorocks.com/"},
        {"title": "How to Tango with Django",
         "url": "http://www.tangowithdjango.com/"}]
    other_pages = [
        {"title": "Bottle",
         "url": "http://bottlepy.org/docs/dev/"},
        {"title": "Flask",
         "url": "http://flask.pocoo.org"}]
    cats = {"Python": {"pages": python_pages, 'views': 128, 'likes': 64},
            "Django": {"pages": django_pages, 'views': 64, 'likes': 32},
            "Other Frameworks": {"pages": other_pages, 'views': 32, 'likes': 16}}
    for cat, cat_data in cats.items():  # 填充信息
        c = add_cat(cat, cat_data['views'], cat_data['likes'])
        for p in cat_data["pages"]:
            p['views'] = random.randint(1,1024)
            add_page(c, p["title"], p["url"], p["views"])
    for c in Category.objects.all():  # 打印信息
        for p in Page.objects.filter(category=c):
            print("- {0} - {1}".format(str(c), str(p)))


def add_page(cat, title, url, views):
    p = Page.objects.get_or_create(category=cat, title=title)[0]    # 如果存在则调取后更新，如果不存在则创建
    p.url = url
    p.views = views
    p.save()
    return p


def add_cat(name, views, likes):
    c = Category.objects.get_or_create(name=name)[0]    # 如果存在则调取后更新，如果不存在则创建
    c.views = views
    c.likes = likes
    c.save()
    return c


# 从这开始执行
if __name__ == '__main__':
    print("Starting Rango population script...")
    populate()
