from django.urls import path
from .views import (inventory_list, 
                    per_product_view, 
                    add_product, 
                    delete_inventory, 
                    update_inventory,
                    addition_inventory,
                    dashboard,
                    sales_inventory,
                    search_inventory,
                    fetch_inventory,
                    )   

urlpatterns = [
    path("", inventory_list, name="inventory_list"),
    path("per_product/<int:pk>", per_product_view, name="per_product"),
    path("add_inventory/", add_product, name="add_inventory"),
    path("delete/<int:pk>", delete_inventory, name="delete_inventory"),
    path("update/<int:pk>", update_inventory, name="update_inventory"),
    path("addition/<int:pk>", addition_inventory, name="addition_inventory"),
    path("dashboard/", dashboard, name="dashboard"),
    path("sales/<int:pk>", sales_inventory, name="sales"),
    path("search/", search_inventory, name="search"),
    path("fetch/", fetch_inventory, name="fetch"),
]
