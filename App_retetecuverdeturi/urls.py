from django.urls import path
from App_retetecuverdeturi.views import home_view, contact, ProductListView, product_detail, upload_product, add_to_cart, delete_product, shopping_cart, finalizeaza_comanda, checkout, confirm_order, update_quantity, search_view
#in cadrul acestui fisier vom defini lista de app-pointuri a aplicatiei

app_name = "App_retetecuverdeturi"


urlpatterns = [
    path('', home_view, name='home'),
    path('upload_product/', upload_product, name='upload_product'),
    path('products/', ProductListView.as_view(), name='products'),
    path('product/<int:product_id>/', product_detail, name='product'),
    #path('category/<slug:category_id>', CategoryView.as_view(), name='category'),
    path('cart/', shopping_cart, name='cart'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('delete_product/<int:product_id>/', delete_product, name='delete_product'),
    path('update_quantity/<int:product_id>/<str:action>/', update_quantity, name='update_quantity'),
    path('checkout/', checkout, name='checkout'),
    path('finalizeaza_comanda/', finalizeaza_comanda, name='finalizeaza_comanda'),
    path('confirm_order/', confirm_order, name='confirm_order'),
    path('contact/', contact, name='contact'),
    path('search/', search_view, name='search'),
]