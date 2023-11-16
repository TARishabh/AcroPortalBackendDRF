# class RegistrationViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = StudentRegistrationSerializer
#     http_method_names = ['post']
    
#     def get_serializer_class(self):
#         if self.action =='post':
#             data = self.request.data
#             if data['role'] == "Student":
#                 return StudentRegistrationSerializer
#             elif data['role'] == "Head of Department":
#                 return HODRegistrationSerializer
#             elif data['role'] == "Teacher":
#                 return TeacherRegistrationSerializer
#             return self.serializer_class
#     def create(self, request, *args, **kwargs):
#         data = self.request.data
#         serializer_class = self.get_serializer_class()
#         print("Serializer Class:", serializer_class)  # Add this line for debugging
#         if serializer_class is None:
#             return Response({"message": "No valid serializer class found."}, status=status.HTTP_400_BAD_REQUEST)
#         serializer = serializer_class(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def list(self, request, *args, **kwargs):
#         return Response({"message":"Invalid Request Method"})