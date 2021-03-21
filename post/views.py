from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Post, Vote
from .serializers import PostSeralizer, VoteSeralizer
from rest_framework.exceptions import ValidationError

class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSeralizer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(poster = self.request.user)


class VoteCreate(generics.CreateAPIView):
    serializer_class = VoteSeralizer
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        user = self.request.user
        post = Post.objects.get(pk=self.kwargs['pk'])
        return Vote.objects.filter(voter=user, post = post)

    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError('You have already voted for this post')
        serializer.save(voter = self.request.user, post=Post.objects.get(pk=self.kwargs['pk']))