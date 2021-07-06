from rest_framework import permissions


class remocaoImpossivel(permissions.BasePermission):
  message = 'Remover Instituição não é permitido'

  def has_permission(self, request, view):
    if request.method == 'DELETE':
      return False
    return True


class IsOwner(permissions.BasePermission):

  def has_object_permission(self, request, view, obj):
    if request.method in permissions.SAFE_METHODS:
      return True

    return obj.owner == request.user
