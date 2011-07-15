from django.shortcuts import render_to_response
import datetime
from django.http import HttpResponse


def hola(peticion):
    ahora = datetime.datetime.now()
    html = "<html> <body> Ahora es %s. </body> </html>" % ahora
    #~ t = get_template('horafecha_actual.html')
    #~ html = t.render(Context({'fechaActual': ahora}))
    return HttpResponse(html)
    #~ return render_to_response('horafecha_actual.html', {'fechaActual': ahora})

def home(peticion):
    ahora = datetime.datetime.now()
    #~ html = "<html> <body> Ahora es %s. </body> </html>" % ahora
    #~ t = get_template('horafecha_actual.html')
    #~ html = t.render(Context({'fechaActual': ahora}))
    #~ return HttpResponse(html)
    return render_to_response('home.html', {'ya': ahora})

def dashboard(request):
    return render_to_response('dashboard.html')
