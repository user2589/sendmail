#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Mass email to list supplied in CSV

This is a console script using Django mail utilities
"""

import smtplib
from email.mime.text import MIMEText


class Sender(object):
    sender = None
    connection = None
    debug = False

    def __init__(self, smtp_host, username, password, use_tls=False,
                 use_ssl=False, sender_email=None, debug=False):

        if not debug:
            if use_tls:
                self.connection = smtplib.SMTP(smtp_host, 587)
                self.connection.ehlo()
                self.connection.starttls()
            elif use_ssl:
                self.connection = smtplib.SMTP_SSL(smtp_host)
            else:
                self.connection = smtplib.SMTP(smtp_host)

            self.connection.login(username, password)

        if sender_email is None:
            sender_email = username

        self.debug = debug
        self.sender = sender_email

    def send_mail(self, subj, body, recipients):
        msg = MIMEText(body)
        msg['Subject'] = subj
        msg['from'] = self.sender
        msg['To'] = ", ".join(recipients)
        if self.debug:
            print msg.as_string()
        else:
            self.connection.sendmail(self.sender, recipients, msg.as_string())


if __name__ == '__main__':

    import csv
    import sys
    import argparse
    import settings

    parser = argparse.ArgumentParser(
        description="Send emails to a list of people in CSV read from stdin.\n"
                    "First line of CSV file will be treated as a header with "
                    "column names. Field named email will be used as address, "
                    "all other fields will be used as template variables.")

    parser.add_argument('subject', type=str,
                        help='email subject')
    parser.add_argument('-y', '--yes', action='store_true',
                        help="whether to really send emails (set to 0) or just "
                             "output dry run to console")

    args = parser.parse_args()

    reader = csv.DictReader(sys.stdin)

    if 'email' not in reader.fieldnames:
        parser.exit(1, "Input CSV is expected to have a column named 'email'")

    debug = not args.yes
    sender = Sender(settings.smtp_server, settings.username, settings.password,
                    settings.use_tls, settings.use_ssl, debug=debug)

    for record in reader:
        body = settings.template.format(**record)
        sender.send_mail(args.subject, body, [record['email']])

    if debug:
        print "="*80
        print "This is an example of emails that would be sent."
        print "If you want to really send them, add -y to the command."
        print "="*80
