#! usr/bin/python
# -*- coding: ISO-8859-1 -*-

import random as rand
import config


def loi_exp_appel():
    if config.hs < 60:
        return rand.expovariate(0.2)
    elif 60 <= config.hs < 180:
        return rand.expovariate(1)
    return rand.expovariate(0.1)


def loi_exp_mail():
    if config.hs < 60:
        return rand.expovariate(2)
    return rand.expovariate(0.2)


def loi_uniform_appel():
    return rand.uniform(5, 15)


def loi_uniform_mail():
    return rand.uniform(3, 7)


def loi_uniform_mail_nuit():
    return rand.randint(20, 80)
