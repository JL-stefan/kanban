# -*- coding: utf-8 -*-
from ..models import Project
from ..serializers import ProjectSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import logging
from django.http import QueryDict
import json

notExist = {}

class ProjectList(APIView):

    def get(self, request, format=None):
        """
        获取所有项目信息
        :param request:
        :param format:
        :return:
        """
        id = request.query_params.get('id', default=0)
        if id != 0:
            try:
                project = Project.objects.get(id=id)
                serializer = ProjectSerializer(project)
                return Response(serializer.data, status.HTTP_200_OK)
            except Project.DoesNotExist:
                return Response(notExist,status=status.HTTP_400_BAD_REQUEST)
        else:
            projects = Project.objects.all()
            serializer = ProjectSerializer(projects, many=True)
            return Response(serializer.data, status.HTTP_200_OK)


    def post(self, request, format=None):
        """
        新增项目
        :param request:
        :param format:
        :return:
        """
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logging.info("新增项目信息:"+str(serializer))
            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


    def put(self, request, format=None):
        """
        更新项目信息
        :param request:
        :param format:
        :return:
        """
        try:
            id = request.data.get("id")
            project = Project.objects.get(id=id)
            serializer = ProjectSerializer(project, request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, format=None):
        """
        删除项目
        :param request:
        :param format:
        :return:
        """
        try:
            id = request.query_params.get("id")
            project = Project.objects.get(id=id)
            project.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Project.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)


