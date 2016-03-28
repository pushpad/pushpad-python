# Pushpad: real push notifications for websites

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

`auth_token` can be found in the user account settings. 

`project_id` can be found in the project settings on Pushpad. A project is a list of subscriptions. 

## Collecting user subscriptions

### Custom API

Read the [docs](https://pushpad.xyz/docs#custom_api_docs).

If you need to generate the HMAC signature for the `uid` you can use this helper:

```python
project.signature_for(current_user_id)
```

### Simple API

Let users subscribe to your push notifications: 

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

## Sending notifications

After you have collected the user subscriptions you can send them push notifications:

```python
import pushpad

project = pushpad.Pushpad(auth_token='5374d7dfeffa2eb49965624ba7596a09', project_id=123)
notification = pushpad.Notification(
    project,
    body="Hello world!",
    title="Website Name", # optional, defaults to your project name
    target_url="http://example.com"  # optional, defaults to your project website
)

# deliver to user
notification.deliver_to(user_id)
# deliver to users list
notification.deliver_to((user1_id, user2_id, user3_id))
# deliver to everyone
notification.broadcast()
```

If no user with that id has subscribed to push notifications, that id is simply ignored.

The methods above return an dict(): `res['scheduled']` contains the number of notifications that will be sent. For example if you call `notification.deliver_to(user)` but the user has never subscribed to push notifications the result will be `{'scheduled': 0}`.

## License

The gem is available as open source under the terms of the [MIT License](http://opensource.org/licenses/MIT).
