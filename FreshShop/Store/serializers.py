from rest_framework import serializers

from Store.models import Goods
from Store.models import GoodType



class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Goods #选用的数据模型
        fields = ['goods_name','goods_price','goods_number','goods_date','goods_safeDate'] #调用时使用的数据字段


class GoodsTypeserializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GoodType
        fields = ['name','description']
