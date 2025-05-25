from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Match, MatchParticipant
from .serializers import MatchSerializer, MatchDetailSerializer

class MatchListView(generics.ListCreateAPIView):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class MatchCreateView(generics.CreateAPIView):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class MatchDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Match.objects.all()
    serializer_class = MatchDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Match.objects.all()

class JoinMatchView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MatchSerializer

    def post(self, request, *args, **kwargs):
        match = get_object_or_404(Match, pk=kwargs['pk'])
        
        if match.current_players >= match.max_players:
            return Response(
                {"detail": "Match is already full."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if MatchParticipant.objects.filter(match=match, user=request.user).exists():
            return Response(
                {"detail": "You have already joined this match."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        MatchParticipant.objects.create(match=match, user=request.user)
        match.current_players += 1
        match.save()
        
        return Response(
            {"detail": "Successfully joined the match."},
            status=status.HTTP_200_OK
        ) 