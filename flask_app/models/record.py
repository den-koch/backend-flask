from datetime import datetime

class Record:
    def __init__(self, **kwargs):
        self.id = kwargs["record_id"]
        self.user_id = kwargs["user_id"]
        self.category_id = kwargs["category_id"]
        self.date_time = datetime.strptime(kwargs["date_time"], '%d/%m/%Y %H:%M')
        self.amount = kwargs["amount"]