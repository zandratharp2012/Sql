from .email import send_mail_html
import pandas as pd
import datetime
from datetime import date, timedelta
import numpy as np
import click

#This function will send an email with a table that includes desired information
def setup():

    #Enter whatever desired in the brackets quotes or brackets for columns and details. 
	data = {'Date': ['2/11/2020'], 
        	'x': ['Good'], 
        	'y': ['Good'],
        	'z': ['Good'],
        	'a': ['Good'],
        	'b': ['Good'],
        	'c': ['Good']
           	} 

	df=pd.DataFrame(data)
    
    #This next dataframe will append second row with details desired. 
	df=df.append({'Date': 'Comments:' ,
		'x': '',
		'y': '',
		'z': '',
		'a': 'There are issues with this dashboard',
		'b': '',
		'c': ''},
		ignore_index=True)

	#---------------- Email Helper -------------#
	html_email_body_start = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
	  <html xmlns="http://www.w3.org/1999/xhtml">
	  <head>
	  <title> Title goes here </title>
	  <meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
	  <style type="text/css">
	  <!--
	body {
	      font: 12px/170% 'Lucida Grande', 'Lucida Sans Unicode',Geneva, Verdana, Sans-Serif;
	      font-size: 10pt;
	      color: #000000;
	      margin: 1;
	      padding: 0;
	      margin-right: auto;
	      margin-left: 1;
	}
	table {
	  border-collapse: collapse;
	  margin: 1;
	  border: 2px solid black;
	  margin-right:auto;
	  width: auto;
	  height: auto;
	}
	th, td {
	  text-align: Center;
	      font-size: 10pt;
	  border-width: 1px;
	    border-style: solid;
	  word-break;
	}
	tr:nth-child(odd){
	  background-color:#FFFFFF;
	}
	tr.t0
	{
	  color: #555;
	  background-color: #FFFFFF;
	  font-weight: bold;
	}
	th {
	  text-align: center;
	  color: #555;
	  background: #F0FBFF;
	  padding: .5em .5em;
	    border-color: #000000 #D8EBF5 #B9DBEE #D8EBF5
	}
	td {
	  padding: .2em .5em;
	  border-color: #EFEFEF;
	}
	td.text {
	  text-align: left;
	}
	}
	  -->
	  </style>
	  </head>
	  <body>"""

	html_df = df.to_html(index=False, justify='left') 
	email_text= ' '

	# Enter desired information in mail_message after table setup
	mail_message =  (email_text+html_email_body_start + html_df 
		+ '<br/> Type what you like here'
		+ '<br/> and here') 
	
	return mail_message

@click.command()
@click.option('--dry_run', is_flag=True, default=False, help='help menu')

def report(dry_run):
  """ Sends out email report with information desired """

  #Title your report 
  strFrom = 'Zandra Tharp <email address goes here>'
  subject = ' '
  email_subj = "Title subject goes here"

  mail_message=setup()
 
  #Modify email lists as desired. 
  if dry_run:
    listTo = ['Zandra Tharp <test email goes here>']
  else:
    listTo = ['y <final email goes here>']
  send_mail_html(strFrom,listTo,email_subj,"Please view as HTML",mail_message)



