from rest_framework import serializers
from social.models import Post, UserRating


class PostSerializer(serializers.ModelSerializer):
    rate = serializers.SerializerMethodField()
    number_of_rates = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'

    @staticmethod
    def get_rate(obj):
        return obj.rate

    @staticmethod
    def get_number_of_rates(obj):
        return obj.number_of_rates


class UserRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRating
        fields = '__all__'
