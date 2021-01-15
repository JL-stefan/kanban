# -*- coding: utf-8 -*-

from rest_framework.schemas import AutoSchema
import coreapi

TASK_GET_SCHEMA = AutoSchema(
    manual_fields=[
        coreapi.Field(name="id", type="number", location="query", description="任务ID")
    ]
)