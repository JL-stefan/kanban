# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import Project, Iteration, Task, ModelBase





class ModelBaseSerializer(serializers.ModelSerializer):
    """
    序列化基础基础时间信息
    """
    class Meta:
        model = ModelBase
        fields = ("createAt", "createBy", "updateAt", "updateBy")

# 基础时间常量
BASE_TIME = ModelBaseSerializer.Meta.fields

class ProjectSerializer(serializers.ModelSerializer):
    """
    项目信息序列化
    """
    desc = serializers.CharField(required=False, allow_blank=True)
    createAt = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    updateAt = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)


    class Meta:
        model = Project
        fields = ("id", "name", "leader", "desc") + BASE_TIME

class IterationSerializer(serializers.ModelSerializer):
    """
    迭代信息序列化
    """
    desc = serializers.CharField(required=False, allow_blank=True)
    createAt = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    updateAt = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)

    class Meta:
        model = Iteration
        fields = ("id", "name", "leader", "desc", "projectID") + BASE_TIME

class TaskSerializer(serializers.ModelSerializer):
    """
    任务信息序列化
    """
    status_display = serializers.SerializerMethodField()

    tag = serializers.CharField(required=False, allow_blank=True)
    desc = serializers.CharField(required=False, allow_blank=True)
    createAt = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    updateAt = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)

    class Meta:
        model = Task
        fields = ("id", "title", "status", "status_display", "user", "tag", "desc", "iterationID") + BASE_TIME

    def get_status_display(self, obj):
        return obj.get_status_display()