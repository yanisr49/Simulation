# -*- coding: utf-8 -*-

import config


def mise_a_jour_aires(old_hs, new_hs):
    config.aire_qt += config.qt * (new_hs - old_hs)
    config.aire_qm += config.qm * (new_hs - old_hs)
    config.aire_ct += config.ct * (new_hs - old_hs)
    config.aire_cm += config.cm * (new_hs - old_hs)
