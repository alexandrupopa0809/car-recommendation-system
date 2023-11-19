from django.shortcuts import render

# Create your views here.

def home_screen_view(request):
    #print(request.headers)
    print(request.POST)
    #
    #if request.method == "POST":
     #   my_recommendation = request.POST.get('recomandare')
      #  print(my_recommendation)
    return render(request, "index.html", {})

