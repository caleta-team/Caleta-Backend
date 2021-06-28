import re

# Make a regular expression
# for validating an Email
regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

class Utils:
    TYPE_STRESS="stress"
    TYPE_ACTIVITY="activity"
    TYPE_RESPIRATION="respiration"

    def checkEmail(email):
        # pass the regular expression
        # and the string in search() method
        if (re.search(regex, email)):
            return True
        else:
            False

    @staticmethod
    def getTypeMD():
        return 0

    @staticmethod
    def getTypeAdmin():
        return 1

    @staticmethod
    def getTypeRelative():
        return 2

    @staticmethod
    def getTypeActivity():
        return 0
    @staticmethod
    def getTypeRespiration():
        return 1
    @staticmethod
    def getTypePain():
        return 2

