from django.shortcuts import render,redirect
from django.contrib import messages
from django.urls import reverse_lazy,reverse
from . models import Contact
from django.core.mail import send_mail
# Create your views here.

def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']

        #check if user has made inquiru already

        if request.user.is_authenticated:
            user_id = request.user.id
            has_coctacted = Contact.objects.all().filter(listing_id=listing_id,user_id=user_id)

            if has_coctacted:
                messages.error(request,'You Have Already Made An Inquiry For This Listing')
                return redirect('/listings/'+listing_id)

        contact = Contact(listing=listing,listing_id=listing_id,name=name,email=email,phone=phone,message=message,user_id=user_id)
        contact.save()

        send_mail(
            'Property Listing Inquire',
            'There has been inquire for '+listing + '. Sign into the admin panel for more info',
            'contact@mahbubalamevan.me',
            [realtor_email,'mahbub.evan00@gmail.com'],
            fail_silently=False
        )

        messages.success(request,'Submitted Successfully, a realtor will get back to you soon !!!')
        return redirect('/listings/'+listing_id)
