from django.shortcuts import render, redirect
import requests


# Create your views here.
def device_API(request):
    response=requests.get('https://nms.matrik.co.id/core/api/v0/devices', headers={'X-Auth-Token':'REDACTED_NMS_API_TOKEN'}).json()
    
    context = {
        #'api_hostname' : devices,
        'api': response['devices'],
        
    }
    return render(request, 'api.html', context)

