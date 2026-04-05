from datetime import date, datetime
from email import message
from email.policy import default
from multiprocessing import context
from re import A
from unittest import result
from webbrowser import get
from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
from paramiko.client import AutoAddPolicy
from masterdata.models import MasterData
from .models import Log, BackupConfig
from .forms import PushForm, PushConfig, UploadBacukp
from .filters import OrderFilter, LogFilter
import paramiko
import time
import os
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='/login')
def index(request):
    all_device = MasterData.objects.all()
    myFilter = OrderFilter(request.POST, queryset=all_device)
    all_device = myFilter.qs
    


    context = {
        'title':'Lazy Network Automation',
        'head_page': 'Automation',
        'page': 'Master Data',
        'all_device': all_device,
        'myFilter': myFilter,

    }
    
    return render(request, 'automation.html', context)

@login_required(login_url='/login')
def history(request):
    logs = Log.objects.all()
    myFilter = LogFilter(request.POST, queryset=logs)
    logs = myFilter.qs

    context = {
        'title':'Lazy Network Automation',
        'head_page': 'Automation',
        'page': 'History',
        'logs': logs,
        'myFilter': myFilter,
    }
    return render(request, 'history.html', context)


@login_required(login_url='/login')
def push_config(request):
    if request.method == "POST":

        yangdipush = request.POST.getlist('pushgw')
        confignya = request.POST.getlist('confignya')

        for x in yangdipush:
            try:

                mangsa = get_object_or_404(MasterData, pk=x)
                ssh_client = paramiko.SSHClient()
                ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh_client.connect(hostname=mangsa.ip_address, username=mangsa.ssh_user, password=mangsa.ssh_pwd, port=mangsa.ssh_port, allow_agent=False, look_for_keys=False, timeout=5)

                vendorna = str(mangsa.device_vendor)
                
                
                if vendorna == 'Ransnet':
                    conn = ssh_client.invoke_shell()
                    conn.send("enable" + "\n")
                    time.sleep(1)
                    conn.send("REDACTED_ENABLE_PASSWORD" + "\n")
                    time.sleep(1)
                    
                    for cmd in confignya:
                        conn.send(cmd + "\n")
                        time.sleep(1)
                        output = conn.recv(65535)
                        print(output.decode())
                        
                    ssh_client.close
                    
                    print("ASIKK MASUKK!!")
                    log = Log(target=mangsa.ip_address, action="Configure", status="Success", time=datetime.now(), messages="No Error")
                    log.save()
                    
                
                else:
                    print("gk tau brand apa")
                
                log = Log(target=mangsa.ip_address, action="Configure", status="Error", time=datetime.now(), messages="Unrecognized Vendor")
                log.save()

                
            except Exception as e:
                print("Errornya adalah : " + str(e))
                log = Log(target=mangsa.ip_address, action="Configure", status="Error", time=datetime.now(), messages=e)
                log.save()
                
        return redirect('/automation/push_config')

    else:
        all_device = MasterData.objects.all()
        myFilter = OrderFilter(request.GET, queryset=all_device)
        print(myFilter)
        all_device = myFilter.qs
        
        context = {
            
            'title':'Lazy Network Automation',
            'head_page': 'Automation',
            'page': 'Push Config',
            'all_device': all_device,
            'myFilter': myFilter,

        }
                
        return render(request, 'configuration.html', context)




@login_required(login_url='/login')
def verify_config(request):
    if request.method == "POST":
        result = []
        yangdipush = request.POST.getlist('pushgw')
        confignya = request.POST.getlist('confignya')
        print(yangdipush)

        for x in yangdipush:
            try:

                mangsa = get_object_or_404(MasterData, pk=x)
                print(mangsa)
                ssh_client = paramiko.SSHClient()
                ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh_client.connect(hostname=mangsa.ip_address, username=mangsa.ssh_user, password=mangsa.ssh_pwd, port=mangsa.ssh_port, allow_agent=False, look_for_keys=False, timeout=5)

                vendorna = str(mangsa.device_vendor).strip().split(" - ")[-1]
                print(vendorna)
                
                if vendorna == 'Ransnet':
                    conn = ssh_client.invoke_shell()
                    conn.send("enable" + "\n")
                    time.sleep(1)
                    conn.send("REDACTED_ENABLE_PASSWORD" + "\n")
                    time.sleep(1)
                    
                    for cmd in confignya:
                        conn.send(cmd + "\n")
                        time.sleep(1)
                        output = conn.recv(65535)
                        result.append(output.decode())
                        print(output.decode())
                        
                    ssh_client.close
                    
                    print("ASIKK MASUKK!!")
                    log = Log(target=mangsa.ip_address, action="Verify Config", status="Success", time=datetime.now(), messages="No Error")
                    log.save()    
                
                else:
                    print("gk tau brand apa")
                
                log = Log(target=mangsa.ip_address, action="Verify Config", status="Error", time=datetime.now(), messages="Unrecognized Vendor")
                log.save()

                
            except Exception as e:
                print("Errornya adalah : " + str(e))
                log = Log(target=mangsa.ip_address, action="Verify Config", status="Error", time=datetime.now(), messages=e)
                log.save()
        
        result = '\n'.join(result)
        return render(request, 'verify_configuration.html', {'result':result})        
        

    else:
        all_device = MasterData.objects.all()
        myFilter = OrderFilter(request.GET, queryset=all_device)
        print(myFilter)
        all_device = myFilter.qs
        
        context = {
            
            'title':'Lazy Network Automation',
            'head_page': 'Automation',
            'page': 'Verify Config',
            'all_device': all_device,
            'myFilter': myFilter,

        }
                
        return render(request, 'configuration.html', context)


@login_required(login_url='/login')
def backup_config(request):
    if request.method == "POST":
        result = []
        yangdipush = request.POST.getlist('pushgw')
        confignya = request.POST.getlist('confignya')

        for x in yangdipush:
            try:

                mangsa = get_object_or_404(MasterData, pk=x)
                ssh_client = paramiko.SSHClient()
                ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh_client.connect(hostname=mangsa.ip_address, username=mangsa.ssh_user, password=mangsa.ssh_pwd, port=mangsa.ssh_port, allow_agent=False, look_for_keys=False, timeout=5)

                vendorna = str(mangsa.device_vendor)
                now = datetime.now()
                dt_string = now.strftime("%d-%m-%Y_%H-%M")

                if vendorna == 'ransnet':
                    conn = ssh_client.invoke_shell()
                    conn.send("enable" + "\n")
                    time.sleep(1)
                    conn.send(mangsa.enab_pwd + "\n")
                    time.sleep(1)
                    
                    for cmd in confignya:
                        conn.send(cmd + "\n")
                        time.sleep(1)
                        output = conn.recv(65535)
                        odc = output.decode()
                        result.append(output.decode())
                        print(output.decode())
                        saveoutput = open("media/backup_config/backup-" + mangsa.ip_address + "_" + str(dt_string)+ ".txt", "w")
                        saveoutput.write(odc)
                        saveoutput.close

                        
                        
                    ssh_client.close
                    
                    print("ASIKK MASUKK!!")
                    
                
                else:
                    print("gk tau brand apa")
                
                log = Log(target=mangsa.ip_address, action="Backup Config", status="Success", time=datetime.now(), messages="No Error")
                log.save()
                filename = "backup_config/"+"backup-"+mangsa.ip_address+"_"+str(dt_string)+ ".txt"
                bu_config = BackupConfig(target=mangsa.ip_address, b_file=filename, status="Success", time=datetime.now(), messages="No Error")
                bu_config.save()

                
            except Exception as e:
                print("Errornya adalah : " + str(e))
                #log = Log(target=mangsa.ip_address, action="Verify Config", status="Error", time=datetime.now(), messages=e)
                #log.save()
        
        result = '\n'.join(result)
        return render(request, 'verify_configuration.html', {'result':result})        
        

    else:
        all_device = MasterData.objects.all()
        myFilter = OrderFilter(request.GET, queryset=all_device)
        print(myFilter)
        all_device = myFilter.qs
        
        context = {
            
            'title':'Lazy Network Automation',
            'head_page': 'Automation',
            'page': 'Backup Config',
            'all_device': all_device,
            'myFilter': myFilter,

        }
                
        return render(request, 'configuration.html', context)

@login_required(login_url='/login')
def fb_list(request):
    fbl = BackupConfig.objects.all()
    context = {
        'title':'Lazy Network Automation',
        'head_page': 'Automation',
        'page': 'Backup Config Files',
        'fbl': fbl,

    }

    return render(request, 'backup_files.html', context)
    


