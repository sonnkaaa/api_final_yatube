from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from posts.models import Post, Group, Comment, Follow
from .serializers import (
    PostSerializer, GroupSerializer,
    CommentSerializer, FollowSerializer
)


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        post = self.get_object()
        if post.author != self.request.user:
            raise PermissionDenied("Вы не можете редактировать чужой пост.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied("Вы не можете удалить чужой пост.")
        instance.delete()


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs.get("post_id")
        return Comment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        post_id = self.kwargs.get("post_id")
        post = Post.objects.get(id=post_id)
        serializer.save(author=self.request.user, post=post)

    def perform_update(self, serializer):
        comment = self.get_object()
        if comment.author != self.request.user:
            raise PermissionDenied("Вы не можете "
                                   "редактировать "
                                   "чужой комментарий.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied("Вы не можете "
                                   "удалить чужой комментарий.")
        instance.delete()


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        following = serializer.validated_data["following"]
        if self.request.user == following:
            raise ValidationError("Нельзя "
                                  "подписаться на самого себя.")
        if Follow.objects.filter(user=self.request.user,
                                 following=following).exists():
            raise ValidationError("Вы уже "
                                  "подписаны на этого пользователя.")
        serializer.save(user=self.request.user)


class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
