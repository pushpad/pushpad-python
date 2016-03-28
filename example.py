# -*- coding: utf-8 -*-

import pushpad

user1 = 'user1'
user2 = 'user2'
user3 = 'user3'
users = [user1, user2, user3]

TOKEN='5374d7dfeffa2eb49965624ba7596a09'
PROJ_ID=123

project = pushpad.Pushpad(TOKEN, PROJ_ID)

print("HMAC signature for the uid: %s is: %s" %(user1, project.signature_for(user1)))
print("Subscribe anonymous to push notifications: %s" %(project.path()))
print("Subscribe current user: %s to push notifications: %s" %(user1, project.path_for(user1)))

notification = pushpad.Notification(
    project,
    body="Hello world!",
    title="Website Name",
    target_url="http://example.com"
)

print("Send notification to user: %s\nResult: %s" % (user1, notification.deliver_to(user1)))
print("Send notification to users: %s\nResult: %s" % (users, notification.deliver_to(users)))
print("Send broadcast notification\nResult: %s" % notification.broadcast())
