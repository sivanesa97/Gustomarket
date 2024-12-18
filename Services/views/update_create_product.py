"""
# The modules have imported for different purpose mentioned as below:
# render : to render an HTML template.
# login_required : checking a user is authorized or not.
# """
from django.shortcuts import render, redirect
from django.db.models import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from Services.models import (ProductAttribute, ProductCategory, ProductTag, SkuSold,
                             SkuPallet, OtherSkuSold, SkuBulk, SkuUnit, SalePresentation,
                             ProductDimension, ProductWeight, ProductPhoto, Product,
                             ProductSubCategory, Supplier, NotificationPreference,
                             SaleWindow, PriceTransport, ProductManufacturer, ProductPackaging,
                             Transportation, HandlingTransport, ProductCertification, Address)
from django.core.exceptions import ValidationError
from datetime import datetime, date


@login_required(login_url='sign_in')
def update_or_create_product(request, pk=0):
    """
    Functionality to handle for creating and updating product to a logged-in vendor.
    """
    supplier = Supplier.objects.get(user=request.user)
    product_inst = Product.objects.filter(
        id=pk, supplier=supplier).first()
    product_categories = ProductCategory.objects.all()
    product_manufacturers = ProductManufacturer.objects.all()
    selling_choices = SkuSold.objects.all()
    bulk_choices = SkuBulk.objects.all()
    unit_choices = SkuUnit.objects.all()
    conditions = Transportation.CONDITION_CHOICES
    handling_choices = HandlingTransport.HANDLING_CHOICES
    certifications = ProductCertification.CERTIFICATION_CHOICES
    frequency_choices = NotificationPreference.objects.all()
    window_choices = SaleWindow.objects.all()
    presentation_choices = SalePresentation.objects.all()
    dimension_choices = ProductDimension.DIMENSION_CHOICES
    weight_choices = ProductWeight.WEIGHT_CHOICES
    addresses = Address.objects.filter(supplier=supplier, is_active=True)

    if request.method == 'POST':
        # Get data from the request.
        product_id = request.POST.get('product_id')
        # product_tags = request.POST.getlist('product-tags')
        product_attributes = request.POST.getlist('product-attributes')
        is_draft = request.POST.get('publish_action', False) == 'draft'
        images = request.FILES.getlist('images[]')
        sku_sold_value = request.POST.get('sku_sold')
        sku_picked_value = request.POST.get('sku_picked')
        perishability = request.POST.get('perishability')

        # Get availability data
        from_time = request.POST.get('from_time')
        to_time = request.POST.get('to_time')
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')

        if product_id:
            product_inst = Product.objects.filter(
                supplier=supplier, id=product_id).first()
        else:
            product_inst = Product.objects.create(supplier=supplier)

        product_inst.product_title = request.POST.get('product_title')
        description_content = request.POST.get('description_content')
        if description_content:
            product_inst.description = description_content
        # product_inst.discussion = request.POST.get('discussion_content')
        product_inst.notification_frequency = request.POST.get(
            'notification_preference')
        if perishability and perishability in dict(Product.PERISHABILITY_CHOICES):
            product_inst.perishability = perishability
        else:
            product_inst.perishability = 'days'  # default value

        # Get and validate availability data
        from_time = request.POST.get('from_time')
        to_time = request.POST.get('to_time')
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')

        try:
            # Validate time range if both are provided
            if from_time and to_time:
                from_time_obj = datetime.strptime(from_time, '%H:%M').time()
                to_time_obj = datetime.strptime(to_time, '%H:%M').time()
                if from_time_obj >= to_time_obj:
                    raise ValidationError("End time must be after start time")
                product_inst.from_time = from_time_obj
                product_inst.to_time = to_time_obj

            # Validate date range if both are provided
            if from_date and to_date:
                from_date_obj = datetime.strptime(from_date, '%Y-%m-%d').date()
                to_date_obj = datetime.strptime(to_date, '%Y-%m-%d').date()
                if from_date_obj >= to_date_obj:
                    raise ValidationError("End date must be after start date")
                if from_date_obj < date.today():
                    raise ValidationError("Start date cannot be in the past")
                product_inst.from_date = from_date_obj
                product_inst.to_date = to_date_obj

            # Save the product instance
            product_inst.save()

        except ValidationError as e:
            context = {
                'error_message': str(e),
                'product': product_inst,
                'product_categories': product_categories,
                'supplier': supplier,
                'product_manufacturers': product_manufacturers,
                'selling_choices': selling_choices,
                'bulk_choices': bulk_choices,
                'unit_choices': unit_choices,
                'frequency_choices': frequency_choices,
                'window_choices': window_choices,
                'presentation_choices': presentation_choices,
                'dimension_choices': dimension_choices,
                'weight_choices': weight_choices,
                'handling_choices': handling_choices,
                'certifications': certifications,
                'conditions': conditions,
                'addresses': addresses,
            }
            return render(request, 'new-product.html', context)

        # Create and update category and sub category.
        category_inst = create_or_get_category(request)
        product_inst.product_category = category_inst[0]
        product_inst.product_sub_category = category_inst[1]

        # Create and update attribute and tag.
        '''
        attributes_and_tags_inst = create_or_get_attributes_and_tags(
            product_attributes, product_tags)
        if attributes_and_tags_inst[0]:
            product_inst.product_attribute.set(attributes_and_tags_inst[0])
        if attributes_and_tags_inst[1]:
            product_inst.product_tag.set(attributes_and_tags_inst[1])'''

        attributes_inst = create_or_get_attributes(product_attributes)
        if attributes_inst:
            product_inst.product_attribute.set(attributes_inst)

        # Create and update price transport.
        try:
            price_transport = update_or_create_price_transport(
                request, product_inst)
            product_inst.price_transport = price_transport
        except ObjectDoesNotExist:
            print("Exception caught")
            context = {
                'error_message': 'Please complete your profile with name and address information before creating a product.'
            }
            return render(request, 'new-product.html', context)

        # Update or create product packaging.
        product_packaging_inst = update_or_create_product_packaging(
            request, product_inst)
        product_inst.product_packaging = product_packaging_inst

        product_inst.is_draft = is_draft
        product_inst.save()

        # Update or create product photos
        ProductPhoto.objects.bulk_create(
            [ProductPhoto(product_photo=image, product=product_inst) for image in images])
        if not product_inst:
            product_inst = Product.objects.create(supplier=supplier)

        # Ensure the product has a packaging instance
        if not product_inst.product_packaging:
            product_packaging = ProductPackaging.objects.create(product=product_inst)
        else:
            product_packaging = product_inst.product_packaging
        
        # Update 'sku_sold'
        if sku_sold_value:
            sku_sold_instance = SkuSold.objects.filter(id=sku_sold_value).first()
            if sku_sold_instance:
                product_packaging.sku_sold = sku_sold_instance

        # Update 'sku_picked'
        if sku_picked_value:
            sku_picked_instance = SkuUnit.objects.filter(id=sku_picked_value).first()
            if sku_picked_instance:
                product_packaging.sku_unit = sku_picked_instance

        # Save the packaging and product
        product_packaging.save()
        product_inst.save()
        if product_id:
            return redirect('listed_unlisted_product')
        return render(request, 'products-thank-you.html')
        


    context = {
        'product_categories': product_categories,
        'supplier': supplier,
        'product': product_inst,
        'product_manufacturers': product_manufacturers,
        'selling_choices': selling_choices,
        'bulk_choices': bulk_choices,
        'unit_choices': unit_choices,
        'frequency_choices': frequency_choices,
        'window_choices': window_choices,
        'presentation_choices': presentation_choices,
        'dimension_choices': dimension_choices,
        'weight_choices': weight_choices,
        'handling_choices': handling_choices,
        'certifications': certifications,
        'conditions': conditions,
        'addresses': addresses,
    }
    return render(request, 'new-product.html', context)


def create_or_get_category(request):
    """
    Update or create a category and sub category of a product.
    """
    # Get data from request.
    product_category_id = request.POST.get('product_category_id')
    sub_category_id = request.POST.get('sub_category_id')
    other_category_option = request.POST.get('other_category_name')
    other_subcategory_option = request.POST.get('other_subcategory_name')

    # Get product category and sub category instance
    product_category_inst = ProductCategory.objects.filter(
        id=int(product_category_id)).first()
    sub_category_inst = ProductSubCategory.objects.filter(
        id=int(sub_category_id)).first()

    # If it doesn't exist, create a new category
    if not product_category_inst:
        product_category_inst, _ = ProductCategory.objects.get_or_create(
            category_name=other_category_option)
        sub_category_inst, _ = ProductSubCategory.objects.get_or_create(
            sub_category_name=other_subcategory_option, product_category=product_category_inst)

    return product_category_inst, sub_category_inst


'''
def create_or_get_attributes_and_tags(product_attributes, product_tags):'''
"""
    Create attribute and tag of a product.
    """
'''
    # Get and create attribute instances.
    attributes = [ProductAttribute.objects.get_or_create(attribute_name=attribute_name)[0]
                  for attribute_name in product_attributes[0].split(',') if attribute_name]

    # Get and Create Tag instances.
    tags = [ProductTag.objects.get_or_create(tag_name=tag_name)[0]
            for tag_name in product_tags[0].split(',') if tag_name]

    return attributes, tags'''


def create_or_get_attributes(product_attributes):
    """
    Create attribute of a product.
    """
    # Get and create attribute instances.
    attributes = [ProductAttribute.objects.get_or_create(attribute_name=attribute_name)[0]
                  for attribute_name in product_attributes[0].split(',') if attribute_name]
    return attributes


def update_or_create_price_transport(request, product_inst):
    """
    Update or create a price transport instance of a product.
    """
    print("Creating price transport")
    print(product_inst)
    # Get data from the request.
    # selected_condition = request.POST.get('transportation')
    # custom_condition = request.POST.get('custom_condition', '')
    # handling_transport = request.POST.get('handling_transport')
    # certification = request.POST.get('certification')
    # start_date = request.POST.get('start_date')
    # end_date = request.POST.get('end_date')

    # Create price transport instance if does not exist.
    price_transport, _ = PriceTransport.objects.get_or_create(
        product=product_inst)
    price_transport.amount = request.POST.get('price')
    # price_transport.stock_count = int(request.POST.get('stock_count'))
    # price_transport.delivery_charge = request.POST.get('delivery_charge')
    # price_transport.minimum_price = request.POST.get('minimum_order')
    '''
    price_transport.is_best_transportation = request.POST.get(
        'best_ransportation', False) == 'on'
    price_transport.is_special_packaging = request.POST.get(
        'special_packaging', False) == 'on'
    price_transport.allowing_customer_request = request.POST.get(
        'specific_condition', False) == 'on'
    '''

    # Save the selected and custom condition.
    '''
    if selected_condition == 'condition' and custom_condition:
        transportation_instance, _ = Transportation.objects.get_or_create(
            condition='condition', custom_condition=custom_condition)
        price_transport.transportation = transportation_instance
    elif selected_condition:
        transportation_instance, _ = Transportation.objects.get_or_create(
            condition=selected_condition)
        price_transport.transportation = transportation_instance'''

    # Save the product transport handling.
    '''
    if handling_transport:
        handling_transport_inst, _ = HandlingTransport.objects.get_or_create(
            handling_option=handling_transport)
        price_transport.handling_transport = handling_transport_inst'''

    # Save the product certification.
    '''
    if certification:
        certification_inst, _ = ProductCertification.objects.get_or_create(
            certification=certification)
        price_transport.certification = certification_inst'''

    # Save the address.
    address = Address.objects.get(id=request.POST.get('address_id'))
    if address:
        price_transport.address = address
    else:
        price_transport.address = None

    '''
    if start_date:
        price_transport.from_seasonality = start_date
    else:
        price_transport.from_seasonality = None
    if end_date:
        price_transport.to_seasonality = end_date
    else:
        price_transport.to_seasonality = None'''

    price_transport.save()

    return price_transport


def update_or_create_product_packaging(request, product_inst):
    """
    Update or create a price packaging instance of a product.
    """
    # Create product packaging instance if does not exist.
    product_packaging_inst, _ = ProductPackaging.objects.get_or_create(
        product=product_inst)

    # Update data and assign product manufacturer instance to product packaging.
    '''
    product_packaging_inst.stacked_layer = (
        request.POST.get('stacked_layer'))
    product_packaging_inst.pieces_per_sku = (
        request.POST.get('pieces_per_sku'))
    product_packaging_inst.waste_per_month = request.POST.get('average-waste')
    product_packaging_inst.is_fast = request.POST.get('is_fast', False) == 'on'
    product_manufacturer_inst = ProductManufacturer.objects.filter(
        id=int(request.POST.get('product_manufacturer'))).first()
    if product_manufacturer_inst:
        product_packaging_inst.product_manufacturer = product_manufacturer_inst'''

    # Get and update sku.
    get_and_update_sku(request, product_packaging_inst)

    # Get or Create notification preference.
    notification_preference_name = request.POST.get('notification_preference')
    if notification_preference_name:
        product_packaging_inst.notification_preference, _ = \
            NotificationPreference.objects.get_or_create(
                frequency=notification_preference_name)

    # Get or Create window of sale.
    '''
    window_sale_name = request.POST.get('window_sale')
    if window_sale_name:
        product_packaging_inst.sale_window, _ = SaleWindow.objects.get_or_create(
            window_name=window_sale_name)
    '''

    # Get or Create sale presentation.
    # sale_presentation_name = request.POST.get('sale_presentation')
    '''
    if sale_presentation_name:
        product_packaging_inst.sale_presentation, _ = SalePresentation.objects.get_or_create(
            presentation_name=sale_presentation_name)'''

    # Save product dimension and weight.
    save_product_dimension_weight(request, product_packaging_inst)

    # Save the product packagaing instance.
    product_packaging_inst.save()

    return product_packaging_inst


def get_and_update_sku(request, product_packaging_inst):
    """
    Update or create a sku instance of a product.
    """
    # Get data from the request.
    sku_sold = request.POST.get('sku_sold')
    sku_bulk_selling = request.POST.get('sku_bulk_selling')
    sku_unit_selling = request.POST.get('sku_unit_selling')
    sku_pallet_selling = request.POST.get('sku_pallet_selling')
    other_sku_selling = request.POST.get('other_sku_selling')

    # Get and assign SkuSold instance to product packaging.
    sku_sold_inst = SkuSold.objects.filter(selling_option=sku_sold).first()
    if sku_sold_inst:
        # Based on SKU sold, handle the specific SKU type instances
        if sku_sold == 'Bulk' and sku_bulk_selling:
            sku_bulk_inst, created = SkuBulk.objects.get_or_create(
                bulk_option=sku_bulk_selling, sku_sold=sku_sold_inst)
            if created:
                sku_bulk_inst.save()

            # Delete existing instances related to product packaging if they are not None.
            if product_packaging_inst.sku_unit:
                product_packaging_inst.sku_unit = None
            if product_packaging_inst.sku_pallet:
                product_packaging_inst.sku_pallet = None
            if product_packaging_inst.other_sku_sold:
                product_packaging_inst.other_sku_sold = None

            product_packaging_inst.sku_bulk = sku_bulk_inst
            product_packaging_inst.sku_sold = sku_sold_inst

        elif sku_sold == 'Per Unit' and sku_unit_selling:
            sku_unit_inst, created = SkuUnit.objects.get_or_create(
                unit_option=sku_unit_selling, sku_sold=sku_sold_inst)
            if created:
                sku_unit_inst.save()

            # Delete existing instances related to product packaging if they are not None.
            if product_packaging_inst.sku_bulk:
                product_packaging_inst.sku_bulk = None
            if product_packaging_inst.sku_pallet:
                product_packaging_inst.sku_pallet = None
            if product_packaging_inst.other_sku_sold:
                product_packaging_inst.other_sku_sold = None

            product_packaging_inst.sku_unit = sku_unit_inst
            product_packaging_inst.sku_sold = sku_sold_inst

        elif sku_sold == 'Pallet' and sku_pallet_selling:
            sku_pallet_inst, created = SkuPallet.objects.get_or_create(
                pallet_info=sku_pallet_selling, sku_sold=sku_sold_inst)
            if created:
                sku_pallet_inst.save()

            # Delete existing instances related to product packaging if they are not None.
            if product_packaging_inst.sku_bulk:
                product_packaging_inst.sku_bulk = None
            if product_packaging_inst.sku_unit:
                product_packaging_inst.sku_unit = None
            if product_packaging_inst.other_sku_sold:
                product_packaging_inst.other_sku_sold = None

            product_packaging_inst.sku_pallet = sku_pallet_inst
            product_packaging_inst.sku_sold = sku_sold_inst

        elif sku_sold == 'Other' and other_sku_selling:
            other_sku_inst, created = OtherSkuSold.objects.get_or_create(
                other_info=other_sku_selling, sku_sold=sku_sold_inst)
            if created:
                other_sku_inst.save()

            # Delete existing instances related to product packaging if they are not None.
            if product_packaging_inst.sku_bulk:
                product_packaging_inst.sku_bulk = None
            if product_packaging_inst.sku_unit:
                product_packaging_inst.sku_unit = None
            if product_packaging_inst.sku_pallet:
                product_packaging_inst.sku_pallet = None

            product_packaging_inst.other_sku_sold = other_sku_inst
            product_packaging_inst.sku_sold = sku_sold_inst


def save_product_dimension_weight(request, product_packaging_inst):
    """
    Update or create a product dimension ad product weight instance of a product.
    """
    # Get data from the request.
    # dimension_unit = request.POST.get('dimension_unit')
    # weight_unit = request.POST.get('weight_unit')

    # Save product_dimension's height, length, and width.
    '''
    if dimension_unit:
        product_packaging_inst.product_dimension, _ = ProductDimension.objects.get_or_create(
            dimension_unit=dimension_unit,
            height=request.POST.get('height'),
            length=request.POST.get('length'),
            width=request.POST.get('width')
        )

    # Save product weight and its value.
    if weight_unit:
        product_packaging_inst.product_weight, _ = ProductWeight.objects.get_or_create(
            weight_unit=weight_unit,
            weight_value=request.POST.get('weight')
        )'''

