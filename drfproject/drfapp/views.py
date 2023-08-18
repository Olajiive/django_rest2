from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.views import APIView
from .models import Article
from .serializers import ArticleSerializer
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
#from rest_framework.authentication import SessionAuthentication, BasicAuthentication 
#from rest_framework.decorators import decorators
#from rest_framework import generics, mixins
#from rest_framework import viewsets



class SignupView(APIView):
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(username=request.data["username"])
            user.set_password(request.data['password'])
            user.save()
            token = Token.objects.create(user=user)
            return Response({"token":token.key, "user":serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        user = get_object_or_404(User, username=request.data['username'])
        if not user.check_password(request.data['password']):
            return Response({"detail": "Not found"}, status=status.HTTP_400_BAD_REQUEST)
        token, created = Token.objects.get_or_create(user=user)
        serializer = UserSerializer(instance=user)
        return Response({"token":token.key, "user":serializer.data})


# Create your views here.
#Viewset and Routers
"""class ArticleViewset(viewsets.ViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    lookup_field = "id"
    authentication_classes=[BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    def list(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = ArticleSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def retrieve(self, request, pk=None):
        try:
            article = Article.objects.get(pk=pk)
            serializer = ArticleSerializer(instance=article)
            return Response(serializer.data)

        except Article.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def edit(self, request, pk=None):
        article = Article.objects.get(pk=pk)
        serializer = ArticleSerializer(instance=article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def destroy(self, request, pk=None):
        try:
            article = Article.objects.get(pk=pk)
            article.delete()
            return Response({'message': 'Successfully deleted'}, status=status.HTTP_204_NO_CONTENT)

        except Article.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)"""
        


#GeneriApiView
"""class GenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    lookup_field = "id"
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request , id=None):
        if id:
            return self.retrieve(request)
        return self.list(request)
    
    def post(self, request):
        return self.create(request)
    
    def update(self, request, id=None):
        return self.update(request, id)
    
    def delete(self, request, id=None):
        return self.delete(request, id)"""
                         
class GetCreate(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes= [IsAuthenticated]
    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ArticleSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetUpdateDelete(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes= [IsAuthenticated]
    def get(self, request, pk):
        try:
            article = Article.objects.get(pk=pk)
            serializer = ArticleSerializer(instance=article)
            return Response(serializer.data)

        except Article.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def put(self, request, pk):
        article = Article.objects.get(pk=pk)
        serializer = ArticleSerializer(instance=article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def delete(self, request, pk):
        try:
            article = Article.objects.get(pk=pk)
            article.delete()
            return Response({'message': 'Successfully deleted'}, status=status.HTTP_204_NO_CONTENT)

        except Article.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        

class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes= [IsAuthenticated]

    def post(self, request):
        if request.method == "POST":
            request.user.auth_token.delete()
        return Response({"message": "you have successfully been logged out"}, status=status.HTTP_200_OK)
