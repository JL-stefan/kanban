# -*- coding: utf-8 -*-
from rest_framework.views import APIView
from ..models import Task
from ..serializers import TaskSerializer
from rest_framework.response import Response
from rest_framework import status
from .. import const
from ..schema_view import DocParam, BaseSchema
import coreapi
from rest_framework.schemas import AutoSchema
from .task_chema_view import *

periodictaskSchema = BaseSchema(params_desc_dict={
    'post': {
        "crontab": "定时crontab. json。 包含的字段有: minute, hour, day_of_week, day_of_month, month_of_year",
        "name": "该定时任务名称",
        "task": "模板任务名",
        "args": "传递给任务模板参数. 数组",
        "kwargs": "传递给任务模板参数. json字符串",
        "queue": "将任务放在哪个队列中.",
        "enabled": "是否开启该任务. True or False. 默认为True",
        "description": "定时任务说明"
    }
},
)

class TaskList(APIView):


    schema = TASK_GET_SCHEMA

    # schema = AutoSchema(
    #     manual_fields=[
    #         coreapi.Field(name="extra_param", required=False, location="form", description="额外参数"),
    #     ]
    # )

    def get(self, request, format=None):
        """
        查询任务信息
        :param request:
        :param format:
        :return:
        """
        id = request.query_params.get("id")
        try:
            if id:
                taskList = Task.objects.get(id=id)
                serializer = TaskSerializer(taskList)
            else:
                taskList = Task.objects.all()
                serializer = TaskSerializer(taskList, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        except Task.DoesNotExist:
            return Response(const.NOT_EXIST, status.HTTP_200_OK)
        except Exception as e:
            return Response(e.args, status.HTTP_400_BAD_REQUEST)


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
        id = request.data.get("id")
        try:
            taskDetail = Task.objects.get(id=id)
            serializer = TaskSerializer(taskDetail, request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status.HTTP_200_OK)
        except Exception as e:
            return Response(e.args, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        """
        删除任务信息
        :param request:
        :param format:
        :return:
        """
        id = request.query_params.get("id")
        try:
            taskDetail = Task.objects.get(id=id)
            taskDetail.delete()
            return Response(const.SUCCESS_REQUEST, status.HTTP_200_OK)
        except Task.DoesNotExist:
            return Response(const.BAD_REQUEST, status.HTTP_400_BAD_REQUEST)


class TaskStatus(APIView):
    '''
    put:
    测试测试测试
    '''

    coreapi_fields = (
        DocParam(name="id", type="number", location="form", description="项目ID", required=True),
        DocParam(name="status", type="number", location="form", description="任务状态", required=True),
    )

    schema = AutoSchema(
        manual_fields=[
            coreapi.Field(name="extra_param", required=False, location="form", description="额外参数"),
        ]
    )

    def put(self, request, *args, **kwargs):
        # """ 更新任务状态 """

        try:
            # 取参
            id = request.data.get("id")
            newStatus = request.data.get("status")
            # 获取对象
            taskDetail = Task.objects.get(id=id)
            # 赋值，修改状态
            taskDetail.status = newStatus
            # 提交保存
            taskDetail.save()
            # 序列化任务信息，用于返回
            serializer = TaskSerializer(taskDetail)
            return Response(serializer.data, status.HTTP_200_OK)
        except Exception as e:
            return Response(e.args, status.HTTP_400_BAD_REQUEST)


