from django.db.models import QuerySet


def mark_as_processed(queryset: QuerySet) -> None:
    for item in queryset:
        item.processed = True
        item.save()
