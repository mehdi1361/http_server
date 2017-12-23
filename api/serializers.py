from django.contrib.auth import get_user_model
from rest_framework import serializers
from objects.models import BenefitBox, UserChest
from django.contrib.auth.models import User


class UserChestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserChest
        fields = ('gem', 'coin')


class UserSerializer(serializers.ModelSerializer):
    # currency = UserBySerializer(many=True, read_only=True)
    currency = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'username',
            'password',
            'email',
            'currency',
            'currency'
        )
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def get_currency(self, request):
        try:
            currency = UserChest.objects.get(user=self.context['request'].user)
            serializer = UserChestSerializer(currency)
            return serializer.data

        except:
            return None

    def create(self, validated_data):
        if 'email' not in validated_data:
            raise serializers.ValidationError({"id": 400, "message": "email required"})

        user = get_user_model().objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super(UserSerializer, self).update(instance, validated_data)


class BenefitSerializer(serializers.ModelSerializer):
    class Meta:
        model = BenefitBox
        fields = (
            'name',
            'box',
            'quantity'
        )
