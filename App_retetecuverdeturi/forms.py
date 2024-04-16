from django import forms
from App_retetecuverdeturi.models import Product, OrderItem, Mesaj




class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name',
                  'description',
                  'price',
                  'image',
                  'available_quantity',
                  'ingredients',
                  'weight_grams'
                  ]

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

    def __init__(self, *args, **kwargs):
        super(OrderItemForm, self).__init__(*args, **kwargs)
        self.fields['product'].widget.attrs['class'] = 'form-control'
        self.fields['quantity'].widget.attrs['class'] = 'form-control'


class MesajForm(forms.ModelForm):
    class Meta:
        model = Mesaj
        fields = ['nume', 'prenume', 'email', 'phone', 'mesaj']