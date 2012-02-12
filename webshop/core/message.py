# -*- coding: utf-8 -*
#
# ePoint WebShop
# Copyright (C) 2011 - 2012 ePoint Systems Ltd
# Author: Andrey Martyanov
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.

from email.message import Message
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.encoders import encode_7or8bit, encode_noop

_boundary = '---=====xUS26BDIIEVkJEIgILh2sFo3eDFVXNi1TYrt=====---'


class EmptyHeaderMessage(Message):
    """
    Message without predefined headers
    """
    
    def __init__(self, text, charset=None, blank_line_after_header=False):
        Message.__init__(self)
        self.set_payload(text)
        self._blank_line_after_header = blank_line_after_header

    def _write_headers(self, gen):
        """
        By default a blank line always separates headers from body
        This function provides control of this behavior
        """
        for h, v in self.items():
            print >> gen._fp, '%s:' % h,
            if gen._maxheaderlen == 0:
                # Explicit no-wrapping
                print >> gen._fp, v
            elif isinstance(v, Header):
                # Header instances know what to do
                print >> gen._fp, v.encode()
            else:
                # Header's got lots of smarts, so use it.
                print >> gen._fp, Header(
                    v, maxlinelen=gen._maxheaderlen,
                    header_name=h, continuation_ws='\t').encode()
        if self._blank_line_after_header:
            print >> gen._fp


class TextMessage(EmptyHeaderMessage):
    """
    Plain text message, just for programming interface consistency
    """
    
    def __init__(self, from_address, to_address, subject, body):
        EmptyHeaderMessage.__init__(self, body, blank_line_after_header=True)
        self.add_header('Content-Type', 'text/plain')
        self.from_address = self['From'] = from_address
        self.to_address = self['To'] = to_address
        self['Subject'] = subject


class EncryptedMessage(object):
    """
    Reorganized into a binary one-pass signature document encrypted  message
    See RFC4880 for details
    """
    
    def __init__(self, ):
        raise NotImplementedError


class MIMESignedMessage(MIMEMultipart):
    """
    Clearsigned PGP/MIME message according to RFC3156
    """
    
    def __init__(self, from_address, to_address, subject, body, signature):
        MIMEMultipart.__init__(self, 'signed',
                               micalg='pgp-sha1',
                               boundary=_boundary,
                               protocol='application/pgp-signature')
        self.from_address = self['From'] = from_address
        self.to_address = self['To'] = to_address
        self['Subject'] = subject
        signed_data = EmptyHeaderMessage(body)
        self.attach(signed_data)
        signature = MIMEApplication(signature, 'pgp-signature; name="signature.asc"',
                                    encode_7or8bit)
        signature['Content-Description'] = 'OpenPGP digital signature'
        signature['Content-Disposition'] = 'attachment; filename="signature.asc"'
        self.attach(signature)


class MIMEEncryptedMessage(MIMEMultipart):
    """
    PGP/MIME encrypted message using encapsulation of PGP/MIME signed
    message method according to RFC3156
    """
    
    def __init__(self, from_address, to_address, subject, body):
        MIMEMultipart.__init__(self, 'encrypted',
                               boundary=_boundary,
                               protocol='application/pgp-encrypted')
        self.from_address = self['From'] = from_address
        self.to_address = self['To'] = to_address
        self['Subject'] = subject
        self.attach(MIMEApplication('Version: 1', 'pgp-encrypted', encode_7or8bit))
        encrypted = MIMEApplication(body, 'octet-stream; name="encrypted.asc"',
                                    encode_noop)
        encrypted['Content-Description'] = 'OpenPGP encrypted message'
        encrypted['Content-Disposition'] = 'inline; filename="encrypted.asc"'
        self.attach(encrypted)
