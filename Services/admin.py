"""
Import below module and models for registering to admin site.
"""
from django.contrib import admin
from Services.admins import CompanyAdmin
from Services.models import Company
from Services.admins import SupplierAdmin
from Services.models import Supplier
from Services.admins import CompanyTypeAdmin
from Services.models import CompanyType
from Services.admins import AddressAdmin
from Services.models import Address
from Services.admins import LocationTypeAdmin
from Services.models import LocationType
from Services.admins import CountryAdmin
from Services.models import Country
from Services.admins import StateAdmin
from Services.models import State
from Services.admins import TeamAdmin
from Services.models import Team
from Services.admins import SeniorityAdmin
from Services.models import Seniority
from Services.models import TermsConditions
from Services.admins import DocumentTypeAdmin
from Services.models import DocumentType
from Services.models import CompanyRegistrationFile
from Services.models import LicenseCertificate
from Services.admins import RoleAdmin
from Services.models import Role
from Services.admins import ProfileAdmin
from Services.models import Profile
from Services.admins import CustomPermissionAdmin
from Services.models import CustomPermission
from Services.admins import ProductAdmin
from Services.models import Product
from Services.admins import ProductAttributeAdmin
from Services.models import ProductAttribute
from Services.admins import ProductCategoryAdmin
from Services.models import ProductCategory
from Services.admins import PriceTransportAdmin
from Services.models import PriceTransport
from Services.admins import ProductSubCategoryAdmin
from Services.models import ProductSubCategory
from Services.admins import ProductPhotoAdmin
from Services.models import ProductPhoto
from Services.admins import ProductOrderAdmin
from Services.models import Order
from Services.admins import OrderItemAdmin
from Services.models import OrderItem
from Services.admins import CartAdmin
from Services.models import Cart
from Services.admins import ProductTagAdmin
from Services.models import ProductTag
from Services.admins import CustomerAdmin
from Services.models import Customer
from Services.admins import PaymentAdmin
from Services.models import Payment
from Services.admins import TooltipDataAdmin
from Services.models import TooltipData
from Services.admins import TooltipAdmin
from Services.models import Tooltip
from Services.admins import ProductManufacturerAdmin
from Services.models import ProductManufacturer
from Services.admins import SkuSoldAdmin
from Services.models import SkuSold
from Services.admins import SkuBulkAdmin
from Services.models import SkuBulk
from Services.admins import SkuUnitAdmin
from Services.models import SkuUnit
from Services.admins import SkuPalletAdmin
from Services.models import SkuPallet
from Services.admins import OtherSkuSoldAdmin
from Services.models import OtherSkuSold
from Services.admins import NotificationPreferenceAdmin
from Services.models import NotificationPreference
from Services.admins import SaleWindowAdmin
from Services.models import SaleWindow
from Services.admins import SalePresentationAdmin
from Services.models import SalePresentation
from Services.admins import ProductDimensionAdmin
from Services.models import ProductDimension
from Services.admins import ProductWeightAdmin
from Services.models import ProductWeight
from Services.admins import ProductPackagingAdmin
from Services.models import ProductPackaging
from Services.admins import TransportationAdmin
from Services.models import Transportation
from Services.admins import HandlingTransportAdmin
from Services.models import HandlingTransport
from Services.admins import ProductCertificationAdmin
from Services.models import ProductCertification


# Register models to the admin site.
admin.site.register(Company, CompanyAdmin)
admin.site.register(Supplier, SupplierAdmin)
admin.site.register(CompanyType, CompanyTypeAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(LocationType, LocationTypeAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Seniority, SeniorityAdmin)
admin.site.register(TermsConditions)
admin.site.register(DocumentType, DocumentTypeAdmin)
admin.site.register(CompanyRegistrationFile)
admin.site.register(LicenseCertificate)
admin.site.register(Role, RoleAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(CustomPermission, CustomPermissionAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductAttribute, ProductAttributeAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(PriceTransport, PriceTransportAdmin)
admin.site.register(ProductSubCategory, ProductSubCategoryAdmin)
admin.site.register(ProductPhoto, ProductPhotoAdmin)
admin.site.register(Order, ProductOrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(ProductTag, ProductTagAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(TooltipData, TooltipDataAdmin)
admin.site.register(Tooltip, TooltipAdmin)
admin.site.register(ProductManufacturer, ProductManufacturerAdmin)
admin.site.register(SkuSold, SkuSoldAdmin)
admin.site.register(SkuBulk, SkuBulkAdmin)
admin.site.register(SkuUnit, SkuUnitAdmin)
admin.site.register(SkuPallet, SkuPalletAdmin)
admin.site.register(OtherSkuSold, OtherSkuSoldAdmin)
admin.site.register(NotificationPreference, NotificationPreferenceAdmin)
admin.site.register(SaleWindow, SaleWindowAdmin)
admin.site.register(SalePresentation, SalePresentationAdmin)
admin.site.register(ProductDimension, ProductDimensionAdmin)
admin.site.register(ProductWeight, ProductWeightAdmin)
admin.site.register(ProductPackaging, ProductPackagingAdmin)
admin.site.register(Transportation, TransportationAdmin)
admin.site.register(HandlingTransport, HandlingTransportAdmin)
admin.site.register(ProductCertification, ProductCertificationAdmin)
