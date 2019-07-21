# -*-coding:utf-8 -*-
# !/usr/bin/env python3
import logging

logging.basicConfig(format='%(asctime)s [%(filename)s:%(lineno)d:%(levelname)s] %(message)s', datefmt='%Y-%m-%d')
logs = logging.getLogger()
logs.setLevel(logging.INFO)
