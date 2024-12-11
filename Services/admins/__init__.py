"""
Importing here becuase have not to define a full path
for importing admin's classes to another file.
"""
from Services.admins.company_admin import CompanyAdmin
from Services.admins.supplier_admin import SupplierAdmin
from Services.admins.company_type_admin import CompanyTypeAdmin
from Services.admins.address_admin import AddressAdmin
from Services.admins.location_type_admin import LocationTypeAdmin
from Services.admins.country_admin import CountryAdmin
from Services.admins.state_admin import StateAdmin
from Services.admins.team_admin import TeamAdmin
from Services.admins.seniority_admin import SeniorityAdmin
from Services.admins.document_type_admin import DocumentTypeAdmin
from Services.admins.role_admin import RoleAdmin
from Services.admins.profile_admin import ProfileAdmin
from Services.admins.custom_permission_admin import CustomPermissionAdmin
from Services.admins.product_admin import ProductAdmin
from Services.admins.price_transport_admin import PriceTransportAdmin
from Services.admins.product_attribute_admin import ProductAttributeAdmin
from Services.admins.product_category_admin import ProductCategoryAdmin
from Services.admins.product_sub_category_admin import ProductSubCategoryAdmin
from Services.admins.product_image_admin import ProductPhotoAdmin
from Services.admins.product_order_admin import ProductOrderAdmin
from Services.admins.order_item_admin import OrderItemAdmin
from Services.admins.cart_admin import CartAdmin
from Services.admins.product_tag_admin import ProductTagAdmin
from Services.admins.customer_admin import CustomerAdmin
from Services.admins.payment_admin import PaymentAdmin
from Services.admins.tooltip_admin import TooltipAdmin, TooltipDataAdmin
from Services.admins.product_manufacturer_admin import ProductManufacturerAdmin
from Services.admins.sku_sold_admin import SkuSoldAdmin, \
    SkuBulkAdmin, SkuUnitAdmin, SkuPalletAdmin, OtherSkuSoldAdmin
from Services.admins.notification_preference_admin import NotificationPreferenceAdmin
from Services.admins.sale_window_admin import SaleWindowAdmin
from Services.admins.sale_presentation_admin import SalePresentationAdmin
from Services.admins.product_dimension_weight_admin import ProductDimensionAdmin, ProductWeightAdmin
from Services.admins.product_packaging_admin import ProductPackagingAdmin
from Services.admins.transportation_admin import TransportationAdmin, \
    HandlingTransportAdmin, ProductCertificationAdmin
