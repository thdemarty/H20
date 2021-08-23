from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import get_list_or_404, render, get_object_or_404
from django.http import HttpResponse
from django.db.models import Q

import reversion

from .models import Patient

@login_required
def dashboard(request):
    context = {}
    return render(request, 'dashboard.html', context)

@permission_required("accounts.can_set_statut_provisoire")
def all_patient_to_provisoire(request):
    with reversion.create_revision():
        # Updates made on object
        obj = Patient.objects.all()
        obj.update(statut="P")
        # Revision meta data
        reversion.set_user(request.user)
        reversion.set_comment("Downgrade all patient identity to PROVISOIRE")
    return HttpResponse("Vous avez défini le statut de toutes les identités en &laquo; PROVISOIRE &raquo;")

@permission_required("accounts.can_view_patient")
def patient_search(request):
    birth_lname = request.GET.get("birth_lname")
    birth_fname = request.GET.get("birth_fname")
    ins = request.GET.get("ins")

    if birth_fname == None: birth_fname = ""
    if birth_lname == None: birth_lname = ""
    if ins == None: ins = ""
    results = Patient.objects.filter(ins__iexact=ins)
    results |= Patient.objects.filter(birth_fnames__iexact=birth_fname)
    results |= Patient.objects.filter(birth_lname__iexact=birth_lname)
    context = {"results": results}
    return render(request, 'patient/patient_search.html', context)

@permission_required("accounts.can_view_detail_patient")
def patient_identity(request, pk):
    context = {"patient": get_object_or_404(Patient, pk=pk)}
    return render(request, "patient/patient_identity.html", context=context)

def patient_agenda(request, pk):
    context = {"patient": get_object_or_404(Patient, pk=pk)}
    return render(request, "patient/patient_agenda.html", context=context)

def patient_health_data(request, pk):
    context = {"patient": get_object_or_404(Patient, pk=pk)}
    return render(request, "patient/patient_health_data.html", context=context)

def patient_acces_permissions(request, pk):
    context = {"patient": get_object_or_404(Patient, pk=pk)}
    return render(request, "patient/patient_acces_permissions.html", context=context)

def patient_health_data_urgence(request, pk):
    context = {"patient": get_object_or_404(Patient, pk=pk)}
    return HttpResponse("Accès d'urgence aux données de santé après validation et enregistrement de l'accès et du motif d'accès")

def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    # using reversion (delete revision and version)
    # To be reverted, we have to store the primary key in a file to be able to retrieve these identity
    patient.delete()
    return HttpResponse("Vous avez supprimé le patient")