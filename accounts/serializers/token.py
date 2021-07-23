from rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers


class TokenSerializer(serializers.Serializer):
    """
      KnoxSerializer
      Serializer for Knox library authentication authentication.
    """
    token = serializers.CharField()
    user = UserDetailsSerializer()
