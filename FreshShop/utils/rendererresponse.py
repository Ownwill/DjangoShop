from rest_framework.renderers import JSONRenderer

class Customrenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        """

        :param data: 返回的数据
        :param accepted_media_type:接收的内容
        :param renderer_context:呈现的内容
        :return:
        """
        if renderer_context: #和if request.method == 'POST'有类似处。如果有数据请求。
            if isinstance(data,dict):    #判断返回的数据是否是字典
                msg = data.pop('msg','请求成功')  #如果是字典获取字典中的msg参数
                code = data.pop('code',0)        #如果是字典获取字典中的code参数
            else:    #非字典请求
                msg = '请求成功'
                code = 0
            ret = {
                'msg':msg,
                'code':code,
                'data':data
            }  #重新组织返回数据的格式
            return super().render(ret, accepted_media_type, renderer_context)
            #返回数据，把ret返回
        else:
            # 没有发生修改，返回原数据格式
            return super().render(data, accepted_media_type, renderer_context)