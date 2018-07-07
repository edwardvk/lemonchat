import requests
import json
database = 'lemonchat'

def publish(topic, *args, **kwargs):
    topic = '%s.%s' % (database, topic)
    return _publish(topic, *args, **kwargs)


def _publish(topic, *args, **kwargs):
    # open("/tmp/wamp.log","a").write(repr(topic))
    headers = {'Content-Type': 'application/json'}
    data = {"topic": topic, "args": args, "kwargs": kwargs}
    try:
        response = requests.post(
            "http://masterpenny.com:8080/push", data=json.dumps(data), headers=headers, timeout=5)
    except Exception as e:
        if kwargs.get('allowfail', True):
            return {'success': False, 'reason': repr(e)}
        else:
            raise
    r = response.json()
    r['success'] = True
    return r


if __name__ == "__main__":
    print(publish("hello", "argument1", "argument", text=1, kwarg2=2))
# curl -H "Content-Type: application/json" \
#     -d '{"topic": "com.example.add2", "args": [1, 2]}' \
#     http://127.0.0.1:8080/push
