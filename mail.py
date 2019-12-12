#! usr/bin/python
# -*- coding: ISO-8859-1 -*-

import config
import lois


# Procédure Arrivé Mail
def arrive_mail():
    print("log - arrive mail")
    import simulation
    config.qm += 1
    x = lois.loi_exp_mail()
    if config.echeancier[0][1] > 0:
        simulation.ajout_evenement(lambda: arrive_mail(), config.hs + x)
    if config.cm < config.nm:
        simulation.ajout_evenement(lambda: prise_en_charge_mail(), config.hs)


# Procédure Prise en charge Mail
def prise_en_charge_mail():
    print("log - prise en charge mail")
    import simulation
    config.qm += 1
    config.cm += 1
    x = lois.loi_uniform_mail()
    simulation.ajout_evenement(lambda: fin_mail(), config.hs + x)


def fin_mail():
    print("log - fin mail")
    import appel
    import simulation
    if config.qt >= config.ct and config.nt < config.nt_max:
        simulation.ajout_evenement(lambda: appel.prise_en_charge_appel(), config.hs)
        config.nt += 1
        config.nm -= 1
    else:
        simulation.ajout_evenement(lambda: prise_en_charge_mail(), config.hs)
        config.nt -= 1
        config.nm += 1
