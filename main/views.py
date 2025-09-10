from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core import serializers

from main.forms import NewsForm
from main.models import News

def show_main(request):
    news_list = News.objects.all()
    context = {
        'npm': '2406365313',
        'name': 'Herdayani Elision Sitio',
        'class': 'PBP KKI',
        'news_list': news_list,
    }
    return render(request, "main.html", context)


def create_news(request):
    form = NewsForm(request.POST or None)
    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_main')
    return render(request, "create_news.html", {'form': form})


def show_news(request, id):
    news = get_object_or_404(News, pk=id)
    news.increment_views()
    return render(request, "news_detail.html", {'news': news})


# --- Data endpoints ---
def show_xml(request):
    news_list = News.objects.all()
    xml_data = serializers.serialize("xml", news_list)
    return HttpResponse(xml_data, content_type="application/xml")


def show_json(request):
    news_list = News.objects.all()
    json_data = serializers.serialize("json", news_list)
    return HttpResponse(json_data, content_type="application/json")


def show_xml_by_id(request, id):
    try:
        # filter returns a queryset (works with serialize without wrapping in a list)
        data = News.objects.filter(pk=id)
        if not data.exists():
            return HttpResponse(status=404)
        return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")
    except News.DoesNotExist:
        return HttpResponse(status=404)


def show_json_by_id(request, id):
    try:
        # get returns one object; wrap in list for serialize()
        item = News.objects.get(pk=id)
        return HttpResponse(serializers.serialize("json", [item]), content_type="application/json")
    except News.DoesNotExist:
        return HttpResponse(status=404)
