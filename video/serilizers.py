from rest_framework import serializers

from .models import Category, Video


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class VideoSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)

    class Meta:
        model = Video
        fields = ['id', 'title', 'description', 'duration', 'categories']

    def create(self, validated_data):
        categories_data = validated_data.pop('categories')
        video = Video.objects.create(**validated_data)
        for category_data in categories_data:
            category, created = Category.objects.get_or_create(**category_data)
            video.categories.add(category)
        return video

    def update(self, instance, validated_data):
        categories_data = validated_data.pop('categories')
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.duration = validated_data.get('duration', instance.duration)
        instance.save()

        # Clear existing categories and add new ones
        instance.categories.clear()
        for category_data in categories_data:
            category, created = Category.objects.get_or_create(**category_data)
            instance.categories.add(category)
        return instance
