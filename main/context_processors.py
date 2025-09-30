from django.contrib.auth.models import AnonymousUser
from .models import Product

def nav_categories(request):
    """
    Return distinct categories for the authenticated user's products.
    Empty list for anonymous users.
    """
    user = getattr(request, "user", AnonymousUser())
    if not getattr(user, "is_authenticated", False):
        return {"nav_categories": []}

    cats = (
        Product.objects
        .filter(user=user)
        .values_list("category", flat=True)
        .distinct()
        .order_by("category")
    )
    return {"nav_categories": list(cats)}