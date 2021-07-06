from rest_framework import serializers
from api.models import Instituicao, Usuario


class InstituicaoSerializer(serializers.ModelSerializer):
  name = serializers.CharField(
      required=True, allow_blank=False, max_length=255)
  owner = serializers.ReadOnlyField(source='owner.username')

  class Meta:
    model = Instituicao
    fields = ['id', 'name', 'created_at', 'updated_at', 'owner']

  def create(self, validated_data):
    """
    Cria e retorna a nova Instituição
    """
    return Instituicao.objects.create(**validated_data)

  def update(self, instance, validated_data):
    """
    Atualiza e retorna uma Instituição
    """
    instance.name = validated_data.get('name', instance.name)

    instance.save()
    return instance


class UsuarioSerializer(serializers.ModelSerializer):
  instituicoes = serializers.PrimaryKeyRelatedField(
      many=True, queryset=Instituicao.objects.all())

  class Meta:
    model = Usuario
    fields = ['id', 'username', 'password', 'instituicoes']

  def create(self, validated_data):
    """
    Cria e retorna a um Usuario
    """
    user = super().create(validated_data)
    user.set_password(validated_data.get('password'))
    user.save()
    return user

  def update(self, instance, validated_data):
    """
    Atualiza e retorna um Usuario
    """
    instance.set_password(validated_data.get('password'))
    instance.save()

    return instance
