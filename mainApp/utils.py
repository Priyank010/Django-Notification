from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def trigger_notification(user_id, notification):
    print("trigger_notifisscation")
    channel_layer = get_channel_layer()
    print(channel_layer)
    group_name = f"user_{user_id}"
    print(group_name)
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'send_notification',
            'notification': notification,
        }
    )
