from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from . views import ProjectViewSet, PeopleOnProjectViewSet, UserViewSet


router = routers.DefaultRouter()
router.register('projects', ProjectViewSet, 'project-list')
router.register('people-on-projects', PeopleOnProjectViewSet, 'people-on-projects-list')
router.register('users', UserViewSet)

urlpatterns = [
    path('', include(router.urls))
]
