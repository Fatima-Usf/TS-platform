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
                    moyenne = moyenneCC*0.4 + detail.note_examen*0.6

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
