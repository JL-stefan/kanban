# -*- coding: utf-8 -*-
from ..models import Project
from ..serializers import ProjectSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .. import const
from ..logger import Logger

# from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser,IsAuthenticatedOrReadOnly,DjangoObjectPermissions,DjangoModelPermissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

logger = Logger().logger

class ProjectList(APIView):

    # authentication_classes = (SessionAuthentication, BasicAuthentication)
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        """
        获取所有项目信息
        :param request:
        :param format:
        :return:
        """
        id = request.query_params.get('id')

        try:
            if id:
                projectList = Project.objects.get(id=id)
                serializer = ProjectSerializer(projectList)
            else:
                projectList = Project.objects.all()
                serializer = ProjectSerializer(projectList, many=True)
            logger.info(serializer.data)
            return Response(serializer.data, status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response(const.NOT_EXIST, status.HTTP_200_OK)
        except Exception as e:
            return Response(e.args, status.HTTP_400_BAD_REQUEST)


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
            logger.info("新增项目信息:"+str(serializer.data))
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            logger.error(serializer.errors)
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


    def put(self, request, format=None):
        """
        更新项目信息
        :param request:
        :param format:
        :return:
        """

        id = request.data.get("id")
        try:
            project = Project.objects.get(id=id)
            serializer = ProjectSerializer(project, request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status.HTTP_200_OK)
        except Exception as e:
            return Response(e.args, status.HTTP_400_BAD_REQUEST)


    def delete(self, request, format=None):
        """
        删除项目
        :param request:
        :param format:
        :return:
        """
        # try:
        #     id = request.query_params.get("id")
        #     id = int(id)
        #     project = Project.objects.get(id=id)
        # except:
        #     return Response(const.BAD_REQUEST, status.HTTP_400_BAD_REQUEST)
        # logger.info(project)
        # project.delete()
        # return Response(const.SUCCESS_REQUEST, status.HTTP_200_OK)

        id = request.query_params.get("id")
        try:
            Project.objects.get(id=id).delete()
            return Response(const.SUCCESS_REQUEST, status.HTTP_200_OK)
        except Exception as e:
            return Response(e.args, status.HTTP_400_BAD_REQUEST)


