from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
  password =serializers.CharField(write_only=True)

  class Meta:
    model = User
    fields = ['username', 'email', 'password']
              
  def create(self, validated_data):
    # Create user
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )

           # Automatically create a token
        Token.objects.create(user=user)
        return user

class LoginSerializer(serializers.Serializer):
   username = serializers.CharField()
   password = serializers.CharField(write_only=True)

   def validate(self, data):
      user = authenticate(
         username=data['username'],
         password=data['password']
      )

      if not user:
         raise serializers.ValidationError("Invalid credentials")
      data['user'] = user
      return data