# Pushpad - Web Push Notifications Service
 
[Pushpad](https://pushpad.xyz) is a service for sending push notifications from your web app. It supports the **Push API** (Chrome and Firefox) and **APNs** (Safari).

Features:

- notifications are delivered even when the user is not on your website
- users don't need to install any app or plugin
- you can target specific users or send bulk notifications

Currently push notifications work on the following browsers:

- Chrome (Desktop and Android)
- Firefox (44+)
- Safari

## Installation

Use [pip](http://pip-installer.org/) or easy_install:

```bash
pip install pushpad-python
```

## Getting started

First you need to sign up to Pushpad and create a project there.

Then set your authentication credentials and project:

```python
import pushpad

project = pushpad.Pushpad(auth_token='5374d7dfeffa2eb49965624ba7596a09', project_id=123)
```

- `auth_token` can be found in the user account settings. 
- `project_id` can be found in the project settings.

## Collecting user subscriptions to push notifications

Pushpad offers two different products. [Learn more](https://pushpad.xyz/docs)

### Pushpad Pro

Choose Pushpad Pro if you want to use Javascript for a seamless integration. [Read the docs](https://pushpad.xyz/docs/pushpad_pro_getting_started)

If you need to generate the HMAC signature for the `uid` you can use this helper:

```python
project.signature_for(current_user_id)
```

### Pushpad Express

If you want to use Pushpad Express, add a link to your website to let users subscribe to push notifications: 

```python
'<a href="{url}">Push notifications</a>'.format(
    url=project.path()
)

# If the user is logged in on your website you should track its user id to target him in the future
'<a href="{url}">Push notifications</a>'.format(
    url=project.path_for(current_user_id)
)
```

`current_user_id` is an identifier (e.g. primary key in the database) of the user currently logged in on your website.

When a user clicks the link is sent to Pushpad, asked to receive push notifications and redirected back to your website.

## Sending push notifications

```python
import pushpad

project = pushpad.Pushpad(auth_token='5374d7dfeffa2eb49965624ba7596a09', project_id=123)
notification = pushpad.Notification(
    project,
    body="Hello world!", # max 120 characters
    title="Website Name", # optional, defaults to your project name, max 30 characters
    target_url="http://example.com",  # optional, defaults to your project website
    icon_url="http://example.com/assets/icon.png", # optional, defaults to the project icon
    ttl=604800 # optional, drop the notification after this number of seconds if a device is offline
)

# deliver to a user
notification.deliver_to(user_id)

# deliver to a group of users
notification.deliver_to((user1_id, user2_id, user3_id))

# deliver to some users only if they have a given preference
# e.g. only the listed users who have also a interested in "events" will be reached
notification.deliver_to((user1_id, user2_id, user3_id), tags=['events'])

# deliver to segments
# e.g. any subscriber that has the tag "segment1" OR "segment2"
notification.broadcast(tags=['segment1', 'segment2'])

# deliver to everyone
notification.broadcast()
```

If no user with that id has subscribed to push notifications, that id is simply ignored.

The methods above return a dictionary: 

- `'id'` is the id of the notification on Pushpad
- `'scheduled'` is the estimated reach of the notification (i.e. the number of devices to which the notification will be sent, which can be different from the number of users, since a user may receive notifications on multiple devices)
- `'uids'` (`deliver_to` only) are the user IDs that will be actually reached by the notification because they are subscribed to your notifications. For example if you send a notification to `['uid1', 'uid2', 'uid3']`, but only `'uid1'` is subscribed, you will get `['uid1']` in response. Note that if a user has unsubscribed after the last notification sent to him, he may still be reported for one time as subscribed (this is due to the way the W3C Push API works).

## License

The library is available as open source under the terms of the [MIT License](http://opensource.org/licenses/MIT).
