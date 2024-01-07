from django.shortcuts import render

from .cache import get_cached_dataframe
from .ml_computations import get_bert_recommendations


def home(request):
    team_name = "Auto Advise Team"
    team_members = ["Popa Alexandru-Matei", "Varzaru Mihnea-Gabriel"]
    return render(
        request, "home.html", {"team_name": team_name, "team_members": team_members}
    )


def filters(request):
    return render(request, "filters.html")


def process_filters(request):
    if request.method == "POST":
        mileage = request.POST.get("mileage")
        price = request.POST.get("price")
        horsepower = request.POST.get("horsepower")
        description = request.POST.get("description")
        inputs = {
            "mileage": mileage,
            "price": price,
            "horsepower": horsepower,
            "description": description,
        }

        df = get_cached_dataframe()
        bert_results = get_bert_recommendations(df, inputs["description"], 5)

        return render(
            request,
            "recommendations.html",
            context={"inputs": inputs, "bert_results": bert_results},
        )

    return render(request, "filters.html")
