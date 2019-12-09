import random as rand
from appel import *
from mail import *
from stats import *
from lois import *

def debut(nb_conseiller_total, nb_conseiller_appel):
    """
    Initialise toutes les varible nécessaire au bon fonctionnement de la simulation

    :param nb_conseiller_total: nombre total de téléconseiller
    :param nb_conseiller_appel: nombre de téléconseiller affectés aux appels
    """

    # Appel variables globales
    global hs, n, nt, nm, ct, cm, qt, qm, aire_ct, aire_cm, aire_qt, aire_qm, nb_appel_traite, nb_mail_traite, nb_mail_non_traite, \
        tp_attente_client_tel, tp_attente_client_tel, taux_occupation_conseille, taux_occupation_postes_tel

    # Paramètres
    n = nb_conseiller_total
    nt = nb_conseiller_appel
    nm = n - nt # nombre de téléconseiller affectés aux mails

    # Initialisation valeurs
    hs = 0
    ct = 0
    cm = 0
    qt = 0
    qm = 0

    # Initialisation indicateurs statistiques
    aire_ct = 0
    aire_cm = 0
    aire_qt = 0
    aire_qm = 0

    nb_appel_traite = 0
    nb_mail_traite = 0
    nb_mail_non_traite = qm
    tp_attente_client_tel = 0
    tp_attente_client_tel = 0
    taux_occupation_conseille = 0
    taux_occupation_postes_tel = 0

    # Génère mails nuit
    for i in range(loi_uniform_mail_nuit()):
        ajout_evenement(arrive_mail(), hs)

    # Génére arrivé mail
    x = loi_exp_appel()
    ajout_evenement(arrive_mail(), hs + x)

    # Génére arrivé appel
    x = loi_exp_appel()
    ajout_evenement(arrive_appel(), hs + x)

    # Génère fin
    ajout_evenement(fin(), hs + 240)

def ajout_evenement(fonction, temps):
    a = 1

def simulation(nb_conseiller_total, nb_conseiller_appel):
    global echeancier, hs
    echeancier = [(debut(nb_conseiller_total, nb_conseiller_appel))]

    while(len(echeancier) > 0):
        old_hs = hs
        hs = echeancier[0][1]
        mise_a_jour_aires(old_hs, hs)
        echeancier[0][0]()
        echeancier.remove(0)

