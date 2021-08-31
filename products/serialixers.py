from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from products.models import Product, Category, Tag, Review


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = "id title description price category tags".split()

    def get_tags(self, product):
        # l = []
        # for i in product.tags.all():
        #   l.append(i.name)
        # return l
        return TagSerializer(product.tags.all(), many=True).data


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CategoryWithProductSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)
    count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = 'id name parent products count'.split()

    def get_count(self, category):
        return category.products.all().count()


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ReviewWithProductSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)
    count = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = "id name parent products count".split()

        def get_count(self, review):
            return review.products.all().count()

class ProductCreateSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=3, max_length=100)
    description = serializers.CharField(max_length=1000)
    price = serializers.FloatField()
    category_id = serializers.IntegerField()
    tags = serializers.ListField(child=serializers.IntegerField())

    def validate_title(self,title):
        products = Product.objects.filter(title=title)
        if products.count()>0:
            raise ValidationError("Такой товар уже есть")
        return title


    def validate_category_id(self, category_id):
        try:
            Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise ValidationError('Данной категории не существует!')
        return category_id


    def validate_tags(self, tags):
        tag = [tags[i] for i in range(len(tags)) if i == tags.index(tags[i])]
        count_tags = len(tag)
        print(tag)
        print(count_tags)
        tag_list = Tag.objects.filter(id__in=tag)
        print(tag_list.count())
        if count_tags != tag_list.count():
            raise ValidationError("Некоторых тегов не существует!")
        return tag