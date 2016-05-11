#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Mass email to list supplied in CSV

This is a console script using Django mail utilities
"""

import smtplib
import os

from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# default charset, select from the list email.charset.CHARSETS
DEFAULT_CHARSET = 'utf-8'
MAX_ATTACHMENT_SIZE = 16777216


class Sender(object):
    """ Class to represent SMTP sender. The main purpose of this class is to
        reuse SMTP connection when sending multiple emails
    """
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
    def send_mail(self, subj, body, recipients, charset='utf-8', files=None):
        """ A shortcut to send multipart/plaintext message """
        msg_body = MIMEText(body, _charset=charset)
        if not files:
            msg = msg_body
        else:
            msg = MIMEMultipart()
            msg.attach(msg_body)
            for filename in files:
                try:
                    if os.path.getsize(filename) > MAX_ATTACHMENT_SIZE:
                        self.logger.error(
                            "Attachment size is over 10Mb: %s", filename)
                        continue
                    fh = open(filename, 'rb')
                    content = fh.read()
                except IOError:
                    self.logger.error(
                        "Can't read the attachment content: %s", filename)
                    return 1
                basename = os.path.basename(filename)
                part = MIMEApplication(
                    content, Name=basename,
                    Content_Disposition='attachment; filename=%s'.format(basename))
                msg.attach(part)

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

    parser.add_argument('subject', type=str, nargs='?',
                        help='email subject', default='')
    parser.add_argument('-a', '--attach', help='attachment',
                        action='append', default=[])
    parser.add_argument('-y', '--yes', action='store_true',
                        help="whether to really send emails (set to 0) or just "
                             "output dry run to console")

    args = parser.parse_args()

    reader = csv.DictReader(sys.stdin)

    if 'email' not in reader.fieldnames:
        parser.exit(1, "Input CSV is expected to have a column named 'email\n\n'")

    if not args.subject and 'subject' not in reader.fieldnames:
        parser.exit(1, "You need to specify subject in the command line or "
                       "add a 'subject' column into the input CSV file\n\n")

    debug = not args.yes
    sender = Sender(settings.smtp_server, settings.username, settings.password,
                    settings.use_tls, settings.use_ssl, debug=debug)

    def clean_files(flist):
        if not flist:
            return []
        return [l for l in [f.strip() for f in flist.split("\n") if f] if l]

    for record in reader:
        subject = args.subject or record['subject']
        body = settings.template.format(**record)
        files = args.attach + clean_files(record.get('attachment'))
        # paths separated by newlines
        sender.send_mail(subject, body, [record['email']], files=files)

    if debug:
        print (
            "="*80, "\nThis is an example of emails that would be sent.\n"
            "If you want to really send them, add -y to the command.\n\n")
