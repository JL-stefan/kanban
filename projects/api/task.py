# -*- coding: utf-8 -*-
from rest_framework.views import APIView
from ..models import Task
from ..serializers import TaskSerializer
from rest_framework.response import Response
from rest_framework import status

notExist = {}

class TaskList(APIView):


    def get(self, request, format=None):
        """
        查询任务信息
        :param request:
        :param format:
        :return:
        """
        id = request.query_params.get("id")
        if id:
            try:
                taskDetail = Task.objects.get(id=id)
                serializer = TaskSerializer(taskDetail)
                return Response(serializer.data, status.HTTP_200_OK)
            except Task.DoesNotExist:
                return Response(notExist, status=status.HTTP_200_OK)
        else:
            try:
                taskList = Task.objects.all()
                serializer = TaskSerializer(taskList, many=True)
                return Response(serializer.data, status.HTTP_200_OK)
            except Task.DoesNotExist:
                return Response(notExist, status=status.HTTP_200_OK)


    def post(self, request, format=None):
        """
        新增任务信息
        :param request:
        :param format:
        :return:
        """

        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        """
        更新任务信息
        :param request:
        :param format:
        :return:
        """

        try:
            id = request.data.get("id")
            taskDetail = Task.objects.get(id=id)
            serializer = TaskSerializer(taskDetail, request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status.HTTP_200_OK)
        except Task.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        """
        删除任务信息
        :param request:
        :param format:
        :return:
        """
        try:
            id = request.query_params.get("id")
            taskDetail = Task.objects.get(id=id)
            taskDetail.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Task.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class TaskStatus(APIView):

    def put(self, request, format=None):
        pass
