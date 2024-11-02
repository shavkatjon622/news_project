from django.urls import path
from .views import NewsListView, ContactPageView, errorPageView, HomePageView, news_detail, \
    LocalNewsView, ForeignNewsView, SportNewsView, TecnologNewsView

urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    path('error/', errorPageView, name = 'error_page' ),
    path("contact-us/", ContactPageView.as_view(),  name = "contact_page"),
    path('all/', NewsListView.as_view(), name = "all_news_list"),
    path('local-news/', LocalNewsView.as_view(), name="local_news_page"),
    path('foreign-news/', ForeignNewsView.as_view(), name="foreign_news_page"),
    path('sport-news/', SportNewsView.as_view(), name="sport_news_page"),
    path('tecnology-news/', TecnologNewsView.as_view(), name="tecnology_news_page"),
    path("<slug:news>/", news_detail, name="news_detail_page"),
]

