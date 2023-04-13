from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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


@login_required
@require_POST # only for a post method (we have also require_GET)
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action') # like or unlike
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status':'ok'})
        except:
            pass
    return JsonResponse({'status':'ok'}) # it returns a velue in JSON


@login_required
def image_list(request):
    images = Image.objects.all()
    paginator = Paginator(images, 8)
    page = request.GET.get('page')
    images_only = request.GET.get('images_only')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        if images_only:
            return HttpResponse('')
        images = paginator.page(paginator.num_pages)
    if images_only:
        return render(request,
                      'images/image/list_images.html',
                      {'section': 'images',
                       'images': images})
    return render(request,
                 'images/image/list.html',
                 {'section': 'images',
                  'images': images})