# Pushpad - Web Push Notifications

[![pypi](https://img.shields.io/pypi/v/pushpad.svg)](https://pypi.python.org/pypi/pushpad)
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
from pushpad import Pushpad

client = Pushpad(auth_token='token', project_id=123)
```

- `auth_token` can be found in the user account settings. 
- `project_id` can be found in the project settings.

If your application uses multiple projects, instead of setting a `project_id` on client, you can pass the `project_id` as a param to methods:

```python
client.notifications.create(body="Your message", project_id=123)

client.notifications.all(page=1, project_id=123)

client.subscriptions.count(project_id=123)

# ...
```

## Collecting user subscriptions to push notifications

You can subscribe the users to your notifications using the Javascript SDK, as described in the [getting started guide](https://pushpad.xyz/docs/pushpad_pro_getting_started).

If you need to generate the HMAC signature for the `uid` you can use this helper:

```python
client.signature_for(current_user_id)
```

## Sending push notifications

Use `client.notifications.create()` (or the `send()` alias) to create and send a notification:

```python
# send a simple notification
client.notifications.send(body="Your message")

# a more complex notification with all the optional fields
client.notifications.create(
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

    # optional, an image to display in the notification content
    # see https://pushpad.xyz/docs/sending_images
    image_url="https://example.com/assets/image.png",

    # optional, drop the notification after this number of seconds if a device is offline
    ttl=604800,

    # optional, prevent Chrome on desktop from automatically closing the notification after a few seconds
    require_interaction=True,

    # optional, enable this option if you want a mute notification without any sound
    silent=False,

    # optional, enable this option only for time-sensitive alerts (e.g. incoming phone call)
    urgent=False,

    # optional, a string that is passed as an argument to action button callbacks
    custom_data="123",

    # optional, add some action buttons to the notification
    # see https://pushpad.xyz/docs/action_buttons
    actions=[
        {
            "title": "My Button 1",
            "target_url": "https://example.com/button-link", # optional
            "icon": "https://example.com/assets/button-icon.png", # optional
            "action": "myActionName" # optional
        }
    ],

    # optional, bookmark the notification in the Pushpad dashboard (e.g. to highlight manual notifications)
    starred=True,

    # optional, use this option only if you need to create scheduled notifications (max 5 days)
    # see https://pushpad.xyz/docs/schedule_notifications
    send_at="2025-11-20T10:09:00Z",

    # optional, add the notification to custom categories for stats aggregation
    # see https://pushpad.xyz/docs/monitoring
    custom_metrics=["examples", "another_metric"], # up to 3 metrics per notification
)

# deliver to a group of users
client.notifications.create(body="Hello world!", uids=["user1", "user2"])

# deliver to some users only if they have a given preference
# e.g. only "users" who have a interested in "events" will be reached
client.notifications.create(body="Hello world!", uids=["user1", "user2"], tags=["events"])

# deliver to segments
# e.g. any subscriber that has the tag "segment1" OR "segment2"
client.notifications.create(body="Hello world!", tags=["segment1", "segment2"])

# you can use boolean expressions 
# they can include parentheses and the operators !, &&, || (from highest to lowest precedence)
# https://pushpad.xyz/docs/tags
client.notifications.create(body="Hello world!", tags=["zip_code:28865 && !optout:local_events || friend_of:Organizer123"])
client.notifications.create(body="Hello world!", tags=["tag1 && tag2", "tag3"]) # equal to 'tag1 && tag2 || tag3'

# deliver to everyone
client.notifications.create(body="Hello world!")
```

You can set the default values for most fields in the project settings. See also [the docs](https://pushpad.xyz/docs/rest_api#notifications_api_docs) for more information about notification fields.

If you try to send a notification to a user ID, but that user is not subscribed, that ID is simply ignored.

These fields are returned by the API:

```python
result = client.notifications.create(**payload)

# Notification ID
print(result.id) # => 1000

# Estimated number of devices that will receive the notification
# Not available for notifications that use send_at
print(result.scheduled) # => 5

# Available only if you specify some user IDs (uids) in the request:
# it indicates which of those users are subscribed to notifications.
# Not available for notifications that use send_at
print(result.uids) # => ["user1", "user2"]

# The time when the notification will be sent.
# Available for notifications that use send_at
print(result.send_at) # => "2025-10-30T10:09:00.000Z"
```

## Getting push notification data

You can retrieve data for past notifications:

```python
notification = client.notifications.get(42)

# get basic attributes
notification.id # => 42
notification.title # => 'Foo Bar'
notification.body # => 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'
notification.target_url # => 'https://example.com'
notification.ttl # => 604800
notification.require_interaction # => False
notification.silent # => False
notification.urgent # => False
notification.icon_url # => 'https://example.com/assets/icon.png'
notification.badge_url # => 'https://example.com/assets/badge.png'
notification.created_at # => '2025-07-06T10:09:14.000Z'

# get statistics
notification.scheduled_count # => 1
notification.successfully_sent_count # => 4
notification.opened_count # => 2
```

Or for multiple notifications of a project at once:

```python
notifications = client.notifications.all(page=1)

# same attributes as for single notification in example above
notifications[0].id # => 42
notifications[0].title # => 'Foo Bar'
```

The REST API paginates the result set. You can pass a `page` parameter to get the full list in multiple requests.

```python
notifications = client.notifications.all(page=2)
```

## Scheduled notifications

You can create scheduled notifications that will be sent in the future:

```python
import datetime

scheduled = client.notifications.create(
  body="This notification will be sent after 60 seconds",
  send_at=(datetime.datetime.utcnow() + datetime.timedelta(seconds=60)).isoformat()
)
```

You can also cancel a scheduled notification:

```python
client.notifications.cancel(scheduled.id)
```

## Getting subscription count

You can retrieve the number of subscriptions for a given project, optionally filtered by `tags` or `uids`:

```python
client.subscriptions.count() # => 100
client.subscriptions.count(uids=["user1"]) # => 2
client.subscriptions.count(tags=["sports"]) # => 10
client.subscriptions.count(tags=["sports && travel"]) # => 5
client.subscriptions.count(uids=["user1"], tags=["sports && travel"]) # => 1
```

## Getting push subscription data

You can retrieve the subscriptions for a given project, optionally filtered by `tags` or `uids`:

```python
client.subscriptions.all()
client.subscriptions.all(uids=["user1"])
client.subscriptions.all(tags=["sports"])
client.subscriptions.all(tags=["sports && travel"])
client.subscriptions.all(uids=["user1"], tags=["sports && travel"])
```

The REST API paginates the result set. You can pass `page` and `per_page` parameters to get the full list in multiple requests.

```python
subscriptions = client.subscriptions.all(page=2)
```

You can also retrieve the data of a specific subscription if you already know its id:

```python
client.subscriptions.get(123)
```

## Updating push subscription data

Usually you add data, like user IDs and tags, to the push subscriptions using the [JavaScript SDK](https://pushpad.xyz/docs/javascript_sdk_reference) in the frontend.

However you can also update the subscription data from your server:

```python
subscriptions = client.subscriptions.all(uids=["user1"])

for subscription in subscriptions:
  # update the user ID associated to the push subscription
  client.subscriptions.update(subscription.id, uid="myuser1")
  
  # update the tags associated to the push subscription
  tags = list(subscription.tags or [])
  tags.append("another_tag")
  client.subscriptions.update(subscription.id, tags=tags)
```

## Importing push subscriptions

If you need to [import](https://pushpad.xyz/docs/import) some existing push subscriptions (from another service to Pushpad, or from your backups) or if you simply need to create some test data, you can use this method:

```python
attributes = {
  "endpoint": "https://example.com/push/f7Q1Eyf7EyfAb1", 
  "p256dh": "BCQVDTlYWdl05lal3lG5SKr3VxTrEWpZErbkxWrzknHrIKFwihDoZpc_2sH6Sh08h-CacUYI-H8gW4jH-uMYZQ4=",
  "auth": "cdKMlhgVeSPzCXZ3V7FtgQ==",
  "uid": "exampleUid", 
  "tags": ["exampleTag1", "exampleTag2"]
}

subscription = client.subscriptions.create(**attributes)
```

Please note that this is not the standard way to collect subscriptions on Pushpad: usually you subscribe the users to the notifications using the [JavaScript SDK](https://pushpad.xyz/docs/javascript_sdk_reference) in the frontend.

## Deleting push subscriptions

Usually you unsubscribe a user from push notifications using the [JavaScript SDK](https://pushpad.xyz/docs/javascript_sdk_reference) in the frontend (recommended).

However you can also delete the subscriptions using this library. Be careful, the subscriptions are permanently deleted!

```python
client.subscriptions.delete(id)
```

## Managing projects

Projects are usually created manually from the Pushpad dashboard. However you can also create projects from code if you need advanced automation or if you manage [many different domains](https://pushpad.xyz/docs/multiple_domains).

```python
attributes = {
  # required attributes
  "sender_id": 123,
  "name": "My project",
  "website": "https://example.com",
  
  # optional configurations
  "icon_url": "https://example.com/icon.png",
  "badge_url": "https://example.com/badge.png",
  "notifications_ttl": 604800,
  "notifications_require_interaction": False,
  "notifications_silent": False
}

project = client.projects.create(**attributes)
```

You can also find, update and delete projects:

```python
projects = client.projects.all()
for p in projects:
  print(f"Project {p.id}: {p.name}")

existing_project = client.projects.get(123)

client.projects.update(existing_project.id, name="The New Project Name")

client.projects.delete(existing_project.id)
```

## Managing senders

Senders are usually created manually from the Pushpad dashboard. However you can also create senders from code.

```python
attributes = {
  # required attributes
  "name": "My sender",
  
  # optional configurations
  # do not include these fields if you want to generate them automatically
  "vapid_private_key": "-----BEGIN EC PRIVATE KEY----- ...",
  "vapid_public_key": "-----BEGIN PUBLIC KEY----- ..."
}

sender = client.senders.create(**attributes)
```

You can also find, update and delete senders:

```python
senders = client.senders.all()
for s in senders:
  print(f"Sender {s.id}: {s.name}")

existing_sender = client.senders.get(987)

client.senders.update(existing_sender.id, name="The New Sender Name")

client.senders.delete(existing_sender.id)
```

## Error handling

API requests can raise errors, described by a `PushpadAPIError` that exposes the HTTP status code, reason, and response body. Network issues and other errors raise a `PushpadClientError`.

```python
from pushpad import Pushpad, PushpadAPIError, PushpadClientError

client = Pushpad(auth_token="token", project_id=123)

try:
  client.notifications.create(body="Hello")
except PushpadAPIError as error:  # HTTP error from the API
  print(error.status_code, error.reason, error.response_body)
except PushpadClientError as error:  # network error or other errors
  print(error)
```

## Type hints

This library includes types for request parameters and responses to improve the developer experience. We recommend enabling Pylance, Pyright, or Python IntelliSense in your code editor for the best experience.

```python
from pushpad import Pushpad

client = Pushpad(auth_token="token", project_id=123)

# parameters, like body, have a specific type
# you can immediately see if a parameter is wrong
result = client.notifications.create(body="Hello")

# the result is a structured object
# it is always clear what attributes can be accessed on the resource
print(result.id)
```

## Documentation

- Pushpad REST API reference: https://pushpad.xyz/docs/rest_api
- Getting started guide (for collecting subscriptions): https://pushpad.xyz/docs/pushpad_pro_getting_started
- JavaScript SDK reference (frontend): https://pushpad.xyz/docs/javascript_sdk_reference

## License

The library is available as open source under the terms of the [MIT License](http://opensource.org/licenses/MIT).
