from django.urls import path
from .views import ReviewListView, ReviewDetailView, ReviewCreateView, ReviewDeleteView, ReviewUpdateView

app_name = 'review'

urlpatterns = [
    path('', ReviewListView.as_view(), name='index'),            # /review/
    path('<int:pk>/', ReviewDetailView.as_view(), name='detail'), # /review/1/
    path('create/', ReviewCreateView.as_view(), name='create'),   # /review/create/
    path('<int:pk>/update/', ReviewUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', ReviewDeleteView.as_view(), name='delete'),

]
