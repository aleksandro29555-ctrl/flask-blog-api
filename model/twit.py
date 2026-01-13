from .user import User

class Twit:
    def __init__(self, id: int, body: str, author: User):
        self.id = id
        self.body = body
        self.author = author
    def to_dict(self):
        return {"id": self.id, "body": self.body, "author": self.author.username}