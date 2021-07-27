import os

from Validator.AbstractValidator import AbstractValidator


class IOSProjectInitializerValidator(AbstractValidator):

    def validate(self, result) -> bool:
        for path in result:
            if os.path.exists(path):
                return False
        return True


