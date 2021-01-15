# -*- coding: utf-8 -*-
from rest_framework.schemas import SchemaGenerator, AutoSchema
from rest_framework.schemas.coreapi import LinkNode, insert_into
from rest_framework.renderers import *
from rest_framework_swagger import renderers
from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAuthenticatedOrReadOnly
from django.http import JsonResponse

class MySchemaGenerator(SchemaGenerator):

    def get_links(self, request=None):
        links = LinkNode()

        paths = []
        view_endpoints = []
        for path, method, callback in self.endpoints:
            view = self.create_view(callback, method, request)
            path = self.coerce_path(path, method, view)
            paths.append(path)
            view_endpoints.append((path, method, view))

        # Only generate the path prefix for paths that will be included
        if not paths:
            return None
        prefix = self.determine_path_prefix(paths)

        for path, method, view in view_endpoints:
            if not self.has_view_permissions(path, method, view):
                continue
            link = view.schema.get_link(path, method, base_url=self.url)
            # 添加下面这一行方便在views编写过程中自定义参数.
            link._fields += self.get_core_fields(view)

            subpath = path[len(prefix):]
            keys = self.get_keys(subpath, method, view)

            # from rest_framework.schemas.generators import LinkNode, insert_into
            insert_into(links, keys, link)

        return links

    # 从类中取出我们自定义的参数, 交给swagger 以生成接口文档.
    def get_core_fields(self, view):
        return getattr(view, 'coreapi_fields', ())

class SwaggerSchemaView(APIView):
    _ignore_model_permissions = True
    exclude_from_schema = True

    permission_classes = [AllowAny]
    # 此处涉及最终展示页面权限问题，如果不需要认证，则使用AllowAny，这里需要权限认证，因此使用IsAuthenticated
    # permission_classes = [IsAuthenticated]
    # from rest_framework.renderers import *
    renderer_classes = [
        CoreJSONRenderer,
        renderers.OpenAPIRenderer,
        renderers.SwaggerUIRenderer
    ]

    def get(self, request):
        # 此处的titile和description属性是最终页面最上端展示的标题和描述
        generator = MySchemaGenerator(title='API说明文档',description='''接口测试、说明文档''')

        schema = generator.get_schema(request=request)

    # from rest_framework.response import Response
        return Response(schema)


def DocParam(name="default", location="query",required=True, description=None, type="string",*args, **kwargs):
    return coreapi.Field(name=name, location=location, required=required, description=description, type=type)




#######自定义文档

class BaseSchema(AutoSchema):
    """
    自动生成的文档会有缺失，或者是因为可读性比较差。所以需要对文档中的字段进行自定义注解。
    该类是通用的对文档中的get、post、put、delete、patch进行注释。
    是在已有字段的基础上修改注释.

    `get`是对get中的字段进行注解说明。
    `other`是`post`、`put`、`delete`、`patch`

    例子:
    {
       "get": {
           "字段名": "对该字段进行注释"
       },
       "post": {
           "字段名": "对该字段进行注释"
       }
    }

    """

    def __init__(self, manual_fields=None, params_desc_dict=None):
        self.params_desc_dict = {
            "get": {
                "page": "当前页码",
                "page_size": "每一页显示的行数. 默认传 10条"
            },
            "other": {

            },
            "post": {
                "page": "当前页码",
                "page_size": "每一页显示的行数. 默认传 10条"
            }
        }

        if params_desc_dict:
            if 'get' in params_desc_dict:
                self.params_desc_dict['get'].update(params_desc_dict['get'])

            if 'other' in params_desc_dict:
                self.params_desc_dict['other'].update(params_desc_dict['other'])

            if 'post' in params_desc_dict:
                self.params_desc_dict['post'].update(params_desc_dict['post'])

        super().__init__(manual_fields)

    def get_link(self, path, method, base_url):
        link = super().get_link(path, method, base_url)

        fields = ["name"]


        # params_method = 'get' if method.lower() == 'get' else 'other'
        params_method = method.lower()

        for field in link.fields:
            if field.name in self.params_desc_dict[params_method].keys():
                field = field._replace(
                    schema=coreschema.String(description=self.params_desc_dict[params_method][field.name])
                )

            fields.append(field)
            print(link.fields)
        return coreapi.Link(
            url=link.url,
            action=link.action,
            encoding=link.encoding,
            fields=fields,
            description=link.description
        )



