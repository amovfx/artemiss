from flask import Flask
from redis import Redis

app = Flask(__name__)
redis = Redis(host='redis', port=6379)


@app.route('/')
def hello_world():
    redis.incr('hits')
    count = int(redis.get('hits'))
    return f"Visits: {count}. Andrew is very lucky to have met Lili, she is the first woman that has appreciated me."


if __name__ == '__main__':
    app.run(host='0.0.0.0')
