from django.db import models


class GSheetClaimsDatabaseManager(models.query.QuerySet):
    def delete(self, *args, **kwargs):
        for obj in self:
            obj.deleted = True
            obj.save()
