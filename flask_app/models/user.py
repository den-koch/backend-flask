class User:
    def __init__(self, **kwargs):
        self.id = kwargs["user_id"]
        self.first_name = kwargs["first_name"]
        self.last_name = kwargs["last_name"]
        self.email = kwargs["email"]
