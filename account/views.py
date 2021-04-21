from django.shortcuts import render
from django.contrib import messages
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from oscar.core.compat import get_user_model
from rest_framework import generics,status
from django.urls import reverse
import jwt
from django.conf import settings

User = get_user_model()
# Create your views here.
class VerifyEmail(generics.GenericAPIView):
    def get(self,request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token,settings.SECRET_KEY,algorithms=["HS256"])
            user = User.objects.get(id=payload['user_id'])
            user.is_active = True
            user.is_verified = True
            user.save()
            messages.info(
                    request,'Account successfully activated')
            # return render(request,'templates/oscar/customer/login_registration.html')

            return Response({'email','Successfully activated'},status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error','Activation expired'},status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error','Activation token'},status=status.HTTP_400_BAD_REQUEST)