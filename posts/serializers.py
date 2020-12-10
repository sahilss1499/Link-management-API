from rest_framework import serializers
from .models import Post,Vote

class PostSerializer(serializers.ModelSerializer):
    # for POST method via the API (user doesn't have to enter the poster and id)
    # and we pass in their default values
    poster = serializers.ReadOnlyField(source='poster.username')
    poster_id = serializers.ReadOnlyField(source='poster.id')
    #to see the votes of each post so we explicitly add a vote column
    votes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'url', 'poster', 'poster_id', 'created', 'votes']
    # name of the function has to be of type get_variable_name
    # this function gets us the count or thee value of votes
    def get_votes(self, post):
        return Vote.objects.filter(post=post).count()


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['id']
