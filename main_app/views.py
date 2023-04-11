from django.shortcuts import render

finches = [
  {'species': 'Evening Grosbeak', 'description': 'yellow and black', 'habitat': 'Northern and montane forests', 'note':'the Evening Grosbeak does not have a complex song, but rather draws from a collection of sweet, piercing notes and burry chirps.'},
  {'species': 'Pine Grosbeak', 'description': 'red and black', 'habitat': 'Open boreal forest', 'note':'Locals in Newfoundland affectionately call Pine Grosbeaks mopes because they can be so tame and slow moving.'},
  {'species': 'Common Redpoll', 'description': 'red white and black', 'habitat': 'Sub-Arctic forests and tundra ', 'note':'Common Redpolls sometimes escape the cold of winter nights by burrowing into snow.'},

]


# Create your views here.
def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def finches_index(request):
   return render(request, 'finches/index.html', {'finches': finches})
