from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView

from .forms import OrderCreateForm, OrderItemFormSet
from .models import Order
from .services import OrderService


class OrderListView(ListView):
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'
    ordering = ['-created_at']


class OrderDetailView(DetailView):
    model = Order
    template_name = 'orders/order_details.html'
    context_object_name = 'order'


class OrderCreateView(View):
    def get(self, request):
        form = OrderCreateForm()
        formset = OrderItemFormSet()
        return render(request, 'orders/order_form.html',
                      {'form': form, 'formset': formset})

    def post(self, request):
        form = OrderCreateForm(request.POST)
        formset = OrderItemFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            order = form.save(commit=False)
            order.status = 'confirmed'
            order.save()

            formset.instance = order

            items = formset.save(commit=False)
            for item in items:
                if item.product:
                    item.price = item.product.price
                item.save()

            service = OrderService(order)
            service.apply_promos()

            return redirect('orders:order_detail', pk=order.pk)

        return render(request, 'orders/order_form.html',
                      {'form': form, 'formset': formset})
