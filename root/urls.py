"""Root URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, include
from graphene_django.views import GraphQLView

from accounts.views import DRFAuthenticatedGraphQLView

urlpatterns = [
    ############################
    # DJANGO ADMIN URL
    ############################
    path('admin/', admin.site.urls),

    #############################
    # REST API URLS
    #############################

    # home page
    path('', lambda request: JsonResponse({"data": "Welcome to the Voting API"})),

    # accounts
    path('accounts/', include('accounts.urls')),

    ############################
    # GRAPH-QL URLS
    ############################

    path("graphi-ql", GraphQLView.as_view(graphiql=True)),
    path("graph-ql", DRFAuthenticatedGraphQLView.as_view()),

]
