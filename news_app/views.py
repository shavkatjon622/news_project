from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, \
    UpdateView, DeleteView, CreateView
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountDetailView, HitCountMixin

from accounts.models import Profile
from config.custom_permissions import OnlyLoggedSuperUser
from .models import News, Category, Comment
from .forms import ContactForm, CommentForm


class NewsListView(ListView):
    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'all_news_list'

# class NewsDetailView(DetailView, HitCountDetailView):
#     model = News
#     count_hit = True
#     template_name = 'news/news_detail.html'
#     context_object_name = 'news_detail_page'


def news_detail(request, news):
    news = get_object_or_404(News, slug=news, status=News.Status.Published)
    context = {}
    # hit count logic
    hit_count = get_hitcount_model().objects.get_for_object(news)
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {'pk': hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits += 1
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits

    comment = news.comments.filter(active=True)
    comment_count = comment.count()
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # yangi komment obyektini yaratamiz lekin databasega saqlamimiz
            new_comment = comment_form.save(commit=False)
            new_comment.news = news
            # izoh egasini request yuborgan userga tengladik
            new_comment.user = request.user
            # malumotlar bazasiga saqlaymiz
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()
        context = {
            'news': news,
            'comments': comment,
            'new_comment': new_comment,
            'comment_count': comment_count,
            'comment_form': comment_form,
        }
        return render(request, 'news/news_detail.html', context)

# def homePageView(request):
#     categories = Category.objects.all()
#     news_list = News.published.all().order_by('-published_time')[:10]
#     local_one = News.published.filter(category__name='Mahalliy').order_by('-published_time')[:1]
#     local_news = News.published.all().filter(category='3').order_by('-published_time')[1:6]
#     context = {
#         'news_list': news_list,
#         'categories': categories,
#         'local_news': local_news,
#         'local_one': local_one,
#     }
#     print(context['news_list'][0])
#     return render(request, 'news/home.html', context)

class HomePageView(ListView):
    model = News
    template_name = 'news/home.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['news_list'] = self.model.published.all().order_by('-published_time')[:15]
        context['mahalliy_xabarlar'] = self.model.published.all().filter(category__name='Mahalliy').order_by('-published_time')[:5]
        context['xorij_xabarlari'] = self.model.published.all().filter(category__name='Xorij').order_by('-published_time')[:5]
        context['sport_xabarlari'] = self.model.published.all().filter(category__name='Sport').order_by('-published_time')[:5]
        context['texnologiya_xabarlari'] = self.model.published.all().filter(category__name='Texnologiya').order_by('-published_time')[:5]
        return context


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


class ForeignNewsView(ListView):
    model = News
    template_name = 'news/xorij.html'
    context_object_name = 'xorij_yangiliklari'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Xorij')
        return news



class LocalNewsView(ListView):
    model = News
    template_name = 'news/mahalliy.html'
    context_object_name = 'mahalliy_yangiliklari'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Mahalliy')
        return news


class TecnologNewsView(ListView):
    model = News
    template_name = 'news/texnologiya.html'
    context_object_name = 'texnologiya_yangiliklari'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Texnologiya')
        return news


class SportNewsView(ListView):
    model = News
    template_name = 'news/sport.html'
    context_object_name = 'sport_yangiliklari'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Sport')
        return news

class NewsUpdateView(OnlyLoggedSuperUser, UpdateView):
    model = News
    fields = ('title', 'slug', 'body', 'image', 'category')
    template_name = 'crud/news_edit.html'

class NewsDeleteView(OnlyLoggedSuperUser, DeleteView):
    model = News
    template_name = 'crud/news_delete.html'
    success_url = reverse_lazy('home_page')

class NewsCreateView(OnlyLoggedSuperUser, CreateView):
    model = News
    template_name = 'crud/news_create.html'
    fields = ('title_uz', 'title_en', 'title_ru',  'slug', 'body_uz', 'body_en', 'body_ru', 'image', 'category', 'status')
    success_url = reverse_lazy('home_page')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_page_view(request):
    admin_users = User.objects.filter(is_superuser=True)
    admin_profile = Profile.objects.all()
    context = {
        'admin_users': admin_users,
        'admin_profile': admin_profile,
    }

    return render(request, 'pages/admin_page.html', context=context)


class SearchResultsView(ListView):
    model = News
    template_name = 'news/search_result.html'
    context_object_name = 'barcha_yangiliklar'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return News.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        )