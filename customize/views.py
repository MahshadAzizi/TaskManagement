from rest_framework import status
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt import exceptions
from rest_framework_simplejwt.views import TokenObtainPairView


class CustomViewSet(ModelViewSet):
    queryset = None
    serializer_class = None

    lookup_field = 'pk'
    lookup_url_kwarg = None

    # The filter backend classes to use for queryset filtering
    filter_backends = api_settings.DEFAULT_FILTER_BACKENDS

    # The style to use for queryset pagination.
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({'results': serializer.data, 'status': status.HTTP_201_CREATED})

    def perform_create(self, serializer):
        serializer.save()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)
        return Response({'results': serializer.data, 'status': status.HTTP_200_OK})

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({'results': serializer.data, 'status': status.HTTP_200_OK})

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response({'results': serializer.data, 'status': status.HTTP_200_OK})

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'results': '', 'status': status.HTTP_204_NO_CONTENT})

    def perform_destroy(self, instance):
        instance.delete()


class CustomJWTAuthenticationView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except exceptions.AuthenticationFailed:
            return Response({
                'error': True,
                'message': 'Invalid Username or Password',
            }, status=status.HTTP_401_UNAUTHORIZED)

        return Response({'results': serializer.validated_data, 'status': status.HTTP_200_OK})
