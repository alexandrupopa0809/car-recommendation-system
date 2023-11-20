from django.shortcuts import render


def home(request):
    if request.method == "POST":
        user_input = request.POST.get("user_input", "")
        print(f"User input: {user_input}")
    return render(request, "home.html")
