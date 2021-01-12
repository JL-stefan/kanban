from django.db import models

# Create your models here.
class ModelBase(models.Model):
    createAt = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    createBy = models.IntegerField(verbose_name="创建人员",default=0)
    updateAt = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    updateBy = models.IntegerField(verbose_name="更新人员",default=0)

    class Meta:
        abstract = True


class Project(ModelBase):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, unique=True, verbose_name="项目名称")
    leader = models.IntegerField(verbose_name="项目负责人")
    desc = models.CharField(max_length=256, verbose_name="项目描述")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "项目"
        verbose_name_plural = "项目信息"

class Iteration(ModelBase):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, unique=True, verbose_name="迭代名称")
    leader = models.IntegerField(verbose_name="迭代负责人")
    desc = models.CharField(max_length=256, verbose_name="迭代描述")
    projectID = models.IntegerField(verbose_name="项目ID")


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "迭代"
        verbose_name_plural = "迭代信息"


STATUS_TODO = 1
STATUS_DOING = 2
STATUS_DONE = 3
STATUS_CANCEL = 4

taskStatus = (
    (STATUS_TODO, "待办"),
    (STATUS_DOING, "进行中"),
    (STATUS_DONE, "已完成"),
    (STATUS_CANCEL, "已取消")
)

class Task(ModelBase):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=128, verbose_name="标题")
    status = models.IntegerField(verbose_name="任务状态", choices=taskStatus, default=STATUS_TODO)
    user = models.IntegerField(verbose_name="执行者")
    tag = models.CharField(max_length=64, verbose_name="标签")
    desc = models.CharField(max_length=1024, verbose_name="描述")
    iterationID = models.IntegerField(verbose_name="迭代ID")

    def __str___(self):
        return self.name

    class Meta:
        verbose_name = "任务"
        verbose_name_plural = "任务信息"