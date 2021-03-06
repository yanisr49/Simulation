#! usr/bin/python
# -*- coding: UTF-8 -*-

import config
import lois


# Procédure Arrivé Mail
def arrive_mail():
    # print("log - arrive mail")
    import simulation
    config.qm += 1
    x = lois.loi_exp_mail()
    simulation.ajout_evenement(lambda: arrive_mail(), config.hs + x)
    if config.cm < config.nm:
        simulation.ajout_evenement(lambda: prise_en_charge_mail(), config.hs)


# Procédure Prise en charge Mail
def prise_en_charge_mail():
    # print("log - prise en charge mail")
    import simulation
    config.qm -= 1
    config.cm += 1
    x = lois.loi_uniform_mail()
    simulation.ajout_evenement(lambda: fin_mail(), config.hs + x)


def fin_mail():
    # print("log - fin mail")
    import appel
    import simulation
    config.cm -= 1
    config.nb_mail_traite += 1
    if config.qt >= config.ct and config.nt < config.nt_max and config.qt > 0:
        simulation.ajout_evenement(lambda: appel.prise_en_charge_appel(), config.hs)
        config.nt += 1
        config.nm -= 1
    elif config.qm > 0:
        simulation.ajout_evenement(lambda: prise_en_charge_mail(), config.hs)
