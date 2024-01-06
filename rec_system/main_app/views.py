from django.shortcuts import render


def home(request):
    team_name = "Auto Advise Team"
    team_members = ["Popa Alexandru-Matei", "Varzaru Mihnea-Gabriel"]
    return render(request, 'home.html', {'team_name': team_name, 'team_members': team_members})


def filters(request):
    return render(request, "filters.html")


def process_filters(request):
    if request.method == "POST":
        mileage = request.POST.get("mileage")
        price = request.POST.get("price")
        horsepower = request.POST.get("horsepower")
        description = request.POST.get("description")

        results = {
            "mileage": mileage,
            "price": price,
            "horsepower": horsepower,
            "description": description,
        }

        return render(request, "recommendations.html", results)

    return render(request, "filters.html")