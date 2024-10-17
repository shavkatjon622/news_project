from django.shortcuts import render, get_object_or_404
from django.template.context_processors import request
from django.views.generic import ListView, DetailView

from .models import News, Category



class NewsListView(ListView):
    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'all_news_list'

class NewsDetailView(DetailView):
    model = News
    template_name = 'news/news_detail.html'
    context_object_name = 'news_detail_page'

def homePageView(request):
    news = News.published.all()
    categories = Category.objects.all()
    context = {
        'news': news,
        'categories': categories
    }
    return render(request, 'news/home.html', context)

def contactPageView(request):
    context = {

    }
    return render(request, 'news/contact.html', context)

def errorPageView(request):
    context = {

    }
    return render(request, 'news/404.html', context=context)



# def news_list(request):
#     news_list = News.published.all()
#     context = {'news_list': news_list}
#     return render(request, 'news/news_list.html', context=context)


# def news_detail(request, id):
#     news = get_object_or_404(News, id=id, status=News.Status.Published)
#     context = {'news': news}
#     return render(request, 'news/news_detail.html', context)