from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView as AuthLoginView, LogoutView as AuthLogoutView
from django.contrib.auth import authenticate, login
from account.forms import RegisterForm
from App_retetecuverdeturi.models import Order, Product
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from account.models import WishlistItem




#in acest fisier vom crea clase, metode sau functii cu ajutorul carora putem gestiona cererile HTTP ptimite de la utilizator


class LoginView(AuthLoginView):          #aceasta clasa moesteneste clasa AuthLoginView() si ne ofera functionalitatea de login,
    template_name = 'account/login.html' #aceasta clasa ne ofera sablonul personalizat pt pagina de login a aplicatiei


class LogoutView(AuthLogoutView):         #aceasta clasa moesteneste clasa AuthLogoutView() si ne ofera functionalitatea de logout
    template_name = 'account/logout.html' #aceasta clasa ne ofera sablonul personalizat pt pagina de logout a aplicatiei


def register(request):          # acesata functie gestioneaza cererile GET - ne afiseaza formularul si POST - ne salveaza noul utilizator in baza de date
    if request.method == "GET":
        form = RegisterForm
        context = {
            "form": form
        }
        return render(request, 'account/register.html', context=context)
    elif request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")

            user = authenticate(username=username, password=password)

            if user:
                login(request, user)

            return redirect('account:login')




def my_account(request):
    # Verifică dacă utilizatorul este autentificat
    if request.user.is_authenticated:
        # Preia istoricul comenzilor utilizatorului din baza de date
        orders = Order.objects.filter(user=request.user)

        # Renderează pagina HTML my_account.html și trimite istoricul comenzilor ca context
        return render(request, 'account/my_account.html', {'orders': orders})
    else:
        # Dacă utilizatorul nu este autentificat, redirecționează-l către pagina de autentificare
        return redirect('login')

@login_required
def wishlist_view(request):
    wishlist = WishlistItem.objects.all()
    context = {
        "w":wishlist
    }
    return render(request, "account/wishlist.html", context)

# def add_to_wishlist(request):
#     product_id = request.GET['id']
#     product = Product.objects.get(id=product_id)
#
#     context = []
#
#     wishlist_count = wishlist_model.objects.filter(product=product, user=request.user).count()
#     print(wishlist_count)
#
#     if wishlist_count > 0:
#         context ={
#             "bool":True
#         }
#
#     else:
#         new_wishlist = wishlist_model.objects.create(
#             product=product,
#             user=request.user
#         )
#     context = {
#         "bool":True
#     }
#     return JsonResponse(context)

def add_to_wishlist(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)

        wishlist_count = WishlistItem.objects.filter(product=product, user=request.user).count()

        if wishlist_count > 0:
            # Produsul este deja în lista de dorințe a utilizatorului
            return JsonResponse({'success': False, 'message': 'Produsul este deja în lista de dorințe'})
        else:
            # Adaugă produsul în lista de dorințe a utilizatorului

            new_wishlist = WishlistItem.objects.create(
                product=product,
                user=request.user
            )
            return JsonResponse({'success': True, 'message': 'Produsul a fost adăugat cu succes în lista de dorințe'})
    else:
        # Cererea nu este de tip POST
        return JsonResponse({'success': False, 'message': 'Cererea trebuie să fie de tip POST'})


