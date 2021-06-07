import re

# Make a regular expression
# for validating an Email
regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

class Utils:
    def checkEmail(email):
        # pass the regular expression
        # and the string in search() method
        if (re.search(regex, email)):
            return True
        else:
            False

    @staticmethod
    def getTypeUser():
        return 0

    @staticmethod
    def getTypeAdmin():
        return 1

    @staticmethod
    def getTypeRoot():
        return 2

    @staticmethod
    def checkAuthToken(token):
        return False