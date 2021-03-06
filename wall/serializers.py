from rest_framework import serializers

from django.contrib.auth.models import User

from wall.models import Post, Like, Notification


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('pk', 'first_name', 'last_name', 'email', 'username',
                  'password')

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            )
        user.set_password(validated_data['password'])
        user.save()
        return user


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class PostSerializer(serializers.ModelSerializer):
    user_data = UserSerializer(source='user', read_only=True)
    id = serializers.ReadOnlyField(source='pk')
    liked = serializers.SerializerMethodField('liked_by_user')
    replies = RecursiveField(many=True, read_only=True)

    def liked_by_user(self, obj):
        request = self.context.get('request', None)
        user = request.user
        if request and not user.is_anonymous():
            liked_by_user = obj.likes.filter(user=request.user).exists()
            return liked_by_user
        return False

    class Meta:
        model = Post
        fields = ('id', 'content', 'user', 'user_data',  'date', 'parent',
                  'like_count', 'liked', 'replies')


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('post', 'user')


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('pk', 'content', 'method', 'trigger', 'user')
