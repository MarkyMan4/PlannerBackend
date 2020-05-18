from rest_framework import serializers
from .models import Project, PeopleOnProject
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        extra_kwargs = {'url': {'required': True}}

class PeopleOnProjectSerializer(serializers.Serializer):
    project = serializers.CharField(read_only=True, source='project.name')
    user = serializers.CharField(read_only=True, source='user.username')
    percent_allocated = serializers.IntegerField()
    
    class Meta:
        model = PeopleOnProject
        fields = ('user', 'percent_allocated')

class UserSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'required': True, 'write_only': True}}

        def create(self, validated_data):
            user = User.objects.create_user(**validated_data)
            Token.objects.create(user=user)

            return user
