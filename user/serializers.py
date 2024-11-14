from rest_framework.serializers import CharField, Serializer


class BroadCastMessageSerializer(Serializer):
    message = CharField()
