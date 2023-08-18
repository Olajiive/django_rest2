from django.urls import path, include
from .views import GetCreate, GetUpdateDelete, SignupView, LoginView, LogoutView
#from .views import GenericAPIView
#from .views import ArticleViewset
#from rest_framework.routers import DefaultRouter

#Viewsets and Routers
"""router = DefaultRouter()
router.register('article', ArticleViewset, basename="article")"""

"""urlpatterns = [
    #Viewset
    path("/viewset/", include(router.urls)),
    path("/viewset/<int:id>/", include(router.urls)),

    #GenericApiview
    path("generic/articles", GenericAPIView.as_view(), name="Articles"  ),
    path("generic/article/<int:id>", GenericAPIView.as_view(), name="Articles" ),
]"""

urlpatterns = [
    path("signup", SignupView.as_view(), name="Signup"),
    path("login", LoginView.as_view(), name="Login"),
    path("logout", LogoutView.as_view(), name="Logout"),
    path("articles", GetCreate.as_view(), name="Get-all-Articles"  ),
    path("article/create", GetCreate.as_view(), name="Create-an-Article"  ),
    path("article/get/<str:pk>", GetUpdateDelete.as_view(), name="Get-an-Article-by-Id" ),
    path("article/update/<str:pk>", GetUpdateDelete.as_view(), name="Update-Article-by-Id" ),
    path("article/delete/<str:pk>", GetUpdateDelete.as_view(), name="Delete-Article-by-Id" )
]