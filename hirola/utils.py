"""

"""


class FormGroupItem:
    def __init__(self, value, give_id=None):
        self.value = value
        self.give_id = give_id


class Button(FormGroupItem):
    @staticmethod
    def sort():
        return "button"


class Text(FormGroupItem):
    @staticmethod
    def sort(self):
        return "text"


class Icon(FormGroupItem):
    @staticmethod
    def sort(self):
        return "icon"
