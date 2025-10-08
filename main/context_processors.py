# main/context_processors.py
from .models import Product

def nav_categories(request):
    if request.user.is_authenticated:
        qs = Product.objects.filter(user=request.user)
    else:
        qs = Product.objects.none()

    categories = (
        qs.order_by()
          .values_list("category", flat=True)
          .distinct()
    )
    return {"nav_categories": list(categories)}
