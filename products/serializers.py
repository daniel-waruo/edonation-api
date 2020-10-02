from rest_framework import serializers

from products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    """    
    def create(self, validated_data):
        images = validated_data.pop('images')
        product = Product.objects.create(**validated_data)
        for image in images:
            ProductImage.objects.create(
                product=product,
                url=image
            )
        return product
        """
