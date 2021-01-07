# -*- coding: utf-8 -*-
from rest_framework.views import APIView
from ..models import Iteration
from rest_framework.response import Response
from rest_framework import status
from ..serializers import IterationSerializer
import json

class IterationsList(APIView):

    def get(self, request, format=None):
        """
        获取迭代信息
        :param request:
        :param format:
        :return:
        """
        id = request.query_params.get("id")
        if id:
            try:
                iterDetail = Iteration.objects.get(id=id)
            except Iteration.DoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            serializer = IterationSerializer(iterDetail)
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            try:
                iterList = Iteration.objects.all()
            except Iteration.DoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            serializer = IterationSerializer(iterList, many=True)
            return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, format=None):
        """
        新增迭代信息
        :param request:
        :param format:
        :return:
        """
        serializer = IterationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


    def put(self, request, format=None):
        """
        更新迭代信息
        :param reuqest:
        :param format:
        :return:
        """
        try:
            id = request.data.get("id")
            iterDetail = Iteration.objects.get(id=id)
            serializer = IterationSerializer(iterDetail, request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status.HTTP_200_OK)
        except Iteration.DoesNotExit:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        """
        删除迭代信息
        :param request:
        :param format:
        :return:
        """
        try:
            id = request.query_params.get("id")
            iterDetail = Iteration.objects.get(id=id)
            iterDetail.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Iteration.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
