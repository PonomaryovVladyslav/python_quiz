from django.db import transaction
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from question.API.permissions import IsRegisterOrGetListOfUsers
from question.API.serializers import QuestionSerializer, AuthTokenActiveSerializer, UserSerializer
from question.models import Question, User

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


class QuestionViewSet(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated, ]


class CustomAuthToken(ObtainAuthToken):
    serializer_class = AuthTokenActiveSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'username': user.username,
        })


class UserViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.filter(is_active=False)
    permission_classes = [IsRegisterOrGetListOfUsers, ]

    def perform_create(self, serializer):
        with transaction.atomic():
            password = serializer.validated_data.get('password')
            user = serializer.save()
            user.set_password(password)
            user.save()

    @action(methods=['post'], detail=True)
    def approve(self, request, pk=None):
        user = self.get_object()
        user.is_active = True
        user.save()
        return Response({'status': 'approved'})
