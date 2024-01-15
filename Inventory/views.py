from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from .models import Inventory
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import (AddInventoryForm, 
                    UpdateInventoryForm, 
                    AdditionInventoryForm,
                    SalesInventoryForm, AddSales)

from django.contrib import messages
from django_pandas.io import read_frame
import plotly
import plotly.express as px
import json




# Create your views here.
def front_page(request):
    context = {
        "front": """One day, while i was still very young the lord said to me,
        i'm with you.Are you looking for a practical strategy to package your 
        gift so that it will deliver the caliber you wish to guarantee for your 
        current recipient or customers? You can find everything you need in our collection 
        of all-in-one luxury gift boxes, which are finely matt laminated and colored both 
        inside and out. To suit your needs and brand, we provide a wide variety of colors. 
        
        To discuss constructing a box that is specific to your needs, get in touch with us 
        right now! Each industry relies heavily on packaging.Each industry provides prizes 
        to its winners, which can be Souvenirs. These Souvenirs must reflect the industry's 
        philosophy. Custom souvenir packaging is the most effective way to achieve this goal. 
        
        Such packaging must be long-lasting and match the quality of the Souvenir. We can make 
        Souvenir packaging to your specifications."""
        }
    return render(request, 'inventory/front_page.html', context=context)


@login_required
def inventory_list(request):
    inventory = Inventory.objects.all()
    context = {
        "title": "Inventory_List",
        "inventory": inventory
    }
    return render(request, "inventory/inventory_list.html", context=context)


@login_required
def per_product_view(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    context = {
        'inventory': inventory
    }
    return render(request, "inventory/per_product.html", context=context)


@login_required
def add_product(request):
    if request.method == "POST":
        add_form = AddInventoryForm(data=request.POST)
        if add_form.is_valid():
            new_inventory = add_form.save(commit=False)
            new_inventory.sales = float(add_form.data['cost_per_item']) * float(add_form.data['quantity_sold'])
            new_inventory.save()
            messages.success(request, "Successfully Added Product")
            return redirect("/login/inventory/")
    else:
        add_form = AddInventoryForm()
    return render(request, "inventory/inventory_add.html", {"form": add_form})


@login_required
def delete_inventory(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    inventory.delete()
    messages.success(request, "Record Deleted")
    return redirect("/login/inventory/")


@login_required
def update_inventory(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    if request.method == "POST":
        updateForm = UpdateInventoryForm(data=request.POST)
        if updateForm.is_valid():
            inventory.name = updateForm.data['name']
            inventory.quantity_in_stock = updateForm.data['quantity_in_stock']
            inventory.quantity_sold = updateForm.data['quantity_sold']
            inventory.cost_per_item = updateForm.data['cost_per_item']
            inventory.sales = float(inventory.cost_per_item) * float(inventory.quantity_sold)
            inventory.save()
            messages.success(request, "Successfully Updated")
            return redirect(f"/inventory/per_product/{pk}")
    else:
        updateForm = UpdateInventoryForm(instance=inventory)
    return render(request, "inventory/inventory_update.html", {"form": updateForm})

@login_required
def dashboard(request):
    inventories = Inventory.objects.all()

    df = read_frame(inventories)

    sales_graph = df.groupby(by="last_sales_date", as_index=False, sort=False)['sales'].sum()
    sales_graph = px.line(sales_graph, x=sales_graph.last_sales_date, y=sales_graph.sales, title="Sales Trend")
    sales_graph = json.dumps(sales_graph, cls=plotly.utils.PlotlyJSONEncoder)

    best_performing_product_df = df.groupby(by="name").sum().sort_values(by="quantity_sold")
    best_performing_product = px.bar(best_performing_product_df, x=best_performing_product_df.index, y=best_performing_product_df.quantity_sold, title="Best Performing Product")
    best_performing_product = json.dumps(best_performing_product, cls=plotly.utils.PlotlyJSONEncoder)

    most_product_in_stock_df = df.groupby(by="name").sum().sort_values(by="quantity_in_stock")
    most_product_in_stock = px.pie(most_product_in_stock_df, names = most_product_in_stock_df.index, values=most_product_in_stock_df.quantity_in_stock, title = "Most Product In Stock")
    most_product_in_stock = json.dumps(most_product_in_stock, cls=plotly.utils.PlotlyJSONEncoder)

    context ={
        "sales_graph": sales_graph,
        "best_performing_product": best_performing_product,
        "most_product_in_stock": most_product_in_stock
    }
    return render(request, "inventory/dashboard.html", context=context)

@login_required
def addition_inventory(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    if request.method == "POST":
        updateForm = AdditionInventoryForm(data=request.POST)
        if updateForm.is_valid():
            inventory.name = updateForm.data['name']
            inventory.quantity_in_stock = inventory.quantity_in_stock + float(updateForm.data['quantity_in_stock'])
            inventory.quantity_sold = inventory.quantity_sold
            inventory.cost_per_item = inventory.cost_per_item
            inventory.sales = inventory.sales
            inventory.save()
            messages.success(request, "New Stock Successfully Added")
            return redirect(f"/inventory/per_product/{pk}")
    else:
        updateForm = AdditionInventoryForm(instance=inventory)
    return render(request, "inventory/addition.html", {"form": updateForm})

@login_required
def sales_inventory(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    if request.method == 'POST':
        salesForm = SalesInventoryForm(data=request.POST)
        if salesForm.is_valid():
            inventory.name = salesForm.data['name']
            inventory.quantity_in_stock = inventory.quantity_in_stock - int(salesForm.data['quantity_sold'])
            inventory.quantity_sold = salesForm.data['quantity_sold']
            inventory.cost_per_item = inventory.cost_per_item
            inventory.sales = inventory.cost_per_item * int(inventory.quantity_sold)
            inventory.save()
            return redirect(f"/login/inventory/per_product/{pk}")
    else:
        salesForm = SalesInventoryForm(instance=inventory)
    return render(request, "inventory/sales.html", {"form": salesForm})

@login_required
def search_inventory(request):
    if request.method == 'POST':
        searched = request.POST['search']
        products = Inventory.objects.filter(name__contains=searched)
        context = {
            'products': products
        }
        return render(request, 'inventory/search.html', context=context)
    else:
        return render(request, 'inventory/search.html')

@login_required   
def fetch_inventory(request):
    if request.method == 'POST':
        load_input_value = request.POST['loaddata']
        model = Inventory.objects.filter(name__contains=load_input_value)
        if request.method == 'GET':
            form = AddSales(request.GET, instance=model)
            if form.is_valid():
                model.name = form.data['name']
                model.quantity_in_stock = model.quantity_in_stock - int(form.data['quantity_sold'])
                model.quantity_sold = form.data['quantity_sold']
                model.cost_per_item = model.cost_per_item
                model.sales = model.cost_per_item * int(model.quantity_sold)
                model.save()
                return redirect(request, '/inventory/')

        else:
            form = AddSales(instance=model)
        return render(request, 'inventory/search.html', {"form": AddSales})