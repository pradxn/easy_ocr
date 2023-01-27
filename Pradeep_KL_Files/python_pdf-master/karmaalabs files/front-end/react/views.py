from django.shortcuts import render
from rest_framework.views import APIView
from page.models import React
from rest_framework.response import Response
from page.serializer import *


# Create your views here.

class ReactView(APIView):
    serializer_class = ReactSerializer

    def get(self, request):
        detail = [{"name": detail.name,
                   "user_num": detail.idno,
                   "treatment": detail.detail,
                   "start_time": detail.start,
                   "end_time": detail.end}
                  for detail in React.objects.all()]
        return Response(detail)

    def post(self, request):
        serializer = ReactSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
