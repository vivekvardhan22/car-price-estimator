from django.shortcuts import render
from .predictor import predict  # import your function

def home(request):
    if request.method == "POST":
        company = request.POST.get("company")
        variant = request.POST.get("variant")
        seller_auth = int(request.POST.get("seller_auth"))
        odometer = int(request.POST.get("odometer"))
        year = int(request.POST.get("year"))

        min_price, max_price = predict(company, variant, seller_auth, odometer, year)

        return render(request, "result.html", {
            "company": company,
            "variant": variant,
            "min_price": min_price,
            "max_price": max_price,
        })
    return render(request, "home.html")

def analysis(request):
    return render(request, "analysis.html")

