from django.shortcuts import render
from rest_framework import generics, permissions, mixins, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .models import Post, Vote
from .serializers import PostSerializer, VoteSerializer


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # specificing who can post method via this api
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(poster=self.request.user)

#view when we want to delete a post
class PostRetrieveDestroy(generics.RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # specificing who can post method via this api
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # the user who posted it only should have the power to delete a post
    def delete(self, request, *args, **kwargs):
        post = Post.objects.filter(pk=kwargs['pk'], poster=self.request.user)
        # checking that if thee current user is the one who posted this post
        if post.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError('This post was not posted by you. Hence cannot delete')



class VoteCreate(generics.CreateAPIView, mixins.DestroyModelMixin):
    serializer_class = VoteSerializer
    # specificing who can post method via this api
    permission_classes = [permissions.IsAuthenticated]
    # to get the info from the path and thus obtain the queryset for models
    def get_queryset(self):
        user = self.request.user
        post = Post.objects.get(pk=self.kwargs['pk'])
        return Vote.objects.filter(voter=user, post=post)

    def perform_create(self, serializer):
        # to check if this user has a vote for this post previousely or not
        if self.get_queryset().exists():
            raise ValidationError('You have already voted for this post ;)')

        serializer.save(voter=self.request.user, post=Post.objects.get(pk=self.kwargs['pk']))

    def delete(self, request, *args, **kwargs):
        # first check that is a vote exists
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError('You had never voted on this post')
