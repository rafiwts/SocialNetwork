from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import Image
from .forms import ImageCreateForm


def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    return render(request,
                  'images/image/detail.html',
                  {'section': 'images',
                   'image': image})

@login_required
def image_create(request):
    if request.method == 'POST':
        form = ImageCreateForm(data=request.POST) # the form has been sent
        if form.is_valid(): # validation (if it exists, then it returns a url)
            new_item = form.save(commit=False)  
            new_item.user = request.user # a user is added to the element 
            new_item.save() # saving to the database
            messages.success(request, "The image has been added")
            return redirect(new_item.get_absolute_url()) # redirected to the newly created element 
    else:
        form = ImageCreateForm(data=request.GET)
    
    return render(request,                            # if it does not exist, it redirect you to create an image
                  'images/image/create.html',
                  {'section': 'images',
                   'form': form})