from django.conf.urls.static import static
from django.urls import path
from config import settings
from .views import NewsListView, NewsDetailView, homePageView, contactPageView, errorPageView

urlpatterns = [
    path('', homePageView, name='home_page'),
    path('all/', NewsListView.as_view(), name = "all_news_list"),
    path("<int:pk>", NewsDetailView.as_view(), name = "news_detail_page"),
    path("contact-us/", contactPageView,  name = "contact_page"),
    path('error/', errorPageView, name = 'error_page' ),
]

