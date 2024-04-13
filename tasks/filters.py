import django_filters

from tasks.models import Task


class TaskFilter(django_filters.FilterSet):
    assigner = django_filters.CharFilter(field_name='assigner__username', lookup_expr='icontains')
    assignee = django_filters.CharFilter(field_name='assignee__username', lookup_expr='icontains')
    start_creation_date = django_filters.DateFilter(field_name='created_at__date', lookup_expr='gte')
    end_creation_date = django_filters.DateFilter(field_name='created_at__date', lookup_expr='lte')

    class Meta:
        model = Task
        fields = ['title', 'start_creation_date', 'end_creation_date', 'assigner', 'assignee']
