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