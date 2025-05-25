from rest_framework import serializers
from .models import Match, MatchParticipant
from users.serializers import UserProfileSerializer

class MatchSerializer(serializers.ModelSerializer):
    created_by = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = Match
        fields = ('id', 'title', 'description', 'date', 'time', 'location', 
                 'latitude', 'longitude', 'max_players', 'current_players', 
                 'status', 'created_by', 'created_at', 'updated_at')
        read_only_fields = ('created_by', 'created_at', 'updated_at', 'current_players')

class MatchDetailSerializer(MatchSerializer):
    participants = serializers.SerializerMethodField()
    
    class Meta(MatchSerializer.Meta):
        fields = MatchSerializer.Meta.fields + ('participants',)
    
    def get_participants(self, obj):
        participants = MatchParticipant.objects.filter(match=obj)
        return [{
            'user': UserProfileSerializer(participant.user).data,
            'team': participant.team,
            'joined_at': participant.joined_at
        } for participant in participants] 