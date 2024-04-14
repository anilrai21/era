from typing import Dict

from django.db.models import QuerySet

from .models import Category


def shop_global_variables(request) -> Dict:
    # Create fixed data structures to pass to template
    # data could equally come from database queries
    # web services or social APIs
    categories: QuerySet = Category.objects.active()
    return {
        "ITEM_CATEGORIES": categories,
    }
