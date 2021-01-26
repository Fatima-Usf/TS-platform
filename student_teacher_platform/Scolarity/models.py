# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.mail import EmailMessage
from django.conf import settings
from .choices import *
from django.contrib.auth.models import User
from datetime import datetime
from datetime import date

import os


# Models
#def get_image_path(instance, filename):
#    return os.path.join('Scolarity/photos', str(instance.id), filename)



# class Personne
class Personne(models.Model):
    nom = models.CharField(max_length=35)
    prenom = models.CharField(max_length=35)
    adress = models.CharField(max_length=100)
    mail = models.EmailField()
    #dateNaissance = models.DateField(max_length=35)
    tel = models.CharField(max_length=35)
    image = models.ImageField(upload_to='profile_image', null=True, blank=True)

    class Meta:
        abstract = True


class Employe(Personne):
    grade = models.CharField(max_length=100, null=True, blank=True)
    code = models.CharField(max_length=10)
    username = models.CharField(max_length=35)

    def __str__(self):
        return "{} {}".format(self.nom, self.prenom)

# class Enseignant
class Enseignant(Personne):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    grade = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return "{} {}".format(self.nom, self.prenom)



class Etudiant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    dateNaissance = models.DateField(max_length=35)
    sexe = models.CharField(max_length=1, choices=SEXE)
    adrs = models.CharField(max_length=200)
    nationality = models.CharField(max_length=35)
    tel = models.CharField(max_length=35)
    mail = models.EmailField()
    status = models.CharField(max_length=3, choices=STATUS_DOSSIER, default="0")
    class Meta:
        verbose_name = "Etudiant"
        verbose_name_plural = "Etudiants"

    def __str__(self):
        return "{} {}".format(self.nom, self.prenom)

    def confirmer_inscription(self):
        self.status = "1"
        self.save()



class Annee(models.Model):
    annee_scolaire = models.IntegerField(default=2018)

    def __str__(self):
        year = self.annee_scolaire
        return "{}/{}".format(str(year), str(year + 1))



class Specialite(models.Model):
    nom = models.CharField(max_length=100)
    responsable = models.OneToOneField(Enseignant, on_delete=models.CASCADE)

    def __str__(self):
        return self.nom



class Section(models.Model):
    numero = models.IntegerField()

    def __str__(self):
        return "S{}".format(self.numero)


class Groupe(models.Model):
    numero = models.IntegerField()

    def __str__(self):
        return "G{}".format(self.numero)


class Inscription(models.Model):
    annee = models.ForeignKey(Annee, on_delete=models.CASCADE)
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    domaine = models.CharField(max_length=1, choices=DOMAINE)
    nomFiliere = models.CharField(max_length=1, choices=FILIERE)
    niveau = models.CharField(max_length=1, choices=NIVEAU)
    specialite = models.ForeignKey(Specialite, blank=True, null=True, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.etudiant.status = 1
        self.etudiant.save()
        user = self.etudiant.user
        user.is_active = True
        user.save()
        super(Inscription, self).save()

    def __str__(self):
        return "{} {}".format(self.etudiant.nom, self.etudiant.prenom)


class Field(models.Model):
    code = models.CharField(max_length=30)
    libele = models.CharField(max_length=100)

    class Meta:
        abstract = True


class Semestre(Field):
    niveau = models.CharField(max_length=1, choices=NIVEAU)

    def __str__(self):
        return "{}".format(self.libele)


class Unity(Field):

    class Meta:
        verbose_name = "Unité"

    nature = models.CharField(max_length=3)
    credit_requis = models.IntegerField()
    coef = models.IntegerField()
    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE)

    def __str__(self):
        return "{}     {}".format(self.code, self.semestre.code)


class Matiere(Field):
    credit = models.IntegerField()
    coef = models.IntegerField()
    unite = models.ForeignKey(Unity, on_delete=models.CASCADE)
    charge_td = models.ForeignKey(Enseignant, related_name='enseignant_td', blank=True, null=True, on_delete=models.CASCADE)
    charge_tp = models.ForeignKey(Enseignant, related_name='charge_td', blank=True, null=True, on_delete=models.CASCADE)

    responsable = models.ForeignKey(Enseignant, on_delete=models.CASCADE)

    def __str__(self):
        return self.libele


class SuitMatiere(models.Model):

    class Meta:
        verbose_name = "Note"
        unique_together = (('etudiant', 'matiere'),)

    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    note_cours = models.FloatField(blank=True, null=True)
    note_td = models.FloatField(blank=True, null=True)
    note_tp = models.FloatField(blank=True, null=True)
    note_examen = models.FloatField()
    session = models.CharField(max_length=2, choices=SESSION, default=0)
    annee = models.ForeignKey(Annee, default=date.today().year, on_delete=models.CASCADE)

    def __str__(self):
        return "Etudiant: {} {} , Matiere: {}".format(self.etudiant.nom, self.etudiant.prenom, self.matiere.libele)
