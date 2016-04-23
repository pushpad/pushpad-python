# Pushpad - Web Push Notifications

Add native push notifications to your web app using [Pushpad](https://pushpad.xyz).

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

Pushpad offers two different ways to collect subscriptions. [Learn more](https://pushpad.xyz/docs#simple_vs_custom_api_docs)

### Custom API

Choose the Custom API if you want to use Javascript for a seamless integration. [Read the docs](https://pushpad.xyz/docs#custom_api_docs)

If you need to generate the HMAC signature for the `uid` you can use this helper:

```python
project.signature_for(current_user_id)
```

### Simple API

Add a link to let users subscribe to push notifications:

```python
'<a href="{url}">Subscribe anonymous to push notifications</a>'.format(
    url=project.path()
)

'<a href="{url}">Subscribe current user to push notifications</a>'.format(
    url=project.path_for(current_user_id)
)
```

`current_user_id` is an identifier (e.g. primary key in the database) of the user currently logged in on your website.

When a user clicks the link is sent to Pushpad, automatically asked to receive push notifications and redirected back to your website.

## Sending push notifications

```python
import pushpad

project = pushpad.Pushpad(auth_token='5374d7dfeffa2eb49965624ba7596a09', project_id=123)
notification = pushpad.Notification(
    project,
    body="Hello world!", # max 90 characters
    title="Website Name", # optional, defaults to your project name, max 30 characters
    target_url="http://example.com"  # optional, defaults to your project website
)

# deliver to a user
notification.deliver_to(user_id)

# deliver to a group of users
notification.deliver_to((user1_id, user2_id, user3_id))

# deliver to some users only if they have a given preference
# e.g. only the listed users who have also a interested in "events" will be reached
notification.deliver_to((user1_id, user2_id, user3_id), tags=['events'])

# deliver to segments
notification.broadcast(tags=['segment1', 'segment2'])

# deliver to everyone
notification.broadcast()
```

If no user with that id has subscribed to push notifications, that id is simply ignored.

The methods above return a dictionary: `'scheduled'` is the number of devices to which the notification will be sent.

## License

The library is available as open source under the terms of the [MIT License](http://opensource.org/licenses/MIT).
