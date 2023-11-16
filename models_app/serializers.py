from rest_framework import serializers
from models_app.models import User,Subjects,Attendance
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
import re

class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta(object):
        model = User
        fields = ['enrollment_number','first_name','last_name','section','year','email','user_type','login_otp','password','password2']
        
    def validate(self, attrs):
        if '@acropolis.in' not in attrs['email']:
            raise serializers.ValidationError({"error": "Invalid Email"})
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        if (attrs['user_type'] == 'Student') and ((attrs.get('enrollment_number') is None) or (attrs.get('section') is None) or (attrs.get('year') is None)):
            raise serializers.ValidationError({"error": "Invalid Format"})
        return attrs
    
    
    # def validate_email(self,value):
    #     if '@acropolis.in' not in value:
    #         raise serializers.ValidationError({"error": "Invalid Email"})
    #     return value
    
    # def validate_user_type(self,value):
        
    


    def create(self, validated_data):
        user = User.objects.create(
            enrollment_number=validated_data.get('enrollment_number', None),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            section=validated_data.get('section', None),
            year=validated_data.get('year', None),
            email=validated_data['email'],
            user_type=validated_data.get('user_type', 'Student'),
            login_otp=validated_data.get('login_otp', None),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserLoginSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ['id','email',]

class SubjectsSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Subjects
        fields = ['id','name','section','code']

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Attendance
        fields = ['id','student_id','faculty_id','subject_id','date','time','section','year']
        many =True




# class PasswordConfirmSerializer(serializers.Serializer):
#     password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
#     confirm_password = serializers.CharField(write_only=True, required=True)

#     def validate(self, attrs):
#         if attrs['password'] != attrs['confirm_password']:
#             raise serializers.ValidationError("Passwords fields don't match")
#         return attrs

# class BaseRegistrationSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
#     password_confirm = PasswordConfirmSerializer(write_only=True, required=True)

#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email', 'name', 'contact_number', 'department']

#     def create(self, validated_data):
#         password_confirm_data = validated_data.pop('password_confirm')
#         user = User.objects.create(**validated_data)
#         user.set_password(password_confirm_data['password'])
#         user.save()
#         return user

#     def validate_contact_number(self, value):
#         if value:
#             pattern = re.compile("^[6-9]\d{9}$")
#             if not pattern.match(value):
#                 raise serializers.ValidationError("Phone Number Not accepted")
#         return value

# class StudentRegistrationSerializer(BaseRegistrationSerializer):
#     class Meta(BaseRegistrationSerializer.Meta):
#         fields = BaseRegistrationSerializer.Meta.fields + ['role', 'enrollment_number', 'department', 'branch', 'year', 'semester']
        
#     def validate_user_type(self, value):
#         if value != "A":
#             raise serializers.ValidationError("Invalid User Type")
#         return value

# class HODRegistrationSerializer(BaseRegistrationSerializer):
#     class Meta(BaseRegistrationSerializer.Meta):
#         fields = BaseRegistrationSerializer.Meta.fields + ['user_type']

#     def validate_user_type(self, value):
#         if value != "C":
#             raise serializers.ValidationError("Invalid User Type")
#         return value

# class TeacherRegistrationSerializer(BaseRegistrationSerializer):
#     class Meta(BaseRegistrationSerializer.Meta):
#         fields = BaseRegistrationSerializer.Meta.fields + ['user_type']

#     def validate_user_type(self, value):
#         if value != "D":
#             raise serializers.ValidationError("Invalid User Type")
#         return value






















# '''OWN'''
# # class StudentRegistrationSerializer(serializers.ModelSerializer):
# #     email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
# #     password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
# #     confirm_password = serializers.CharField(write_only=True, required=True)
# #     class Meta(object):
# #         model = User
# #         fields = ['id','username','email','role','name','contact_number','enrollment_number','department','branch','year','semester']
        
# #     def validate(self, attrs):
# #         if attrs['password'] != attrs['confirm_password']:
# #             raise serializers.ValidationError("Passwords fields don't match")
# #         return attrs

# #     def validate_contact_number(self,value):
# #         if value:
# #             pattern = re.compile("^[6-9]\d{9}$")
# #             if not pattern.match(value):
# #                 raise serializers.ValidationError("Phone Number Not accepted")
# #         return value

# #     def create(self, validated_data):
# #         user = User.objects.create(
# #             username = validated_data['username'],
# #             email = validated_data['email'],
# #             role = validated_data['role'],
# #             name = validated_data['name'],
# #             contact_number = validated_data['contact_number'],
# #             enrollment_number = validated_data['enrollment_number'],
# #             department = validated_data['department'],
# #             branch = validated_data['branch'],
# #             year = validated_data['year'],
# #             semester = validated_data['semester'],
# #         )
# #         user.set_password(validated_data['password'])
# #         user.save()
# #         return user
    
# # class HODRegistrationSerializer(serializers.ModelSerializer):
# #     email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
# #     password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
# #     confirm_password = serializers.CharField(write_only=True, required=True)
# #     class Meta(object):
# #         model = User
# #         fields = ['id','username','email','user_type','role','name','contact_number','department',]
        
# #     def validate(self, attrs):
# #         if attrs['password'] != attrs['confirm_password']:
# #             raise serializers.ValidationError("Passwords fields don't match")
# #         return attrs
    
# #     def validate_contact_number(self,value):
# #         if value:
# #             pattern = re.compile("^[6-9]\d{9}$")
# #             if not pattern.match(value):
# #                 raise serializers.ValidationError("Phone Number Not accepted")
# #         return value
    
# #     def validate_user_type(self,value):
# #         if value != "C":
# #             raise serializers.ValidationError("Invalid User Type")
# #         return value

# #     # def validate_role(self,value):
# #     #     if value != "Head of Department":
# #     #         raise serializers.ValidationError("Invalid Role Selection")
# #     #     return value
    
# #     def create(self, validated_data):
# #         user = User.objects.create(
# #             username = validated_data['username'],
# #             email = validated_data['email'],
# #             role = validated_data['role'],
# #             user_type = validated_data['user_type'],
# #             name = validated_data['name'],
# #             contact_number = validated_data['contact_number'],
# #             department = validated_data['department'],
# #         )
# #         user.set_password(validated_data['password'])
# #         user.save()
# #         return user
    

# # class TeacherRegistrationSerializer(serializers.ModelSerializer):
# #     email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
# #     password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
# #     confirm_password = serializers.CharField(write_only=True, required=True)
# #     class Meta(object):
# #         model = User
# #         fields = ['id','username','email','user_type','role','name','contact_number','department',]
        
# #     def validate(self, attrs):
# #         if attrs['password'] != attrs['confirm_password']:
# #             raise serializers.ValidationError("Passwords fields don't match")
# #         return attrs
    
# #     def validate_contact_number(self,value):
# #         if value:
# #             pattern = re.compile("^[6-9]\d{9}$")
# #             if not pattern.match(value):
# #                 raise serializers.ValidationError("Phone Number Not accepted")
# #         return value
    
# #     def validate_user_type(self,value):
# #         if value != "D":
# #             raise serializers.ValidationError("Invalid User Type")
# #         return value

# #     # def validate_role(self,value):
# #     #     if value != "Teacher":
# #     #         raise serializers.ValidationError("Invalid Role Selection")
# #     #     return value
    
# #     def create(self, validated_data):
# #         user = User.objects.create(
# #             username = validated_data['username'],
# #             email = validated_data['email'],
# #             role = validated_data['role'],
# #             user_type = validated_data['user_type'],
# #             name = validated_data['name'],
# #             contact_number = validated_data['contact_number'],
# #             department = validated_data['department'],
# #         )
# #         user.set_password(validated_data['password'])
# #         user.save()
# #         return user
    
    
# # class UserLoginSerializer(serializers.ModelSerializer):
# #     class Meta(object):
# #         model = User
# #         fields = ['username']

