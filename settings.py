# -*- coding: utf-8 -*-
import os

smtp_server = "smtp.gmail.com"
use_tls = True
use_ssl = False
username = ""  # username@gmail.com
password = ""  # does not work with two-factor auth


template_path = os.path.join(os.path.dirname(__file__), 'template.txt')
template_fh = open(template_path, 'rb')
template = template_fh.read()
