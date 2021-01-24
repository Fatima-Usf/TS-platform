from django.conf.urls import url
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin


urlpatterns = [
    url(r'^$', index0, name='indexGeneral'),
    url(r'^index/$', index, name='index'),
    url(r'^inscription/$', inscription, name='inscription'),
    url(r'^tableau-de-bord/$', t_bord, name='t-bord'),
    url(r'^mon-groupe/$', groupe , name='mon-groupe'),
    url(r'^teacherProfil/$', teacherProfil, name='profil'),
    url(r'^matiere-non-acquise/$', matiere_non_acquise , name='matiere-non-acquise'),
    url(r'^teacherModule/$', teacherModule, name='teacherModule'),
    url(r'^pv-matiere/$', pv_matiere , name='pv-matiere'),
    url(r'^teacherPvnote/$', teacherPvnote, name='teacherPvnote'),
    url(r'^teacherStatistic/$', teacherStatistic, name='teacherStatistic'),
    url(r'^pvSout/$', pvSout, name='pvSout'),
    url(r'^pv-semestre/$', pv_semestre , name='pv-semestre'),
    url(r'^pv-annee/$', pv_annee , name='pv-annee'),
    url(r'^mon-releve/$', releve , name='mon-releve'),
    url(r'^teacher/$', teacher, name='teacher'),
    url(r'^logout/$', my_logout , name='my_logout'),
    url(r'^teacherPvnote/(?P<matiere_id>[0-9]+)/$', note, name='note'),
    url(r'^teacherPvnote/(?P<matiere_id>[0-9]+)/(?P<etudiant_id>[0-9]+)/(?P<tab>.+)/$', note_etudiant, name='note_etudiant'),
    url(r'^relevepdf/(?P<id>[0-9]+)/$', Pdf.as_view(), name='releve_pdf'),
]# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
