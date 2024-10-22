from lib2to3.fixes.fix_input import context

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from .models import News, Category
from .forms import ContactForm



class NewsListView(ListView):
    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'all_news_list'

class NewsDetailView(DetailView):
    model = News
    template_name = 'news/news_detail.html'
    context_object_name = 'news_detail_page'

def homePageView(request):
    news_list = News.published.all().order_by('-published_time')
    categories = Category.objects.all()
    context = {
        'news_list': news_list,
        'categories': categories
    }
    print(context['news_list'][0])
    return render(request, 'news/home.html', context)


class ContactPageView(TemplateView):
    template_name = 'news/contact.html'

    def get(self, request, *args, **kwargs):
        form = ContactForm()
        context = {
            'from': form
        }
        return render(request, 'news/contact.html', context)

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if request.method == 'POST' and form.is_valid():
            form.save()
            return HttpResponse("<h1> Aloqaga chiqqaningiz uchun tashakkur!</h2> ")
        context = {
            'form': form
        }
        return render(request, 'news/contact.html', context)

# def contactPageView(request):
#     form = ContactForm(request.POST or None)
#     if request.method == "POST" and form.is_valid():
#         form.save()
#         return HttpResponse("Biz bilan bog`langaningiz uchun rahmat")
#     context = {
#         "form": form
#     }
#     return render(request, 'news/contact.html', context=context)

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