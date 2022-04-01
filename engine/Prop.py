class Prop:

    def __init__(self, description="There is an object here."):
        self.description = description

    def __str__(self):
        return f"{self.description}"
