class User:
    def __init__(self, user_id: int, username: str):
        self.user_id = user_id
        self.username = username
    def to_dict(self):
        return {"id": self.user_id, "name": self.username} 