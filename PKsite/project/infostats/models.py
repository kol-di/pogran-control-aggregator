# # from django.db import models
# from djongo import models
#
#
# class Tag(models.Model):
#
#     class Meta:
#         abstract = True
#
#
# class Location(models.Model):
#     _id = models.ObjectIdField()
#     date = models.DateTimeField(
#         null=True
#     )
#     refused = models.BooleanField()
#     tags = models.EmbeddedField(
#         model_container=Tag,
#         null=True)
#
#     # class Meta:
#     #     db_table = 'locations'
