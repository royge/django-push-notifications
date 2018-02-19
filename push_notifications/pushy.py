"""
Pushy
Documentation is available on their website:
https://pushy.me/docs/backend
"""

import json

try:
    from urllib.request import Request, urlopen
except ImportError:
    # Python 2 support
    import urllib2
    from urllib2 import Request, urlopen

from django.core.exceptions import ImproperlyConfigured
from . import NotificationError
from .settings import PUSH_NOTIFICATIONS_SETTINGS as SETTINGS


class PushyError(NotificationError):
    pass


def _pushy_send(data, content_type, key=None):
    key = key or SETTINGS.get("PUSHY_API_KEY")
    if not key:
        raise ImproperlyConfigured(
            ('You need to set PUSH_NOTIFICATIONS_SETTINGS["PUSHY_API_KEY"] '
             'to send messages through Pushy.')
        )

    headers = {
        "Content-Type": content_type,
        "Authorization": "key=%s" % (key),
        "Content-Length": str(len(data)),
    }

    request = Request(
        "%s/push?api_key=%s" % (SETTINGS["PUSHY_API_URL"], key),
        data,
        headers)

    return urlopen(request).read()


def _pushy_send_json(
    registration_ids,
    data,
    key=None
):
    """
    Sends a Pushy notification to one or more registration_ids.
    The registration_ids
    needs to be a list.
    This will send the notification as json data.
    """

    values = {"registration_ids": registration_ids}

    if data is not None:
        values["data"] = data

    data = json.dumps(
        values,
        separators=(",", ":"),
        sort_keys=True
    ).encode("utf-8")  # keys sorted for tests

    try:
        if key:
            result = _pushy_send(data, "application/json", key)
        else:
            result = _pushy_send(data, "application/json")
    except Exception, e:
        if isinstance(e, urllib2.HTTPError):
            raise PushyError(
                "Pushy API returned HTTP error " + str(e.code) + ": " + e.read()
            )
        raise PushyError(e)

    if "error" in result:
        raise PushyError(result)

    return result


def pushy_send_message(
    registration_id,
    data,
    key=None
):
    """
    Sends a Pushy notification to a single registration_id.

    This will send json data.

    If sending multiple notifications, it is more efficient to use
    pushy_send_bulk_message() with a list of registration_ids

    :param string registration_id: Device token.
    :param dict data: Payload up to 4kb.
    :return dict
    """

    args = data, key

    return _pushy_send_json([registration_id], *args)


def pushy_send_bulk_message(
    registration_ids,
    data,
    key=None
):
    """
    Sends a Pushy notification to one or more registration_ids.
    The registration_ids needs to be a list.
    This will send the notification as json data.

    :param list registration_id: List of device tokens.
    :param dict data: Payload up to 4kb.
    :return dict
    """

    args = data, key

    return _pushy_send_json(registration_ids, *args)
