from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import ProjectSerializer, PeopleOnProjectSerializer, UserSerializer
from .models import Project, PeopleOnProject
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        is_active = self.request.query_params.get('active')

        # if the active query parameter doesn't have a boolean value or isn't provided, default to True
        if is_active == 'false':
            is_active = False
        else:
            is_active = True

        # need to cast to boolean since it comes in as a string
        queryset = Project.objects.filter(active=is_active)
        
        return queryset

    @action(methods=['POST'], detail=True)
    def deactivate(self, request, pk=None):
        proj = Project.objects.get(id=pk)
        proj.active = False
        proj.save()

        serializer = ProjectSerializer(proj, many=False)
        response = {'message': 'project has been deactivated', 'result': serializer.data}

        return Response(response, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=True)
    def update_project(self, request, pk):
        try:
            proj = Project.objects.get(id=pk)
            proj.name = request.data['name']
            proj.description = request.data['description']
            proj.start_date = request.data['start_date']
            proj.end_date = request.data['end_date']
            proj.save()

            serializer = ProjectSerializer(proj, many=False)
            response = {'message': 'project has been updated', 'result': serializer.data}

            return Response(response, status=status.HTTP_200_OK)
        except:
            response = {'message': 'failed to update project'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], detail=True)
    def allocate_time(self, request, pk=None):
        if 'percent_allocated' in request.data:
            project = Project.objects.get(id=pk)
            percent_allocated = request.data['percent_allocated']
            user = request.user

            # update allocations if it already exists
            try:
                emp_proj = PeopleOnProject.objects.get(user=user.id, project=project.id)
                emp_proj.percent_allocated = percent_allocated
                emp_proj.save()

                serializer = PeopleOnProjectSerializer(emp_proj, many=False)
                response = {'message': 'allocation has been updated', 'result': serializer.data}

                return Response(response, status=status.HTTP_200_OK)
            
            # enter a new allocation if no allocation existed previously
            except:
                emp_proj = PeopleOnProject.objects.create(user=user, project=project, percent_allocated=percent_allocated)
                serializer = PeopleOnProjectSerializer(emp_proj, many=False)
                response = {'message': 'allocation has been created', 'result': serializer.data}

                return Response(response, status=status.HTTP_200_OK)

        else:
            response = {'message': 'please enter percent allocation'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

class PeopleOnProjectViewSet(viewsets.ModelViewSet):
    # queryset = PeopleOnProject.objects.all()
    serializer_class = PeopleOnProjectSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        proj_id = self.request.query_params.get('proj_id')
        queryset = PeopleOnProject.objects.filter(project=proj_id)

        return queryset

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
