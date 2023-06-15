from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

class MixinViewSet(viewsets.ModelViewSet):

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data_t = self.get_paginated_response(serializer.data)
        else:
            data_t = self.get_serializer(queryset, many=True)
        return Response({'code': 20000, 'message': data_t.data}, status=status.HTTP_200_OK)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({'code': 20000, 'message': serializer.data}, status=status.HTTP_200_OK)
    
    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            return Response({'code': 20000, 'message': serializer.data}, status=status.HTTP_200_OK)
        except Exception as ex:
            print(ex)
            return Response({'code': 30000, 'message': ex}, status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'code': 20000, 'message': serializer.data}, status=status.HTTP_201_CREATED, headers=headers)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'code': 20000, 'message': ''}, status=status.HTTP_202_ACCEPTED)
