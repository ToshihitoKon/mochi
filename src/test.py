#!/usr/bin/env python3

from v2.config import Config
from v2.hidamari import model as hidamari

if __name__ == '__main__':
    cfg = Config()
    m_hidamari = hidamari.get_model(cfg)
    m_hidamari.lightSwitch()

