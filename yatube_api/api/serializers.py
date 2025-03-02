from rest_framework import serializers
from posts.models import Post, Group, Comment, Follow, User


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    group = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = Post
        fields = ["id", "text", "author", "pub_date", "group"]


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")
    post = serializers.ReadOnlyField(source="post.id")

    class Meta:
        model = Comment
        fields = ("id", "text", "author", "post", "created")
        extra_kwargs = {
            "author": {"read_only": True},
            "post": {"read_only": True}
        }


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(), slug_field="username"
    )

    class Meta:
        model = Follow
        fields = ("user", "following")

    def validate_following(self, value):
        user = self.context["request"].user
        if user == value:
            raise serializers.ValidationError("Нельзя подписаться на себя!")
        if Follow.objects.filter(user=user, following=value).exists():
            raise serializers.ValidationError("Вы уже подписаны на этого пользователя.")
        return value
