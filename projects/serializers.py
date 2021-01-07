# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import Project, Iteration, Task

class ProjectSerializer(serializers.ModelSerializer):
    """
    项目信息序列化
    """
    desc = serializers.CharField(required=False, allow_blank=True)
    createAt = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    updateAt = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)


    class Meta:
        model = Project
        fields = "__all__"

class IterationSerializer(serializers.ModelSerializer):
    """
    迭代信息序列化
    """
    desc = serializers.CharField(required=False, allow_blank=True)
    createAt = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    updateAt = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)

    class Meta:
        model = Iteration
        fields = "__all__"

class TaskSerializer(serializers.ModelSerializer):
    """
    任务信息序列化
    """
    tag = serializers.CharField(required=False, allow_blank=True)
    desc = serializers.CharField(required=False, allow_blank=True)
    createAt = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    updateAt = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)

    class Meta:
        model = Task
        fields = "__all__"