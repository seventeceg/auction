from django.http import Http404

from login.models import(
    CustomUser,
    ProductAd,
    Bids,
)

from login.serializers import AdSerializer


def get_user_by_username(api_view, request, username):
    try:
        obj = CustomUser.objects.get(username=username)
        api_view.check_object_permissions(request, obj)
        return obj
    except CustomUser.DoesNotExist:
        raise Http404


def get_ad_by_primary_key(api_view, request, pk):
    try:
        obj = ProductAd.objects.get(pk=pk)
        # api_view.check_object_permissions(request, obj)
        return obj
    except ProductAd.DoesNotExist:
        raise Http404


def does_user_exist(username):
    """
    Return bool representing if the requested user is already registered.
    """
    try:
        CustomUser.objects.get(username=username)
        return True
    except CustomUser.DoesNotExist:
        return False


def _send_push_notification(data, reg_ids):
    from gcm import GCM
    gcm = GCM('AIzaSyAKqZ5WrMh3ZinQLkVH8ftdE2qi1DRCCZg')
    gcm.json_request(registration_ids=reg_ids, data=data)


def _really_delete(pk):
    """Delete an ad by primary key and send a push notification."""
    notify_data = {}
    try:
        ad = ProductAd.objects.get(pk=pk)
        notify_data.update({'ad_id': ad.id})
        notify_data.update({'ad_owner': str(ad.owner)})
        serializer = AdSerializer(ad)
        if not did_someone_bid(pk):
            ad.delete()
            notify_data.update({'type': 'ad_expired'})
            send_push_by_subscribed_categories(notify_data,
                                               serializer.data.get('category'))
        else:
            # Sell to the highest bidder
            highest_bid = get_highest_bid(pk)
            notify_data.update({'type': 'sold_to_highest_bidder'})
            notify_data.update({'price': str(highest_bid.bid)})
            notify_data.update({'sold_to': highest_bid.bidder_name()})
            ad.sold = True
            ad.sold_to = highest_bid.bidder_name()
            ad.save()
            send_push_by_subscribed_categories(notify_data,
                                               serializer.data.get('category'))
    except ProductAd.DoesNotExist:
        # Just do nothing if the ad was already deleted.
        pass


def delete_ad(pk, delay):
    """Delete an ad with a delay."""
    import threading
    t1 = threading.Timer(float(delay / 2), _send_half_time_no_bid_notification,
                         args=(pk,))

    t2 = threading.Timer(float(delay), _really_delete, args=(pk,))

    t1.start()
    t2.start()


def _send_half_time_no_bid_notification(pk):
    if not did_someone_bid(pk):
        ad = ProductAd.objects.get(pk=pk)
        notify_data = {}
        notify_data.update({'ad_id': ad.id})
        notify_data.update({'type': 'half_time_no_bid'})
        notify_data.update({'ad_owner': str(ad.owner)})
        send_push_by_subscribed_categories(notify_data, ad.category)


def send_push_by_subscribed_categories(message_data, category):
    users = CustomUser.objects.filter(interests__contains=category,
                                      is_active=True)
    push_ids = []
    for user in users:
        if user.push_key:
            push_ids.append(user.push_key)

    if push_ids:
        _send_push_notification(message_data, reg_ids=push_ids)


def did_someone_bid(pk):
    ad = ProductAd.objects.get(pk=pk)
    return ad.bids.count() > 0


def get_user_id_by_name(username):
    try:
        return CustomUser.objects.get(username=username).id
    except CustomUser.DoesNotExist:
        raise Http404


def did_user_already_bid(ad_id, bidder_id):
    bids = Bids.objects.filter(ad_id=ad_id, bidder_id=bidder_id)
    return len(bids) > 0


def get_highest_bid(pk):
    bids = Bids.objects.filter(ad=pk)
    highest_bid = None
    last_bid = 0.0
    for bid in bids:
        if bid.bid > last_bid:
            last_bid = bid.bid
            highest_bid = bid

    return highest_bid
