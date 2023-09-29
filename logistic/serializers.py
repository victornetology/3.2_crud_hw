from rest_framework import serializers
from logistic.models import Product, Stock, StockProduct
from rest_framework.fields import ListField

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']



class StringArrayField(ListField):
    def to_representation(self, obj):
        obj = super().to_representation(self, obj)
        return ",".join([str(element) for element in obj])

    def to_internal_value(self, data):
        data = data.split(",")  # convert string to list
        return super().to_internal_value(self, data)

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'

    positions = ProductPositionSerializer(many=True)
    #products = StringArrayField()
    def create(self, validated_data):
        positions = validated_data.pop('positions')
        stock = super().create(validated_data)
        for position in positions:
            StockProduct.objects.create(stock=stock, **position)
        return stock

    def update(self, instance, validated_data):
        positions = validated_data.pop('positions')
        stock = super().update(instance, validated_data)
        stock.positions.all().delete()
        for position in positions:
            StockProduct.objects.create(stock=stock, **position)
        return stock
