# """
# The modules have imported for different purpose mentioned as below:
# """
# import django_filters
# from django.db.models import Q
# from Services.models import Product


# class CustomSearchFilter(django_filters.Filter):
#     """
#     CustomSearchFilter
#     """
#     def filter(self, queryset, value):
#         """
#         filter
#         """
#         if value:
#             return queryset.filter(
#                 Q(product_title__icontains=value) |
#                 Q(product_category__category_name__icontains=value) |
#                 Q(product_sub_category__sub_category_name__icontains=value)|
#                 Q(product_attribute__icontains=value) |
#                 Q(tags__icontains=value)|
#                 Q(description__icontains=value)|
#                 Q(price_transport__amount__icontains=value)
#             )
#         return queryset

# class ProductFilter(django_filters.FilterSet):
#     """
#     ProductFilter
#     """
#     custom_search = CustomSearchFilter(
#         label='Custom Search',
#         field_name='your_model_field'
#     )
#     class Meta:
#         model = Product
#         fields = ['custom_search', ]
