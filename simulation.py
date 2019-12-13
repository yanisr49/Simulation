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
    config.hs = 0.0
    config.ct = 0.0
    config.cm = 0.0
    config.qt = 0.0
    config.qm = 0.0

    # Initialisation indicateurs statistiques
    config.aire_ct = 0.0
    config.aire_cm = 0.0
    config.aire_qt = 0.0
    config.aire_qm = 0.0

    config.nb_appel_traite = 0.0
    config.nb_mail_traite = 0.0

    # Genere evenement fin
    config.echeancier = [(lambda: fin(), config.hs + 240)]

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
    if temps < 240:
        i = 0
        while temps >= config.echeancier[i][1]:
            i += 1
        config.echeancier.insert(i, (fonction, temps))


def simulation(nb_conseiller_total, nb_conseiller_appel, nb_poste_max):
    debut(nb_conseiller_total, nb_conseiller_appel, nb_poste_max)

    while config.echeancier[0][1] < 240:
        old_hs = config.hs
        config.hs = config.echeancier[0][1]
        stats.mise_a_jour_aires(old_hs, config.hs)
        config.echeancier[0][0]()
        del config.echeancier[0]

def evaluation(p0, p1, p2, p3, p4, p5):
    global eval
    eval += p0 * (config.nb_appel_traite / (config.nb_appel_traite + config.qt)) \
         + p1 * (config.nb_mail_traite / (config.nb_mail_traite + config.qm)) \
         + p2 * (1 - (config.aire_qt / (240 * (config.nb_appel_traite + config.qt)))) \
         + p3 * (1 - (config.aire_qm / (240 * (config.nb_mail_traite + config.qm)))) \
         + p4 * ((config.aire_ct + config.aire_cm) / (240 * config.n)) \
         + p5 * (config.aire_ct / (240 * config.nt_max))

def indicateurs():
    global ind
    ind[0] += config.nb_appel_traite
    ind[1] += config.nb_mail_traite
    ind[2] += config.qt
    ind[3] += config.qm
    ind[4] += config.aire_qt / (config.qt + config.ct + config.nb_appel_traite)
    ind[5] += config.aire_qm / (config.qm + config.cm + config.nb_mail_traite)
    ind[6] += (config.aire_ct + config.aire_cm) / (240 * config.n) * 100
    ind[7] += config.aire_ct / (240 * config.nt_max) * 100


if __name__ == "__main__":
    best_eval = 0
    best_parametres = []
    best_indicateurs = []

    nb_conseille_total_min = 15
    nb_conseille_total_max = 20
    for nb_conseille_total in range(nb_conseille_total_min, nb_conseille_total_max):
        print("Simulation : " + str((nb_conseille_total-nb_conseille_total_min) / float(nb_conseille_total_max-nb_conseille_total_min-1) * 100) + "%")
        for nb_poste in range(8, nb_conseille_total):
            for nb_conseille_appel in range(nb_conseille_total):
                eval = 0
                ind = [0]*8
                n = 3
                for i in range(n):
                    simulation(nb_conseille_total, nb_conseille_appel, nb_poste)
                    evaluation(1, 1, 1, 1, 1, 1)
                    indicateurs()
                if eval > best_eval:
                    best_eval = eval
                    best_parametres = [nb_conseille_total, nb_conseille_appel, nb_poste]
                    best_indicateurs = [(value / n) for value in ind]

    print("\nNombre conseillé total : " + str(best_parametres[0]))
    print("Nombre conseillé appel : " + str(best_parametres[1]))
    print("Nombre poste : " + str(best_parametres[2]))

    print("\neval : " + str(best_eval))

    print("\nNombre appel traite : " + str(best_indicateurs[0]))
    print("Nombre mail traite : " + str(best_indicateurs[1]))
    print("Nombre appel non traite : " + str(best_indicateurs[2]))
    print("Nombre mail non traite : " + str(best_indicateurs[3]))
    print("Temps moyen dans la queue (appel) : " + str(best_indicateurs[4]) + " min")
    print("Temps moyen dans la queue (mail) : " + str(best_indicateurs[5]) + " min")
    print("Taux occupation conseille : " + str(best_indicateurs[6]) + " %")
    print("Taux occupation poste telephonique : " + str(best_indicateurs[7]) + " %")
