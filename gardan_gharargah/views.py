from django.shortcuts import render

def gardan_gharargah_dashboard(request):
    context = {}
    return render(request,'main/gardan_gharargah_dashboard.html',context)

def gurd_dashboard(request):
    context = {}
    return render(request,'gurd/grud_dashbaord.html',context)
