from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import MedicalData
from .forms import MedicalDataForm
import os
import json
import xml.etree.ElementTree as ET

def save_data(request):
    if request.method == 'POST':
        form = MedicalDataForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if request.POST.get('save_to') == 'db':
                if not MedicalData.objects.filter(patient_id=data['patient_id']).exists():
                    MedicalData.objects.create(**data)
                    return JsonResponse({'message': 'Data saved to database.'})
                else:
                    return JsonResponse({'message': 'Duplicate entry found.'}, status=400)
            elif request.POST.get('save_to') == 'file':
                file_format = request.POST.get('file_format')
                data_dir = 'data'
                os.makedirs(data_dir, exist_ok=True)
                file_path = os.path.join(data_dir, f'{data["patient_id"]}.{file_format}')

                if file_format == 'json':
                    with open(file_path, 'w') as f:
                        json.dump(data, f)
                elif file_format == 'xml':
                    root = ET.Element("MedicalData")
                    for key, value in data.items():
                        child = ET.SubElement(root, key)
                        child.text = str(value)
                    tree = ET.ElementTree(root)
                    tree.write(file_path)
                return JsonResponse({'message': 'Data saved to file.'})
    else:
        form = MedicalDataForm()
    return render(request, 'health_data_app/save_data.html', {'form': form})

def load_data(request):
    if request.method == 'POST':
        file = request.FILES['file']
        file_format = file.name.split('.')[-1]
        if file_format == 'json':
            try:
                data = json.load(file)
                if 'patient_id' not in data:
                    return JsonResponse({'message': 'Missing patient_id in JSON file.'}, status=400)
                if not MedicalData.objects.filter(patient_id=data['patient_id']).exists():
                    MedicalData.objects.create(**data)
                    return JsonResponse({'message': 'Data loaded from JSON file.'})
                else:
                    return JsonResponse({'message': 'Duplicate entry found.'}, status=400)
            except json.JSONDecodeError:
                return JsonResponse({'message': 'Invalid JSON file.'}, status=400)
        elif file_format == 'xml':
            try:
                tree = ET.parse(file)
                root = tree.getroot()
                data = {child.tag: child.text for child in root}
                if 'patient_id' not in data:
                    return JsonResponse({'message': 'Missing patient_id in XML file.'}, status=400)
                if not MedicalData.objects.filter(patient_id=data['patient_id']).exists():
                    MedicalData.objects.create(**data)
                    return JsonResponse({'message': 'Data loaded from XML file.'})
                else:
                    return JsonResponse({'message': 'Duplicate entry found.'}, status=400)
            except ET.ParseError:
                return JsonResponse({'message': 'Invalid XML file.'}, status=400)
    return render(request, 'health_data_app/load_data.html')

def list_data(request):
    source = request.GET.get('source', 'db')
    if source == 'db':
        data = MedicalData.objects.all()
    else:
        data_dir = 'data'
        if not os.path.exists(data_dir):
            return JsonResponse({'message': 'No files found.'}, status=404)
        files = os.listdir(data_dir)
        if not files:
            return JsonResponse({'message': 'No files found.'}, status=404)
        data = []
        for file in files:
            file_format = file.split('.')[-1]
            file_path = os.path.join(data_dir, file)
            if file_format == 'json':
                with open(file_path, 'r') as f:
                    data.append(json.load(f))
            elif file_format == 'xml':
                tree = ET.parse(file_path)
                root = tree.getroot()
                data.append({child.tag: child.text for child in root})
    return render(request, 'health_data_app/list_data.html', {'data': data})

def edit_data(request, patient_id):
    record = get_object_or_404(MedicalData, patient_id=patient_id)
    if request.method == 'POST':
        form = MedicalDataForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Data updated successfully.'})
    else:
        form = MedicalDataForm(instance=record)
    return render(request, 'health_data_app/edit_data.html', {'form': form, 'patient_id': patient_id})

def delete_data(request, patient_id):
    record = get_object_or_404(MedicalData, patient_id=patient_id)
    if request.method == 'POST':
        record.delete()
        return JsonResponse({'message': 'Data deleted successfully.'})
    return render(request, 'health_data_app/delete_data.html', {'patient_id': patient_id})
