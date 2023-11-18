from django.shortcuts import render,get_object_or_404
from rest_framework import viewsets,status
from models_app.models import User,Attendance,Subjects
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import Http404
from models_app.serializers import UserRegistrationSerializer,UserLoginSerializer,AttendanceSerializer
import pdb
from acroportal.settings import FACULTY_SECRET_KEY
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework.decorators import permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
# Create your views here.

def responsegenerator(status, results=None, message=None, errors=None):
    response_data = {"statusCode": status}
    
    if results is not None:
        response_data["results"] = results

    if message is not None:
        response_data["message"] = message

    if errors is not None:
        response_data["errors"] = errors

    return response_data


from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
@api_view(['POST'])
def getuser(request):
    data = request.data
    email = data.get('email')

    try:
        if '@acropolis.in' not in email:
            api_response = responsegenerator(status=status.HTTP_400_BAD_REQUEST,message='Invalid Email')
            return Response(api_response)
        # Use get_object_or_404 to get the user or raise a 404 if not found
        user = get_object_or_404(User, email=email)

        # If you reach here, it means the user was found
        api_response = responsegenerator(status=status.HTTP_200_OK, results=True)
        return Response(api_response)

    except Http404:
        # Custom response for 404 error
        api_response = responsegenerator(status=status.HTTP_404_NOT_FOUND, results=False)
        return Response(api_response)

    except Exception as e:
        # Handle other exceptions if needed
        print(e)
        api_response = responsegenerator(status=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Something Went Wrong')
        return Response(api_response)
    

@api_view(['POST'])
def registeruser(request):
    data = request.data
    try:
        email = data.get('email')
        secret_key = data.get('secret_key')
        user_type = "Student" if any(char.isdigit() for char in email) else "Faculty"
        data['user_type'] = user_type
        if data['user_type'] == 'Faculty' and secret_key != FACULTY_SECRET_KEY:
            api_response = responsegenerator(status=status.HTTP_400_BAD_REQUEST,errors="Invalid User")
            return Response(api_response)
        enrollment_number = data.get('enrollment_number')
        serializer = UserRegistrationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            api_response = responsegenerator(status=status.HTTP_200_OK,results=serializer.data)
            return Response(api_response)
        api_response = responsegenerator(status=status.HTTP_400_BAD_REQUEST,errors=serializer.errors)
        return Response(api_response)
    except Exception as e:
        print(e)
        api_response = responsegenerator(status=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Something Went Wrong')
        return Response(api_response)

@api_view(['POST'])
def login(request):
    data = request.data
    try:
        email = data.get('email')
        password = data.get('password')
        
        user = authenticate(email=email,password=password)
        if user is None:
            response = responsegenerator(status=status.HTTP_400_BAD_REQUEST,message="Unable to login, Please check email or password.")
            return Response(response)
        tokens = get_tokens_for_user(user)
        serializer = UserLoginSerializer(user)
        api_response = responsegenerator(status=status.HTTP_200_OK,message='Logged In',)
        api_response['token'] = tokens
        return Response(api_response)
    except Exception as e:
        print(e)
        api_response = responsegenerator(status=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Something Went Wrong')
        return Response(api_response)
    

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def mark_attendance(request):
    data = request.data
    try:
        if str(request.user) == 'AnonymousUser':
            api_response = responsegenerator(status=status.HTTP_401_UNAUTHORIZED,message='Permission Denied')
            return Response(api_response)
        user_type_fetch = User.objects.get(id=request.user.id)
        if user_type_fetch.user_type != 'Faculty':
            api_response = responsegenerator(status=status.HTTP_401_UNAUTHORIZED,message='Permission Denied')
            return Response(api_response)
        student_ids = data.get('student_id', [])
        if len(student_ids) < 1:
            api_response = responsegenerator(status=status.HTTP_400_BAD_REQUEST,message='No Students Selected')
            return Response(api_response)
        faculty_id = request.user.id
        subject_id = int(data.get('subject_id'))
        date = data.get('date')
        time = data.get('time')
        section = data.get('section')
        year = data.get('year')
        for student in student_ids:
            attendance_data = {
                'faculty_id': faculty_id,
                'student_id': student,
                'date': date,
                'time': time,
                'subject_id': subject_id,
                'section':section,
                'year':year,
            }
            serializer = AttendanceSerializer(data=attendance_data)
            if serializer.is_valid():
                serializer.save()
            else:
                # Handle validation errors if needed
                api_response = responsegenerator(status=status.HTTP_400_BAD_REQUEST, errors=serializer.errors)
                return Response(api_response)
        api_response = responsegenerator(status=status.HTTP_200_OK, message='Attendance marked successfully')
        return Response(api_response)

    except Exception as e:
        print(e)
        api_response = responsegenerator(status=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Something Went Wrong')
        return Response(api_response)

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST','DELETE'])
def view_attendance(request):
    data = request.data
    try:
        if str(request.user) == 'AnonymousUser':
            api_response = responsegenerator(status=status.HTTP_401_UNAUTHORIZED,message='Permission Denied')
            return Response(api_response)
        
        subject_id = data.get('subject_id')
        date = data.get('date')
        user_type_fetch = User.objects.get(id=request.user.id)
        if user_type_fetch.user_type == 'Faculty':
            if request.method == 'DELETE':
                attendance_id = data.get('attendance_id')
                attendance = Attendance.objects.get(id=int(attendance_id))
                attendance.is_deleted = True
                attendance.save()
                api_response = responsegenerator(status=status.HTTP_200_OK,message='Deleted Succesfully')
                return Response(api_response)
            queryset = Attendance.objects.filter(is_deleted=False)
            serializer = AttendanceSerializer(queryset,many=True)
            api_response = responsegenerator(status=status.HTTP_200_OK,results=serializer.data)
            return Response(api_response)
        queryset = Attendance.objects.filter(student_id=request.user.id,is_deleted=False)
        if subject_id:
            queryset = Attendance.objects.filter(student_id=request.user.id,subject_id=subject_id,is_deleted=False)
        if date:
            queryset = Attendance.objects.filter(student_id=request.user.id,date=date,is_deleted=False)
        serializer = AttendanceSerializer(queryset,many=True)
        api_response = responsegenerator(status=status.HTTP_200_OK,results=serializer.data)
        return Response(api_response)
    except Exception as e:
        print(e)
        api_response = responsegenerator(status=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Something Went Wrong')
        return Response(api_response)