from django.shortcuts import render

def show_main(request):
    context = {
        "app_name": "KickoffKart",
        "your_name": "Juansao Fortunio",
        "your_class": "PBP Ganjil 2025/2026",
    }
    return render(request, "main.html", context)
