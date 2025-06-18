from django.shortcuts import get_object_or_404

from rest_framework import mixins
from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Template
from .serializers import TemplateSerializer, MinTemplateSerializer


class MinTemplateView(mixins.ListModelMixin,
                      generics.GenericAPIView):
    queryset = Template.objects.all()
    serializer_class = MinTemplateSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class GetTemplateView(mixins.RetrieveModelMixin,
                      generics.GenericAPIView):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class TemplateListCreateView(mixins.ListModelMixin,
                             generics.GenericAPIView):
    queryset = Template.objects.all()
    serializer_class = MinTemplateSerializer
    
    def get(self, request: Request):
        return self.list(request)

    # def post(self, request: Request): # TODO : finish this after session app created
    #     query_session_id = request.query_params.get("session_id")
    #     cookie_session_id = request.COOKIES.get("session_id")

    #     if not query_session_id:
    #         return Response(status=400) # TODO : add message
    #     if not cookie_session_id:
    #         return Response(status=401) # TODO : add message
    #     if query_session_id != cookie_session_id:
    #         return Response(status=401) # TODO : add message
        
    #     session = Session.objects.get(id=query_session_id)



class TemplateRetreiveView(mixins.RetrieveModelMixin,
                   generics.GenericAPIView):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer

    def get(self, request: Request, pk: int):
        return self.retrieve(request, pk)
