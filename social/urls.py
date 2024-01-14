from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from social.views import PostListAPIView, UserRatingAPIView

urlpatterns = [
    path('login/', obtain_auth_token),
    path('posts/', PostListAPIView.as_view()),
    path('post/', UserRatingAPIView.as_view())
]
