    
# @csrf_exempt
# class UserLogin(APIView):
#     # authentication_classes = [TokenAuthentication]
#     permission_classes = (permissions.AllowAny,)
#     authentication_classes = (SessionAuthentication,)
#     def post(self, request):
#         user = authenticate(username=request.data['email'], password=request.data['password'])
#         if user:
#             # token, created = Token.objects.get_or_create(user=user)
#             login(request, user)
#             # return Response({'token': token.key})
#             return Response('User Logged in', status=status.HTTP_200_OK)
#         else:
#             return Response({'error': 'Invalid credentials'}, status=401)
class UserLogin(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (SessionAuthentication,)
    def post(self, request):
        data = request.data
        print(data)
        
        # serializer = UserLoginSerializer(data=data)
        # print(serializer)
        # if serializer.is_valid(raise_exception=True):
        #     user = serializer.check_user(data)
        #     login(request, user)
        # print(request.data)
        user = authenticate(username=request.data['email'], password=request.data['password'])
        if user:
            login(request, user)
            return Response("logged in", status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=401)
        
