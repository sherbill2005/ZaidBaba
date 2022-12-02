from django.shortcuts import render, redirect
def i(request):
    return render(request, "shop/home.html")