from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from accounts.models import User
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from accounts.serializers import UserSerializer, PasswordChangeSerializer
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.utils.decorators import method_decorator
from django.conf import settings
from accounts.utils import send_activation_email  , send_reset_password_email
from rest_framework.permissions import IsAuthenticated
# from rest_framework.permissions import IsAuthenticated


@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCSRFToken(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({'success': 'CSRF Cookie Set'})


@method_decorator(csrf_protect, name='dispatch')
class RegistrationView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        return render(request, 'accounts/registration.html')
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.create(serializer.validated_data)

            # Send Account Activation
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            activation_link = reverse(
                'activate', kwargs={'uid': uid, 'token': token})
            activation_url = f'{settings.SITE_DOMAIN}{activation_link}'

            send_activation_email(user.email, activation_url)

            return Response({'user': serializer.data, 'activation_url': activation_url}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_protect, name='dispatch')
class ActivateView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        uid = kwargs.get('uid')
        token = kwargs.get('token')

        if not uid or not token:
            return Response({'detail': "Missing Uid or Token"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)

            if default_token_generator.check_token(user, token):
                if user.is_active:
                    return Response({'detail': 'Account has already been Activated!'}, status=status.HTTP_200_OK)
                user.is_active = True
                user.save()

                return Response({'detail': 'Account has been activated Successfully!'}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Invalid Activation Link Provided'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'detail': 'Invalid Activation Link Provided'}, status=status.HTTP_400_BAD_REQUEST)
        
@method_decorator(csrf_protect, name='dispatch')
class ActivationConfirm(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        uid = request.data.get('uid')
        token = request.data.get('token')

        if not uid or not token:
            return Response(
                {'detail': "Missing Uid or Token"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)

            if default_token_generator.check_token(user, token):
                if user.is_active:
                    return Response(
                        {'detail': 'Account has already been Activated!'},
                        status=status.HTTP_201_CREATED
                    )
                user.is_active = True
                user.save()

                return Response({'detail': 'Account has been activated Successfully!'}, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'detail': 'Invalid Activation Link Provided'
                }, status=status.HTTP_400_BAD_REQUEST
                )
        except User.DoesNotExist:
            return Response({
                'detail': 'Invalid Activation Link Provided'
            }, status=status.HTTP_400_BAD_REQUEST)



@method_decorator(csrf_protect, name='dispatch')
class LoginView(APIView):
    permission_classes = [AllowAny]


    def get(self, request):
        return render(request, 'accounts/login.html')
    

    def post(self, request):

        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return Response(
                    {'detail': 'Logged in Successfully!'},
                    status=status.HTTP_201_CREATED
                )
        else:
            return Response({'detail': 'Email or Password incorrect'
                             }, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    def get(self, request):
        serializer = UserSerializer(request.user)
        data = serializer.data
        data['is_staff'] = request.user.is_staff
        return Response(data)

    def patch(self, request):
        serializer = UserSerializer(request.user,
                                    data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):

    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data)

        if serializer.is_valid():
            user = request.user
            old_password = request.data.get('old_password')
            new_password = request.data.get('confirm_password')
            user = request.user

            if not user.check_password(old_password):
                return Response(
                    {'detail': 'Invalid old password'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if new_password == old_password:
                return Response(
                    {'detail': 'Old and Newpasswords must be different'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user.set_password(new_password)
            user.save()
            return Response(
                {'detail': 'Password Changed'}
            )

@method_decorator(csrf_protect, name='dispatch')
class ResetPasswordEmailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')

        if not User.objects.filter(email=email).exists():
            return Response(
                {'detail': 'User with this email does not exist'}, status=status.HTTP_400_BAD_REQUEST
            )
        user = User.objects.get(email=email)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_link = reverse('reset_password', kwargs={'uid': uid, 'token': token}
        )
        
        reset_url = f'{settings.SITE_DOMAIN}{reset_link}'

        send_reset_password_email(user.email, reset_url)
        
        return Response(
            {'detail':'Password reset email sent successfully'}, status=status.HTTP_200_OK
        )
@method_decorator(csrf_protect, name='dispatch')
class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

@method_decorator(csrf_protect, name='dispatch')
class ResetPasswordConfirmView(APIView):
    permission_classes=[AllowAny]
    def post(self, request):
        uid = request.data.get('uid')
        token = request.data.get('token')
        if not uid or not token:
            return Response({'detail': 'Missing uid or token.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
            if default_token_generator.check_token(user, token):
                new_password = request.data.get('new_password')

                if not new_password:
                    return Response({'detail': 'New password is required.'}, status=status.HTTP_400_BAD_REQUEST)

                user.set_password(new_password)
                user.save()
                return Response({'detail': 'Password reset successful.'}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Invalid reset password link.'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'detail': 'Invalid reset password link.'}, status=status.HTTP_400_BAD_REQUEST)


class DeleteView(APIView):

    def delete(self, request):
        user = request.user
        user.delete()
        return Response(
            {'detail': 'Account Delete'},
            status=status.HTTP_204_NO_CONTENT
        )


class LogoutView(APIView):

    def post(self, request):
        logout(request)
        return Response(
            {'detail': 'LoggedOut Successfully! '},
            status=status.HTTP_200_OK
        )


class IsLoggedInView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        is_logged_in = user.is_authenticated
        return Response({'is_logged_in': is_logged_in})
        
        