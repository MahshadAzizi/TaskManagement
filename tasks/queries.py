from tasks.models import Task


def get_tasks_all():
    return Task.objects.all()


def get_task_by_id(pk: int):
    try:
        return Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Task.DoesNotExist()
