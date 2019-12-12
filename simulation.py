#! usr/bin/python
# -*- coding: ISO-8859-1 -*-

import config
import lois
import mail
import appel


def debut(nb_conseiller_total, nb_conseiller_appel, nb_poste_max):
    """
    Initialise toutes les varible nécessaire au bon fonctionnement de la simulation

    :param nb_conseiller_total: nombre total de téléconseiller
    :param nb_conseiller_appel: nombre de téléconseiller affectés aux appels
    :param nb_poste_max: nombre de téléconseiller maximum affectés aux appels
    """

    # Paramètres
    config.n = nb_conseiller_total
    config.nt = nb_conseiller_appel
    config.nm = config.n - config.nt
    config.nt_max = nb_poste_max

    # Initialisation valeurs
    config.hs = 0
    config.ct = 0
    config.cm = 0
    config.qt = 0
    config.qm = 0

    # Initialisation indicateurs statistiques
    config.aire_ct = 0
    config.aire_cm = 0
    config.aire_qt = 0
    config.aire_qm = 0

    config.nb_appel_traite = 0
    config.nb_mail_traite = 0
    config.nb_mail_non_traite = config.qm
    config.tp_attente_client_tel = 0
    config.tp_attente_client_tel = 0
    config.taux_occupation_conseille = 0
    config.taux_occupation_postes_tel = 0

    # Génère mails nuit
    for i in range(1):
        ajout_evenement(lambda: mail.arrive_mail(), config.hs)

    # Génére arrivé mail
    x = lois.loi_exp_appel()
    ajout_evenement(lambda: mail.arrive_mail(), config.hs + x)

    # Génére arrivé appel
    x = lois.loi_exp_appel()
    ajout_evenement(lambda: appel.arrive_appel(), config.hs + x)


def fin():
    print("fin")
    # Calcul les statistiques de fin
    # l'échéancier est deja vide ?!
    # fin


def ajout_evenement(fonction, temps):
    ajouter = False
    i = 0

    while ajouter == False and i < len(config.echeancier):
        if temps < config.echeancier[i][1]:
            ajouter = True
        i += 1
    if ajouter:
        config.echeancier.insert(i - 1, (fonction, temps))


def simulation(nb_conseiller_total, nb_conseiller_appel, nb_poste_max):
    config.hs = 0
    config.echeancier = [(lambda: fin(), config.hs + 240)]
    debut(nb_conseiller_total, nb_conseiller_appel, nb_poste_max)

    while (config.echeancier[0][1] < 240):
        old_hs = config.hs
        config.hs = config.echeancier[0][1]
        # mise_a_jour_aires(old_hs, config.hs)
        config.echeancier[0][0]()
        del config.echeancier[0]
    config.echeancier[0][0]()


if __name__ == "__main__":
    simulation(10, 2, 5)
