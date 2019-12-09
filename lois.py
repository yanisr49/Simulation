import random as rand


def loi_exp_appel():

    global hs

    x = 0
    if hs < 60:
        return rand.expovariate(1/5)
    elif hs >= 60 and hs < 180:
        return rand.expovariate(1)
    return rand.expovariate(1/10)


def loi_exp_mail():

    global hs

    x = 0
    if hs < 60:
        return rand.expovariate(2)
    return rand.expovariate(1/5)


def loi_uniform_appel():
    return rand.uniform(5,15)


def loi_uniform_mail():
    return rand.uniform(3,7)


def loi_uniform_mail_nuit():
    return rand.uniform(20,80)