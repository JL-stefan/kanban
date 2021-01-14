# -*- coding: utf-8 -*-
from rest_framework.views import APIView
from ..models import Iteration
from rest_framework.response import Response
from rest_framework import status
from ..serializers import IterationSerializer
from .. import const
from ..schema_view import DocParam

class IterationsList(APIView):

    coreapi_fields = (
        DocParam(name="id", location="query", description="项目ID", required=True, type=int)
    )

    def get(self, request, format=None):
        """
        获取迭代信息
        :param request:
        :param format:
        :return:
        """
        id = request.query_params.get("id")
        try:
            if id:
                iterList = Iteration.objects.get(id=id)
                serializer = IterationSerializer(iterList)
            else:
                iterList = Iteration.objects.all()
                serializer = IterationSerializer(iterList, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        except Iteration.DoesNotExist:
            return Response(const.NOT_EXIST, status.HTTP_200_OK)
        except Exception as e:
            return Response(e.args, status.HTTP_400_BAD_REQUEST)


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
        id = request.data.get("id")
        try:
            iterDetail = Iteration.objects.get(id=id)
            serializer = IterationSerializer(iterDetail, request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status.HTTP_200_OK)
        except Exception as e:
            return Response(e.args, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        """
        删除迭代信息
        :param request:
        :param format:
        :return:
        """

        id = request.query_params.get("id")
        try:
            iterDetail = Iteration.objects.get(id=id)
            iterDetail.delete()
            return Response(const.SUCCESS_REQUEST, status.HTTP_200_OK)
        except Exception as e:
            return Response(e.args, status.HTTP_400_BAD_REQUEST)
