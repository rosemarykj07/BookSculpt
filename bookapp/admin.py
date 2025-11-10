from django.contrib import admin
from . models import register_tbl,Book_tbl,ReadBook_tbl,ReadingList,SubscriptionPlan,UserSubscription,Profile,Payment,UserBook

# Register your models here.

admin.site.register(register_tbl)
admin.site.register(Book_tbl)
admin.site.register(ReadBook_tbl)
admin.site.register(ReadingList)
admin.site.register(SubscriptionPlan)
admin.site.register(UserSubscription)
admin.site.register(Profile)
admin.site.register(Payment)
admin.site.register(UserBook)


