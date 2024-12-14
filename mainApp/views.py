from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
from rest_framework.response import Response

class UserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        users = CustomUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class NotificationViewSet(ModelViewSet):
    queryset = Notification.objects.all().order_by('-created_at')
    serializer_class = NotificationSerializer
    # permission_classes = [IsAuthenticated]

    def get(self, request, user_id, format=None):
        # Get notifications for a specific user
        notifications = Notification.objects.filter(user_id=user_id)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)

from django.shortcuts import render
from .models import Notification
from django.contrib.auth.decorators import login_required

@login_required
def user_notifications(request):
    user = request.user  # This will be the logged-in user
    notifications = Notification.objects.filter(user=user).order_by('-created_at')
    return render(request, 'notifications.html', {'notifications': notifications})

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

def send_notification(user_id, message):
    channel_layer = get_channel_layer()
    group_name = f"user_{user_id}"  # Match the group name in your consumer

    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": "send_notification",  # This should match the method in your consumer
            "notification": message,
        }
    )

from django.http import JsonResponse
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

def trigger_notification(request, user_id):
    """
    Trigger a notification for a specific user via WebSocket.
    """
    message = "You have a new notification!"
    channel_layer = get_channel_layer()

    # Send a notification to the WebSocket group for this user
    async_to_sync(channel_layer.group_send)(
        f"user_{user_id}",
        {
            "type": "send_notification",  # Must match the consumer's method name
            "notification": message,
        }
    )
    return JsonResponse({"status": "Notification sent!"})