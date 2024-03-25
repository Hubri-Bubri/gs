import PyPDF2
import collections
from time import gmtime, strftime
from datetime import datetime, timedelta, timezone

from base64 import b64encode
import urllib.request
from urllib.request import urlopen

import base64

import os

import io
import os.path
import time
import json
import sched
# Import smtplib for the actual sending function
import smtplib
import re
from PIL import Image
# Import the email modules we'll need
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders 

import imaplib

from aiohttp import web

from weasyprint import HTML, CSS
from jinja2 import Template

from aiohttp_jinja2 import template
from aiohttp_session import get_session
from uuid import uuid4
from aiohttp_security import remember, has_permission, login_required
from gs_security.authorization import check_credentials
# from gs_api.dictionary import (Application, User, Project, Projects, Offer, Invoice, add_same, Del_offer, Offers, Docs, Customer, Prices, Devices,
#                                Damage, Personals, Balance, Sub, add_same_sub, SubInvoice, Del_offer_sub, Reports, System)
from gs_api.dictionary import (User, Project, Projects, Offer, Invoice, add_same, Del_offer, Docs, Customer, Prices, Devices,
                               Damage, Personals, Balance, Sub, add_same_sub, SubInvoice, Reports, System)
from gs_api.langcore import language
from asyncio import ensure_future, gather, shield




from .environment import APPLICATION_DIR
ws_clients = []

routes = web.RouteTableDef()


@routes.get('/')
@template('index.html')
async def dashboard(request):
    return {'nocache': hash(uuid4())}

@routes.get('/profile')
async def profile(request):
    session = await get_session(request)
    return web.json_response(await User.select_profile(session.get('AIOHTTP_SECURITY'), request.query['subDomain']))

@routes.get('/variables')
async def method (request):
    return web.json_response(await Projects.variables())

@routes.get('/logout')
async def profile(request):
    # await session.close()
    session = await get_session(request)
    session.clear()
    # print(session)
    # session["AIOHTTP_SECURITY"] = None
    return web.json_response('')


@routes.get('/favicon.ico')
async def method (request):
    return web.json_response('')

@routes.get('/clear!')
async def method (request):
    await System.clear()
    return web.json_response('')

@routes.get('/fixed_items!')
async def method (request):
    await System.fixed_items()
    return web.json_response('')

@routes.get('/general!')
async def method (request):
    await System.general()
    return web.json_response('')

# @routes.get('/remove_empty_percent!')
# async def method (request):
#     await System.remove_empty_percent()
#     return web.json_response('')

@routes.get('/check_for_percent_transfer!')
async def method (request):
    await System.check_for_percent_transfer()
    return web.json_response('')

@routes.get('/percents!')
async def method (request):
    await System.percents()
    return web.json_response('')

@routes.post('/send_mail')
async def method (request):
    form = await request.json()
    senderFilename = form['filename']
    sender = form['from']
    to = form['to']
    subject = form['subject']
    content = form['content']
    senderFiles = form['files']

    pass_from_mail = await Docs.user_pass(sender)
    password = (pass_from_mail['pass_from_mail'])
    toaddr = []
    files = []
    docs = []
    ns=[]

    for reciver in to.split(','):
        toaddr.append(reciver)
    for file in senderFiles.split(','):
        arrfiles = file.split('-')
        if arrfiles[0] == 'f':
            files.append(arrfiles[1])
        if arrfiles[0] == 'd':
            docs.append(arrfiles[1])

    htmls = await Docs.select_split_doc(docs)

    split_files = await Docs.select_split_files(files)

    msg = MIMEMultipart() 
    msg['From'] = sender 
    msg['To'] = to 
    msg['Subject'] = subject
    body = """
    <html>
      <head></head>
      <body>
      """+content+"""
     </body>
    </html>
    """
    msg.attach(MIMEText(body, 'html')) 

    if senderFilename!='':
        html=''
        for i, item  in enumerate(htmls):
            if i < len(htmls)-1:
                html = html + item['html'] + '<div style="page-break-before:always;"></div>'
            else:
                html = html + item['html']

        html = re.sub("\\s+", " ", html.replace("\\n", '').replace("\\t", '').replace("\\", ""))

        pdf = HTML(string=html).write_pdf(stylesheets=[CSS(string='@page { size: A4; margin-top: 5mm; margin-left: 10mm; margin-right: 10mm; margin-bottom: 3mm; }')])
        file = bytes(pdf)
        pdf_file = io.BytesIO(file)
        pdfWriter = PyPDF2.PdfFileWriter()

        if htmls!=[]:
            fff = PyPDF2.PdfFileReader(pdf_file, strict=False)
            for pageNum in range(fff.numPages):
                pageObj = fff.getPage(pageNum)
                pdfWriter.addPage(pageObj)
        
        if split_files!=[]:
            for f in split_files:
                bf = bytes(f['content'])
                bf = io.BytesIO(bf)
                fr = PyPDF2.PdfFileReader(bf, strict=False)

                for pageNum in range(fr.numPages):
                    pageObj = fr.getPage(pageNum)
                    pdfWriter.addPage(pageObj)

        pdf_bytes = io.BytesIO()
        pdfWriter.write(pdf_bytes)
        pdf_bytes.seek(0)
        attachment = pdf_bytes
        
        if senderFiles != '_':
            p = MIMEBase('application', 'octet-stream') 
            p.set_payload((attachment).read()) 
            encoders.encode_base64(p)
            p.add_header('Content-Disposition', 'attachment', filename=os.path.basename(senderFilename.split('.pdf')[0]+'.pdf'))
            msg.attach(p)
    else:
        for dn in htmls:
            htmls = dn['html']
            html = re.sub("\\s+", " ", htmls.replace("'}{'html': '", '<div style="page-break-before:always;"></div>').replace("{'html': '", '').replace("'}", '').replace("\\n", '').replace("\\t", '').replace("\\", ""))
            pdf = HTML(string=html).write_pdf(stylesheets=[CSS(string='@page { size: A4; margin-top: 5mm; margin-left: 10mm; margin-right: 10mm; margin-bottom: 3mm; }')])

            file = bytes(pdf)
            pdf_file = io.BytesIO(file)
            pdfWriter = PyPDF2.PdfFileWriter()
            fff = PyPDF2.PdfFileReader(pdf_file, strict=False)

            for pageNum in range(fff.numPages):
                pageObj = fff.getPage(pageNum)
                pdfWriter.addPage(pageObj)

            pdf_bytes = io.BytesIO()
            pdfWriter.write(pdf_bytes)
            pdf_bytes.seek(0)
            attachment = pdf_bytes

            p = MIMEBase('application', 'octet-stream') 
            p.set_payload((attachment).read())
            encoders.encode_base64(p)
            p.add_header('Content-Disposition', 'attachment', filename=os.path.basename(dn['name']+'.pdf'))
            msg.attach(p)

        for f in split_files:
            pdfWriter = PyPDF2.PdfFileWriter()
            bf = bytes(f['content'])
            bf = io.BytesIO(bf)
            fr = PyPDF2.PdfFileReader(bf, strict=False)

            for pageNum in range(fr.numPages):
                pageObj = fr.getPage(pageNum)
                pdfWriter.addPage(pageObj)

            pdf_bytes = io.BytesIO()
            pdfWriter.write(pdf_bytes)
            pdf_bytes.seek(0)
            attachment = pdf_bytes

            p = MIMEBase('application', 'octet-stream') 
            p.set_payload((attachment).read())
            encoders.encode_base64(p)
            p.add_header('Content-Disposition', 'attachment', filename=os.path.basename(f['name']))
            msg.attach(p)

    s = smtplib.SMTP('mail.awe.do', 587)
    s.starttls()
    s.ehlo()
    s.login(sender, password)
    text = msg.as_string() 
    s.sendmail(sender, toaddr, text) 
    s.quit() 

    imap = imaplib.IMAP4('mail.awe.do', 143)
    imap.starttls()
    imap.login(sender, password)
    imap.select("Sent")
    imap.append('Sent', '', imaplib.Time2Internaldate(time.time()), text.encode('utf8'))
    imap.logout()

    return web.json_response('')


@routes.post('/plan_mail')
async def method (request):
    form = await request.json()
    item = form['item']
    period = form['period']
    sender = form['from']
    to = form['to']
    subject = form['subject']
    content = form['content']
    autosend = form['autosend']
    autodate = form['autodate']
    pushToWorkDays=form['pushToWorkDays']
    autoperiodworks = form['autoperiodworks']
    name = form['name']
    

    return web.json_response(await Docs.plan_mail(item,period,sender,to,subject,content,autosend,autodate,pushToWorkDays,autoperiodworks,name))

@routes.post('/replan_mail')
async def method (request):
    form = await request.json()
    item = form['item']
    period = form['period']
    sender = form['from']
    to = form['to']
    subject = form['subject']
    content = form['content']
    name = form['name']
    autosend = form['autosend']
    autodate = form['autodate']
    pushToWorkDays=form['pushToWorkDays']
    autoperiodworks = form['autoperiodworks']
    planId = form['id']

    return web.json_response(await Docs.replan_mail(item,period,sender,to,subject,content,name,autosend,autodate,pushToWorkDays,autoperiodworks,planId))

@routes.post('/remove_mail')
async def method (request):
    form = await request.json()
    planId = form['id']
    return web.json_response(await Docs.remove_mail(planId))

@routes.get('/start_mail_send') #auto send by timetable
async def method (request):
    return web.json_response(await Docs.start_mail_send(request, ws_clients))

@routes.get('/get_plan')
async def method (request):
    return web.json_response(await Docs.get_plan(request.query['id']))

@routes.get('/plan_exec')
async def method (request):
    return web.json_response(await Docs.plan_exec(request.query['id'], request, ws_clients))

@routes.get('/closeWasSent')
async def method (request):
    return web.json_response(await Docs.closeWasSent(request.query['wassentids']))

@routes.get('/get_addresbook')
async def method (request):
    return web.json_response(await Project.get_addresbook())
    
@routes.get('/countries')
async def method (request):
    return web.json_response(await Project.countries())

@routes.get('/project_detail')
async def method (request):
    return web.json_response(await Project.select_project(request.query['id']))

@routes.get('/project_user')
async def method (request):
    return web.json_response(await Project.project_user(request.query['id']))

@routes.get('/updateProjectTaxs')
async def method (request):
    result = web.json_response(await Project.updateProjectTaxs(
        request.query['id'],
        request.query['tax'],
        request.query['taxDub'],
        request.query['taxP'],
        request.query['taxPDub'],
        request.query['disc'],
        request.query['discP'],
        request.query['butDiscPerc'],
        request.query['addtaxColapse']
        ))
    for client in ws_clients:
        await client.send_str('getProjectDetail')
    return result



@routes.get('/get_types_for_tables')
async def method (request):
    return web.json_response(await Projects.get_types_for_tables())

@routes.get('/project_detail_new')
async def method (request):
    return web.json_response(await Projects.select_project_new(request.query['id']))

# @routes.get('/get_tables')
# async def method (request):
#     return web.json_response(await Projects.get_tables(request.query['id']))

@routes.get('/get_tables_for_docs')
async def method (request):
    return web.json_response(await Projects.get_tables_for_docs(request.query['id']))

@routes.get('/get_tables_in_edit')
async def method (request):
    return web.json_response(await Projects.get_tables_in_edit(request.query['id']))

@routes.get('/get_rows_in_table')
async def method (request):
    return web.json_response(await Projects.get_rows_in_table(request.query['id']))

@routes.get('/del_row_from_table')
async def method (request):
    await Projects.del_row_from_table(request.query['table_id'], request.query['index'], request.query['id'], request.query['item_id'], ws_clients)
    return web.json_response('')

@routes.get('/del_row_from_devices')
async def method (request):
    await Devices.del_row_from_devices(request.query['id'], request.query['tableId'], ws_clients)
    return web.json_response('')

@routes.get('/del_row_from_report')
async def method (request):
    web.json_response(await Reports.del_row_from_reports(request.query['id'], request.query['tableId'], ws_clients))
    return web.json_response('')

@routes.get('/delmeasrow')
async def method (request):
    await Devices.delmeasrow(request.query['id'], request.query['tableId'], ws_clients)
    return web.json_response('')

@routes.get('/del_row_from_damage')
async def method (request):
    await Damage.del_row_from_damage(request.query['id'], request.query['tableId'], ws_clients)
    return web.json_response('')

@routes.get('/addMeasrow')
async def method (request):
    await Devices.addMeasrow(request.query['id'], request.query['tableId'], ws_clients)
    return web.json_response('')

@routes.get('/addMeasureProtocolrow')
async def method (request):
    await Devices.addMeasureProtocolrow(request.query['id'], request.query['tableId'], ws_clients)
    return web.json_response('')
       
@routes.get('/measureProtocolDel')
async def method (request):
    await Devices.measureProtocolDel(request.query['id'], request.query['tableId'], ws_clients)
    return web.json_response('')
    
@routes.get('/updateDeviceList')
async def method (request):
    await Devices.updateDeviceList(request.query['tableId'], request.query['index'], request.query['newData'], request.query['fild'], request.query['id'], ws_clients)
    return web.json_response('')

@routes.get('/updateReportsList')
async def method (request):
    web.json_response(await Reports.updateReportList(request.query['newData'], request.query['fild'], request.query['id'], request.query['index'], request.query['tableId'], ws_clients))
    return web.json_response('')

@routes.get('/updateDamage')
async def method (request):
    await Damage.updateDamage(request.query['tableId'], request.query['index'], request.query['newData'], request.query['fild'], request.query['id'], ws_clients)
    return web.json_response('')


@routes.post('/updateImageDamage')
async def method (request):
    form = await request.json()
    id = form.get('params').get('id')
    newImage = form.get('params').get('newImage')
    schema = form.get('params').get('schema')
    # id = params.get('id')

    match = re.search(r'(.*):(.*);(.*)(,)(.*)', newImage)

    if not match:
        raise ValueError()

    _, content_type, _, _, content = match.groups()

    content = base64.b64decode(
        content.encode(),
    )

    await Damage.updateImageDamage(content, str(schema), id)
    for client in ws_clients:
        await client.send_str('updateImageDamage:'+str(id))
    return web.json_response('')

@routes.get('/updateDeviceIntern')
async def method (request):
    await Devices.updateDeviceIntern(request.query['subIndex'], request.query['index'], request.query['tableId'], request.query['newData'], request.query['fild'], request.query['id'], ws_clients)
    return web.json_response('')

@routes.get('/updateMeasureProtocol')
async def method (request):
    await Devices.updateMeasureProtocol(request.query['tableId'],request.query['index'],request.query['newData'], request.query['fild'], request.query['id'], ws_clients)
    return web.json_response('')

@routes.get('/update_part_device')
async def method (request):
    await Devices.update_part_device(request.query['part_name'], request.query['id'], ws_clients)
    return web.json_response('')



@routes.get('/update_id_in_one_table')
async def method (request):
    result = (await Projects.update_id_in_one_table(request.query['newIndex'], request.query['oldIndex'], request.query['newPart']))
    for client in ws_clients:
        await client.send_str('getProjectDetail')
    return result

# @routes.get('/update_id_in_one_table_reports')
# async def method (request):
#     result =  web.json_response(await Reports.update_id_in_one_table_reports(request.query['newIndex'], request.query['oldIndex'], request.query['newPart']))
#     for client in ws_clients:
#         await client.send_str('getProjectDetail')
#     return result

@routes.get('/update_id_in_one_damage')
async def method (request):
    await Damage.update_id_in_one_damage(request.query['newIndex'], request.query['oldIndex'], request.query['newPart'])
    # for client in ws_clients:
    #     await client.send_str('getProjectDetail')
    return web.json_response('')

@routes.get('/update_id_damage')
async def method (request):
    await Damage.update_id_damage(request.query['newIndex'], request.query['newPart'], request.query['oldIndex'], request.query['oldPart'])
    # for client in ws_clients:
    #     await client.send_str('getProjectDetail')
    return web.json_response('')

@routes.get('/update_id')
async def method (request):
    result =  web.json_response(await Projects.update_id(request.query['newIndex'], request.query['newPart'], request.query['oldIndex'], request.query['oldPart']))
    for client in ws_clients:
        await client.send_str('getProjectDetail')
    return result

@routes.get('/update_id_reports')
async def method (request):
    await Reports.update_id_reports(request.query['newIndex'], request.query['newPart'], request.query['oldIndex'], request.query['oldPart'])
    return web.json_response('')

@routes.get('/update_id_in_prise')
async def method (request):
    await Project.update_id_in_prise(request.query['newid'], request.query['oldid'])
    return web.json_response('')

@routes.get('/update_id_table')
async def method (request):
    result = web.json_response(await Projects.update_id_table(request.query['newIndex'], request.query['oldIndex'], request.query['id']))
    for client in ws_clients:
        await client.send_str('getProjectDetail')
    return result

@routes.post('/update_checkbox_table')
async def method (request):
    form = await request.json()
    uid = form['id']
    fild = form['fild']
    data = form['data']
    result = web.json_response(await Projects.update_checkbox_table(uid, fild, data))
    for client in ws_clients:
        await client.send_str('getProjectDetail')
    return result

@routes.get('/changeDisableTable')
async def method (request):
    # print(ws_clients)
    await Projects.changeDisableTable(
        request.query['type_operation'], request.query['fild'], request.query['id'], request.query['user'], ws_clients)

    for client in ws_clients:
        await client.send_str('getLoocks')
    return web.json_response('')

@routes.get('/getLoocks')
async def method (request):
     return web.json_response(await Projects.getLoocks())


# @routes.get('/paypal')
# async def method (request):
#     # with urllib.request.urlopen("https://www.paypal.com/de/signin") as url:
#     #     s = url.read()
#     #     # I'm guessing this would output the html source code ?
    
#     # print(str(s))
#     fp = urllib.request.urlopen("https://www.paypal.com/de/signin")
#     mybytes = fp.read()
#     mystr = mybytes.decode("utf8")
#     fp.close()

#     mystr = mystr.replace('<head>', '<head><base target="_self"> ')
#     mystr = mystr.replace('="/', '="/bfiles?url=/')
#     mystr = mystr.replace(':"/', ':"/bfiles?url=/')
#     mystr = mystr.replace('if (self === top || isEligibleIntegration()) {var antiClickjack = document.getElementById("antiClickjack");if (antiClickjack) {antiClickjack.parentNode.removeChild(antiClickjack);}} else {top.location = self.location;}', '')
    
#     print(mystr)
#     return web.json_response(mystr)

@routes.get('/bfiles')
async def method (request):
    url = request.query['url']
    fp = urllib.request.urlopen("https://www.paypal.com"+url)
    mybytes = fp.read()
    # print('run')
    resp = web.StreamResponse(headers={
         'CONTENT-DISPOSITION': 'inline'
        })
    resp.content_type ="text/html"

    await resp.prepare(request)
    await resp.write(mybytes)
    return resp

@routes.get('/get_damage')
async def method (request):
    return web.json_response(await Projects.get_damage(request.query['id']))


@routes.get('/domage_images')
async def method (request):
    return web.json_response(await Projects.get_damage_images(request.query['id'], request.query['project']))

@routes.get('/get_files_company')
async def method (request):
    return web.json_response(await Projects.get_files_company(request.query['id']))

@routes.get('/domage_images_customer')
async def method (request):
    return web.json_response(await Projects.get_damage_images_customer(request.query['id']))

@routes.get('/domage_images_person')
async def method (request):
    return web.json_response(await Projects.get_damage_images_person(request.query['id']))

@routes.get('/get_files_firma')
async def method (request):
    return web.json_response(await Projects.get_files_firma(request.query['id']))

@routes.get('/get_files_spreson')
async def method (request):
    return web.json_response(await Projects.get_files_spreson(request.query['id']))

@routes.get('/get_files_customer')
async def method (request):
    return web.json_response(await Projects.get_files_customer(request.query['id']))

@routes.get('/get_files_preson')
async def method (request):
    return web.json_response(await Projects.get_files_preson(request.query['id']))

@routes.get('/get_images')
async def method (request):
    return web.json_response(await Projects.get_images(request.query['id']))

@routes.get('/change_type')
async def method (request):
    result =  web.json_response(await Projects.change_type(request.query['id'], request.query['type']))
    for client in ws_clients:
        await client.send_str('get_types_for_tables_f')
    return result

@routes.get('/customers')
async def method (request):
    return web.json_response(await Project.select_customers(request.query['old']))
@routes.get('/person_date')
async def method (request):
    return web.json_response(await Project.select_person_date(request.query['old']))

@routes.get('/mails')
async def method (request):
    return web.json_response(await Project.select_mails(request.query['id']))

@routes.get('/phons')
async def method (request):
    return web.json_response(await Project.select_phons(request.query['id']))

@routes.get('/faxs')
async def method (request):
    return web.json_response(await Project.select_faxs(request.query['id']))
  
@routes.get('/projects')
async def method (request):
    return web.json_response(await Projects.select_projects(request.query['done']))
    # return web.json_response(await Projects.select_projects(request.query['page']))
@routes.get('/date_logo')
async def method (request):
    return web.json_response(await Docs.date_logo())

@routes.get('/customer')
async def method (request):
    return web.json_response(await Customer.select_customers())

@routes.get('/customer_sub')
async def method (request):
    return web.json_response(await Customer.select_customers_sub())

@routes.get('/get_sub_emails')
async def method (request):
    return web.json_response(await Customer.get_sub_emails(request.query['factory']))


@routes.get('/add_project')
async def method (request):
    result = web.json_response(await Projects.add_project(strftime("%Y", gmtime()), strftime("%Y-%m-%d", gmtime()), request.query['contry'], request.query['area'], request.query['city'], request.query['street'], request.query['zip'], request.query['user']))
    for client in ws_clients:
        await client.send_str('getProjects')
    return result

@routes.post('/updateProject')
async def method (request):
    form = await request.json()
    uid = form['id']
    date = form['date']
    fild = form['fild']
    try:
        result = web.json_response(await Project.update(uid, date, fild))
    except KeyError:
        try:
            return web.json_response('')
        except KeyError:
            return web.json_response('')

    fild = str(fild)
    updateProjectSend = ''

    # if((fild == 'person_id') | (fild == 'mail') | (fild == 'phone') | (fild == 'fax')):
    #     # updateProjectSend = 'get_person' #get_person
   
    if((fild == 'area') | (fild == 'zip1') | (fild == 'city1') | (fild == 'street1') | (fild == 'date') | (fild == 'other')):
        updateProjectSend = 'getProjectDetail'

    for client in ws_clients:
        await client.send_str(str(updateProjectSend))
    return result

@routes.get('/add_contact')
async def method (request):
    result= web.json_response(await Project.add_contact(request.query['type'], request.query['val'], request.query['person'], request.query['sel'], request.query['project']))
    for client in ws_clients:
        await client.send_str('get_person')
    return result

@routes.get('/table_data')
async def method (request):
    return web.json_response(await Project.table_data(request.query['id']))

@routes.get('/invoice_data_table')
async def method (request):
    return web.json_response(await Project.invoice_data_table(request.query['id']))

@routes.get('/update_table_data')
async def method (request):
    await Project.update_table_data(request.query['table_id'], request.query['id'], request.query['fild'], request.query['data'], request.query['index'], True, ws_clients)
    return web.json_response('')

@routes.get('/chenge_unit_type')
async def method (request):
    await Project.chenge_unit_type(request.query['table_id'], request.query['id'], request.query['data'], request.query['index'], request.query['item_id'], ws_clients)
    return web.json_response('')

@routes.get('/checked_for_percent')
async def method (request):
    await Project.checked_for_percent(request.query['table_id'], request.query['id'], request.query['event'], request.query['index'],
                                      request.query['part_percent'], request.query['old'], request.query['item_id'], True, ws_clients)
    return web.json_response('')

@routes.get('/update_for_summ')
async def method (request):
    await Project.update_for_summ(request.query['table_id'], request.query['id'], request.query['fild'], request.query['data'], request.query['index'], request.query['item_id'], True, ws_clients)
    return web.json_response('')

@routes.get('/send_discont')
async def method (request):
    await Project.send_discont(request.query['table_id'], request.query['id'], request.query['data'], request.query['index'], request.query['item_id'], ws_clients)
    return web.json_response('')
@routes.get('/send_mode_calc')
async def method (request):
    await Project.send_mode_calc(request.query['table_id'], request.query['id'], request.query['data'], request.query['index'], request.query['item_id'], ws_clients)
    return web.json_response('')
@routes.get('/chenge_tax')
async def method (request):
    await Project.chenge_tax(request.query['table_id'], request.query['id'], request.query['data'], request.query['index'], request.query['item_id'], ws_clients)
    return web.json_response('')
@routes.get('/update_table_data_editor')
async def method (request):
    return web.json_response(await Project.update_table_data(request.query['id'], request.query['fild'], request.query['data']))



@routes.get('/get_units')
async def method (request):
    return web.json_response(await Project.get_units())

@routes.get('/add_part_form_price')
async def method (request):
     result = web.json_response(
        await Project.add_part_form_price(
            request.query['part_name'], request.query['type'], request.query['item_id'],
            request.query['position_number'], request.query['description_head'], request.query['description_work'],
            request.query['description_from_price'], request.query['count'], request.query['discount'], request.query['price'], request.query['status'], request.query['alttax'],
            request.query['summa'], request.query['unit'], request.query['without']
            ))
#     # for client in ws_clients:
#     #     await client.send_str('getProjectDetail')
     return result
    
@routes.get('/add_person1')
async def method (request):
    return web.json_response(await Project.add_person1())


@routes.get('/add_person')
async def method (request):
    result=web.json_response(
        await Project.add_person(
            request.query['name'].replace(',', ' '), request.query['other'],
            request.query['appeal'],
            request.query['dep'],
            request.query['pos'],
            request.query['firm'],
            request.query['fax'],
            request.query['phone'],
            request.query['mail']
            )
        )

    for client in ws_clients:
        await client.send_str('get_persons')
    return result

@routes.get('/add_customer')
async def method (request):
    result=web.json_response(
        await Project.add_custom(
            request.query['name'],
            request.query['zip'],
            request.query['city'],
            request.query['tax'],
            request.query['web'],
            request.query['bic'],
            request.query['iban'],
            request.query['other'],
            request.query['mail'],
            request.query['phone'],
            request.query['fax'],
            request.query['street'],
            )
        )

    for client in ws_clients:
        await client.send_str('getProjectDetail')
    return result

@routes.get('/add_part')
async def method (request):
    await Project.add_part(request.query['parts_names'], request.query['item_id'], request.query['pid'], ws_clients)
    return web.json_response('')

@routes.get('/update_part')
async def method (request):
    await Project.update_part(request.query['part_name'], request.query['id'], ws_clients)
    return web.json_response('')

@routes.get('/checnge_count_percent')
async def method (request):
    await Project.checnge_count_percent(request.query['unitPercent'], request.query['dir'], request.query['row_id'], request.query['table_id'], ws_clients)
    return web.json_response('')

@routes.get('/table_delete')
async def method (request):
    await Project.table_delete(request.query['id'], request.query['item_id'], ws_clients)
    return web.json_response('')



@routes.get('/updateNameDevice')
async def method (request):
    result= web.json_response(await Project.updateNameDevice(request.query['nameDevice'], request.query['id']))
    for client in ws_clients:
        await client.send_str('getProjectDetail')
    return result

@routes.get('/updateNameReport')
async def method (request):
    result= web.json_response(await Reports.updateNameReport(request.query['nameReport'], request.query['id']))
    for client in ws_clients:
        await client.send_str('getProjectDetail')
    return result

@routes.get('/delImageFromPart')
async def method (request):
    web.json_response(await Damage.delImageFromPart(request.query['tableId'], ws_clients))
    return web.json_response('')

@routes.get('/add_group_damage')
async def method (request):
    result= web.json_response(await Project.add_group_damage(request.query['item_id']))
    for client in ws_clients:
        await client.send_str('getProjectDetail')
    return result

@routes.get('/damage_update')
async def method (request):
    result= web.json_response(await Project.damage_update(request.query['fild'], request.query['event'], request.query['id']))
    for client in ws_clients:
        await client.send_str('getProjectDetail')
    return result

@routes.get('/update_task')
async def method (request):
    # print(request.query['data'], request.query['fild'], request.query['id'])
    result= web.json_response(await Docs.update_task(request.query['data'], request.query['fild'], request.query['id']))
    for client in ws_clients:
        await client.send_str('getProjectDetail')
    return result


@routes.get('/add_task')
async def method (request):
    result = web.json_response(await Docs.add_task(request.query['name'], request.query['id'], request.query['start'], request.query['end']))
    for client in ws_clients:
        await client.send_str('getProjectDetail')
    return result

@routes.get('/task_time_damage')
async def method (request):
    result = web.json_response(await Docs.task_time_damage(request.query['id']))
    for client in ws_clients:
        await client.send_str('getProjectDetail')
    return result

@routes.get('/workers_task')
async def method (request):
    result = web.json_response(await Project.workers_task(request.query['workers'], request.query['id']))
    for client in ws_clients:
        await client.send_str('getProjectDetail')
    return result


@routes.get('/add_customer_list')
async def method (request):
    result= web.json_response(await Customer.add_customer_list(strftime("%Y-%m-%d", gmtime())))
    for client in ws_clients:
        await client.send_str('getCustomers')
    return result

@routes.get('/add_customer_sub_list')
async def method (request):
    return web.json_response(await Customer.add_customer_sub_list(strftime("%Y-%m-%d", gmtime())))

@routes.get('/customer_old')
async def method (request):
    result=web.json_response(
        await Customer.customer_old(
            request.query['id'],
            request.query['event']
            )
        )

    for client in ws_clients:
        await client.send_str('getCustomers')
    return result

@routes.get('/customer_detail')
async def method (request):
    return web.json_response(await Customer.select_customer(request.query['id']))

@routes.get('/get_persons')
async def method (request):
    return web.json_response(await Customer.select_persons(request.query['id']))

@routes.get('/updateCustomer')
async def method (request):

    result= web.json_response(await Customer.update(request.query['id'], request.query['date'], request.query['fild']))
    
    for client in ws_clients:
        await client.send_str('getCustomerDetail')
    return result

@routes.get('/get_contactData')
async def method (request):
    return web.json_response(await Customer.select_customer_contact(request.query['fild'], request.query['customer']))

@routes.get('/add_contact_from_customer')
async def method (request):
    return web.json_response(await Customer.add_customer_contact(request.query['type'], request.query['val'], request.query['id']))

@routes.get('/updateContact')
async def method (request):
    # print(request.query['id'], request.query['date'], request.query['type'])

    result= web.json_response(await Customer.updateContact(request.query['id'], request.query['date'], request.query['type']))
    for client in ws_clients:
        await client.send_str('getSubDetail')
    return result
    
@routes.get('/updatePerson')
async def method (request):
    result= web.json_response(await Customer.updatePerson(request.query['id'], request.query['data'], request.query['fild']))
    for client in ws_clients:
        await client.send_str('getCustomerDetail')
    return result

@routes.get('/del_person')
async def method (request):
    result =  web.json_response(await Customer.del_person(request.query['id']))
    for client in ws_clients:
        await client.send_str('get_persons')
    return result

@routes.get('/get_contact_person')
async def method (request):
    return  web.json_response(await Customer.get_contact_person(request.query['id']))

@routes.get('/edit_contact_person')
async def method (request):
    result = web.json_response(await Customer.edit_contact_person(request.query['fild'], request.query['value'], request.query['id'], request.query['type']))
    if request.query['type']=='person':
        update = 'getCustomerContact'
    if request.query['type']=='personal':
        update = 'getPersonal'

    for client in ws_clients:
        await client.send_str(update)
    return result

@routes.get('/contact_in_person_remove_row')
async def method (request):
    result = web.json_response(await Customer.contact_in_person_remove_row(request.query['fild'], request.query['id'], request.query['value'], request.query['type']))
    if request.query['type']=='person':
        update = 'getCustomerContact'
    if request.query['type']=='personal':
        update = 'getPersonal'

    for client in ws_clients:
        await client.send_str(update)
    return result

@routes.get('/offer')
async def method (request):
    return web.json_response(await Offer.select_offer(request.query['id']))

@routes.get('/invoice')
async def method (request):
    return web.json_response(await Invoice.select_invoice(request.query['id']))

@routes.get('/detect_invoice')
async def method (request):
    return web.json_response(await Invoice.detect_invoice())

@routes.get('/get_reports')
async def method (request):
    return web.json_response(await Invoice.get_reports(request.query['id']))

@routes.get('/add_invoice')
async def method (request):
    result = web.json_response(await Invoice.add_invoice(request.query['id'], request.query['type'], request.query['number'], request.query['newRange'], request.query['labelForDelete']))
    for client in ws_clients:
        await client.send_str('get_types_for_tables_f')
    return result

@routes.get('/add_same')
async def method (request):
    return web.json_response(await add_same.add_same(
        request.query['add_number'],
        request.query['add_work'],
        request.query['add_insurance_number'],
        request.query['add_place'],
        request.query['add_comment'],
        request.query['add_project_id'],
        request.query['type'],
        ))
    
@routes.get('/del_item')
async def method (request):
    await Del_offer.del_item(request.query['id'], ws_clients)
    return web.json_response('')
    
    
# @routes.get('/offers')
# async def method (request):
#     return web.json_response(await Offers.select_offers(request.query['id']))

@routes.get('/invoices')
async def method (request):
    return web.json_response(await Invoice.select_invoices(request.query['id']))

@routes.get('/reports')
async def method (request):
    return web.json_response(await Reports.select_reports(request.query['id']))

@routes.get('/prices')
async def method (request):
    return web.json_response(await Prices.select_prices(request.query['id']))

@routes.get('/devices')
async def method (request):
    return web.json_response(await Devices.select_devices(request.query['id']))

@routes.get('/get_tables_in_devices')
async def method (request):
    return web.json_response(await Devices.get_tables_in_devices(request.query['id']))

@routes.get('/get_device_list')
async def method (request):
    return web.json_response(await Devices.get_device_list(request.query['id']))

@routes.get('/get_MeasureProtocol_list')
async def method (request):
    return web.json_response(await Devices.get_MeasureProtocol_list(request.query['id']))

@routes.get('/show_docs')
async def method (request):
    return web.json_response('')

@routes.get('/show_imgs')
async def method (request):
    return web.json_response('')
    # return web.json_response(await Docs.show_docs(request.query['id']))

@routes.get('/price_menu')
async def method (request):
    return web.json_response(await Prices.price_menu())

@routes.get('/devices_menu')
async def method (request):
    return web.json_response(await Devices.devices_menu())

@routes.get('/docs_menu')
async def method (request):
    return web.json_response(await Docs.docs_menu(request.query['project']))

@routes.get('/images_menu')
async def method (request):
    return web.json_response(await Docs.images_menu(request.query['project']))

@routes.get('/docs_customer_menu')
async def method (request):
    return web.json_response(await Docs.docs_customer_menu(request.query['project']))

@routes.get('/docs_sub_menu')
async def method (request):
    return web.json_response(await Docs.docs_sub_menu(request.query['project']))

@routes.get('/docs_sperson_menu')
async def method (request):
    return web.json_response(await Docs.docs_sperson_menu(request.query['project']))

@routes.get('/docs_person_menu')
async def method (request):
    return web.json_response(await Docs.docs_person_menu(request.query['project']))

@routes.get('/docs_personal_menu')
async def method (request):
    return web.json_response(await Docs.docs_personal_menu(request.query['project']))

# @routes.get('/get_files_sperson')
# async def method (request):
#     return web.json_response(await Docs.get_files_sperson(request.query['project']))

@routes.get('/change_parrent_menu')
async def method (request):
    result = web.json_response(await Prices.change_parrent_menu(request.query['drag1'], request.query['drag2']))
    for client in ws_clients:
        await client.send_str('getPrices')
    return result

@routes.get('/change_parrent_menu_devices')
async def method (request):
    result = web.json_response(await Devices.change_parrent_menu_devices(request.query['drag1'], request.query['drag2']))
    for client in ws_clients:
        await client.send_str('getDevices')
    return result

@routes.get('/add_price_menu')
async def method (request):
    result = web.json_response(await Prices.add_price_menu(request.query['parent_id']))
    for client in ws_clients:
        await client.send_str('getPrices')
    return result

@routes.get('/add_devices_menu')
async def method (request):
    result = web.json_response(await Devices.add_devices_menu(request.query['parent_id']))
    for client in ws_clients:
        await client.send_str('getDevices')
    return result

@routes.get('/add_report_menu')
async def method (request):
    result = web.json_response(await Reports.add_reports_menu(request.query['parent_id']))
    for client in ws_clients:
        await client.send_str('getReports')
    return result

@routes.get('/reports_menu')
async def method (request):
    return web.json_response(await Reports.reports_menu())

@routes.get('/add_docs_menu')
async def method (request):
    result = web.json_response(await Docs.add_docs_menu(request.query['parent_id'], request.query['project'], request.query['newName']))
    for client in ws_clients:
        await client.send_str('getDocs')
    return result

@routes.get('/add_images_menu')
async def method (request):
    result = web.json_response(await Docs.add_images_menu(request.query['parent_id'], request.query['project'], request.query['newName']))
    for client in ws_clients:
        await client.send_str('getDocs')
    return result

@routes.get('/add_images_person_menu')
async def method (request):
    result = web.json_response(await Docs.add_images_person_menu(request.query['parent_id'], request.query['project'], request.query['newName']))
    for client in ws_clients:
        await client.send_str('getSpersonFiles')
    return result

@routes.get('/add_images_sperson_menu')
async def method (request):
    result = web.json_response(await Docs.add_images_sperson_menu(request.query['parent_id'], request.query['project'], request.query['newName']))
    for client in ws_clients:
        await client.send_str('getPersonFiles')
    return result

@routes.get('/add_docs_sub_menu')
async def method (request):
    result = web.json_response(await Docs.add_docs_sub_menu(request.query['parent_id'], request.query['project']))
    for client in ws_clients:
        await client.send_str('getSubFiles')
    return result

@routes.get('/add_images_sub_menu')
async def method (request):
    result = web.json_response(await Docs.add_images_sub_menu(request.query['parent_id'], request.query['project']))
    for client in ws_clients:
        await client.send_str('getSubFiles')
    return result

@routes.get('/add_images_customer_menu')
async def method (request):
    result = web.json_response(await Docs.add_images_customer_menu(request.query['parent_id'], request.query['project']))
    for client in ws_clients:
        await client.send_str('getCustomerFiles')
    return result

@routes.get('/images_sub_menu')
async def method (request):
    return web.json_response(await Docs.images_sub_menu(request.query['project']))

@routes.get('/images_customer_menu')
async def method (request):
    return web.json_response(await Docs.images_customer_menu(request.query['project']))

@routes.get('/images_person_menu')
async def method (request):
    return web.json_response(await Docs.images_person_menu(request.query['project']))

@routes.get('/images_customer_person_menu')
async def method (request):
    return web.json_response(await Docs.images_customer_person_menu(request.query['project']))

@routes.get('/add_sperson_menu')
async def method (request):
    result = web.json_response(await Docs.add_sperson_menu(request.query['parent_id'], request.query['project']))
    for client in ws_clients:
        await client.send_str('getSpersonFiles')
    return result

@routes.get('/add_docs_customer_menu')
async def method (request):
    result = web.json_response(await Docs.add_docs_customer_menu(request.query['parent_id'], request.query['project']))
    for client in ws_clients:
        await client.send_str('getCustomerFiles')
    return result

@routes.get('/add_person_menu')
async def method (request):
    result = web.json_response(await Docs.add_person_menu(request.query['parent_id'], request.query['project']))
    for client in ws_clients:
        await client.send_str('getPersonFiles')
    return result

@routes.get('/add_docs_personal_menu')
async def method (request):
    result = web.json_response(await Docs.add_docs_personal_menu(request.query['parent_id'], request.query['project']))
    for client in ws_clients:
        await client.send_str('getPersonalFiles')
    return result

@routes.get('/add_price_menu1')
async def method (request):
    return web.json_response(await Prices.add_price_menu1()) 


@routes.get('/update_name_reports_menu')
async def method (request):
    result = web.json_response(await Reports.update_name_reports_menu(request.query['name'], request.query['id']))
    for client in ws_clients:
        await client.send_str('getReports')
    return result

@routes.get('/update_name_price_menu')
async def method (request):
    result = web.json_response(await Prices.update_name_price_menu(request.query['name'], request.query['id']))
    for client in ws_clients:
        await client.send_str('getPrices')
    return result

@routes.get('/update_name_devices_menu')
async def method (request):
    result = web.json_response(await Devices.update_name_devices_menu(request.query['name'], request.query['id']))
    for client in ws_clients:
        await client.send_str('getDevices')
    return result

@routes.get('/update_name_docs_menu')
async def method (request):
    result = web.json_response(await Docs.update_name_docs_menu(request.query['name'], request.query['id']))
    for client in ws_clients:
        await client.send_str('getDocs')
    return result

@routes.get('/update_name_images_menu')
async def method (request):
    result = web.json_response(await Docs.update_name_images_menu(request.query['name'], request.query['id']))
    for client in ws_clients:
        await client.send_str('getDocs')
    return result

@routes.get('/update_name_images_person_menu')
async def method (request):
    result = web.json_response(await Docs.update_name_images_person_menu(request.query['name'], request.query['id']))
    for client in ws_clients:
        await client.send_str('getSpersonFiles')
    return result

@routes.get('/update_name_images_sperson_menu')
async def method (request):
    result = web.json_response(await Docs.update_name_images_sperson_menu(request.query['name'], request.query['id']))
    for client in ws_clients:
        await client.send_str('getPersonFiles')
    return result

@routes.get('/update_name_images_sub_menu')
async def method (request):
    result = web.json_response(await Docs.update_name_images_sub_menu(request.query['name'], request.query['id']))
    for client in ws_clients:
        await client.send_str('getSubFiles')
    return result

@routes.get('/update_name_images_customer_menu')
async def method (request):
    result = web.json_response(await Docs.update_name_images_customer_menu(request.query['name'], request.query['id']))
    for client in ws_clients:
        await client.send_str('getCustomerFiles')
    return result

@routes.get('/update_name_docs_sub_menu')
async def method (request):
    result = web.json_response(await Docs.update_name_docs_sub_menu(request.query['name'], request.query['id']))
    for client in ws_clients:
        await client.send_str('getSubFiles')
    return result

@routes.get('/update_name_sperson_menu')
async def method (request):
    result = web.json_response(await Docs.update_name_sperson_menu(request.query['name'], request.query['id']))
    for client in ws_clients:
        await client.send_str('getSpersonFiles')
    return result

@routes.get('/update_name_docs_customer_menu')
async def method (request):
    result = web.json_response(await Docs.update_name_docs_customer_menu(request.query['name'], request.query['id']))
    for client in ws_clients:
        await client.send_str('getCustomerFiles')
    return result

@routes.get('/update_name_person_menu')
async def method (request):
    result = web.json_response(await Docs.update_name_person_menu(request.query['name'], request.query['id']))
    for client in ws_clients:
        await client.send_str('getPersonFiles')
    return result

@routes.get('/update_name_docs_personal_menu')
async def method (request):
    result = web.json_response(await Docs.update_name_docs_personal_menu(request.query['name'], request.query['id']))
    for client in ws_clients:
        await client.send_str('getPersonalFiles')
    return result

@routes.get('/add_report')
async def method (request):
    result = web.json_response(await Reports.add_reports(request.query['id']))
    for client in ws_clients:
        await client.send_str('getReports')
    return result

@routes.get('/add_price')
async def method (request):
    result = web.json_response(await Prices.add_price(request.query['id']))
    for client in ws_clients:
        await client.send_str('getPrices')
    return result

@routes.get('/add_devices')
async def method (request):
    result = web.json_response(await Devices.add_devices(request.query['id']))
    for client in ws_clients:
        await client.send_str('getDevices')
    return result


@routes.get('/remove_report_menu')
async def method (request):
    result = web.json_response(await Reports.remove_reports_menu(request.query['remove_id']))
    for client in ws_clients:
        await client.send_str('getReports')
    return result

@routes.get('/remove_report')
async def method (request):
    result = web.json_response(await Reports.remove_reports(request.query['id']))
    for client in ws_clients:
        await client.send_str('getReports')
    return result

@routes.get('/remove_price')
async def method (request):
    result = web.json_response(await Prices.remove_price(request.query['id']))
    for client in ws_clients:
        await client.send_str('getPrices')
    return result

@routes.get('/remove_devices')
async def method (request):
    result = web.json_response(await Devices.remove_devices(request.query['id']))
    for client in ws_clients:
        await client.send_str('getDevices')
    return result

@routes.get('/remove_price_menu')
async def method (request):
    result = web.json_response(await Prices.remove_price_menu(request.query['remove_id']))
    for client in ws_clients:
        await client.send_str('getPrices')
    return result

@routes.get('/remove_devices_menu')
async def method (request):
    result = web.json_response(await Devices.remove_devices_menu(request.query['remove_id']))
    for client in ws_clients:
        await client.send_str('getDevices')
    return result

@routes.get('/remove_docs_menu')
async def method (request):
    result = web.json_response(await Docs.remove_docs_menu(request.query['remove_id']))
    for client in ws_clients:
        await client.send_str('getDocs')
    return result

@routes.get('/remove_image_menu')
async def method (request):
    result = web.json_response(await Docs.remove_image_menu(request.query['remove_id']))
    for client in ws_clients:
        await client.send_str('getDocs')
    return result

@routes.get('/remove_image_sperson_menu')
async def method (request):
    result = web.json_response(await Docs.remove_image_sperson_menu(request.query['remove_id']))
    for client in ws_clients:
        await client.send_str('getPersonFiles')
    return result

@routes.get('/remove_image_customer_menu')
async def method (request):
    result = web.json_response(await Docs.remove_image_customer_menu(request.query['remove_id']))
    for client in ws_clients:
        await client.send_str('getCustomerFiles')
    return result

@routes.get('/remove_image_person_menu')
async def method (request):
    result = web.json_response(await Docs.remove_image_person_menu(request.query['remove_id']))
    for client in ws_clients:
        await client.send_str('getSpersonFiles')
    return result

@routes.get('/remove_image_sub_menu')
async def method (request):
    result = web.json_response(await Docs.remove_image_sub_menu(request.query['remove_id']))
    for client in ws_clients:
        await client.send_str('getSubFiles')
    return result


@routes.get('/remove_docs_sperson_menu')
async def method (request):
    result = web.json_response(await Docs.remove_docs_sperson_menu(request.query['remove_id']))
    for client in ws_clients:
        await client.send_str('getSpersonFiles')
    return result

@routes.get('/remove_docs_sub_menu')
async def method (request):
    result = web.json_response(await Docs.remove_docs_sub_menu(request.query['remove_id']))
    for client in ws_clients:
        await client.send_str('getSubFiles')
    return result

@routes.get('/remove_docs_person_menu')
async def method (request):
    result = web.json_response(await Docs.remove_docs_person_menu(request.query['remove_id']))
    for client in ws_clients:
        await client.send_str('getPersonFiles')
    return result

@routes.get('/remove_docs_customer_menu')
async def method (request):
    result = web.json_response(await Docs.remove_docs_customer_menu(request.query['remove_id']))
    for client in ws_clients:
        await client.send_str('getCustomerFiles')
    return result

@routes.get('/remove_docs_personal_menu')
async def method (request):
    result = web.json_response(await Docs.remove_docs_personal_menu(request.query['remove_id']))
    for client in ws_clients:
        await client.send_str('getPersonalFiles')
    return result


@routes.get('/update_report')
async def method (request):
    result = web.json_response(await Reports.update_reports(request.query['data'], request.query['fild'], request.query['id']))
    for client in ws_clients:
        await client.send_str('getReports')
    return result

@routes.get('/update_price')
async def method (request):
    result = web.json_response(await Prices.update_price(request.query['data'], request.query['fild'], request.query['id']))
    for client in ws_clients:
        await client.send_str('getPrices')
    return result

@routes.get('/update_devices')
async def method (request):
    result = web.json_response(await Devices.update_devices(request.query['data'], request.query['fild'], request.query['id']))
    for client in ws_clients:
        await client.send_str('getDevices')
    return result

@routes.get('/cp_mv_to_report')
async def method (request):
    result = web.json_response(await Reports.cp_mv_to_reports(request.query['reports_ids'], request.query['new_menu'], request.query['operation']))
    for client in ws_clients:
        await client.send_str('getReports')
    return result

@routes.get('/get_tables_in_reports')
async def method (request):
    return web.json_response(await Reports.get_tables_in_reports(request.query['id']))

@routes.get('/cp_mv_to_price')
async def method (request):
    result = web.json_response(await Prices.cp_mv_to_price(request.query['price_ids'], request.query['new_menu'], request.query['operation']))
    for client in ws_clients:
        await client.send_str('getPrices')
    return result

@routes.get('/mv_docs')
async def method (request):
    result = web.json_response(await Docs.mv_docs(request.query['docs_ids'], request.query['files_ids'], request.query['new_menu']))
    for client in ws_clients:
        await client.send_str('getDocs')
    return result

@routes.get('/mv_images')
async def method (request):
    result = web.json_response(await Docs.mv_images(request.query['files_ids'], request.query['new_menu']))
    for client in ws_clients:
        await client.send_str('getDocs')
    return result

# @routes.get('/mv_sub_images')
# async def method (request):
#     result = web.json_response(await Docs.mv_sub_images(request.query['files_ids'], request.query['new_menu']))
#     for client in ws_clients:
#         await client.send_str('getDocs')
#     return result

@routes.get('/mv_files_sub')
async def method (request):
    result = web.json_response(await Docs.mv_files_sub(request.query['files_ids'], request.query['new_menu']))
    for client in ws_clients:
        await client.send_str('getSubFiles')
    return result

@routes.get('/mv_files_sperson')
async def method (request):
    result = web.json_response(await Docs.mv_files_sperson(request.query['files_ids'], request.query['new_menu']))
    for client in ws_clients:
        await client.send_str('getSpersonFiles')
    return result

@routes.get('/mv_files_customer')
async def method (request):
    result = web.json_response(await Docs.mv_files_customer(request.query['files_ids'], request.query['new_menu']))
    for client in ws_clients:
        await client.send_str('getCustomerFiles')
    return result

@routes.get('/mv_files_person')
async def method (request):
    result = web.json_response(await Docs.mv_files_person(request.query['files_ids'], request.query['new_menu']))
    for client in ws_clients:
        await client.send_str('getPersonFiles')
    return result

@routes.get('/mv_files_company')
async def method (request):
    result = web.json_response(await Docs.mv_files_company(request.query['files_ids'], request.query['new_menu']))
    for client in ws_clients:
        await client.send_str('getPersonalFiles')
    return result

@routes.get('/cp_mv_to_devices')
async def method (request):
    result = web.json_response(await Devices.cp_mv_to_devices(request.query['price_ids'], request.query['new_menu'], request.query['operation']))
    for client in ws_clients:
        await client.send_str('getDevices')
    return result

@routes.get('/send_reports')
async def method (request):
    await Reports.send_reports(request.query['ids'], request.query['names'], ws_clients)
    return web.json_response('')

@routes.get('/update_part_report')
async def method (request):
    await Reports.update_part_reports(request.query['part_name'], request.query['id'], ws_clients)
    return web.json_response('')

@routes.get('/get_reports_list')
async def method (request):
    return web.json_response(await Reports.get_reports_list(request.query['id']))

@routes.get('/send_price')
async def method (request):
    await Prices.send_price(request.query['ids'], request.query['names'], ws_clients)
    return web.json_response('')

@routes.get('/send_devices')
async def method (request):
    await Devices.send_devices(request.query['ids'], request.query['names'], ws_clients)
    return web.json_response('')

@routes.get('/send_damage')
async def method (request):
    await Damage.send_damage(request.query['ids'], request.query['names'], ws_clients)
    return web.json_response('')

@routes.get('/get_tables_in_damages')
async def method (request):
    return web.json_response(await Damage.get_tables_in_damages(request.query['id']))

@routes.get('/get_damage_list')
async def method (request):
    return web.json_response(await Damage.get_damage_list(request.query['id']))

@routes.get('/update_item_from_project')
async def method (request):
    await Project.update_item(request.query['val'], request.query['type'], request.query['id'], ws_clients)
    return web.json_response('')

@routes.post('/update_comment_in_project')
async def method (request):
    data = await request.json()
    await Project.update_item(data['val'], 'comment', data['id'], ws_clients)
    return web.json_response('')

@routes.get('/update_item_discont')
async def method (request):
    await Project.update_discont(request.query['val'], request.query['type'], request.query['id'], ws_clients)
    return web.json_response('')

@routes.get('/updatefilename')
async def method (request):
    result = web.json_response(await Project.updatefilename(request.query['val'], request.query['type'], request.query['id']))
    for client in ws_clients:
        await client.send_str('getDocs')
                # await client.send_str('getProjectDetail')
    return result

@routes.get('/updatefilename_company')
async def method (request):
    return web.json_response(await Project.updatefilename_company(request.query['val'], request.query['type'], request.query['id']))

@routes.get('/updatefilename_customer')
async def method (request):
    return web.json_response(await Project.updatefilename_customer(request.query['val'], request.query['type'], request.query['id']))

@routes.get('/updatefilename_person')
async def method (request):
    return web.json_response(await Project.updatefilename_person(request.query['val'], request.query['type'], request.query['id']))

@routes.get('/updatefilename_sub')
async def method (request):
    return web.json_response(await Project.updatefilename_sub(request.query['val'], request.query['type'], request.query['id']))

@routes.get('/updatefilename_sperson')
async def method (request):
    return web.json_response(await Project.updatefilename_sperson(request.query['val'], request.query['type'], request.query['id']))


@routes.get('/updatefilenames')
async def method (request):
    for oneid in request.query['id'].split(','):
        await Project.updatefilename(request.query['val'], request.query['type'], int(oneid))
    for client in ws_clients:
        await client.send_str('getDocs')
                # await client.send_str('getProjectDetail')
    return web.json_response('')

@routes.get('/updatedocname')
async def method (request):
    result = web.json_response(await Project.updatedocname(request.query['val'], request.query['type'], request.query['id']))
    for client in ws_clients:
        await client.send_str('getDocs')
                # await client.send_str('getProjectDetail')
    return result

@routes.get('/get_workers')
async def method (request):
    return web.json_response(await Project.get_workers())
    
@routes.get('/get_type_works')
async def method (request):
    return web.json_response(await Project.get_type_works())
    

# Personals
@routes.get('/get_templates_for_factory')
async def method (request):
    return web.json_response(await Personals.get_templates_for_factory())

@routes.get('/add_row_in_template_for_factory')
async def method (request):
    result = web.json_response(await Personals.add_row_in_template_for_factory(request.query['id']))
    for client in ws_clients:
        await client.send_str('getPersonal')
    return result

@routes.get('/remove_row_in_template_for_factory')
async def method (request):
    result = web.json_response(await Personals.remove_row_in_template_for_factory(request.query['id']))
    for client in ws_clients:
        await client.send_str('getPersonal')
    return result

@routes.get('/update_row_in_template_for_factory')
async def method (request):
    result = web.json_response(await Personals.update_row_in_template_for_factory(
        request.query['id'], request.query['value'], request.query['type']
        ))
    for client in ws_clients:
        await client.send_str('getPersonal')
    return result

@routes.get('/add_Item_in_template_for_factory')
async def method (request):
    result = web.json_response(await Personals.add_Item_in_template_for_factory())
    for client in ws_clients:
        await client.send_str('getPersonal')
    return result

@routes.get('/remove_Item_in_template_for_factory')
async def method (request):
    result = web.json_response(await Personals.remove_Item_in_template_for_factory(request.query['id']))
    for client in ws_clients:
        await client.send_str('getPersonal')
    return result

@routes.get('/update_Item_in_template_for_factory')
async def method (request):
    result = web.json_response(await Personals.update_Item_in_template_for_factory(request.query['id'], request.query['value']))
    for client in ws_clients:
        await client.send_str('getPersonal')
    return result

@routes.get('/personals')
async def method (request):
    return web.json_response(await Personals.select_personals(request.query['id'], request.query['type']))

@routes.get('/personal_menu')
async def method (request):
    return web.json_response(await Personals.personal_menu()) 


@routes.get('/add_personal_menu')
async def method (request):
    result = web.json_response(await Personals.add_personal_menu(request.query['parent_id'], request.query['type']))
    for client in ws_clients:
        await client.send_str('getPersonal')
    return result

@routes.get('/update_name_personal_menu')
async def method (request):
    result = web.json_response(await Personals.update_name_personal_menu(request.query['name'], request.query['id']))
    for client in ws_clients:
        await client.send_str('getPersonal')
    return result


@routes.get('/add_personal')
async def method (request):
    result = web.json_response(await Personals.add_personal(request.query['id'], request.query['type'],
        request.query['option'], request.query['option_id']))
    for client in ws_clients:
        await client.send_str('getPersonal')
    return result

@routes.get('/add_block')
async def method (request):
    result = web.json_response(await Personals.add_block(request.query['id'], request.query['l']))
    for client in ws_clients:
        await client.send_str('getPersonal')
    return result

@routes.get('/remove_block')
async def method (request):
    result = web.json_response(await Personals.remove_block(request.query['remove_count'], request.query['remove_id'], request.query['detail_id']))
    for client in ws_clients:
        await client.send_str('getPersonal')
    return result

@routes.get('/update_block')
async def method (request):
    result = web.json_response(await Personals.update_block(request.query['val'], request.query['count'], request.query['inc'], request.query['index'], request.query['detail']))
    for client in ws_clients:
        await client.send_str('getPersonal')
    return result


@routes.get('/remove_personal')
async def method (request):
    result = web.json_response(await Personals.remove_personal(request.query['id'], request.query['type']))
    for client in ws_clients:
        await client.send_str('getPersonal')
    return result


@routes.get('/remove_personal_menu')
async def method (request):
    result = web.json_response(await Personals.remove_personal_menu(request.query['remove_id']))
    for client in ws_clients:
        await client.send_str('getPersonal')
    return result

@routes.get('/update_personal')
async def method (request):
    result = web.json_response(await Personals.update_personal(request.query['data'], request.query['fild'], request.query['id'], request.query['type']))
    for client in ws_clients:
        await client.send_str('getPersonal')
    return result

@routes.get('/cp_mv_to_personal')
async def method (request):
    result = web.json_response(await Personals.cp_mv_to_personal(request.query['price_ids'], request.query['new_menu'], request.query['operation'], request.query['type']))
    for client in ws_clients:
        await client.send_str('getPersonal')
    return result

@routes.get('/change_parrent_menu_personal')
async def method (request):
    result = web.json_response(await Personals.change_parrent_menu_personal(request.query['drag1'], request.query['drag2']))
    for client in ws_clients:
        await client.send_str('getPersonal')
    return result


@routes.get('/change_parrent_menu_reports')
async def method (request):
    result = web.json_response(await Reports.change_parrent_menu_reports(request.query['drag1'], request.query['drag2']))
    for client in ws_clients:
        await client.send_str('getReports')
    return result

@routes.get('/getdata_personal')
async def method (request):
    return web.json_response(await Personals.getdata_personal()) 

#end of Personals
#start of Sub

@routes.get('/sub_order')
async def method (request):
    return web.json_response(await Sub.sub_order())

@routes.get('/send_price_sub')
async def method (request):
    result = web.json_response(await Sub.send_price(request.query['ids'], request.query['names']))
    for client in ws_clients:
        await client.send_str('getSubDetail')
    return result

@routes.get('/add_part_sub')
async def method (request):
    result= web.json_response(await Sub.add_part(request.query['part_name'], request.query['item_id']))
    for client in ws_clients:
        await client.send_str('getSubDetail')
    return result

@routes.get('/sub')
async def method (request):
    return web.json_response(await Sub.select_projects(request.query['page']))

@routes.get('/sub_detail')
async def method (request):
    return web.json_response(await Sub.select_project(request.query['id']))

@routes.get('/get_tables_sub')
async def method (request):
    return web.json_response(await Sub.get_tables(request.query['id']))


@routes.get('/del_row_from_table_sub')
async def method (request):
    result =  web.json_response(await Sub.del_row_from_table(request.query['id']))
    for client in ws_clients:
        await client.send_str('getSubDetail')
    return result

@routes.get('/update_id_in_one_table_sub')
async def method (request):
    result =  web.json_response(await Sub.update_id_in_one_table(request.query['newIndex'], request.query['oldIndex'], request.query['newPart']))
    for client in ws_clients:
        await client.send_str('getSubDetail')
    return result

@routes.get('/update_id_sub')
async def method (request):
    result =  web.json_response(await Sub.update_id(request.query['newIndex'], request.query['newPart'], request.query['oldIndex'], request.query['oldPart']))
    for client in ws_clients:
        await client.send_str('getSubDetail')
    return result

@routes.get('/update_id_table_sub')
async def method (request):
    result = web.json_response(await Sub.update_id_table(request.query['newIndex'], request.query['oldIndex'], request.query['id']))
    for client in ws_clients:
        await client.send_str('getSubDetail')
    return result

@routes.get('/update_checkbox_table_sub')
async def method (request):
    result = web.json_response(await Sub.update_checkbox_table(request.query['id'], request.query['fild'], request.query['data']))
    for client in ws_clients:
        await client.send_str('getSubDetail')
    return result

@routes.get('/get_workers_sub')
async def method (request):
    return web.json_response(await Sub.get_workers())

@routes.get('/getLoocks_sub')
async def method (request):
     return web.json_response(await Sub.getLoocks())

@routes.get('/updateProjectTaxsSub')
async def method (request):
    result = web.json_response(await Sub.updateProjectTaxs(
        request.query['id'],
        request.query['tax'],
        request.query['taxDub'],
        request.query['taxP'],
        request.query['taxPDub'],
        request.query['disc'],
        request.query['discP'],
        request.query['butDiscPerc'],
        request.query['addtaxColapse']
        ))
    for client in ws_clients:
        await client.send_str('getSubDetail')
    return result

@routes.get('/changeDisableTableSub')
async def method (request):
    # print(ws_clients)
    await Sub.changeDisableTable(
        request.query['type_operation'], request.query['fild'], request.query['id'], request.query['user'], ws_clients)

    for client in ws_clients:
        await client.send_str('getLoocksSub')
    return web.json_response('')


@routes.get('/sub_detail_new')
async def method (request):
    return web.json_response(await Sub.select_project_new(request.query['id']))

@routes.get('/get_damage_sub')
async def method (request):
    return web.json_response(await Sub.get_damage(request.query['id']))

@routes.get('/domage_images_sub')
async def method (request):
    return web.json_response(await Sub.get_damage_images(request.query['id'], request.query['project']))

@routes.get('/get_images_sub')
async def method (request):
    return web.json_response(await Sub.get_images(request.query['id']))

@routes.get('/add_sub')
async def method (request):
    result = web.json_response(await Sub.add_project(strftime("%Y", gmtime()), strftime("%Y-%m-%d", gmtime()), request.query['contry'], request.query['area'],  request.query['street'], request.query['zip']))
    for client in ws_clients:
        await client.send_str('getSub')
    return result

@routes.get('/updatSub')
async def method (request):
    # print(request.query['id'], request.query['date'], request.query['fild'])
    result= web.json_response(await Sub.update(request.query['id'], request.query['date'], request.query['fild']))
    fild = str(request.query['fild'])
    updateSubSend = 'getSubDetail'

    if((fild == 'person_id') | (fild == 'mail') | (fild == 'phone') | (fild == 'fax')):
        updateSubSend = 'get_person' #get_person

    if((fild == 'zip') | (fild == 'city') | (fild == 'street') | (fild == 'date')):
        updateSubSend = 'project_sub_f'


    # print(updateProjectSend)

    for client in ws_clients:
        await client.send_str(str(updateSubSend))
    return result



@routes.get('/update_table_data_sub')
async def method (request):
    result = web.json_response(await Sub.update_table_data(request.query['id'], request.query['fild'], request.query['data']))
    for client in ws_clients:
        await client.send_str('getSubDetail')
    return result

# @routes.get('/offer_sub')
# async def method (request):
#     return web.json_response(await SubOffer.select_offer(request.query['id']))

@routes.get('/invoice_sub')
async def method (request):
    return web.json_response(await SubInvoice.select_invoice(request.query['id']))

@routes.get('/detect_invoice_sub')
async def method (request):
    return web.json_response(await SubInvoice.detect_invoice())

@routes.get('/get_reports_sub')
async def method (request):
    return web.json_response(await SubInvoice.get_reports(request.query['id']))

@routes.get('/add_invoice_sub')
async def method (request):
    result = web.json_response(await Invoice.add_invoice(request.query['id'], request.query['type'], request.query['number'], request.query['newRange'], request.query['labelForDelete']))
    for client in ws_clients:
        await client.send_str('get_types_for_tables_f')
    return result

@routes.get('/add_same_sub')
async def method (request):
    return web.json_response(await add_same_sub.add_same(
        request.query['add_number'],
        request.query['add_work'],
        request.query['add_insurance_number'],
        request.query['add_place'],
        request.query['add_comment'],
        request.query['add_project_id'],
        request.query['order_id'],
        request.query['type'],
        ))
    
# @routes.get('/del_item_sub')
# async def method (request):
#     result = web.json_response(await Del_offer_sub.del_item(request.query['id']))
#     for client in ws_clients:
#         await client.send_str('sub_detail_new_f')
#     return result

# @routes.get('/offers_sub')
# async def method (request):
#     return web.json_response(await SubOffers.select_offers(request.query['id']))

@routes.get('/invoices_sub')
async def method (request):
    return web.json_response(await SubInvoice.select_invoices(request.query['id']))

@routes.get('/update_item_from_sub')
async def method (request):
    result = web.json_response(await Sub.update_item(request.query['val'], request.query['type'], request.query['id']))
    for client in ws_clients:
        await client.send_str('getSub')
        await client.send_str('getSubDetail')
    return result

@routes.get('/change_type_sub')
async def method (request):
    result =  web.json_response(await Sub.change_type(request.query['id'], request.query['type']))
    for client in ws_clients:
        await client.send_str('get_types_for_sub_tables_f')
    return result

# end of SUB
#Offers
@routes.get('/suggest')
async def method (request):
    return web.json_response(await Projects.select_part(request.query['type'], request.query['mode']))
# Balance
@routes.get('/balance')
async def method (request):
    return web.json_response(await Balance.select_balances(request.query['mode']))

@routes.get('/billing')
async def method (request):
    return web.json_response(await Balance.billing())

@routes.get('/add_payment')
async def method (request):
    result = web.json_response(await Balance.add_payment(request.query['savearr']))
    for client in ws_clients:
        await client.send_str('getBalanceAfterPay')
    return result

@routes.get('/remove_payment')
async def method (request):
    result = web.json_response(await Balance.remove_payment(request.query['id']))
    for client in ws_clients:
        await client.send_str('getBalanceAfterPay')
    return result

@routes.get('/update_payment')
async def method (request):
    result = web.json_response(await Balance.update_payment(request.query['id'], request.query['value'], request.query['fild']))
    for client in ws_clients:
        await client.send_str('getBalanceAfterPay')
    return result

@routes.get('/update_comment')
async def method (request):
    result = web.json_response(await Balance.update_comment(request.query['id'], request.query['value']))
    for client in ws_clients:
        await client.send_str('getBalanceAfterPay')
    return result

@routes.get('/update_comment_sub')
async def method (request):
    result = web.json_response(await Balance.update_comment_sub(request.query['id'], request.query['value']))
    for client in ws_clients:
        await client.send_str('getBalance')
    return result

# end of Balance

@routes.get('/docs')
async def method (request):
    return web.json_response(await Docs.select_docs(request.query['id']))

@routes.get('/files')
async def method (request):
    return web.json_response(await Docs.select_files(request.query['id']))

@routes.get('/filesToCompany')
async def method (request):
    return web.json_response(await Docs.select_file_company(request.query['id']))


@routes.get('/del_doc')
async def method (request):
    return web.json_response(await Docs.del_doc(request.query['id'], request.query['number']))

@routes.get('/del_file')
async def method (request):
    return web.json_response(await Docs.del_file(request.query['id'], request.query['number']))


@routes.get('/delfile')
async def method (request):
    result= web.json_response(await Docs.delfile(request.query['id']))
    for client in ws_clients:
        await client.send_str('getDocs')
        # await client.send_str('getProjectDetail')
    return result

@routes.get('/delfile_company')
async def method (request):
    result= web.json_response(await Docs.delfile_company(request.query['id']))
    for client in ws_clients:
        await client.send_str('getPersonalFiles')
    return result


@routes.get('/delfile_customer')
async def method (request):
    result= web.json_response(await Docs.delfile_customer(request.query['id']))
    for client in ws_clients:
        await client.send_str('getSubDetail')
    return result

@routes.get('/delfile_person')
async def method (request):
    result= web.json_response(await Docs.delfile_person(request.query['id']))
    for client in ws_clients:
        await client.send_str('getPersonFiles')
    return result


@routes.get('/delfile_sub')
async def method (request):
    result= web.json_response(await Docs.delfile_sub(request.query['id']))
    for client in ws_clients:
        await client.send_str('getSubFiles')
    return result

@routes.get('/delfile_sperson')
async def method (request):
    result= web.json_response(await Docs.delfile_sperson(request.query['id']))
    for client in ws_clients:
        await client.send_str('getSpersonFiles')
    return result


@routes.get('/deldoc')
async def method (request):
    result= web.json_response(await Docs.deldoc(request.query['id']))
    # print('deldoc')
    for client in ws_clients:
        await client.send_str('getDocs')
    return result


@routes.post('/load_img_in_group')
async def method(request):
    reader = await request.multipart()
    part = await reader.next()
    filename = part.filename
    file_extension = os.path.splitext(filename)

    group_id = request.headers.get('X-Group-Id')
    arr = bytearray()

    while True:
        chunk = await part.read_chunk()  # 8192 bytes by default.

        if not chunk:
            break

        arr.extend(chunk)
        file = bytes(arr)

        
    added = strftime("%d-%m-%Y %H:%M:%S", gmtime())
    #print(file, filename, group_id, added)
    result= web.json_response(await Docs.upload_img_for_damages(
        file, filename, group_id, added))
    for client in ws_clients:
        await client.send_str('getProjectDetail')
    return result


# @routes.post('/loadFiles')
# async def method(request):
#     reader = await request.multipart()
#     part = await reader.next()

#     filename = part.filename
#     file_extension = os.path.splitext(filename)

#     number = request.headers.get('number')
#     group = request.headers.get('group')
#     user = request.headers.get('user')
#     arr = bytearray()

#     print('= - =')

#     print(request.content_length)

#     result = await shield(part.read())
#     print(result)
#     print('= - =')

#     return web.json_response('OK')



@routes.post('/send_replace_image')
async def method(request):
    form = await request.json()

    id = form.get('id')
    image = form.get('toImg')

    new_data = image.replace('data:image/jpeg;base64,', '')
    imgdata = base64.b64decode(new_data)
    # print(imgdata)

    return web.json_response(await Docs.send_replace_image(imgdata, id))

@routes.post('/loadFiles')
async def method(request):

 #   print(request)
    reader = await request.multipart()
 #   print('1')
    part = await reader.next()
 #   print('2')
    filename = part.filename
    file_extension = os.path.splitext(filename)
    
    #print('------------')
    #print(request.headers)

    number = request.headers.get('X-Number')
    group = request.headers.get('X-Group')
    user = request.headers.get('X-User')
    folder = request.headers.get('X-Folder')

# print(number)
# print(group)
# print(user)
    # print(folder)

    arr = bytearray()

    while True:
       # print('3')
        chunk = await part.read_chunk()  # 8192 bytes by default.
  #      print(len(chunk))
        if not chunk:
            break

        arr.extend(chunk)
        file = bytes(arr)
        page_content=''
        number_of_pages=0

    if file_extension[1] == '.pdf':
        pdf_file = io.BytesIO(file)
        read_pdf = PyPDF2.PdfFileReader(pdf_file)
        number_of_pages = read_pdf.getNumPages()
        c = collections.Counter(range(number_of_pages))
        for i in c:
           page = read_pdf.getPage(i)
           page_content = page_content + page.extractText().replace('\n', '<br />')
        
    added = strftime("%d-%m-%Y %H:%M:%S", gmtime())
   # print('3.5')
    
    result = (web.json_response(await Docs.upload_doc(
            file, filename, number, number_of_pages, group, added, user, page_content, folder)))
    for client in ws_clients:
            await client.send_str('getDocs')
    return result

@routes.post('/loadFilesWorkers')
async def method(request):

 #   print(request)
    reader = await request.multipart()
 #   print('1')
    part = await reader.next()
 #   print('2')
    filename = part.filename
    file_extension = os.path.splitext(filename)
    
    #print('------------')
    #print(request.headers)

    number = request.headers.get('X-Number')
    projet_id = request.headers.get('X-id')
    user = request.headers.get('X-User')
    folder = request.headers.get('X-Folder')
    group = None
# print(number)
# print(group)
# print(user)
    # print(folder)

    arr = bytearray()

    while True:
       # print('3')
        chunk = await part.read_chunk()  # 8192 bytes by default.
  #      print(len(chunk))
        if not chunk:
            break

        arr.extend(chunk)
        file = bytes(arr)
        page_content=''
        number_of_pages=0

    if file_extension[1] == '.pdf':
        pdf_file = io.BytesIO(file)
        read_pdf = PyPDF2.PdfFileReader(pdf_file)
        number_of_pages = read_pdf.getNumPages()
        c = collections.Counter(range(number_of_pages))
        for i in c:
           page = read_pdf.getPage(i)
           page_content = page_content + page.extractText().replace('\n', '<br />')
    added = strftime("%d-%m-%Y %H:%M:%S", gmtime())
    added_foolder = strftime("%d.%m", gmtime())

    # print('1 stage')
    # print(folder, projet_id, added_foolder+' '+user)

    foolder_check = (await Docs.foolder_check(folder, projet_id, added_foolder+' '+user))
    # print('2 stage')
    # print(foolder_check)

    if (foolder_check == None):
        # print('foolder_check == None')
        # print(folder, projet_id, added_foolder+' '+user)
        foolder_id = (await Docs.add_images_menu(folder, projet_id, added_foolder+' '+user))
    else:
        # print('foolder_check != None')
        foolder_id = foolder_check
    # print('3 stage')
    # print(foolder_id)
    result = web.json_response(await Docs.upload_doc(file, filename, number, number_of_pages, group, added, user, page_content, foolder_id['id']))

    del_foolder = (await Docs.del_foolder(folder, projet_id, added_foolder+' '+user))

    for client in ws_clients:
            await client.send_str('getDocs')
    return result

@routes.post('/loadFilesToCompany')
async def method(request):
 
 #   print(request)
    reader = await request.multipart()
 #   print('1')
    part = await reader.next()
 #   print('2')
    filename = part.filename
    file_extension = os.path.splitext(filename)
    
    #print('------------')
    #print(request.headers)

    number = request.headers.get('X-Number')
    # group = request.headers.get('X-Group')
    folder = request.headers.get('X-Folder')
    user = request.headers.get('X-User')
   # print(user)
    arr = bytearray()

    while True:
       # print('3')
        chunk = await part.read_chunk()  # 8192 bytes by default.
  #      print(len(chunk))
        if not chunk:
            break

        arr.extend(chunk)
        file = bytes(arr)
        page_content=''
        number_of_pages=0

    if file_extension[1] == '.pdf':
        pdf_file = io.BytesIO(file)
        read_pdf = PyPDF2.PdfFileReader(pdf_file)
        number_of_pages = read_pdf.getNumPages()
        c = collections.Counter(range(number_of_pages))
        for i in c:
           page = read_pdf.getPage(i)
           page_content = page_content + page.extractText().replace('\n', '<br />')
        
    added = strftime("%d-%m-%Y %H:%M:%S", gmtime())
   # print('3.5')
    for client in ws_clients:
        await client.send_str('getPersonalFiles')
   # print('4')
    return web.json_response(await Docs.upload_to_company(
        file, filename, number, number_of_pages, added, user, page_content, folder))

# @routes.get('/pdf_check')
# async def method (request):
#     file_path = input('/var/www/it-vision.pro/html/pdfs/pdf.pdf')
#     return web.json_response(os.path.exists(file_path))

@routes.post('/loadFilesToCustomer')
async def method(request):
 
 #   print(request)
    reader = await request.multipart()
 #   print('1')
    part = await reader.next()
 #   print('2')
    filename = part.filename
    file_extension = os.path.splitext(filename)
    
    #print('------------')
    #print(request.headers)

    number = request.headers.get('X-Number')
    # group = request.headers.get('X-Group')
    folder = request.headers.get('X-Folder')
    user = request.headers.get('X-User')
   # print(user)
    arr = bytearray()

    while True:
       # print('3')
        chunk = await part.read_chunk()  # 8192 bytes by default.
  #      print(len(chunk))
        if not chunk:
            break

        arr.extend(chunk)
        file = bytes(arr)
        page_content=''
        number_of_pages=0

    if file_extension[1] == '.pdf':
        pdf_file = io.BytesIO(file)
        read_pdf = PyPDF2.PdfFileReader(pdf_file)
        number_of_pages = read_pdf.getNumPages()
        c = collections.Counter(range(number_of_pages))
        for i in c:
           page = read_pdf.getPage(i)
           page_content = page_content + page.extractText().replace('\n', '<br />')
        
    added = strftime("%d-%m-%Y %H:%M:%S", gmtime())
   # print('3.5')
    for client in ws_clients:
        await client.send_str('getCustomerFiles')
   # print('4')
    return web.json_response(await Docs.upload_to_customer(
        file, filename, number, number_of_pages, added, user, page_content, folder))

# @routes.get('/pdf_check')
# async def method (request):
#     file_path = input('/var/www/it-vision.pro/html/pdfs/pdf.pdf')
#     return web.json_response(os.path.exists(file_path))

 

@routes.post('/loadFilesToPerson')
async def method(request):
 
 #   print(request)
    reader = await request.multipart()
 #   print('1')
    part = await reader.next()
 #   print('2')
    filename = part.filename
    file_extension = os.path.splitext(filename)
    
    #print('------------')
    #print(request.headers)

    number = request.headers.get('X-Number')
    # group = request.headers.get('X-Group')
    folder = request.headers.get('X-Folder')
    user = request.headers.get('X-User')
   # print(user)
    arr = bytearray()

    while True:
       # print('3')
        chunk = await part.read_chunk()  # 8192 bytes by default.
  #      print(len(chunk))
        if not chunk:
            break

        arr.extend(chunk)
        file = bytes(arr)
        page_content=''
        number_of_pages=0

    if file_extension[1] == '.pdf':
        pdf_file = io.BytesIO(file)
        read_pdf = PyPDF2.PdfFileReader(pdf_file)
        number_of_pages = read_pdf.getNumPages()
        c = collections.Counter(range(number_of_pages))
        for i in c:
           page = read_pdf.getPage(i)
           page_content = page_content + page.extractText().replace('\n', '<br />')
        
    added = strftime("%d-%m-%Y %H:%M:%S", gmtime())
   # print('3.5')
    for client in ws_clients:
        await client.send_str('getPersonFiles')
   # print('4')
    return web.json_response(await Docs.upload_to_contact(
        file, filename, number, number_of_pages, added, user, page_content, folder))

@routes.post('/loadFilesToSub')
async def method(request):
 
 #   print(request)
    reader = await request.multipart()
 #   print('1')
    part = await reader.next()
 #   print('2')
    filename = part.filename
    file_extension = os.path.splitext(filename)
    
    #print('------------')
    #print(request.headers)

   #  number = request.headers.get('X-Number')
   #  # group = request.headers.get('X-Group')
   #  user = request.headers.get('X-User')
   #  folder = request.headers.get('X-Folder')
   #  # print(folder)
   # # print(user)+++


    number = request.headers.get('X-Number')
    group = request.headers.get('X-Group')
    user = request.headers.get('X-User')
    folder = request.headers.get('X-Folder')

    arr = bytearray()

    while True:
       # print('3')
        chunk = await part.read_chunk()  # 8192 bytes by default.
  #      print(len(chunk))
        if not chunk:
            break

        arr.extend(chunk)
        file = bytes(arr)
        page_content=''
        number_of_pages=0

    if file_extension[1] == '.pdf':
        pdf_file = io.BytesIO(file)
        read_pdf = PyPDF2.PdfFileReader(pdf_file)
        number_of_pages = read_pdf.getNumPages()
        c = collections.Counter(range(number_of_pages))
        for i in c:
           page = read_pdf.getPage(i)
           page_content = page_content + page.extractText().replace('\n', '<br />')
        
    added = strftime("%d-%m-%Y %H:%M:%S", gmtime())
   # print('3.5')
    for client in ws_clients:
        await client.send_str('getSubFiles')
   # print('4')
    return web.json_response(await Docs.upload_to_sub(
        file, filename, number, number_of_pages, group, added, user, page_content, folder))






@routes.post('/loadFilesToSperson')
async def method(request):
 
 #   print(request)
    reader = await request.multipart()
 #   print('1')
    part = await reader.next()
 #   print('2')
    filename = part.filename
    file_extension = os.path.splitext(filename)
    
    #print('------------')
    #print(request.headers)

    number = request.headers.get('X-Number')
    user = request.headers.get('X-User')
    # group = request.headers.get('X-Group')
    folder = request.headers.get('X-Folder')
   # print(user)
    arr = bytearray()

    while True:
       # print('3')
        chunk = await part.read_chunk()  # 8192 bytes by default.
  #      print(len(chunk))
        if not chunk:
            break

        arr.extend(chunk)
        file = bytes(arr)
        page_content=''
        number_of_pages=0

    if file_extension[1] == '.pdf':
        pdf_file = io.BytesIO(file)
        read_pdf = PyPDF2.PdfFileReader(pdf_file)
        number_of_pages = read_pdf.getNumPages()
        c = collections.Counter(range(number_of_pages))
        for i in c:
           page = read_pdf.getPage(i)
           page_content = page_content + page.extractText().replace('\n', '<br />')
        
    added = strftime("%d-%m-%Y %H:%M:%S", gmtime())
   # print('3.5')
    for client in ws_clients:
        await client.send_str('getSpersonFiles')
   # print('4')
    return web.json_response(await Docs.upload_to_sperson(
        file, filename, number, number_of_pages, added, user, page_content, folder))



@routes.get('/google')
async def method (request):
    link = request.query['link'].replace('|','?')
    # print(link)
    request_headers = {
    "Accept-Language": "de-DE,de;q=0.5",
    "User-Agent": "Mozilla/5.0 (Linux; Android 7.0; SM-G892A Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/60.0.3112.107 Mobile Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Referer": "http://thewebsite.com",
    "Connection": "keep-alive" 
    }
    # response = urlopen(link)
    req = urllib.request.Request(link, headers=request_headers)
    response = urllib.request.urlopen(req)
    html = response.read()
    dec = html.decode("ISO-8859-1") 
    dec = dec.replace('<head>','<head><base target="_self" href="https://www.google.com/">')
    dec = dec.replace('target="_blank"','target="result"')
    dec = dec.replace('<a','<a target="result"')
    dec = dec.replace('<header','<header style="display:none"')
    dec = dec.replace('<form','<form style="display:none"')

    
    
    html = dec.encode('utf-8')
    # print(html)
    resp = web.StreamResponse(headers={
        'CONTENT-DISPOSITION': 'inline'
    })

    resp.content_type ="text/html"
    # html = html.encode('utf-8').replace('','')
    await resp.prepare(request)
    await resp.write(html)
    return resp


# @routes.get('/image_damage')
# async def method (request):
#         file = await Docs.select_image_damage(request.query['id'])

#         if (file['newImage']==None):
#             content = file['content']
#         else:
#             content = file['newImage']

#         resp = web.StreamResponse(headers={
#          'CONTENT-DISPOSITION': 'inline'
#         })

#         resp.content_type ="image/jpeg"

#         await resp.prepare(request)
#         await resp.write(content)
#         return resp


@routes.get('/image_damage')
async def method (request):
        try:
            stream = io.BytesIO()
            file = await Docs.select_image_damage(request.query['id'])
            if (file['newImage']==None):
                content = file['content']
            else:
                content = file['newImage']
            im = Image.open(io.BytesIO(content))
            rgb_im = im.convert("RGB")
            rgb_im.save(stream, "JPEG", quality=int(request.query['q']))
            return web.Response(body=stream.getvalue(), content_type="image/jpeg")
        except Exception as e:
            print("ex /image_damage")


# @routes.get('/image_damage')
# async def method (request):
#         file = await Docs.select_image_damage(request.query['id'])

#         if (file['newImage']==None):
#             content = file['content']
#         else:
#             content = file['newImage']

#         im = Image.open(io.BytesIO(content))
#         im.thumbnail((500,500), Image.ANTIALIAS)
#         stream = io.BytesIO()

#         content_type ="image/jpeg"
#         withoutdot = "JPEG"

#         im.save(stream, withoutdot)

#         return web.Response(body=stream.getvalue(), content_type=content_type)


@routes.get('/image_edit')
async def method (request):
        file = await Docs.select_image_damage(request.query['id'])

        content = file['content']

        resp = web.StreamResponse(headers={
         'CONTENT-DISPOSITION': 'inline'
        })

        resp.content_type ="image/jpeg"

        await resp.prepare(request)
        await resp.write(content)
        return resp


# @routes.get('/image')
# async def method (request):
#         file = await Docs.select_file(request.query['id'])
#         file_extension = os.path.splitext(file['name'])
#         resp = web.StreamResponse(headers={
#         'CONTENT-DISPOSITION': 'inline'
#         })

#         if file_extension[1] == '.pdf':
#             resp.content_type ="application/pdf"
#         if file_extension[1] == '.jpeg' or file_extension[1] == '.jpg':
#             resp.content_type ="image/jpeg"
#         if file_extension[1] == '.png':
#             resp.content_type ="image/png"
            
#         await resp.prepare(request)
#         await resp.write(file['content'])

        
        
#         return resp

@routes.get('/image')
async def method (request):
        # print("Executing coroutine")
        try:
            file = await Docs.select_file(request.query['id'])
            file_extension = os.path.splitext(file['name'])
            im = Image.open(io.BytesIO(file['content']))
            # im.thumbnail((500,500), Image.ANTIALIAS)
            stream = io.BytesIO()
            if file_extension[1] == '.jpeg' or file_extension[1] == '.jpg':
                content_type ="image/jpeg"
                withoutdot = "JPEG"
            if file_extension[1] == '.png':
                content_type ="image/png"
                withoutdot = "PNG"
            im.save(stream, withoutdot, quality=int(request.query['q']))
            return web.Response(body=stream.getvalue(), content_type=content_type)
        except Exception as e:
            print("ex /image")
                # break

        #     print("Done waiting")

        # print("Done executing coroutine")



        # file = await Docs.select_file(request.query['id'])

        


        # print(image.size)
        # thumb_img = image.copy()
        # image.thumbnail((100, 100))
        # print(thumb_img.size)
        # print(image.size)

        # image = Image.open(io.BytesIO(file['content']))
        # MAX_SIZE = (100, 100) 
        # image.thumbnail(MAX_SIZE)
        # print(image.size)

        # image.tobytes()
        # image.show()
        # img.thumbnail((500,500), Image.ANTIALIAS)
        # bytes = img.tobytes()
        # print(bytes)
        # img.save('somepic.jpg')

        # resp = web.StreamResponse(headers={
        # 'CONTENT-DISPOSITION': 'inline'
        # })

        # if file_extension[1] == '.jpeg' or file_extension[1] == '.jpg':
        #     resp.content_type ="image/jpeg"
        # if file_extension[1] == '.png':
        #     resp.content_type ="image/png"

        # print(resp.content_type)

        # response.content_type = 'image/png'
        # await resp.prepare(request)
        # return(io.BytesIO(thumb_img.tobytes()))
        # return resp


@routes.get('/image_company')
async def method (request):
        file = await Docs.select_file_company(request.query['id'])
        file_extension = os.path.splitext(file['name'])
        resp = web.StreamResponse(headers={
        'CONTENT-DISPOSITION': 'inline'
        })

        if file_extension[1] == '.pdf':
            resp.content_type ="application/pdf"
        if file_extension[1] == '.jpeg' or file_extension[1] == '.jpg':
            resp.content_type ="image/jpeg"
        if file_extension[1] == '.png':
            resp.content_type ="image/png"
        await resp.prepare(request)
        await resp.write(file['content'])
        return resp

@routes.get('/image_customer')
async def method (request):
        file = await Docs.select_file_customer(request.query['id'])
        file_extension = os.path.splitext(file['name'])
        resp = web.StreamResponse(headers={
        'CONTENT-DISPOSITION': 'inline'
        })

        if file_extension[1] == '.pdf':
            resp.content_type ="application/pdf"
        if file_extension[1] == '.jpeg' or file_extension[1] == '.jpg':
            resp.content_type ="image/jpeg"
        if file_extension[1] == '.png':
            resp.content_type ="image/png"
        await resp.prepare(request)
        await resp.write(file['content'])
        return resp

@routes.get('/image_person')
async def method (request):
        file = await Docs.select_file_person(request.query['id'])
        file_extension = os.path.splitext(file['name'])
        resp = web.StreamResponse(headers={
        'CONTENT-DISPOSITION': 'inline'
        })

        if file_extension[1] == '.pdf':
            resp.content_type ="application/pdf"
        if file_extension[1] == '.jpeg' or file_extension[1] == '.jpg':
            resp.content_type ="image/jpeg"
        if file_extension[1] == '.png':
            resp.content_type ="image/png"
        await resp.prepare(request)
        await resp.write(file['content'])
        return resp


@routes.get('/image_sub')
async def method (request):
        # print("Executing coroutine")
        try:
            file = await Docs.select_file_sub(request.query['id'])
            file_extension = os.path.splitext(file['name'])
            im = Image.open(io.BytesIO(file['content']))
            # im.thumbnail((500,500), Image.ANTIALIAS)
            stream = io.BytesIO()
            if file_extension[1] == '.jpeg' or file_extension[1] == '.jpg':
                content_type ="image/jpeg"
                withoutdot = "JPEG"
            if file_extension[1] == '.png':
                content_type ="image/png"
                withoutdot = "PNG"
            im.save(stream, withoutdot, quality=int(request.query['q']))
            return web.Response(body=stream.getvalue(), content_type=content_type)
        except Exception as e:
            print("ex /image_sub")

# @routes.get('/image_sub')
# async def method (request):
#         file = await Docs.select_file_sub(request.query['id'])
#         file_extension = os.path.splitext(file['name'])
#         resp = web.StreamResponse(headers={
#         'CONTENT-DISPOSITION': 'inline'
#         })

#         if file_extension[1] == '.pdf':
#             resp.content_type ="application/pdf"
#         if file_extension[1] == '.jpeg' or file_extension[1] == '.jpg':
#             resp.content_type ="image/jpeg"
#         if file_extension[1] == '.png':
#             resp.content_type ="image/png"
#         await resp.prepare(request)
#         await resp.write(file['content'])
#         return resp

@routes.get('/image_sperson')
async def method (request):
        file = await Docs.select_file_sperson(request.query['id'])
        file_extension = os.path.splitext(file['name'])
        resp = web.StreamResponse(headers={
        'CONTENT-DISPOSITION': 'inline'
        })

        if file_extension[1] == '.pdf':
            resp.content_type ="application/pdf"
        if file_extension[1] == '.jpeg' or file_extension[1] == '.jpg':
            resp.content_type ="image/jpeg"
        if file_extension[1] == '.png':
            resp.content_type ="image/png"
        await resp.prepare(request)
        await resp.write(file['content'])
        return resp


@routes.post('/pdf1')
async def method (request):
    data = await request.post()
    html = await Docs.select_doc(data['id']) # это id
    pdf = HTML(string=html['html']).write_pdf(stylesheets=[CSS(string='@page { size: A4; margin-top: 5mm; margin-left: 10mm; margin-right: 10mm; margin-bottom: 3mm; }')])
    resp = web.StreamResponse(headers={
        'CONTENT-DISPOSITION': 'inline'
    })
    resp.content_type ="application/pdf"
    await resp.prepare(request)
    await resp.write(pdf)
    return resp

@routes.post('/pdf2')
async def method (request):
    data = await request.post()
    file = await Docs.select_file(data['id'])
    # print(file)
    file_extension = os.path.splitext(file['name'])
    resp = web.StreamResponse(headers={
        'CONTENT-DISPOSITION': 'inline'
        })

    if file_extension[1] == '.pdf':
            resp.content_type ="application/pdf"
    if file_extension[1] == '.jpeg' or file_extension[1] == '.jpg':
            resp.content_type ="image/jpeg"
    if file_extension[1] == '.png':
            resp.content_type ="image/png"    

    await resp.prepare(request)
    await resp.write(file['content'])
    return resp

@routes.post('/pdf_file_from_company')
async def method (request):
    data = await request.post()
    # print(data['id'])
    file = await Docs.select_file_company(data['id'])

    file_extension = os.path.splitext(file['name'])
    resp = web.StreamResponse(headers={
        'CONTENT-DISPOSITION': 'inline'
        })

    if file_extension[1] == '.pdf':
            resp.content_type ="application/pdf"
    if file_extension[1] == '.jpeg' or file_extension[1] == '.jpg':
            resp.content_type ="image/jpeg"
    if file_extension[1] == '.png':
            resp.content_type ="image/png"    

    await resp.prepare(request)
    await resp.write(file['content'])
    return resp

@routes.post('/pdf_file_from_customer')
async def method (request):
    data = await request.post()
    file = await Docs.select_file_customer(data['id'])
    file_extension = os.path.splitext(file['name'])
    resp = web.StreamResponse(headers={
        'CONTENT-DISPOSITION': 'inline'
        })

    if file_extension[1] == '.pdf':
            resp.content_type ="application/pdf"
    if file_extension[1] == '.jpeg' or file_extension[1] == '.jpg':
            resp.content_type ="image/jpeg"
    if file_extension[1] == '.png':
            resp.content_type ="image/png"    

    await resp.prepare(request)
    await resp.write(file['content'])
    return resp

@routes.post('/pdf_file_from_person')
async def method (request):
    data = await request.post()
    file = await Docs.select_file_person(data['id'])
    file_extension = os.path.splitext(file['name'])
    resp = web.StreamResponse(headers={
        'CONTENT-DISPOSITION': 'inline'
        })

    if file_extension[1] == '.pdf':
            resp.content_type ="application/pdf"
    if file_extension[1] == '.jpeg' or file_extension[1] == '.jpg':
            resp.content_type ="image/jpeg"
    if file_extension[1] == '.png':
            resp.content_type ="image/png"    

    await resp.prepare(request)
    await resp.write(file['content'])
    return resp


@routes.post('/pdf_file_from_sub')
async def method (request):
    data = await request.post()
    file = await Docs.select_file_sub(data['id'])
    file_extension = os.path.splitext(file['name'])
    resp = web.StreamResponse(headers={
        'CONTENT-DISPOSITION': 'inline'
        })

    if file_extension[1] == '.pdf':
            resp.content_type ="application/pdf"
    if file_extension[1] == '.jpeg' or file_extension[1] == '.jpg':
            resp.content_type ="image/jpeg"
    if file_extension[1] == '.png':
            resp.content_type ="image/png"    

    await resp.prepare(request)
    await resp.write(file['content'])
    return resp


@routes.post('/pdf_file_from_sperson')
async def method (request):
    data = await request.post()
    file = await Docs.select_file_sperson(data['id'])
    file_extension = os.path.splitext(file['name'])
    resp = web.StreamResponse(headers={
        'CONTENT-DISPOSITION': 'inline'
        })

    if file_extension[1] == '.pdf':
            resp.content_type ="application/pdf"
    if file_extension[1] == '.jpeg' or file_extension[1] == '.jpg':
            resp.content_type ="image/jpeg"
    if file_extension[1] == '.png':
            resp.content_type ="image/png"    

    await resp.prepare(request)
    await resp.write(file['content'])
    return resp

@routes.get('/get_type_docs')
async def method (request):
    return web.json_response(await Docs.get_type_docs(request.query['type']))

@routes.get('/pdf')
async def method (request):
    return await language.pdf(request, request.query['addPdf'], request.query['forPreview'], request.query['pid'], request.query['itemId'], request.query['type'], request.query['today'], request.query['stworks'], request.query['fworks'],
                              request.query['dateForInspect'], request.query['byForInspect'], request.query['selectedDocsList'], ws_clients)
 

@routes.get('/ws')
async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    ws_clients.append(ws)
    try:
        async for msg in ws:
           for client in ws_clients:
                await client.send_str(msg.data)
    except ConnectionResetError:
        print("ConnectionResetError, reconnecting...")
        os.system("killall -9 python");
    ws_clients.remove(ws)
    return ws


# register static routes
routes.static('/static', f"{APPLICATION_DIR}/static")
'//127.0.0.1:8081/static/bundle/bootstrap-vue.css'