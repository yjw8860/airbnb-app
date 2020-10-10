from rest_framework import serializers
from users.serializers import UserSerializer
from .models import Room


class ReadRoomSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)
    is_fav = serializers.SerializerMethodField()

    class Meta:
        model = Room
        exclude = ('modified',)
        read_only_fields = ('user', 'id', 'created', 'updated')

    def validate(self, data):
        if self.instance:
            check_in = data.get("check_in", self.instance.check_in)
            check_out = data.get("check_out", self.instance.check_out)
        else:
            check_in = data.get("check_in")
            check_out = data.get("check_out")
        if check_in==check_out:
            raise serializers.ValidationError("Not enough time")
        return data

    def get_is_fav(self, obj):
        request = self.context.get('request')
        if request:
            user = request.user
            if user.is_authenticated:
                return obj in user.favs.all()
        return False

    def create(self, validated_data):
        request = self.context.get('request')
        room = Room.objects.create(**validated_data, user=request.user)
        return room


class WriteRoomSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=140)
    address = serializers.CharField(max_length=140)
    price = serializers.IntegerField(help_text="USD per night")
    beds = serializers.IntegerField(default=1)
    lat = serializers.DecimalField(max_digits=10, decimal_places=6)
    lng = serializers.DecimalField(max_digits=10, decimal_places=6)
    bedrooms = serializers.IntegerField(default=1)
    bathrooms = serializers.IntegerField(default=1)
    check_in = serializers.TimeField(default="00:00:00")
    check_out = serializers.TimeField(default="00:00:00")
    instant_book = serializers.BooleanField(default=False)


