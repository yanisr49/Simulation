#! usr/bin/python
# -*- coding: ISO-8859-1 -*-

import config
import lois
import mail


def arrive_appel():
    import simulation
    config.qt += 1
    x = lois.loi_exp_appel()
    simulation.ajout_evenement(lambda: arrive_appel(), config.hs + x)
    if config.ct < config.nt:
        simulation.ajout_evenement(lambda: prise_en_charge_appel(), config.hs)


def prise_en_charge_appel():
    import simulation
    config.qt -= 1
    config.ct += 1
    x = lois.loi_uniform_appel()
    simulation.ajout_evenement(lambda: fin_appel(), config.hs + x)


def fin_appel():
    import simulation
    if config.qt > 0:
        simulation.ajout_evenement(lambda: prise_en_charge_appel(), config.hs)
    else:
        simulation.ajout_evenement(lambda: mail.prise_en_charge_mail(), config.hs)
        config.nt -= 1
        config.nm += 1
