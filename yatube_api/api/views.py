from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from posts.models import Post, Group, Comment, Follow
from .serializers import (
    PostSerializer, GroupSerializer,
    CommentSerializer, FollowSerializer
)


class PostViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с постами."""
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Post.objects.all().select_related("author", "group")

    def list(self, request, *args, **kwargs):
        """Возвращает список постов."""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        """Создает пост и возвращает его с автором и группой."""
        post = serializer.save(author=self.request.user)
        return Response(PostSerializer(post).data,
                        status=status.HTTP_201_CREATED)

    def perform_update(self, serializer):
        post = self.get_object()
        if post.author != self.request.user:
            raise PermissionDenied("Вы не можете "
                                   "редактировать чужой пост.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied("Вы не можете "
                                   "удалить чужой пост.")
        instance.delete()


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для работы с группами."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def list(self, request, *args, **kwargs):
        """Возвращает список групп."""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с комментариями."""
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs.get("post_id")
        return Comment.objects.filter(
            post_id=post_id).select_related("author", "post")

    def list(self, request, *args, **kwargs):
        """Возвращает список комментариев к посту."""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        post_id = self.kwargs.get("post_id")
        post = get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user, post=post)

    def perform_update(self, serializer):
        comment = self.get_object()
        if comment.author != self.request.user:
            raise PermissionDenied("Вы не можете "
                                   "редактировать чужой комментарий.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied("Вы не можете "
                                   "удалить чужой комментарий.")
        instance.delete()


class FollowViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с подписками."""
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Follow.objects.filter(
            user=self.request.user).select_related("following")
        search_param = self.request.query_params.get("search", None)
        if search_param:
            queryset = queryset.filter(following__username__icontains=search_param)
        return queryset

    def list(self, request, *args, **kwargs):
        """Возвращает список подписок."""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        following = serializer.validated_data["following"]
        if self.request.user == following:
            raise ValidationError("Нельзя подписаться "
                                  "на самого себя.")
        if Follow.objects.filter(
                user=self.request.user, following=following).exists():
            raise ValidationError("Вы уже подписаны "
                                  "на этого пользователя.")
        serializer.save(user=self.request.user)
