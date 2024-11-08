from rest_framework.serializers import Serializer, CharField


class BroadCastMessageSerializer(Serializer):
    message = CharField()
