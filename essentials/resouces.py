from import_export import resources
from .models import Variant

class VariantResource(resources.ModelResource):
    class Meta:
        model = Variant