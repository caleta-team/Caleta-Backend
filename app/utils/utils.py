import re

# Make a regular expression
# for validating an Email
regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

class Utils:
    TYPE_STRESS = "stress"
    TYPE_ACTIVITY = "act"
    TYPE_RESPIRATION = "resp"
    MQTT_TOPIC_BASE="caleta"
    MQTT_TOPIC_STRESS=MQTT_TOPIC_BASE+"/"+TYPE_STRESS
    MQTT_TOPIC_ACTIVITY = MQTT_TOPIC_BASE + "/" + TYPE_ACTIVITY
    MQTT_TOPIC_RESPIRATION = MQTT_TOPIC_BASE+"/"+TYPE_RESPIRATION
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
        return Utils.TYPE_ACTIVITY
    @staticmethod
    def getTypeRespiration():
        return Utils.TYPE_RESPIRATION
    @staticmethod
    def getTypePain():
        return Utils.TYPE_STRESS

