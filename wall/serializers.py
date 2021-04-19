import datetime
from rest_framework import serializers
from wall.models import Wall, Comment, Like, DisLike


class CommentSerializer(serializers.ModelSerializer):
    """
    serializer to handle turning our `Comment` object into
    something that can be JSONified and sent to the client
    """
    created_by = serializers.SerializerMethodField()
    modified_by = serializers.SerializerMethodField()

    def create(self, validated_data):
        """
        Function is used to create Comment object with serializer.
        :param validated_data: keep all Comment related data.
        :return: Comment object.
        """
        validated_data['created_by'] = self.context['request'].user
        validated_data['modified_by'] = self.context['request'].user
        comment = Comment.objects.create(**validated_data)
        return comment

    def update(self, instance, validated_data):
        """
        Function is used for the update comment information.
        :param instance: comment object instance
        :param validated_data: new info passed in request.
        :return: comment object.
        """
        instance.modified_on = datetime.datetime.now()
        instance.modified_by = self.context['request'].user
        return super(CommentSerializer, self).update(instance, validated_data)

    def get_modified_by(self, obj):
        return obj.created_by.username

    def get_created_by(self, obj):
        return obj.created_by.username

    class Meta:
        model = Comment
        fields = ('id', 'wall', 'comment_content', 'created_on',
                  'modified_on', 'created_by', 'modified_by')


class WallSerializer(serializers.ModelSerializer):
    """
    serializer to handle turning our `Wall` object into
    something that can be JSONified and sent to the client
    """
    created_by = serializers.SerializerMethodField()
    modified_by = serializers.SerializerMethodField()
    likes = serializers.ReadOnlyField(source='get_total_likes')
    dis_likes = serializers.ReadOnlyField(source='get_total_dis_likes')

    def create(self, validated_data):
        """
        Function is used to create Wall object with serializer.
        :param validated_data: keep all Wall related data.
        :return: Wall object.
        """
        validated_data['created_by'] = self.context['request'].user
        validated_data['modified_by'] = self.context['request'].user
        wall = Wall.objects.create(**validated_data)
        Like.objects.create(wall=wall)
        DisLike.objects.create(wall=wall)
        return wall

    def update(self, instance, validated_data):
        """
        Function is used for the update Wall information.
        :param instance: wall object instance
        :param validated_data: new info passed in request.
        :return: Wall object.
        """
        instance.modified_on = datetime.datetime.now()
        instance.modified_by = self.context['request'].user
        return super(WallSerializer, self).update(instance, validated_data)

    def get_modified_by(self, obj):
        if obj.modified_by:
            return obj.modified_by.username

    def get_created_by(self, obj):
        if obj.created_by:
            return obj.created_by.username

    comments = CommentSerializer(many=True, required=False)

    class Meta:
        model = Wall
        fields = ('id', 'title', 'content', 'likes', 'dis_likes', 'created_on', 'comments',
                  'modified_on', 'created_by', 'modified_by')
