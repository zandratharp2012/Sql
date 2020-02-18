"""
Utility methods for email messaging.
"""
import smtplib
import os
import logging

from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
from email.Utils import COMMASPACE, formatdate
from email import Encoders
from email.message import Message

def send(send_from, send_to, message, server="server goes here"):
    """Open an SMTP connection, send the message, and close the connection."""
    assert isinstance(message, Message)
    smtp = smtplib.SMTP(server)
    smtp.sendmail(send_from, send_to, message.as_string())
    smtp.close()

def make_mail(send_from, send_to, subject, text, files=[]):
    """Makes an plain text email message with attachments."""
    assert type(send_to)==list
    assert type(files)==list
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    msg.attach( MIMEText(text) )
    for f in files:
        part = MIMEBase('application', "octet-stream")
        part.set_payload( open(f,"rb").read() )
        Encoders.encode_base64(part)
        part.add_header('Content', 'attachment; filename="%s"' % os.path.basename(f))
        msg.attach(part)
    return msg

def send_mail(send_from, send_to, subject, text, files=[], server="server goes here"):
    """Sends a plain text email with attachements."""
    mail = make_mail(send_from, send_to, subject, text, files)
    send(send_from, send_to, mail, server)

def make_mail_html(send_from,send_to,subject,text,html):
    """Makes an HTML email message."""
    assert type(send_to)==list
    msg = MIMEMultipart('alternative')
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    msg.attach( MIMEText(text) )
    text_part = MIMEText(text,'plain')
    html_part = MIMEText(html,'html')
    msg.attach(text_part)
    msg.attach(html_part)
    return msg

def send_mail_html(send_from, send_to, subject, text, html, server="server goes here"):
    """Sends an HTML email message."""
    mail = make_mail_html(send_from, send_to, subject, text, html)
    send(send_from, send_to, mail, server)

def make_mail_files(send_from, send_to, subject, text, files=[]):
    """Makes an email message with attachments."""
    assert type(send_to)==list
    assert type(files)==list
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    msg.attach( MIMEText(text) )
    for f in files:
        part = MIMEBase('application', "octet-stream")
        part.set_payload( open(f,"rb").read() )
        Encoders.encode_base64(part)
        part.add_header('Content', 'attachment; filename="%s"' % os.path.basename(f))
        msg.attach(part)
    return msg

def send_mail_files(send_from, send_to, subject, text, files=[], server="server goes here"):
    """Sends an email with attachments."""
    mail = make_mail_files(send_from, send_to, subject, text, files)
    send(send_from, send_to, mail, server)

def make_mail_images(send_from,send_to,subject,text,images=[],cols=1,image_map=None,image_map_res=None) :
    """Makes an HTML email message with embedded images."""
    assert type(send_to)==list
    assert type(images)==list
    msg = MIMEMultipart('related')
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msgAlternative = MIMEMultipart('alternative')
    msg.attach(msgAlternative)
    msgText = MIMEText('Please view as HTML')
    msgAlternative.attach(msgText)

    if image_map is not None :
        rows = len(image_map)
        if image_map_res is not None :
            if rows != len(image_map_res) :
                print 'Must provide image_map and image_map_res with matching dimensions'
                return False
            for i in range(rows) :
                if len(image_map[i]) != len(image_map_res[i]) :
                    print 'Must provide image_map and image_map_res with matching dimensions'
                    return False
        res = ''
        html_body = '%s <br>'%text
        for i in range(len(image_map)) :
            for j in range(len(image_map[i])) :
                if image_map_res is not None :
                    res = ' width="%s" height="%s"'%image_map_res[i][j]
                html_body += '<img src="cid:image' + str(i) + '_' + str(j) + '"' + res + '>'
                img = open(image_map[i][j],'rb')
                msgImage = MIMEImage(img.read())
                img.close()
                msgImage.add_header('Content-ID', '<image' + str(i) + '_' + str(j) + '>')
                msg.attach(msgImage)
            html_body += '<br>'

    else :
        html_body = '%s <br>'%text
        for i in range(len(images)) :
            html_body += '<img src="cid:image' + str(i) + '">'
            img = open(images[i],'rb')
            msgImage = MIMEImage(img.read())
            img.close()
            msgImage.add_header('Content-ID', '<image' + str(i) + '>')
            msg.attach(msgImage)
            if i % cols == (cols-1) :
                html_body += '<br>'

    msgText = MIMEText(html_body,'html')
    msgAlternative.attach(msgText)
    return msg

def send_mail_images(send_from,send_to,subject,text,images=[],cols=1,image_map=None,image_map_res=None, server='server goes here'):
    """Sends an HTML email with embedded images."""
    mail = make_mail_images(send_from,send_to,subject,text,image_map=image_map,image_map_res=image_map_res)
    send(send_from, send_to, mail, server)


    