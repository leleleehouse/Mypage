from django.urls import path
from . import views

app_name = 'pybo'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('create/', views.ProjectCreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.ProjectUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.ProjectDeleteView.as_view(), name='delete'),
    path('auth/', views.auth_check, name='auth'),  # 인증 관련은 그대로 function view
    path('logout/', views.logout_view, name='logout'),
]


