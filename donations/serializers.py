from rest_framework import serializers

from products.models import Product


class OrderProductSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        if not Product.objects.filter(id=value, deleted=False):
            raise serializers.ValidationError
        return value

    number = serializers.IntegerField(min_value=1)

    def validate_number(self, value):
        try:
            product = Product.objects.get(id=value, deleted=False)
        except Exception as e:
            raise serializers.ValidationError(str(e))
        if value > product.number_donated:
            raise serializers.ValidationError("You ordered more products than the ones available")
        return value

    def save(self, **kwargs):
        # add it to the order
        pass
