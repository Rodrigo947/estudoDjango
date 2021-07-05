from api.permissions import IsOwner, remocaoImpossivel
from api.models import Usuario, Instituicao
from api.serializers import UsuarioSerializer, InstituicaoSerializer
from django.http import Http404
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response


class InstituicaoList(APIView):
  """
  Lista todas as Instituições ou cria uma
  """
  # authentication_classes = [TokenAuthentication]

  def get(self, request, format=None):
    instituicoes = Instituicao.objects.all()
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
  permission_classes = [IsOwner, remocaoImpossivel]

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
  queryset = Usuario.objects.all()
  serializer_class = UsuarioSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
  """
  Lista, atualiza ou deleta um Usuário
  """
  queryset = Usuario.objects.all()
  serializer_class = UsuarioSerializer
