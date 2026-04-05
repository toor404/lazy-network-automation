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
import subprocess
import difflib
import platform
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
                    conn.send(mangsa.enab_pwd + "\n")
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
                    conn.send(mangsa.enab_pwd + "\n")
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


@login_required(login_url='/login')
def ping_tool(request):
    results = []
    all_device = MasterData.objects.all()
    myFilter = OrderFilter(request.GET, queryset=all_device)
    all_device = myFilter.qs

    if request.method == 'POST':
        targets = request.POST.getlist('pushgw')
        os_name = platform.system()
        for pk in targets:
            device = get_object_or_404(MasterData, pk=pk)
            try:
                if os_name == 'Windows':
                    cmd = ['ping', '-n', '4', '-w', '2000', device.ip_address]
                elif os_name == 'Darwin':
                    cmd = ['ping', '-c', '4', '-W', '2000', device.ip_address]
                else:  # Linux
                    cmd = ['ping', '-c', '4', '-W', '2', device.ip_address]
                proc = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
                output = proc.stdout or proc.stderr
                status = 'Success' if proc.returncode == 0 else 'Unreachable'
            except Exception as e:
                output = str(e)
                status = 'Error'
            results.append({'device': device, 'output': output, 'status': status})

        return render(request, 'ping.html', {
            'title': 'Lazy Network Automation',
            'head_page': 'Tools',
            'page': 'Ping',
            'results': results,
            'all_device': all_device,
            'myFilter': myFilter,
        })

    return render(request, 'ping.html', {
        'title': 'Lazy Network Automation',
        'head_page': 'Tools',
        'page': 'Ping',
        'all_device': all_device,
        'myFilter': myFilter,
    })


@login_required(login_url='/login')
def snmp_walk(request):
    result = ''
    all_device = MasterData.objects.all()

    if request.method == 'POST':
        pk = request.POST.get('device')
        oid = request.POST.get('oid', '1.3.6.1.2.1.1').strip() or '1.3.6.1.2.1.1'
        device = get_object_or_404(MasterData, pk=pk)
        snmp_ver = str(device.snmp_ver).strip().split(' - ')[-1]
        community = device.snmp_community or 'public'
        port = str(device.snmp_port or 161)

        if snmp_ver in ('v3', 'SNMPv3', 'snmpv3'):
            result = 'SNMPv3 not yet supported — use v1 or v2c.'
        else:
            version_flag = '2c' if '2' in snmp_ver else '1'
            os_name = platform.system()
            # Common snmpwalk paths per OS
            snmpwalk_candidates = ['snmpwalk']
            if os_name == 'Darwin':
                snmpwalk_candidates += [
                    '/opt/homebrew/bin/snmpwalk',
                    '/usr/local/bin/snmpwalk',
                ]
            elif os_name == 'Windows':
                snmpwalk_candidates += [
                    r'C:\usr\bin\snmpwalk.exe',
                    r'C:\net-snmp\bin\snmpwalk.exe',
                ]
            else:
                snmpwalk_candidates += ['/usr/bin/snmpwalk']

            snmpwalk_bin = None
            for candidate in snmpwalk_candidates:
                if os.path.isfile(candidate) or candidate == 'snmpwalk':
                    snmpwalk_bin = candidate
                    break

            try:
                proc = subprocess.run(
                    [snmpwalk_bin, '-v', version_flag, '-c', community,
                     '-p', port, device.ip_address, oid],
                    capture_output=True, text=True, timeout=30
                )
                result = proc.stdout or proc.stderr or 'No output.'
            except FileNotFoundError:
                install_hint = {
                    'Darwin': 'brew install net-snmp',
                    'Windows': 'Download from http://www.net-snmp.org/download.html',
                }.get(os_name, 'sudo apt install snmp  # or  sudo yum install net-snmp-utils')
                result = f'snmpwalk not found.\nInstall: {install_hint}'
            except Exception as e:
                result = str(e)

    return render(request, 'snmp_walk.html', {
        'title': 'Lazy Network Automation',
        'head_page': 'Tools',
        'page': 'SNMP Walk',
        'all_device': all_device,
        'result': result,
    })


@login_required(login_url='/login')
def compare_file(request):
    diff_html = ''
    files = BackupConfig.objects.all().order_by('-time')

    if request.method == 'POST':
        file1_id = request.POST.get('file1')
        file2_id = request.POST.get('file2')
        try:
            f1 = get_object_or_404(BackupConfig, pk=file1_id)
            f2 = get_object_or_404(BackupConfig, pk=file2_id)
            path1 = os.path.join('media', str(f1.b_file))
            path2 = os.path.join('media', str(f2.b_file))
            with open(path1) as a, open(path2) as b:
                lines1 = a.readlines()
                lines2 = b.readlines()
            diff = difflib.unified_diff(
                lines1, lines2,
                fromfile=str(f1.b_file),
                tofile=str(f2.b_file),
            )
            diff_html = ''.join(diff) or 'Files are identical.'
        except FileNotFoundError as e:
            diff_html = f'File not found: {e}'
        except Exception as e:
            diff_html = str(e)

    return render(request, 'compare_file.html', {
        'title': 'Lazy Network Automation',
        'head_page': 'Tools',
        'page': 'Compare File',
        'files': files,
        'diff_html': diff_html,
    })
