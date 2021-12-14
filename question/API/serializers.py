from rest_framework import serializers
from question.models import Option, Question, User
from django.db import transaction
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from django.core import exceptions
import django.contrib.auth.password_validation as validators


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ('text', 'correct')


class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True)

    class Meta:
        model = Question
        fields = ('id', 'text', 'options', 'lesson')

    def create(self, validated_data):
        options = validated_data.pop('options')
        with transaction.atomic():
            question = Question.objects.create(**validated_data)
            options_to_create = [
                Option(text=option.get('text'), correct=option.get('correct', False), question=question) for option in
                options]
            Option.objects.bulk_create(options_to_create)
        return question


class AuthTokenActiveSerializer(AuthTokenSerializer):
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                try:
                    user = User.objects.get(username=username)
                    pass_correct = user.check_password(password)
                    if pass_correct and not user.is_active:
                        msg = _('User is not active yet. Please contact with admin to activate it')
                        raise serializers.ValidationError(msg, code='authorization')
                except User.DoesNotExist:
                    pass
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(write_only=True, required=False)
    last_name = serializers.CharField(write_only=True, required=False)
    date_joined = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'full_name', 'first_name', 'last_name', 'email', 'date_joined')

    def validate(self, data):
        # here data has all the fields which have validated values
        # so we can create a User instance out of it
        user = User(**data)

        # get the password from the data
        password = data.get('password')

        errors = dict()
        try:
            # validate the password and catch the exception
            validators.validate_password(password=password, user=user)

        # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return super(UserSerializer, self).validate(data)
