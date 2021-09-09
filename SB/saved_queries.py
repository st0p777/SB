from django import template
from django.db.models import Q

from ..models import SavedSearch


register = template.Library()


@register.filter
def saved_queries(user):
    try:
        filters = Q(shared__exact=True)
        if user.is_authenticated:
            filters |= Q(user=user)
        user_saved_queries = SavedSearch.objects.filter(filters)
        return user_saved_queries
    except Exception as e:
        import sys
        print("'saved_queries' template tag (django-helpdesk) crashed with following error:",
              file=sys.stderr)
        print(e, file=sys.stderr)
        return ''
