from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, serializers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .permissions import IsAdminOrReadOnly
from .serializers import get_base_serializer_class


class CreateListRetrieveViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """
    A viewset that provides `retrieve`, `create`, and `list` actions.

    To use it, override the class and set the `.queryset` and
    `.serializer_class` attributes.
    """

    pass


def get_viewset(
    model_class,
    serializer=None,
    query: QuerySet = None,
    lookup_field: str = None,
    *args,
    **kwargs
):
    class BaseViewSet(CreateListRetrieveViewSet):
        queryset = query or model_class.objects.all()
        serializer_class = serializer or get_base_serializer_class(model_class)
        permission_classes = [IsAdminOrReadOnly]
        filter_backends = [filters.SearchFilter, DjangoFilterBackend]

        @action(detail=False)
        def meta(self, request):
            """
            Returns a meta.
            """
            fields = model_class.field_list()
            return Response(fields)

        @action(detail=False)
        def table(self, request):
            fields = model_class.table_fields()
            return Response(fields)

    if lookup_field:
        setattr(BaseViewSet, "lookup_field", lookup_field)

    # if model_class.search_fields():
    #     setattr(BaseViewSet, "search_fields", model_class.search_fields())
    #
    # if model_class.filter_fields():
    #     setattr(BaseViewSet, "filterset_fields", model_class.filter_fields())

    return BaseViewSet
