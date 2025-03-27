from django.shortcuts import render

def accueil(request):
    return render(request, 'accueil.html')  # Rend le template accueil.html