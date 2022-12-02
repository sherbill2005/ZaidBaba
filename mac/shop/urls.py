from django.urls import path
from . import views
from django.contrib.auth import views as auth_view
from .forms import LoginForm

urlpatterns = [
    # Urls for costumer and users
    path("", views.index, name="ShopHome"),
    path("about/", views.about, name="AboutUs"),
    path("contact/", views.contact, name="ContactUs"),
    path("registration/", views.CustomerRegister.as_view(), name="customerregistration"),
    path("accounts/login/", auth_view.LoginView.as_view(template_name='shop/login.html', authentication_form=LoginForm), name="login"),
    path('logout/', auth_view.LogoutView.as_view(next_page='login'), name="logout"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("search/", views.search, name="search"),
    path("address/", views.address, name="address"),

    # Urls for products and cart
    path("products/<int:myid>", views.productView, name="productView"),
    path("checkout/", views.checkout, name="checkout"),
    path("order/", views.orders, name="orders"),
    path("payment_done/", views.payment_done, name="payment"),
    path("cart/", views.carts),
    path("Showcarts/", views.showcart, name='Showcarts'),
    path('addCart/', views.plusCart, name="plusCart"),
    path("minusCart/", views.minCart),
    path("removeCart/", views.revCart)
    ]