from rest_framework import serializers

from .models import Product, Stock, StockProduct

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id','title', 'description']

class ProductPositionSerializer(serializers.ModelSerializer):

    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']

class StockSerializer(serializers.ModelSerializer):

    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['id','address', 'positions']

    def create(self, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # создаем склад по его параметрам
        stock = super().create(validated_data)
        for pos in positions:
            StockProduct.objects.create(stock=stock, **pos)

        return stock

    def update(self, instance, validated_data):
        # достаем связанные данные для других таблиц

        positions = validated_data.pop('positions')

        # обновляем склад по его параметрам
        stock = super().update(instance, validated_data)
        data_stockProduct = StockProduct.objects.all()

        n = len(positions)
        q = len(StockProduct.objects.filter(stock_id=instance.id))
        i = 0

        if n == q:
            for data in data_stockProduct:
                if data.stock_id == instance.id:
                    pos = positions[i]
                    StockProduct.objects.filter(stock_id=instance.id, id = data.id ).update(stock=stock, **pos)
                    i = +1

        elif q == 0:
            for pos in positions:
                StockProduct.objects.filter(stock_id=instance.id).create(stock=stock, **pos)

        elif n > q:

            while i < q:
                for data in data_stockProduct:
                    if data.stock_id == instance.id:
                        pos = positions[i]
                        StockProduct.objects.filter(stock_id=instance.id, id = data.id ).update(stock=stock, **pos)
                        i = +1
                        n = n - 1
            else:
                for pos in positions[i+1:]:
                    StockProduct.objects.filter(stock_id=instance.id).create(stock=stock, **pos)

        elif n < q:

            for data in data_stockProduct:

                if data.stock_id == instance.id and i <= n:
                    print(n,i)
                    pos = positions[i]
                    StockProduct.objects.filter(stock_id=instance.id, id=data.id).update(stock=stock, **pos)
                    i = +1
                    n = n - 1
                elif data.stock_id == instance.id and i > n:

                    StockProduct.objects.filter(stock_id=instance.id, id=data.id).delete()

        return stock

