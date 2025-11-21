# Upgrading to version 2.x

This version is a major rewrite of the library and adds support for the full REST API, including Notifications, Subscriptions, Projects and Senders.

This version has some breaking changes:

- `notification.deliver_to` and `notification.broadcast` were removed. Instead you should use `client.notifications.create()` (or the `send()` alias).
- When you call `client.notifications.create()`, you cannot pass a `project` object as an argument, like in the previous version, but you can pass an optional `project_id` argument (however in most cases you don't need to set the `project_id` argument, because you already set it on the client instance).
- When you call `client.notifications.create()`, for the fields that expect multiple items (like `actions`, `custom_metrics`, `uids` and `tags`), you should use a `list` (e.g. use `tags=["tag1", "tag2"]` instead of `tags=("tag1", "tag2")`).
- When you call `client.notifications.create()` with the `send_at` argument, you should pass a ISO 8601 string (and not a `datetime` object like in the previous version). For example, you can use `(datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=60)).isoformat()` to send a notification after 60 seconds.
- When you call `client.notifications.create()`, an object is returned as a result (previous version returned a `dict`). The fields returned remain the same (e.g. use `result.id` instead of `result["id"]`).
