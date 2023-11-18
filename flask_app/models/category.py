class Category:
    def __init__(self, **kwargs):
        self.id = kwargs["category_id"]
        self.category_name = kwargs["category_name"]