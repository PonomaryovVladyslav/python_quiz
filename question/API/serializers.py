from rest_framework import serializers
from question.models import Option, Question, User
from django.db import transaction
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _


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
