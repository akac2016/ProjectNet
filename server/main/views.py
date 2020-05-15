from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from main.models import Node
from main.forms import NewNode
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.core import serializers
from django.views.generic import View
from django.http import HttpResponse
from django.conf import settings
from django.middleware.csrf import get_token
import os
import logging

#Homepage View
def home(request):
        if request.user.is_authenticated:
            return render(request,'../../client/build/index.html')
        else:
            return redirect('signup')


#NewNode Form
def node_form(request):
    form = NewNode()
    return render(request, 'main/form.html', {'form':form})


#Ajax
def form_ajax(request):
    if request.method == 'POST':
        form = NewNode(request.POST, request.FILES)
        if form.is_valid():
            interview = form.cleaned_data.get('interview')
            image = form.cleaned_data.get('image')
            name = form.cleaned_data.get('name')
            obj = Node.objects.create(
                interview = interview, 
                image = image, 
                name = name
            )
            obj.save()
        else:
            return JsonResponse({'responseText': "Invalid Form"})
        return JsonResponse({'responseText':False})
    else:
        return JsonResponse({'responseText': "Bad Request"})

def csrf(request):
    return JsonResponse({'csrfToken': get_token(request)})

def get_node_image(request, pk):
    if (request.method == "GET"):
        return JsonResponse({"Hmmmmmm": "Hmmmmm"})
        # return JsonResponse({imageU})

#Nodes Page
def nodes_ajax(request):
    if request.method == "GET":
        obj = Node.objects.all()

        data = serializers.serialize("json", obj, fields=("name","interview","image"))
        return JsonResponse(data,safe=False)

class FrontendAppView(View):
    """
    Serves the compiled frontend entry point (only works if you have run `yarn
    run build`).
    """

    def get(self, request):
        logger = logging.getLogger(__name__)
        logger.info("HERE")
        try:
            with open(os.path.join(settings.REACT_APP_DIR, 'build', 'index.html')) as f:
                return HttpResponse(f.read())
        except FileNotFoundError:
            logging.exception('Production build of app not found')
            return HttpResponse(
                """
                This URL is only used when you have built the production
                version of the app. Visit http://localhost:3000/ instead, or
                run `yarn run build` to test the production version.
                """,
                status=501,
            )