# -*- coding: utf-8 -*-
"""Example usage of the Pushpad Python client."""

import pushpad

TOKEN = "5374d7dfeffa2eb49965624ba7596a09"
PROJECT_ID = 123

client = pushpad.Pushpad(auth_token=TOKEN, project_id=PROJECT_ID)

print(f"HMAC signature for 'user1': {client.signature_for('user1')}")

created = client.notifications.create(
    body="Hello world!",
    title="Website Name",
    target_url="https://example.com",
    uids=["user1", "user2", "user3"],
    tags=["segment1", "segment2"],
)
print(f"Notification accepted with id: {created.id}")

latest = client.notifications.all(page=1)
print(f"Latest notifications: {latest}")

subscriptions = client.subscriptions.all(per_page=5)
print(f"First page of subscriptions: {subscriptions}")

count = client.subscriptions.count(tags=["segment1 && !optout"])
print(f"Subscribers in the filtered segment: {count}")
