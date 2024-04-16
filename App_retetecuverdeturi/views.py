from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse
from App_retetecuverdeturi.models import Product, Order, OrderItem
from django.views.generic import ListView
from django.db.models import F
from .forms import OrderItemForm, ProductForm, MesajForm




def home_view(request):
    return render(request, 'App_retetecuverdeturi/home.html')


class ProductListView(ListView): # clasa cu ajutorul caruia afisam o lista de obiecte
    model = Product
    template_name = 'App_retetecuverdeturi/products.html'

    def get_context_data(self, **kwargs): # metoda cu ajutorul caruia furnizam date suplimentare  catre sablon, pagina products.html
        context = super().get_context_data(**kwargs)
        context['products'] = context['object_list']
        return context


def product_detail(request, product_id): # functia care ne afiseaza informatii despre produs tinand cond de un id
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'App_retetecuverdeturi/product.html', {'product': product})


def upload_product(request): # functie cu ajutorul caruia putem incarca produse in aplicatia noastra folosind un sablon, pagina upload_product.html
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            return redirect('/')
    else:
        form = ProductForm()

    return render(request, 'App_retetecuverdeturi/upload_product.html', {'form': form})

@login_required
def add_to_cart(request, product_id): # functie cu ajutorul cauia putem adauga produse in cosul de cumparaturi
    try:
        # Obtine produsul pe baza id-ului
        product = get_object_or_404(Product, id=product_id)

        # Verificam daca exista deja un OrderItem pentru acest produs și utilizator
        order_item, created = OrderItem.objects.get_or_create(
            user=request.user,
            ordered=False,
            product=product
        )

        if created:
            messages.success(request, f"{product.name} a fost adăugat în coș.")
        else:
            # Daca OrderItem exista deja, vom actualiza cantitatea
            order_item.quantity = F('quantity') + 1
            order_item.save()
            messages.info(request, f"Cantitatea pentru {product.name} a fost actualizată în coș.")

        # Redirectionam catre pagina de shopping cart
        return redirect(reverse('App_retetecuverdeturi:cart'))
    except Exception as e:
        # Putem gestiona eroarea si returnam un mesaj
        messages.error(request, f"Eroare la adăugarea produsului în coș: {str(e)}")
        return redirect('/')


@login_required
def create_order(request): # functie cu ajutorul cauia putem crea o comanda
    form = OrderItemForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            product_id = form.cleaned_data['product'].id
            quantity = form.cleaned_data['quantity']

            order_item, created = OrderItem.objects.get_or_create(
                user=request.user,
                ordered=False,
                product_id=product_id,
            )
            order_item.quantity += quantity
            order_item.save()

            return JsonResponse({'status': 'success'})

    order_items = OrderItem.objects.filter(user=request.user, ordered=False)
    order_total = sum(item.get_final_price() for item in order_items)

    context = {
        'form': form,
        'order_items': order_items,
        'order_total': order_total,
    }
    return render(request, 'App_retetecuverdeturi/cart.html', context)


def checkout(request):
    order_items = OrderItem.objects.filter(user=request.user, ordered=False)
    order_total = sum(item.get_final_price() for item in order_items)
    return render(request, 'App_retetecuverdeturi/checkout.html', {'order_items': order_items, 'total_cumparaturi': order_total})



def finalizeaza_comanda(request):
    if request.method == 'POST':

        order_items = OrderItem.objects.filter(user=request.user, ordered=False)

        new_order = Order.objects.create(user=request.user, ordered=True)
        new_order.items.set(order_items)

        order_items.update(ordered=True)

        messages.success(request, 'Comanda a fost plasată cu succes!')
        return redirect(reverse('App_retetecuverdeturi:confirm_order'))

    return redirect(reverse('App_retetecuverdeturi:home'))


def shopping_cart(request):
    order_items = OrderItem.objects.filter(user=request.user, ordered=False)

    order_total = sum(item.get_final_price() for item in order_items)

    context = {
        'order_items': order_items,
        'total_cumparaturi': order_total,
    }

    return render(request, 'App_retetecuverdeturi/cart.html', context)


@login_required
def delete_product(request, product_id):
    if request.method == 'DELETE':
        try:
            order_item = OrderItem.objects.get(user=request.user, product_id=product_id, ordered=False)
            order_item.delete()
            return JsonResponse({'status': 'success'})
        except OrderItem.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Produsul nu a fost găsit în coș'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Metoda solicitată nu este permisă'})


@login_required
def update_quantity(request, product_id, action):
    if request.method == 'POST':
        # Verifică dacă utilizatorul este autentificat sau nu, dacă este necesar
        if request.user.is_authenticated:
            # Obține obiectele OrderItem din coșul de cumpărături care corespund condițiilor de interogare
            order_items = OrderItem.objects.filter(product_id=product_id, user=request.user, ordered=False)

            # Verifică dacă există cel puțin un obiect
            if order_items.exists():
                # Iterează prin lista de obiecte și aplică acțiunea dorită pentru fiecare
                for order_item in order_items:
                    if action == 'increase':
                        order_item.quantity += 1
                    elif action == 'decrease':
                        order_item.quantity -= 1
                        if order_item.quantity <= 0:
                            # Dacă cantitatea devine 0 sau mai mică, elimină produsul din coș
                            order_item.delete()
                    order_item.save()

                return JsonResponse({'status': 'success', 'new_quantity': order_items[
                    0].quantity})  # Poți returna noua cantitate a primului obiect din listă, deoarece toate obiectele au aceeași cantitate
            else:
                return JsonResponse(
                    {'status': 'error', 'message': 'Nu s-au găsit produse în coș pentru utilizatorul curent'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Utilizatorul nu este autentificat'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Metoda de solicitare nu este acceptată'})


def contact(request):
    if request.method == 'POST':
        form = MesajForm(request.POST)
        if form.is_valid():
            mesaj_nou = form.save(commit=False)
            mesaj_nou.status = 'necitit'
            mesaj_nou.save()
            return redirect('/')  # Redirectionam la pagina de home
    else:
        form = MesajForm()

    return render(request, 'App_retetecuverdeturi/contact.html', {'form': form})


from django.shortcuts import render

def confirm_order(request):
    return render(request, 'App_retetecuverdeturi/confirm_order.html')



def search_view(request):
    query = request.GET.get('query')
    if query:
        results = Product.objects.filter(name__icontains=query)
    else:
        results = None
    return render(request, 'App_retetecuverdeturi/search.html', {'query': query, 'results': results})

#
# class CategoryView(View):
#     def get(self, request, ):
#         categories = Category.objects.all()
#         return render(request, "App_Retetecuverdeturi/category.html", {'categories': categories})
#
