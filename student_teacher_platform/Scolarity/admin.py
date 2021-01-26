# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .views import *
from .render import Render

from django.contrib import admin

from django.utils.html import format_html
from django.urls import reverse
from .models import *


def accept_students(modeladmin, request, queryset):
    queryset.update(status="1")


accept_students.short_description = "Accepter les etudiants"

def generer_relever(modeladmin, request, queryset):
    for q in queryset:

        params = {}
        etudiant = Etudiant.objects.get(pk=q.id)
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

        return Render.render('Scolarity/relevePDF.html', params)


generer_relever.short_description =" Generer un relever de notes "

def generer_certafica(modeladmin,request, queryset):
    pass

generer_certafica.short_description=" Generer un certafica de scolarité"

class Etudiants(admin.TabularInline):
    model = Etudiant
    fields = ('nom', 'prenom', 'dateNaissance')



class EtudiantAdmin(admin.ModelAdmin):
    list_display = ['nom', 'prenom', 'status']
    list_filter = ['status']
    list_display_link = ['nom', 'prenom', ]
    actions = [accept_students, generer_relever, generer_certafica ]
    search_fields = ['nom', 'prenom']

    class Meta:
        model = Etudiant


# def get_queryset(self, request):
# qs = super(EtudiantAdmin, self).get_queryset(request)
# if self.value():
# return qs.filter(status="1")
# else :
# return qs

# Register your models here.
class InscriptionAdmin(admin.ModelAdmin):
    list_display = ['etudiant','niveau', 'annee', 'specialite', 'section', 'groupe']
    list_filter = ['niveau', 'annee', 'specialite', 'section', 'groupe']

# class ListeAdmin(admin.ModelAdmin):
#     list_filter = ['annee_scolaire', 'niveau', ]
#     inlines = [
#         Etudiants
#     ]

class UnityAdmin(admin.ModelAdmin):
    list_display = ['libele', 'semestre']


class MatiereAdmin(admin.ModelAdmin):
    list_display = ['libele', 'credit', 'coef', 'unite', 'responsable']
    list_display_link = ['libele']

class SuitMatiereAdmin(admin.ModelAdmin):
    list_display = ['etudiant', 'matiere', 'note_cours', 'note_td', 'note_tp', 'note_examen']
    list_filter = ['etudiant', 'matiere']
    search_fields = ['etudiant', 'matiere']

class EnseignantAdmin(admin.ModelAdmin):
    list_display = ['nom', 'prenom', 'mail', 'tel']

admin.site.register(Etudiant, EtudiantAdmin)
admin.site.register(Enseignant, EnseignantAdmin)
admin.site.register(Employe)
admin.site.register(Matiere, MatiereAdmin)
admin.site.register(Semestre)
admin.site.register(Inscription, InscriptionAdmin )
admin.site.register(Section)
admin.site.register(Groupe)
admin.site.register(Annee)
admin.site.register(Specialite)
admin.site.register(SuitMatiere, SuitMatiereAdmin)
admin.site.register(Unity, UnityAdmin)
