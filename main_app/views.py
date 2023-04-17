import os
import uuid
import boto3


from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Finch, Toy, Photo
from .forms import FeedingForm





# Create your views here.
def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def finches_index(request):
   finches = Finch.objects.all()
   return render(request, 'finches/index.html', {'finches': finches})

def finches_detail(request, finch_id):
  finch = Finch.objects.get(id=finch_id)
  id_list = finch.toys.all().values_list('id')
  toys_finch_doesnt_have = Toy.objects.exclude(id__in=id_list)
  feeding_form = FeedingForm()
  return render(request, 'finches/detail.html', { 'finch': finch, 'feeding_form': feeding_form, 'toys':toys_finch_doesnt_have })

def add_feeding(request, finch_id):
  form = FeedingForm(request.POST)
  if form.is_valid():
    new_feeding = form.save(commit=False)
    new_feeding.finch_id = finch_id
    new_feeding.save()
  return redirect('detail', finch_id=finch_id)

def assoc_toy(request, finch_id, toy_id):
  # Note that you can pass a toy's id instead of the whole toy object
  Finch.objects.get(id=finch_id).toys.add(toy_id)
  return redirect('detail', finch_id=finch_id)

def remove_toy(request, finch_id, toy_id):
    finch = Finch.objects.get(id=finch_id)
    toy = Toy.objects.get(id=toy_id)
    finch.toys.remove(toy)
    return redirect(reverse('detail', kwargs={'finch_id': finch_id}))

def add_photo(request, finch_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            # build the full url string
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            # we can assign to cat_id or cat (if you have a cat object)
            Photo.objects.create(url=url, finch_id=finch_id)
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
    return redirect('detail', finch_id=finch_id)


class FinchCreate(CreateView):
  model = Finch
  fields = ['species', 'description', 'habitat', 'note']

class FinchUpdate(UpdateView):
  model = Finch
  fields =['description', 'habitat', 'note']

class FinchDelete(DeleteView):
  model = Finch
  success_url = '/finches'
