from django.shortcuts import render

def show_main(request):
    context = {
        'npm': '2406365313',   
        'name': 'Herdayani Elision Sitio', 
        'class': 'KKI',     
    }
    return render(request, "main.html", context)
