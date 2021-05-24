from django.core import exceptions
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import password_validation, get_user_model, authenticate

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    confirm_password = serializers.CharField(max_length=128, required=True, write_only=True)

    @staticmethod
    def validate_password(password):

        try:
            password_validation.validate_password(password)
        except exceptions.ValidationError as ve:
            raise serializers.ValidationError(detail=ve.messages)
        return password

    def validate(self, data):

        if data['password'] != data.pop('confirm_password'):
            raise serializers.ValidationError(detail={'confirm_password': 'Password must match confirm password'})
        return data

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }


class CustomAuthTokenSerializer(AuthTokenSerializer):

    username = None
    email = serializers.CharField(
        label=_("Email"),
        write_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
