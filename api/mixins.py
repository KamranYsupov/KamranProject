from django.db.models import Model
from rest_framework import serializers


class BaseSerializerMixin(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    time_create = serializers.SerializerMethodField()

    class Meta:
        model = Model
        fields = '__all__'

    @staticmethod
    def get_author(instance):
        return str(instance.author)

    @staticmethod
    def get_likes(instance):
        return instance.likes.count()

    @staticmethod
    def get_time_create(instance):
        return instance.time_create.strftime("%d-%m-%Y %H:%M:%S")

