import lois.py
from simulation import ajout_evenement

# Procédure Arrivé Mail
def arrive_mail() :
    global qm, hs, cm, nm
    qm = qm + 1
    x = lois.loi_exp_mail()
    ajout_evenement(arrive_mail(), hs + x)
    if cm < nm :
        ajout_evenement(arrive_mail(), hs + 1)



#Procédure Prise en charge Mail
def prise_en_charge_mail() :
    global qm, hs, cm
    qm = qm + 1
    cm = cm + 1
    x = lois.loi_uniform_mail()
    ajout_evenement(prise_en_charge_mail(), hs + x)
