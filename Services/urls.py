"""
URL Patterns for User Authentication Views

This module defines URL patterns for user authentication-related views in a Django project.

- The empty path ('') maps to the 'base' view and represents the root URL of the application.
  It serves as a landing page or a starting point for users.

- The 'signin/' path maps to the 'sign_in' view and is used for user login functionality.
  Users can visit '/signin/' to access the login page.

- The 'signup/' path maps to the 'signup' view and is used for user registration functionality.
  Users can visit '/signup/' to access the registration page.

These URL patterns are used to route incoming HTTP requests to their respective views
and give each view a unique name for easy reverse URL lookups.
"""
from django.urls import path
from Services.views.custom_error_404 import custom_404
from Services.views import (
    account_registration, add_to_cart, product_cart, verify_otp,
    approved_supplier, change_password, contact_list,
    checkout_session, credit_notes, customer_list,
    delete_cart_item, delete_product, document_registration,
    earnings, forgot_password, get_cart_item_count,
    get_country_state, get_document_types, get_sub_category,
    join_team, listed_unlisted_product, manage_location,
    manage_team, past_purchases, payment_registration,
    payment_success, payouts, preference,
    product_info, product_list, purchases,
    purchase_details, refunds, resend_otp,
    seller_dashboard, services_account, set_password,
    setup_stripe_connect, sign_in, sign_out, sign_up,
    statements, stripe_connect_callback, stripe_webhook,
    team_registration, terms_conditions, update_cart_quantity,
    update_create_product, help_page, change_prices,  update_subtotal_price, new_poduct_view,
    inventory,
)
from .views import product
from .views.inventory import (
    inventory_list, get_inventory, get_inventory_history, 
    update_inventory, add_inventory
)


handler404 = custom_404


urlpatterns = [
    path('products', purchases.purchases, name="products"),
    path('', sign_up.sign_up, name='sign_up'),
    path('verify-otp', verify_otp.verify_otp, name='verify_otp'),
    path('resend-otp', resend_otp.resend_otp, name='resend_otp'),
    path('set-password', set_password.set_password, name='set_password'),
    path('sign-in', sign_in.sign_in, name='sign_in'),
    path('sign-out', sign_out.sign_out, name='sign_out'),
    path('change-password/', change_password.change_password, name='change_password'),
    path('account-registration/<str:editable>/', account_registration.account_registration,
         name='account_registration'),
    path('team-registration/', team_registration.team_registration,
         name='team_registration'),
    path('setup-stripe-connect/', setup_stripe_connect.setup_stripe_connect,
         name='setup_stripe_connect'),
    path('document-registration/', document_registration.document_registration,
         name='document_registration'),
    path('terms-conditions/', terms_conditions.terms_conditions,
         name='terms_conditions'),
    path('get-country-state/', get_country_state.get_country_state,
         name='get_country_state'),
    path('get-document-types/', get_document_types.get_document_types,
         name='get_document_types'),
    path('manage-team/', manage_team.manage_team, name='manage_team'),
    path('manage-location/', manage_location.manage_location, name='manage_location'),
    path('get-sub-category/', get_sub_category.get_sub_category,
         name="get_sub_category"),
    path('product-delete/<int:pk>/',
         delete_product.product_delete, name='product_delete'),
    path('products/<str:status>/', product_list.product_list, name='product_list'),
    path('past-purchase/', past_purchases.past_purchase, name='past_purchase'),
    path('earnings/', earnings.earnings, name='earnings'),
    path('credit-notes/', credit_notes.credit_notes, name='credit_notes'),
    path('services-account/', services_account.services_account,
         name='services_account'),
    path('seller-dashboard/', seller_dashboard.seller_dashboard,
         name='seller_dashboard'),
    path('move_to_ordered/', seller_dashboard.move_to_ordered, name='move_to_ordered'),
    path('cart/', product_cart.cart, name='cart'),
    path('customer-list/', customer_list.customer_list, name='customer_list'),
    path('payouts/', payouts.payouts, name='payouts'),
    path('statements/', statements.statements, name='statements'),
    path('refunds/', refunds.refunds, name='refunds'),
    path('contact-list/', contact_list.contact_list, name='contact_list'),
    path('purchase-details/', purchase_details.purchase_details,
         name='purchase_details'),
    path('product-info/<int:pk>/', product_info.product_info, name='product_info'),
    path('stripe-connect-callback/', stripe_connect_callback.stripe_connect_callback,
         name='stripe_connect_callback'),
    path('listed-unlisted-product/', listed_unlisted_product.listed_unlisted_product,
         name='listed_unlisted_product'),
    path('payment-registration/', payment_registration.payment_registration,
         name='payment_registration'),
    path('forgot-password/', forgot_password.forgot_password, name='forgot_password'),
    path('forgot-password-confirm/<str:uidb64>/<str:token>/',
         forgot_password.forgot_password_confirm, name='forgot_password_confirm'),
    path('join-team/', join_team.join_team, name='join_team'),
    path('join-team2/', join_team.join_team_2, name='join_team_2'),
    path('preference/', preference.preference, name='preference'),
    path('add-to-cart/<int:product_id>/',
         add_to_cart.add_to_cart, name='add_to_cart'),
    path('delete-cart-item/<int:pk>/',
         delete_cart_item.delete_cart_item, name='delete_cart_item'),
    path('update-cart-quantity/<int:cart_item_id>/',
         update_cart_quantity.update_cart_quantity, name='update_cart_quantity'),
    path('create-checkout-session/', checkout_session.create_checkout_session,
         name='create_checkout_session'),
    path('get-cart-item-count/', get_cart_item_count.get_cart_item_count,
         name='get_cart_item_count'),
    path('success/', payment_success.payment_success, name='payment_success'),
    path('cancel/', payment_success.payment_cancel, name='payment_cancel'),
    path('get-picklist-data/<str:order_id>/', payment_success.get_picklist_data, name='get_picklist_data'),
    path('get-invoice-data/<str:order_id>/', payment_success.get_invoice_data, name='get_invoice_data'),
    path('get-purchase-order/<str:order_id>/', payment_success.get_purchase_order, name='get_purchase_order'),
    path('stripe-webhook/', stripe_webhook.stripe_webhook, name='stripe_webhook'),
    path('supplier-list/', approved_supplier.approved_supplier,
         name='approved_supplier'),
    path('add-product/<int:pk>/',
         update_create_product.update_or_create_product, name="add_product"),
    path('help', help_page.help, name="help"),
    path('change_prices', change_prices.change_prices, name="change_prices"),
    path('update_total_price', update_subtotal_price.update_subtotal_price, name='update_total_price'),
    path('new-product/', new_poduct_view.new_product_view, name='new_product'),
    path('inventory/', inventory_list, name='inventory_list'),
    path('inventory/<int:id>/get/', get_inventory, name='get_inventory'),
    path('inventory/<int:id>/history/', get_inventory_history, name='get_inventory_history'),
    path('inventory/<int:id>/update/', update_inventory, name='update_inventory'),
    path('products/search/', product.search_products, name='product_search'),
    path('inventory/bulk-update/', inventory.bulk_update_inventory, name='inventory_bulk_update'),
    path('inventory/adjustment-report/', inventory.get_adjustment_report, name='inventory_adjustment_report'),
    path('inventory/<int:id>/history/', inventory.get_inventory_history, name='inventory_history'),
    path('inventory/add/', add_inventory, name='add_inventory'),
    
    
]
