from simulation import *
from lois import *


def arrive_appel():
    global hs, qt, ct, nt

    qt = qt + 1
    x = loi_exp_appel()
    ajout_evenement(arrive_appel(), hs + x)
    if ct < nt:
        ajout_evenement(prise_en_charge_appel(), hs)


def prise_en_charge_appel():
    global hs, qt, ct

    qt = qt - 1
    ct = ct + 1
    x = loi_uniform_appel()
    ajout_evenement(fin_appel(), hs + x)


def fin_appel():
    global hs, qt, nt, nm

    if qt > 0:
        ajout_evenement(prise_en_charge_appel(), hs)
    else:
        ajout_evenement(prise_en_charge_mail(), hs)
        nt = nt - 1
        nm = nm + 1
