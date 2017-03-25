from rest_framework import serializers

from login.models import(
    CustomUser,
    ProductAd,
    UserReview,
    Bids,
    AdCategories,
    Messages
)


class UserSerializer(serializers.ModelSerializer):

    photo = serializers.ImageField(required=False)
    email = serializers.EmailField(required=True)
    interests = serializers.CharField(required=False)
    push_notifications_key = serializers.CharField(required=False)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'address', 'phone_number',
                  'city', 'photo', 'interests', 'push_notifications_key',
                  'id')


class UserReviewSerializer(serializers.ModelSerializer):

    review = serializers.CharField(required=False)
    stars = serializers.IntegerField(required=True)
    reviewer_name = serializers.CharField(read_only=True)

    class Meta:
        model = UserReview
        fields = ('review', 'stars', 'reviewer', 'review_time',
                  'reviewer_name', 'reviewee', 'reviewee_name')


class UserInterestsSerializer(serializers.Serializer):

    interests = serializers.CharField(required=True)

    def update(self, instance, validated_data):
        instance.interests = validated_data.get('interests')
        instance.save()
        return instance


class UserPushIdSerializer(serializers.Serializer):

    push_key = serializers.CharField(required=True)

    def update(self, instance, validated_data):
        instance.push_key = validated_data.get('push_key')
        instance.save()
        return instance


class AdSerializer(serializers.ModelSerializer):

    bids = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True, required=False)
    currency = serializers.CharField(required=True)
    delivery_time = serializers.CharField(required=True)
    owner = serializers.CharField(read_only=True)
    owner_email = serializers.CharField(read_only=True)
    sold = serializers.BooleanField(required=False)
    sold_to = serializers.CharField(required=False)

    photo2 = serializers.ImageField(required=False)
    photo3 = serializers.ImageField(required=False)
    photo4 = serializers.ImageField(required=False)
    photo5 = serializers.ImageField(required=False)
    photo6 = serializers.ImageField(required=False)
    photo7 = serializers.ImageField(required=False)
    photo8 = serializers.ImageField(required=False)

    class Meta:
        model = ProductAd
        fields = ('id', 'created', 'title', 'description', 'category', 'price',
                  'photo1', 'photo2', 'photo3', 'photo4', 'photo5', 'photo6',
                  'photo7', 'photo8', 'currency', 'bids', 'delivery_time',
                  'owner', 'sold', 'sold_to', 'owner_email')


class AdBidSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bids
        fields = ('id', 'bid', 'ad', 'bidder')

    def create(self, validated_data):
        bid = Bids(
            ad=validated_data.get('ad'),
            bid=validated_data.get('bid'),
            bidder=validated_data.get('bidder')
        )
        bid.save()
        return bid

    def update(self, instance, validated_data):
        instance.bid = validated_data.get('bid', instance.bid)
        instance.save()
        return instance


class BidsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bids
        fields = ('ad', 'bid', 'bid_time', 'bidder', 'id', 'bidder_name')


class AdCategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdCategories


class MessagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Messages
