from rest_framework import serializers
from api.models import Instituicao


class InstituicaoSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        required=True, allow_blank=False, max_length=255)

    class Meta:
        model = Instituicao
        fields = ['id', 'name', 'created_at', 'updated_at']

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
