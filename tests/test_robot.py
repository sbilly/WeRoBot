import hashlib
import time
import six

from werobot import WeRoBot
from werobot.utils import generate_token


def test_signature_checker():
    token = generate_token()

    robot = WeRoBot(token)

    timestamp = str(int(time.time()))
    nonce = '12345678'

    sign = [token, timestamp, nonce]
    sign.sort()
    sign = ''.join(sign)
    if six.PY3:
        sign = sign.encode()
    sign = hashlib.sha1(sign).hexdigest()

    assert robot.check_signature(timestamp, nonce, sign)


def test_register_handlerss():
    robot = WeRoBot()

    for type in robot.message_types:
        assert hasattr(robot, type)

    @robot.text
    def text_handler():
        return "Hi"

    assert robot._handlers["text"] == [text_handler]

    @robot.image
    def image_handler():
        return 'nice pic'

    assert robot._handlers["image"] == [image_handler]
