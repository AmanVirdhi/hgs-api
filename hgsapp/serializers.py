from rest_framework import serializers  
from .models import Grievance, Signup

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signup
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        # Create a new user instance and save it to the database
        user = Signup(**validated_data)  # The password will be hashed in the model's save method
        user.save()
        return user  

# class SignupSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Signup
#         fields = ['username', 'email', 'password']
#         extra_kwargs = {'password': {'write_only': True}}

#     def create(self, validated_data):
#         user = Signup(
#             username=validated_data['username'],
#             email=validated_data['email']
#         )
#         user.set_password(validated_data['password'])
#         user.save()
#         return user
class GrievanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grievance
        fields = '__all__'   