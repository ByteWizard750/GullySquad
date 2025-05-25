from rest_framework import serializers
from .models import Squad, SquadMember
from users.serializers import UserProfileSerializer

class SquadMemberSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = SquadMember
        fields = ('user', 'role', 'joined_at')
        read_only_fields = ('joined_at',)

class SquadSerializer(serializers.ModelSerializer):
    created_by = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = Squad
        fields = ('id', 'name', 'description', 'created_by', 'created_at', 'updated_at')
        read_only_fields = ('created_by', 'created_at', 'updated_at')

class SquadDetailSerializer(SquadSerializer):
    members = serializers.SerializerMethodField()
    
    class Meta(SquadSerializer.Meta):
        fields = SquadSerializer.Meta.fields + ('members',)
    
    def get_members(self, obj):
        members = SquadMember.objects.filter(squad=obj)
        return SquadMemberSerializer(members, many=True).data 