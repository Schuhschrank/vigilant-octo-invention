from engine.Var import Var


class Statement:

    def __init__(self, variable: Var, value):
        self.value = value
        self.variable: Var = variable

    def __bool__(self):
        return self.is_true()

    def __str__(self):
        return f"{self.variable} equals {self.value}"

    def is_true(self):
        return self.variable.value == self.value

    def make_true(self):
        self.variable.value = self.value
