# app/utils/notifications.py

import firebase_admin
from firebase_admin import messaging
from app.utils.db import get_all_fcm_tokens  # A function to get all FCM tokens from DB

firebase_admin.initialize_app()

async def send_notification_to_all_users(prayer_name: str, dua_message: str):
    # Query the database to get all FCM tokens of subscribed users
    fcm_tokens = await get_all_fcm_tokens()

    # Prepare the message
    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title=f"Time for {prayer_name} Prayer",
            body=f"{dua_message}",
        ),
        tokens=fcm_tokens  # List of FCM tokens for all users
    )

    # Send the notification
    response = messaging.send_multicast(message)
    print(f"Sent {prayer_name} notification to {response.success_count} users.")
