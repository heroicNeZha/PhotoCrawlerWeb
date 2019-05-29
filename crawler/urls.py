from django.urls import path
import crawler.views as v

app_name = 'crawler'
urlpatterns = [
    path('index', v.index, name='index'),
    path('user/<uid>', v.user, name='user'),
    path('', v.login, name='login')
]