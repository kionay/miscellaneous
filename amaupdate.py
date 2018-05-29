import praw
import threading
from pushbullet import Pushbullet

app_name = "{app_name}"
app_id = "{app_id}"
app_secret = "{app_secret}"
user_agent_string = "required_custom (by {username})"
redirect_uri = "http://localhost:8080"
developer_username = "username"
developer_password = "password"

pushbullet_access_token = "{pushbullet access token}"

reddit_object = praw.Reddit(client_id=app_id,
                     client_secret=app_secret,
                     password=developer_password,
                     user_agent=user_agent_string,
                     username=developer_username)

last_ama_id = "??????"

def loop():
    reduser = reddit_object.redditor("{redditor username}")
    for post in reduser.submissions.new(limit=1):
        if "ama" in post.title.lower() and post.id != last_ama_id:
            push_bullet = Pushbullet(pushbullet_access_token)
            my_phone = push_bullet.get_device("{device identifier}")
            my_phone.push_note("AMA Posted","User {redditor username} is doing an AMA!")
            exit()
    threading.Timer(10.0,loop).start()

loop()
