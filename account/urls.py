from django.urls import path
from .views import LoginView, register, my_account, wishlist_view, add_to_wishlist
# in acest fisier definim rutele specifice acestei functionalitati

app_name = 'account' # in cadrul variabilei app_name salvam numele aplicatiei unde am definit url-urile specifice acesti functionaliati
                     # ne vom folosi de acest nume cand vom  gestiona url-urile in sabloanele(fisierele html)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', register, name='register'),
    path('my_account/', my_account, name='my_account'),
    path('wishlist/', wishlist_view, name='wishlist'),
    path('add_to_wishlist/', add_to_wishlist, name='add_to_wishlist'),

    # aici vom adauga si alte rute specifice acestei functionalitati
]