import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class Instituicao(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  name = models.CharField(max_length=255)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  # O default possui o id do usuario aleatorio que o django cria. Esse id muda a cada vez que o banco e resetado
  owner = models.ForeignKey('api.Usuario', related_name='instituicoes',
                            on_delete=models.CASCADE, default='65dfb47d-fce6-4a78-b483-50bfc0e63cca')
