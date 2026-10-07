from django.contrib import admin

from .models import CartItem, Notification, Order, OrderItem, Payment, Product, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'role', 'created_at')
    list_filter = ('role',)
    search_fields = ('name', 'email', 'auth0_user_id')
    ordering = ('-created_at',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'is_active', 'popularity_score')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'category', 'description')
    list_editable = ('price', 'stock', 'is_active')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_email', 'total_amount', 'order_status', 'payment_status', 'created_at')
    list_filter = ('order_status', 'payment_status')
    search_fields = ('user__email', 'id')
    ordering = ('-created_at',)
    list_select_related = ('user',)

    @admin.display(description='Customer email', ordering='user__email')
    def customer_email(self, obj):
        return obj.user.email


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'customer_email', 'amount', 'status', 'payment_method', 'stripe_payment_id', 'created_at')
    list_filter = ('status', 'payment_method')
    search_fields = ('stripe_payment_id', 'order__user__email', 'order__id')
    list_select_related = ('order', 'order__user')

    @admin.display(description='Customer email', ordering='order__user__email')
    def customer_email(self, obj):
        return obj.order.user.email


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'is_read', 'created_at')
    list_filter = ('type', 'is_read')


admin.site.register(CartItem)
admin.site.register(OrderItem)
