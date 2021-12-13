from rest_framework import serializers
from question.models import Option, Question
from django.db import transaction


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
