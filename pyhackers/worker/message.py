import logging
from pyhackers.model.message import Message
from pyhackers.model.user import User
from pyhackers.model.cassandra.hierachy import (
    User as CsUser, Post as CsPost, UserPost as CsUserPost, UserFollower as CsUserFollower,
    UserTimeLine
    )

from pyhackers.util.textractor import Parser

parser = Parser()

class MessageWorker():
    def __init__(self, user, message, context):
        self.user_id = user
        self.message_id = message
        self.context = context
        self.user = None
        self.message = None
        self.message_text = ''

    def resolve(self):
        self.user = User.query.get(self.user_id)
        self.message = Message.query.get(self.message_id)
        self.message_text = parser.parse(self.message.content)

        logging.warn("Process {}".format(self.message))

    def create_cassa(self):
        CsPost.create(id=self.message.id, text=self.message.content, user_id=self.user_id)
        post_id = self.message_id

        CsUserPost.create(user_id=self.user_id, post_id=post_id)
        user_followers_q = CsUserFollower.objects.filter(user_id=self.user_id).all()
        count = 0
        for follower in user_followers_q:
            UserTimeLine.create(user_id=follower.follower_id, post_id=post_id)
            count += 1

        logging.warn("Message [{}-{}] distributed to {} followers".format(self.message_id, post_id, count))

    def index(self):
        logging.warn("Index...{}".format(self.message))

    def url_rewrite(self):
        logging.warn("URL Rewrite..{}".format(self.message))

    def wait(self):
        logging.warn("Long running thing..")
        logging.warn("=" * 40)

    def run(self):
        self.resolve()
        self.create_cassa()
        self.index()
        self.url_rewrite()
        self.wait()


def foo(user, message, context):
    logging.warn("[WORKER][FOO] {} - {} - {}".format(user, message, context))
    MessageWorker(user, message, context).run()