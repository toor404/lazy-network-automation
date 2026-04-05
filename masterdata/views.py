from multiprocessing import context
from django.shortcuts import render, redirect, HttpResponse
from .models import MasterData, LOV,LOVType
from django.contrib import messages
from .forms import AddData, LOVForm
from django.contrib.auth.decorators import login_required



# add master data
@login_required(login_url='/login')
def index(request):
    all_device = MasterData.objects.all()
    add_data = AddData()
    fdt = LOV.objects.filter(type="device_type")
    fdv = LOV.objects.filter(type="device_vendor")
    fsnmp = LOV.objects.filter(type="snmp_version")
    print(fdt)
    print(fdv)
    if request.method == 'POST':
        add_data = AddData(request.POST)
        if add_data.is_valid():
            add_data.save()
            messages.success(request, "Device Added Succesfully")
        else:
            messages.error(request, "Data Tidak Valid")

    
        return redirect('/masterdata')
    else:
        
        context = {
            'title':'Lazy Network Automation',
            'head_page':'Main',
            'page': 'Master Data',
            'all_device': all_device,
            'add_data': add_data,
            'fdt': fdt,
            'fdv': fdv,
            'fsnmp': fsnmp,
        }
        
        return render(request, 'forms.html', context)

#add LOV
def lov(request):
    """Menampilkan daftar LOV dan form untuk menambahkan LOV baru."""
    lovs = LOV.objects.all()
    form = LOVForm()
    lovsT = LOVType.choices

    if request.method == "POST":
        form = LOVForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "LOV added successfully.")
            return redirect("lov")  # Refresh halaman setelah submit
        else:
            # Handle form errors, including duplicate validation
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

    # Render the form and LOV list
    context = {
        'title': 'Lazy Network Automation',
        'head_page': 'Main',
        'page': 'LOV',
        'lovs': lovs,
        'form': form,
        'lovsT': lovsT,
    }
    return render(request, 'lov.html', context)