from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Squad, SquadMember
from .serializers import SquadSerializer, SquadDetailSerializer
from django.db import models

class SquadListView(generics.ListCreateAPIView):
    serializer_class = SquadSerializer
    permission_classes = [permissions.AllowAny]  # Allow anyone to view squads

    def get_queryset(self):
        queryset = Squad.objects.all()
        search = self.request.query_params.get('search', '')
        sort = self.request.query_params.get('sort', 'newest')
        filter_by = self.request.query_params.get('filter', 'all')
        
        if search:
            queryset = queryset.filter(name__icontains=search)
            
        if filter_by == 'my_squads' and self.request.user.is_authenticated:
            queryset = queryset.filter(members=self.request.user)
        elif filter_by == 'available' and self.request.user.is_authenticated:
            queryset = queryset.exclude(members=self.request.user)
            
        if sort == 'oldest':
            queryset = queryset.order_by('created_at')
        elif sort == 'name':
            queryset = queryset.order_by('name')
        elif sort == 'members':
            queryset = queryset.annotate(member_count=models.Count('members')).order_by('-member_count')
        else:  # newest
            queryset = queryset.order_by('-created_at')
            
        return queryset

    def perform_create(self, serializer):
        squad = serializer.save(created_by=self.request.user)
        SquadMember.objects.create(
            squad=squad,
            user=self.request.user,
            role='captain'
        )

class SquadCreateView(generics.CreateAPIView):
    serializer_class = SquadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        squad = serializer.save(created_by=self.request.user)
        SquadMember.objects.create(
            squad=squad,
            user=self.request.user,
            role='captain'
        )

class SquadDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SquadDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Squad.objects.filter(members=self.request.user)

class JoinSquadView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SquadSerializer

    def post(self, request, *args, **kwargs):
        squad = get_object_or_404(Squad, pk=kwargs['pk'])
        
        if SquadMember.objects.filter(squad=squad, user=request.user).exists():
            return Response(
                {"detail": "You are already a member of this squad."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        SquadMember.objects.create(squad=squad, user=request.user)
        
        return Response(
            {"detail": "Successfully joined the squad."},
            status=status.HTTP_200_OK
        ) 