# # -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django import forms
from .forms import InscriptionEtudiant
from .choices import *
from .models import *

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.template.loader import render_to_string

from django.views.generic import View
from django.utils import timezone
from .render import Render

# Create your views here.

def index0(request):
    return render(request,'Scolarity/index0.html')

def index(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if not user or user.is_superuser:
            error = True
            return render(request, 'Scolarity/index.html', locals())

        else:
            login(request, user)
            try:
                etudiant = Etudiant.objects.get(user=user)
            except Etudiant.DoesNotExist:
                etudiant = None
            if etudiant:
                return redirect('t-bord')
            return redirect('teacher')

    return render(request, 'Scolarity/index.html')


def inscription(request):

    context = {}
    registered = False
    if request.method == "POST":

        form = InscriptionEtudiant(request.POST)
        #form = AddUser(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            re_password = form.cleaned_data['re_password']
            mail = form.cleaned_data['mail']
            user = User.objects.filter(username=username)
            if not user.exists():
                user = User.objects.create_user(
                    username, mail, password, is_active=False)
                nom = form.cleaned_data['nom']
                prenom = form.cleaned_data['prenom']
                dateNaissance = form.cleaned_data['dateNaissance']
                sexe = form.cleaned_data['sexe']
                adrs = form.cleaned_data['adrs']
                nationality = form.cleaned_data['nationality']
                tel = form.cleaned_data['tel']
                etudiant = Etudiant.objects.create(user=user, nom=nom, prenom=prenom, dateNaissance=dateNaissance,
                                                   sexe=sexe, adrs=adrs,nationality=nationality, tel=tel, mail=mail, status=STATUS_DOSSIER[1])
                etudiant.save()
                registered = True

            else:

                if user.exists():
                    context['user_taken'] = True

                if password != re_password:
                    context['mdp'] = True

            context['registered'] = registered
            context['form'] = form
            return render(request, 'Scolarity/inscription.html', context)

    form = InscriptionEtudiant()
    context['form'] = form
    return render(request, 'Scolarity/inscription.html', context)


def t_bord(request):
    if not request.user.is_authenticated:

        return redirect('index')
    user = request.user
    etudiant = Etudiant.objects.get(user=user)
    return render(request, 'Scolarity/t-bord.html', locals())


def teacher(request):
    if not request.user.is_authenticated:
        return redirect('index')

    user = request.user
    enseignant = Enseignant.objects.get(user=user)
    return render(request, 'Scolarity/dashbordTeacher.html', locals())


def groupe(request):
    if not request.user.is_authenticated:
        return redirect('index')
    user = request.user
    etudiant = Etudiant.objects.get(user=user)
    inscription = Inscription.objects.get(etudiant=etudiant)
    inscriptions = Inscription.objects.filter(nomFiliere=inscription.nomFiliere,
                                              niveau=inscription.niveau,
                                              specialite=inscription.specialite,
                                              section=inscription.section,
                                              groupe=inscription.groupe)
    etudiants = [inscription.etudiant for inscription in inscriptions]
    context = {
        'etudiants': etudiants,
    }
    return render(request, 'Scolarity/mon-groupe.html', context)

def teacherProfil(request):
    if not request.user.is_authenticated:
        return redirect('index')
    user = request.user
    enseignant = Enseignant.objects.get(user=user)
    return render(request, 'Scolarity/teacherProfil.html', locals())


def matiere_non_acquise(request):
    if not request.user.is_authenticated:
        return redirect('index')

    context = {}
    user = request.user
    etudiant = Etudiant.objects.get(user=user)
    details = SuitMatiere.objects.filter(etudiant=etudiant)
    list_semestre = []
    tab3 = []
    for detail in details:
        sem = detail.matiere.unite.semestre
        if sem not in list_semestre:
            list_semestre.append(sem)

            unites = Unity.objects.filter(semestre=sem)
            unites = [unite for unite in unites]

            somme3 = 0
            compteur3 = 0
            tab2 = []

            for unite in unites:

                matieres = details.filter(matiere__unite=unite)

                somme2 = 0
                compteur2 = 0

                tab = []
                for mat in matieres:

                    compteur = 0
                    somme = 0

                    if mat.note_cours:
                        compteur += 1
                        somme += mat.note_cours

                    if mat.note_td:
                        compteur += 1
                        somme += mat.note_td

                    if mat.note_tp:
                        compteur += 1
                        somme += mat.note_tp

                    matiere = mat.matiere

                    moyenneCC = somme/compteur
                    moyenne = moyenneCC*0.4 + mat.note_examen*0.6

                    somme2 += moyenne*matiere.coef

                    obj = {
                            'matiere': matiere,
                            'moyenneCC' : moyenneCC,
                            'exam' : detail.note_examen,
                            'note' : moyenne,
                            'cc' : moyenneCC,
                            'ef' : mat.note_examen,
                           }

                    tab.append(obj)

                moyenne = somme2/unite.coef

                obj = {
                        'unite' : unite,
                        'matieres' : tab,
                        'note' : moyenne,
                        }

                tab2.append(obj)

                somme3 += moyenne*unite.coef
                compteur3 += unite.coef

            moyenne = somme3/compteur3

            if moyenne >= 10:
                credit3 = 30

            obj = {'semestre' : sem,
                    'unites' : tab2,
                    'note' : moyenne,
                    }
            tab3.append(obj)

    tab = []
    for semestre in tab3:
        if semestre['note'] < 10:
            for unite in semestre['unites']:
                if unite['note'] < 10:
                    for matiere in unite['matieres']:
                        if matiere['note'] < 10:
                            i = matiere['matiere']
                            mat = {
                                    'libele' : i.libele,
                                    'unite' : i.unite.libele,
                                    'semestre' : i.unite.semestre.code,
                                    'cc' : matiere['moyenneCC'],
                                    'exam' : matiere['exam'],
                                    'moyenne' : matiere['note'],
                                    'cc' : matiere['cc'],
                                    'ef' : matiere['ef'],
                                    }
                            tab.append(mat)

    context['matieres'] = tab

    return render(request, 'Scolarity/matiere-non-acquise.html', context)

def teacherModule(request):
    if not request.user.is_authenticated:
        return redirect('index')

    user = request.user
    context = {}
    enseignant = Enseignant.objects.get(user=user)
    context['photo'] = enseignant.image
    matieres = Matiere.objects.filter(responsable=enseignant)
    matieres = [mat for mat in matieres]
    tab = []
    count = 0
    for matiere in matieres:
        count += 1
        obj = {'id' : matiere.id,
                'index' : count,
                'intitule' : matiere.libele,
                'unite' : matiere.unite.libele,
                'semestre': matiere.unite.semestre.libele,
                'niveau' :  matiere.unite.semestre.niveau,

        }
        tab.append(obj)
    context['matieres'] = tab
    return render(request, 'Scolarity/teacherModule.html', context)

def pv_matiere(request):
    if not request.user.is_authenticated:
        return redirect('index')
    context = {}
    user = request.user
    etudiant = Etudiant.objects.get(user=user)
    details = SuitMatiere.objects.filter(etudiant=etudiant)

    # Initialisation des variables compteur
    tab = []
    semestres = []
    for detail in details:
        c = 0
        somme = 0
        obj = {'matiere': detail.matiere.libele,
               'note_cours' : detail.note_cours,
               'note_td' : detail.note_td,
               'note_tp' : detail.note_tp,
               'note_examen' : detail.note_examen,
               'semestre' : detail.matiere.unite.semestre.code,
               }

        semestre = detail.matiere.unite.semestre

        if semestre not in semestres:
            semestres.append(semestre)

        if detail.note_cours:
            c += 1
            somme += detail.note_cours

        if detail.note_td:
            c += 1
            somme += detail.note_td

        if detail.note_tp:
            c += 1
            somme += detail.note_tp

        moyenneCC = somme/c
        moyenne = moyenneCC*0.4 + detail.note_examen*0.6

        obj['moyenneCC'] = moyenneCC
        obj['moyenne'] = moyenne
        tab.append(obj)

    context['tab'] = tab
    context['listSemestre'] = semestres
    return render(request, 'Scolarity/pv-matiere.html', context)


def teacherPvnote(request):
    if not request.user.is_authenticated:
        return redirect('index')

    context = {}
    user = request.user
    enseignant = Enseignant.objects.get(user=user)
    context['photo'] = enseignant.image
    matieres = Matiere.objects.filter(responsable=enseignant)
    matieres = [mat for mat in matieres]
    tab = []
    count = 0
    for matiere in matieres:
        count += 1
        obj = {'id' : matiere.id,
                'index' : count,
                'intitule' : matiere.libele,
                'unite' : matiere.unite.libele,
                'semestre': matiere.unite.semestre.libele,
                'niveau' :  matiere.unite.semestre.niveau,

        }
        tab.append(obj)

    context['matieres'] = tab
    return render(request, 'Scolarity/teacherPvnote.html', context)

def note(request, matiere_id):
    context = {}
    user = request.user
    enseignant = Enseignant.objects.get(user=user)
    context['photo'] = enseignant.image
    error = False
    matiere_id = int(matiere_id)
    matiere = None
    try:
        matiere = Matiere.objects.get(pk=matiere_id)
    except Matiere.DoesNotExist:
        error = True

    if not error and matiere is not None:
        context['matiere'] = matiere.libele
        context['matiere_id'] = matiere_id

        niveau = matiere.unite.semestre.niveau
        annee = datetime.now().year
        try:
            inscriptions = Inscription.objects.filter(niveau=niveau, annee__annee_scolaire=annee)
        except Inscription.DoesNotExist:
            inscriptions = None

        if inscriptions is not None:
            tab = []
            indices = []
            count = 0
            for insc in inscriptions:
                count += 1
                etudiant = insc.etudiant
                obj = {'id' : etudiant.id,
                        'indexe' : count,
                        'nom' : etudiant.nom,
                        'prenom' : etudiant.prenom,
                        'sexe' : etudiant.sexe,
                        'groupe' : insc.groupe,
                        'section' : insc.section,
                }
                indices.append(etudiant.id)
                tab.append(obj)

            print(len(tab))
            print(len(indices))
            context['etudiants'] = tab
            context['indices'] = indices

    return render(request, 'Scolarity/notes.html', context)

def note_etudiant(request, matiere_id, etudiant_id, tab):

    user = request.user
    enseignant = Enseignant.objects.get(user=user)

    matiere_id = int(matiere_id)
    etudiant_id = int(etudiant_id)
    matiere = Matiere.objects.get(pk=matiere_id)
    etudiant = Etudiant.objects.get(pk=etudiant_id)

    suivant = tab.index(str(etudiant_id)) + 1

    tab2 = []
    for t in tab:
        try:
            i = int(t)
            tab2.append(i)
        except:
            pass

    if suivant > len(tab2):
        suivant = None
        print('YES')

    context = {'etudiant' : etudiant,
                'etudiant_id' : etudiant_id,
                'suivant' : suivant,
                'matiere_id' : matiere_id,
                'matiere' : matiere,
                'tab' : tab2,
                }

    #context['photo'] = enseignant.image

    try:
        note = SuitMatiere.objects.get(etudiant=etudiant, matiere=matiere)
    except SuitMatiere.DoesNotExist:
        note = None

    if request.method == 'POST':
        note_cours = request.POST['cours']
        note_td = request.POST['td']
        note_tp = request.POST['tp']
        note_examen = request.POST['examen']

        if not note_cours:
            note_cours = None
        else:
            note_cours = float(note_cours)

        if not note_td:
            note_td = None
        else:
            note_td = float(note_td)

        if not note_tp:
            note_tp = None
        else:
            note_tp = float(note_tp)

        note_examen = float(note_examen)

        if note is None:
            note = SuitMatiere.objects.create(etudiant=etudiant,
            matiere=matiere, note_cours=note_cours, note_td=note_td, note_examen=note_examen)
        else:
            note.note_cours = note_cours
            note.note_td = note_td
            note.note_tp = note_tp
            note.note_examen = note_examen
            note.save(force_update=True)


    return render(request, 'Scolarity/note-etudiant.html', context)

def pvSout(request):
    if not request.user.is_authenticated:
        return redirect('index')

    context = {}
    user = request.user
    enseignant = Enseignant.objects.get(user=user)
    context['photo'] = enseignant.image
    return render(request, 'Scolarity/pvSout.html', locals())



def teacherStatistic(request):
    if not request.user.is_authenticated:
        return redirect('index')

    context = {}
    user = request.user
    enseignant = Enseignant.objects.get(user=user)
    context['photo'] = enseignant.image
    return render(request, 'Scolarity/teacherStatistic.html', locals())


def pv_semestre(request):
    if not request.user.is_authenticated:
        return redirect('index')
    return render(request, 'Scolarity/pv-semestre.html', locals())


def pv_annee(request):
    if not request.user.is_authenticated:
        return redirect('index')
    return render(request, 'Scolarity/pv-annee.html', locals())


def releve(request):
    if not request.user.is_authenticated:
        return redirect('index')

    context = {}
    user = request.user
    etudiant = Etudiant.objects.get(user=user)
    context['etudiant_id'] = etudiant.id
    details = SuitMatiere.objects.filter(etudiant=etudiant)
    list_semestre = []
    tab3 = []
    for detail in details:
        sem = detail.matiere.unite.semestre
        if sem not in list_semestre:
            list_semestre.append(sem)

            unites = Unity.objects.filter(semestre=sem)
            unites = [unite for unite in unites]

            nb_matieres = 0
            somme3 = 0
            compteur3 = 0
            credit3 = 0
            tab2 = []
            for unite in unites:

                matieres = details.filter(matiere__unite=unite)

                nbMatieres = 0

                somme2 = 0
                compteur2 = 0
                credit2 = 0

                tab = []
                for mat in matieres:

                    nbMatieres += 1

                    compteur = 0
                    somme = 0

                    if mat.note_cours:
                        compteur += 1
                        somme += mat.note_cours

                    if mat.note_td:
                        compteur += 1
                        somme += mat.note_td

                    if mat.note_tp:
                        compteur += 1
                        somme += mat.note_tp

                    matiere = mat.matiere

                    moyenneCC = somme/compteur
                    moyenne = moyenneCC*0.4 + mat.note_examen*0.6

                    somme2 += moyenne*matiere.coef

                    credit = 0

                    if moyenne >= 10:
                        credit = matiere.credit

                    credit2 += credit

                    obj = {
                            'matiere': matiere,
                            'note' : moyenne,
                            'session' : mat.session,
                            'credit' : credit,
                           }

                    tab.append(obj)
                    compteur2 += 1

                nb_matieres += compteur2

                moyenne = somme2/unite.coef

                if moyenne >= 10:
                    credit2 = unite.credit_requis

                first = tab[0]
                del tab[0]

                obj = {
                        'unite' : unite,
                        'matieres' : tab,
                        'first' : first,
                        'note' : moyenne,
                        'credit' : credit2,
                        'nb_matieres' : nbMatieres,
                        }

                tab2.append(obj)

                somme3 += moyenne*unite.coef
                compteur3 += unite.coef
                credit3 += credit2

            moyenne = somme3/compteur3

            if moyenne >= 10:
                credit3 = 30

            obj = {'semestre' : sem,
                    'unites' : tab2,
                    'note' : moyenne,
                    'credit' : credit3,
                    }
            nb_matieres2 = len(Matiere.objects.filter(unite__semestre=sem))
            if nb_matieres == nb_matieres2:
                tab3.append(obj)

    context['list_semestre'] = tab3
    return render(request, 'Scolarity/mon-releve.html', context)

def my_logout(request):
    logout(request)
    return redirect('index')

class Pdf(View):

    def get(self, request, id):
        params = {}
        user = request.user
        etudiant = Etudiant.objects.get(user=user)
        params['etudiant_id'] = etudiant.id
        details = SuitMatiere.objects.filter(etudiant=etudiant)
        list_semestre = []
        tab3 = []
        for detail in details:
            sem = detail.matiere.unite.semestre
            if sem not in list_semestre:
                list_semestre.append(sem)

                unites = Unity.objects.filter(semestre=sem)
                unites = [unite for unite in unites]

                nb_matieres = 0
                somme3 = 0
                compteur3 = 0
                credit3 = 0
                tab2 = []
                for unite in unites:

                    matieres = details.filter(matiere__unite=unite)

                    nbMatieres = 0

                    somme2 = 0
                    compteur2 = 0
                    credit2 = 0

                    tab = []
                    for mat in matieres:

                        nbMatieres += 1

                        compteur = 0
                        somme = 0

                        if mat.note_cours:
                            compteur += 1
                            somme += mat.note_cours

                        if mat.note_td:
                            compteur += 1
                            somme += mat.note_td

                        if mat.note_tp:
                            compteur += 1
                            somme += mat.note_tp

                        matiere = mat.matiere

                        moyenneCC = somme/compteur
                        moyenne = moyenneCC*0.4 + mat.note_examen*0.6

                        somme2 += moyenne*matiere.coef

                        credit = 0

                        if moyenne >= 10:
                            credit = matiere.credit

                        credit2 += credit

                        obj = {
                                'matiere': matiere,
                                'note' : moyenne,
                                'credit' : credit,
                               }

                        tab.append(obj)
                        compteur2 += 1

                    print(mat)
                    nb_matieres += compteur2

                    moyenne = somme2/unite.coef

                    if moyenne >= 10:
                        credit2 = unite.credit_requis

                    first = tab[0]
                    del tab[0]

                    obj = {
                            'unite' : unite,
                            'matieres' : tab,
                            'first' : first,
                            'note' : moyenne,
                            'credit' : credit2,
                            'nb_matieres' : nbMatieres,
                            }

                    tab2.append(obj)

                    somme3 += moyenne*unite.coef
                    compteur3 += unite.coef
                    credit3 += credit2

                moyenne = somme3/compteur3

                if moyenne >= 10:
                    credit3 = 30

                obj = {'semestre' : sem,
                        'unites' : tab2,
                        'note' : moyenne,
                        'credit' : credit3,
                        }
                nb_matieres2 = len(Matiere.objects.filter(unite__semestre=sem))
                if nb_matieres == nb_matieres2:
                    tab3.append(obj)

        params['list_semestre'] = tab3
        params['request'] = request

        return Render.render('Scolarity/relevePDF.html', params)
