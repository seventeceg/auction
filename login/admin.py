from django.contrib import admin

from login.models import(
    CustomUser,
    ProductAd,
    AdCategories,
    ProductAdInline,
    UserReview,
    Bids,
    Messages
)


class UserReviewAdmin(admin.ModelAdmin):
    pass


class BidsAdmin(admin.ModelAdmin):
    pass


class MessagesAdmin(admin.ModelAdmin):
    pass


class UserProfileAdmin(admin.ModelAdmin):
    can_delete = False
    verbose_name_plural = 'userprofile'
    list_per_page = 15
    search_fields = ('username', 'email')
    list_display = ('username', 'email', 'created', 'is_active')

    exclude = ('user_permissions', 'groups')
    inlines = [ProductAdInline]


class AdAdmin(admin.ModelAdmin):
    can_delete = False
    verbose_name_plural = 'product ad'
    list_per_page = 15
    list_display = ('title', 'created')
    search_fields = ('title', )

    # inlines = [AdCommentsInline]


class AdCategoriesAdmin(admin.ModelAdmin):
    can_delete = False
    verbose_name = "Phone"
    verbose_name_plural = 'Ad Categories'
    list_per_page = 15
    list_display = ('name', 'photo')

admin.site.register(UserReview, UserReviewAdmin)
admin.site.register(Bids, BidsAdmin)
admin.site.register(CustomUser, UserProfileAdmin)
admin.site.register(ProductAd, AdAdmin)
admin.site.register(AdCategories, AdCategoriesAdmin)
