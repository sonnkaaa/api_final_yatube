from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешает изменение и удаление только автору объекта.
    Чтение доступно всем.
    """

    def has_permission(self, request, view):
        # Разрешаем все запросы на чтение
        if request.method in permissions.SAFE_METHODS:
            return True
        # Все остальные запросы требуют аутентификацию
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Разрешаем чтение любому пользователю
        if request.method in permissions.SAFE_METHODS:
            return True
        # Разрешаем изменения только автору объекта
        return obj.author == request.user
