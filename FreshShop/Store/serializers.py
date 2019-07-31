from rest_framework import serializers

from Store.models import Goods
from Store.models import GoodType



class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Goods
        fields = ['goods_name','goods_price','goods_number','goods_date','goods_safeDate']


class GoodsTypeserializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GoodType
        fields = ['name','description']
