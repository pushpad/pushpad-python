# Pushpad - Web Push Notifications

![Build Status](https://github.com/pushpad/pushpad-python/workflows/CI/badge.svg)
 
[Pushpad](https://pushpad.xyz) is a service for sending push notifications from websites and web apps. It uses the **Push API**, which is a standard supported by all major browsers (Chrome, Firefox, Opera, Edge, Safari).

The notifications are delivered in real time even when the users are not on your website and you can target specific users or send bulk notifications.

## Installation

Use [pip](http://pip-installer.org/):

```bash
pip install pushpad
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

You can subscribe the users to your notifications using the Javascript SDK, as described in the [getting started guide](https://pushpad.xyz/docs/pushpad_pro_getting_started).

If you need to generate the HMAC signature for the `uid` you can use this helper:

```python
project.signature_for(current_user_id)
```

## Sending push notifications

```python
import pushpad

project = pushpad.Pushpad(auth_token='5374d7dfeffa2eb49965624ba7596a09', project_id=123)

notification = pushpad.Notification(
    project,

    # required, the main content of the notification
    body="Hello world!",

    # optional, the title of the notification (defaults to your project name)
    title="Website Name",

    # optional, open this link on notification click (defaults to your project website)
    target_url="https://example.com",

    # optional, the icon of the notification (defaults to the project icon)
    icon_url="https://example.com/assets/icon.png",

    # optional, the small icon displayed in the status bar (defaults to the project badge)
    badge_url="https://example.com/assets/badge.png",

    # optional, drop the notification after this number of seconds if a device is offline
    ttl=604800,

    # optional, prevent Chrome on desktop from automatically closing the notification after a few seconds
    require_interaction=True,

    # optional, enable this option if you want a mute notification without any sound
    silent=False,

    # optional, enable this option only for time-sensitive alerts (e.g. incoming phone call)
    urgent=False,

    # optional, an image to display in the notification content
    # see https://pushpad.xyz/docs/sending_images
    image_url="https://example.com/assets/image.png",

    # optional, a string that is passed as an argument to action button callbacks
    custom_data="123",

    # optional, add some action buttons to the notification
    # see https://pushpad.xyz/docs/action_buttons
    actions=(
      {
        'title': "My Button 1",
        'target_url': "https://example.com/button-link", # optional
        'icon': "https://example.com/assets/button-icon.png", # optional
        'action': "myActionName" # optional
      },
    ),

    # optional, bookmark the notification in the Pushpad dashboard (e.g. to highlight manual notifications)
    starred=True,

    # optional, use this option only if you need to create scheduled notifications (max 5 days)
    # see https://pushpad.xyz/docs/schedule_notifications
    send_at=datetime.datetime(2016, 7, 25, 10, 9, 0, 0), # you need to import datetime and use UTC

    # optional, add the notification to custom categories for stats aggregation
    # see https://pushpad.xyz/docs/monitoring
    custom_metrics=('examples', 'another_metric') # up to 3 metrics per notification
)

# deliver to a user
notification.deliver_to(user_id)

# deliver to a group of users
notification.deliver_to((user1_id, user2_id, user3_id))

# deliver to some users only if they have a given preference
# e.g. only the listed users who have also a interested in "events" will be reached
notification.deliver_to((user1_id, user2_id, user3_id), tags=('events',))

# deliver to segments
# e.g. any subscriber that has the tag "segment1" OR "segment2"
notification.broadcast(tags=('segment1', 'segment2'))

# you can use boolean expressions
# they can include parentheses and the operators !, &&, || (from highest to lowest precedence)
# https://pushpad.xyz/docs/tags
notification.broadcast(tags='zip_code:28865 && !optout:local_events || friend_of:Organizer123')
notification.deliver_to((user1_id, user2_id), tags=('tag1 && tag2', 'tag3')) # equal to 'tag1 && tag2 || tag3'

# deliver to everyone
notification.broadcast()
```

You can set the default values for most fields in the project settings. See also [the docs](https://pushpad.xyz/docs/rest_api#notifications_api_docs) for more information about notification fields.

If you try to send a notification to a user ID, but that user is not subscribed, that ID is simply ignored.

The methods above return a dictionary: 

- `'id'` is the id of the notification on Pushpad
- `'scheduled'` is the estimated reach of the notification (i.e. the number of devices to which the notification will be sent, which can be different from the number of users, since a user may receive notifications on multiple devices)
- `'uids'` (`deliver_to` only) are the user IDs that will be actually reached by the notification because they are subscribed to your notifications. For example if you send a notification to `['uid1', 'uid2', 'uid3']`, but only `'uid1'` is subscribed, you will get `['uid1']` in response. Note that if a user has unsubscribed after the last notification sent to him, he may still be reported for one time as subscribed (this is due to the way the W3C Push API works).
- `'send_at'` is present only for scheduled notifications. The fields `'scheduled'` and `'uids'` are not available in this case.

## License

The library is available as open source under the terms of the [MIT License](http://opensource.org/licenses/MIT).
