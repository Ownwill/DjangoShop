from django.utils.deprecation import MiddlewareMixin#中间件父类
from django.shortcuts import render_to_response
from django.http import HttpResponse

import os
import datetime
from FreshShop.settings import BASE_DIR

class MiddlewareTest(MiddlewareMixin):
    # def process_request(self,request):
    #     #例：在这个位置可以拦截用户，禁止可疑用户访问
    #     username = request.GET.get('username')
    #     if username and username == 'sss':
    #         return HttpResponse('404')

    # def process_view(self,request,view_func,view_args,view_kwargs):
    #     print('*'*20,'process_view')

    # def process_exception(self,request,exception):
    #     """
    #     例：这个地方可以进行错误记录制作错误日志
    #     :param request:视图处理中的请求
    #     :param exception:
    #     :return:
    #     """
    #     now = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S') #获取出错时间
    #     level = 'Error'                                             #错误等级
    #     content = str(exception)                                    #避免格式错误，都转成字符串
    #     log_result = '%s [%s] %s'%(now,level,content)               #上述内容整合
    #     file_path = os.path.join(BASE_DIR,'error.log')              #将错误日志保存在根目录下
    #     with open(file_path,'a') as f:
    #         f.write(log_result)                                     #将错误写入文件中
    #
    #
    #     # print('process_exception')
    #     # print(exception)
    #
    #
    #
    #


    # def process_template_response(self,request,response):
    #     print('process_template_response')
    #     return response


    def process_response(self,request,response):
        print('process_response')
        return response