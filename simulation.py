#! usr/bin/python
# -*- coding: UTF-8 -*-

import config
import lois
import mail
import appel
import stats


def debut(nb_conseiller_total, nb_conseiller_appel, nb_poste_max):
    """
    Initialise toutes les varible nécessaire au bon fonctionnement de la simulation

    :param nb_conseiller_total: nombre total de téléconseiller
    :param nb_conseiller_appel: nombre de téléconseiller affectés aux appels
    :param nb_poste_max: nombre de téléconseiller maximum affectés aux appels
    """
    # print("log - début")

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
    config.qm += lois.loi_uniform_mail_nuit() - 1
    ajout_evenement(lambda: mail.arrive_mail(), config.hs)

    # Génére arrivé mail
    x = lois.loi_exp_appel()
    ajout_evenement(lambda: mail.arrive_mail(), config.hs + x)

    # Génére arrivé appel
    x = lois.loi_exp_appel()
    ajout_evenement(lambda: appel.arrive_appel(), config.hs + x)


def fin():
    print("Nombre appel traite : " + str(config.nb_appel_traite))
    print("Nombre mail traite : " + str(config.nb_mail_traite))
    print("Nombre appel non traite : " + str(config.qt))
    print("Nombre mail non traite : " + str(config.qm))
    print("Temps moyen dans la queue (appel) : " + str(
        config.aire_qt / (config.qt + config.ct + config.nb_appel_traite)) + " min")
    print("Temps moyen dans la queue (mail) : " + str(
        config.aire_qm / (config.qm + config.cm + config.nb_mail_traite)) + " min")
    print("Taux occupation conseille : " + str((config.aire_ct + config.aire_cm) / (240 * config.n) * 100) + " %")
    print("Taux occupation poste telephonique : " + str(config.aire_ct / (240 * config.nt_max) * 100) + " %")


def ajout_evenement(fonction, temps):
    i = 0
    if temps < 240:
        while temps >= config.echeancier[i][1]:
            i += 1
        config.echeancier.insert(i, (fonction, temps))


def simulation(nb_conseiller_total, nb_conseiller_appel, nb_poste_max):
    config.hs = 0
    config.echeancier = [(lambda: fin(), config.hs + 240)]
    debut(nb_conseiller_total, nb_conseiller_appel, nb_poste_max)

    while config.echeancier[0][1] < 240:
        old_hs = config.hs
        config.hs = config.echeancier[0][1]
        stats.mise_a_jour_aires(old_hs, config.hs)
        config.echeancier[0][0]()
        del config.echeancier[0]

    config.echeancier[0][0]()


if __name__ == "__main__":
    simulation(20, 2, 10)
