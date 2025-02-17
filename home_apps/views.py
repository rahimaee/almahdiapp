from django.shortcuts import render


# Create your views here.


def home(request):
    return render(request, 'home_apps/home.html')


def header_partial_view(request, *args, **kwargs):
    return render(request, 'shared/_Header.html')


def header_references_partial_view(request, *args, **kwargs):
    return render(request, 'shared/_HeaderReferences.html')


def navbar_partial_view(request, *args, **kwargs):
    user = request.user.is_staff == True
    return render(request, 'shared/_Navbar.html')


def footer_partial_view(request, *args, **kwargs):
    return render(request, 'shared/_Footer.html')


def footer_references_partial_view(request, *args, **kwargs):
    return render(request, 'shared/_FooterReferences.html')
