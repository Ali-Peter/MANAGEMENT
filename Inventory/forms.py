from django.forms import ModelForm
from .models import Inventory

class AddInventoryForm(ModelForm):
    class Meta:
        model = Inventory
        fields = ['name', 'cost_per_item', 'quantity_in_stock', 'quantity_sold']


class UpdateInventoryForm(ModelForm):
    class Meta:
        model = Inventory
        fields = ['name', 'cost_per_item', 'quantity_in_stock', 'quantity_sold']
        

class AdditionInventoryForm(ModelForm):
    class Meta:
        model = Inventory
        fields = ['name', 'quantity_in_stock']

class SalesInventoryForm(ModelForm):
    class Meta:
        model = Inventory
        fields = ['name', 'quantity_sold', 'cost_per_item']


class AddSales(ModelForm):
    class Meta:
        model = Inventory
        fields = ['name', 'quantity_sold','quantity_in_stock']