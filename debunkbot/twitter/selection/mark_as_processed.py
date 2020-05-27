from django.db.models import QuerySet


def mark_as_processed(queryset: QuerySet) -> None:
    """Marks a queryset as processed.
    """
    for item in queryset:
        item.processed = True
        item.save()
