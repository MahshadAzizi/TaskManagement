from rest_framework import serializers

from tasks.models import Task
from users.models import User
from users.serializers import UserSerializer


class CreateTaskSerializer(serializers.ModelSerializer):
    assignee = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all(),
                                            required=False)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'assignee']

    def create(self, validated_data):
        user = self.context['request'].user
        return Task.objects.create(assigner=user, **validated_data)


class TaskSerializer(serializers.ModelSerializer):
    assigner = UserSerializer(many=False, read_only=True)
    assignee = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'assigner', 'assignee', 'created_at', 'updated_at']
