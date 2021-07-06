from api.permissions import IsOwner, remocaoImpossivel
from api.models import Usuario, Instituicao
from api.serializers import UsuarioSerializer, InstituicaoSerializer
from django.http import Http404
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken


class InstituicaoList(APIView):
  """
  Lista todas as Instituições ou cria uma
  """
  authentication_classes = [TokenAuthentication]

  def get(self, request, format=None):
    # SELECT * FROM instituicao WHERE owner = id_do_usuario
    instituicoes = Instituicao.objects.filter(owner=request.user)
    serializer = InstituicaoSerializer(instituicoes, many=True)
    return Response(serializer.data)

  def post(self, request, format=None):
    serializer = InstituicaoSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save(owner=request.user)
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InstituicaoDetail(APIView):
  """
  Lista, atualiza ou deleta uma instiuicao
  """
  authentication_classes = [TokenAuthentication]
  permission_classes = [remocaoImpossivel]

  def get_object(self, pk):
    try:
      obj = Instituicao.objects.get(pk=pk)
    except Instituicao.DoesNotExist as instituicao_nao_existe:
      raise Http404 from instituicao_nao_existe
    # verifica se o objeto instituição atende a todos os requisitos de permissions
    self.check_object_permissions(self.request, obj)

    return obj

  def get(self, request, pk, format=None):
    instituicao = self.get_object(pk)
    serializer = InstituicaoSerializer(instituicao)

    return Response(serializer.data)

  def put(self, request, pk, format=None):
    instituicao = self.get_object(pk)
    serializer = InstituicaoSerializer(instituicao, data=request.data)

    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, pk, format=None):
    instituicao = self.get_object(pk)
    instituicao.delete()

    return Response(status=status.HTTP_204_NO_CONTENT)


class UserList(generics.ListCreateAPIView):
  """
  Lista todas os Usuários ou cria um
  """

  authentication_classes = [TokenAuthentication]

  queryset = Usuario.objects.all()
  serializer_class = UsuarioSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
  """
  Lista, atualiza ou deleta um Usuário
  """
  queryset = Usuario.objects.all()
  serializer_class = UsuarioSerializer


class CustomTokenAuth(ObtainAuthToken):

  def post(self, request, *args, **kwargs):
    serializer = self.serializer_class(data=request.data,
                                       context={'request': request})
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    token, created = Token.objects.get_or_create(user=user)
    return Response({
        'token': token.key,
        'user_id': user.pk,
        'email': user.email,
        'username': user.username,
    })
