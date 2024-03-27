import PyPDF2
from time import localtime, strftime
from datetime import datetime, timedelta, timezone

import io
import os.path
import time
import json
# Import smtplib for the actual sending function
import smtplib
from aiohttp import web
from weasyprint import HTML, CSS
from jinja2 import Template
from aiohttp_jinja2 import template
from aiohttp_session import get_session
from uuid import uuid4
import re
from PIL import Image
from base64 import b64encode
from gs_api.dictionary import Docs, Customer, Project, Projects, General, Devices, Damage, Reports
###
# import asyncio
import nest_asyncio
nest_asyncio.apply()
class language:
    @classmethod

    async def pdf(cls, request, addPdf, forPreview, pid, itemId, type, user_first_name, user_second_name, user_phone, user_mail, today, stworks, fworks, dateForInspect, byForInspect, selectedDocsList, ws_clients):
        # print(pid, item)
        project = await Project.select_project(pid)
        item = await General.get_item_for_pdf(itemId)
        pNumer = (str(language.nulsformat(project['project_number']))+str(project['project_number'])+'-'+str(project['project_number_year']))

        tables = []
        imagesForPdf=[]

        if type=='Invoices':
            invNum = item['number'].split(' ')
            if len(invNum)==5:
                item['number'] = invNum[3]
            else:
                 item['number'] = language.nulsformat(invNum[1])+invNum[1]+'-'+invNum[0].split('-')[1]

        if((type=='Orders')|(type=='Offers')|(type=='Invoices')|(type=='SUB')):
            tables = (await Projects.get_tables_in_edit(itemId))
            for table in tables:
                table['content'] = (await Projects.get_rows_in_table(table['id']))
        if((type=='Devices')):
            tables = (await Devices.get_tables_in_devices(itemId))
            for table in tables:
                table['devices_content'] = (await Devices.get_device_list(table['id']))
                table['measure_protocol'] = (await Devices.get_MeasureProtocol_list(table['id']))

        if((type=='Damage')):
            tables = (await Damage.get_tables_in_damages(itemId))
            for table in tables:
                table['damage_content'] = (await Damage.get_damage_list(table['id']))
                for damage in table['damage_content']:
                    image={}
                    stream = io.BytesIO()
                    image['content'] = await Docs.images_for_pdf(damage['imgId'])
                    im = Image.open(io.BytesIO(image['content']))
                    conv = im.convert('RGB')
                    conv.save(stream, 'JPEG', quality=40)
                    img_str = b64encode(stream.getvalue()).decode()
                    image['content'] = img_str
                    image['name'] = damage['name']
                    image['desc'] = damage['desc']
                    imagesForPdf.append(image)
        if((type=='Reports')):
            tables = (await Reports.get_tables_in_reports(itemId))
            for table in tables:
                table['reports_content'] = (await Reports.get_reports_list(table['id']))
        # print(project['zip']+' '+project['city'])
        data={'dateInspect': item['dateInspect'],
                'dateEvent': item['dateEvent'],
                'customercontract': item['other'],
                # 'worker': '',
                'customerСontract': '',
                'getCustomer': project['name'],
                'getPerson': project['appeal']+' '+project['names'],
                'getCustomerAdress': project['street'],
                'getCustomerAdress1': project['zip']+' '+project['city'],
                'offerHead': type,
                # 'subHead': '',
                'editor': user_first_name+' '+user_second_name,
                'userTel': user_phone,
                'userFax': '',
                'userMail': user_mail,
                'number': item['number'],
                'date': datetime.strptime(today, '%Y-%m-%d').strftime("%d.%m.%Y"),
                'work': item['work'],
                'pNumber': pNumer,
                'street': project['street1'],
                'zip': project['zip1'],
                'contry': project['country'], 
                'area': project['area'],
                'city': project['city1'],
                'dateProject': project['date'],
                'insurance': item['insurance_number'],
                'insurname': item['insurname'],
                'place': item['place'],
                'stworks': stworks,
                'fworks': fworks,
                'inspectedby': byForInspect,
                # 'positions': '',
                # 'comment': item['comment'],
                'project_id': pid,
                'selected_docs_list': selectedDocsList,
                'tables': tables,
                'summ': item['gen_summa'],
                'summ1': item['gen_summa'],
                'discP': item['discP'],
                'butDiscPerc': item['butDiscPerc'],
                'disc': item['gen_discont'],
                'netto': item['gen_summa'],
                'taxP': item['taxP'],
                'tax': item['tax'],
                'taxP2': item['taxPDub'],
                'tax2': item['taxDub'],
                'brutto': item['brutto'],
                'addtaxColapse': item['addtaxColapse']}
        if item['comment'] != None:
            data['comment']= item['comment']
        else:
            data['comment']= ''

        if ((dateForInspect != '')):
            data['inspected'] = datetime.strptime(dateForInspect, '%Y-%m-%d').strftime("%d.%m.%Y")
        else:
            data['inspected'] = 'not set'

        if fworks != 'null':
            if stworks != 'null':
                data['finishWork'] = 'Die Arbeit wurde ausgeführt: vom '+datetime.strptime(stworks, '%Y-%m-%d').strftime("%d.%m.%Y")+' bis '
            else:
                data['finishWork'] = 'Datum der Fertigstellung der Arbeiten: '+datetime.strptime(fworks, '%Y-%m-%d').strftime("%d.%m.%Y")
        else:
            data['finishWork'] = ''

        result =  (await Docs.select_template(data['selected_docs_list']))

        docs = ''.join(map(str, result))
        docs = re.sub("\\s+", " ", docs.replace("'}{'template': '", '<div style="page-break-before:always;"></div>').replace("{'template': '", '').replace("'}", '').replace("\\n", '').replace("\\t", '').replace("\\", ""))
        template = Template(docs)
   
        # objs = await Docs.select_image_damage_pdf(json.loads(data['loadDamages']))
        # images_for_pdf = await Docs.images_for_pdf(152)
        
        # print(data['tables'])
        tables=(data['tables'])
        # tables=json.loads(data['tables'])

        # print(tables)
  


        date_logo = await Docs.date_logo()

        def template_function(func):
            template.globals[func.__name__] = func
            return func

        @template_function
        def digit_formater(val):
            value = round(val * 100) / 100
            parts = str(value).split('.')
            main = parts[0]
            lenx = len(main)
            output = ''
            i = lenx - 1

            while (i >= 0):
                output = main[i] + output
                if (((lenx - i) % 3 == 0) & (i > 0)):
                    output = '.' + output
                i -= 1

            if (len(parts) > 1):
                output += ',' + parts[1]
                if (len(parts[1])==1):
                    output += '0'
            else:
                output += ',00'
           
            output = output.replace('-.','-')
            return output

        @template_function
        def difTime(start, end, format):
            s = datetime.strptime(start, "%Y-%m-%d %H:%M")
            e = datetime.strptime(end, "%Y-%m-%d %H:%M")
            sec = timedelta(seconds=(e-s).total_seconds())
            d = datetime(1,1,1) + sec
            
            if (format=='f'):   
                output = ("%d Tage" % (d.day-1))
            if (format=='h'):
                output = ((e-s).total_seconds() / 3600)
            return output

        @template_function
        def formDate(val):
            # print(val)
            d = datetime.strptime(val, "%Y-%m-%d %H:%M")
            return d.strftime("%d.%m.%Y")

        @template_function
        def digit_count(val):
            output = str(val)
            outputfull = output.split('.')
            if int(outputfull[1])>1:
                output = output.replace('.',',')
            else:
                output = outputfull[0]
            return output

        @template_function
        def sortfrom(val):
            if val != []:
                sortedDate = []
                for date in val:
                    if (date.split(' ')[0])!='':
                        sortedDate.append(datetime.strptime(date.split(' ')[0], "%Y-%m-%d"))
                sortedDate.sort()
                return sortedDate[0].strftime("%d.%m.%Y")
            else:
                return ''

        @template_function
        def sortto(val):
            if val != []:
                sortedDate = []
                for date in val:
                    if (date.split(' ')[0])!='':
                        sortedDate.append(datetime.strptime(date.split(' ')[0], "%Y-%m-%d"))
                sortedDate.sort(reverse=True)
                return sortedDate[0].strftime("%d.%m.%Y")
            else:
                return ''
                
        customers = (await Customer.detectSub(data['number'].split(' ')[0]))
        @template_function
        def detectSub():
            output = str(customers['name'])+'<br/>'
            output = output + str(customers['street'])+'<br/>'
            output = output + str(customers['zip'])+' '
            output = output + str(customers['city'])
            return output 

        def format_seconds_to_hhmmss(seconds):
                hours = seconds // (60*60)
                seconds %= (60*60)
                minutes = seconds // 60
                seconds %= 60
                return "%02i:%02i" % (hours, minutes)
        if '' == data['date']:
            skontodate = 'not set'
            date = 'not set'
        else:
            # skontodate = (datetime.strptime(data['date'], '%Y-%m-%d') + timedelta(days=14)).strftime('%d.%m.%Y')
            skontodate = (datetime.strptime(data['date'], '%d.%m.%Y') + timedelta(days=14)).strftime('%d.%m.%Y')
            date = data['date']
        h=template.render(
            date=date,
            skontodate=skontodate,
            imagesForPdf=imagesForPdf,
            offerHead=data['offerHead'],
            number=data['number'],
            selected_docs_list=data['selected_docs_list'],
              # number=number.split(' ')[0],
            getCustomer=data['getCustomer'],
            getPerson=data['getPerson'],
            getCustomerAdress=data['getCustomerAdress'],
            getCustomerAdress1=data['getCustomerAdress1'],
            editor=data['editor'],
            userTel=data['userTel'],
            userFax=data['userFax'],
            userMail=data['userMail'],
            work=data['work'],
            pNumber=data['pNumber'],
            street=data['street'],
            zip=data['zip'],
            city=data['city'],
            contry=data['contry'],
            area=data['area'],
            insurance=data['insurance'],
            insurname=data['insurname'],
            place=data['place'],
            firstText=data['stworks'],
            secondText=data['fworks'],
            dateProject=data['dateProject'],
            inspected=data['inspected'],
            inspectedby=data['inspectedby'],
            # threText='',
            # fourText='',
            # fiveText='',
            # sixText='',
            summ=data['summ'],
            summ1=data['summ1'],
            customercontract = data['customercontract'],
            finishWork=data['finishWork'],
            discP=data['discP'],
            butDiscPerc=data['butDiscPerc'],
            disc=data['disc'],
            taxP=data['taxP'],
            tax=data['tax'],
            taxP2=data['taxP2'],
            tax2=data['tax2'],
            brutto=data['brutto'],
            netto=data['netto'],
            tables=(data['tables']),
            # tables=json.loads(data['tables']),
            comment=data['comment'],
            # prices='',
            date_logo = date_logo['date_logo'],
            date_logo_head = date_logo['date_logo_head'],
            date_logo_address = date_logo['date_logo_address'],
            date_logo_image = date_logo['date_logo_image']
            )
        if addPdf == 'true':
            # print('true')
            date=data['date']
            offerHead=data['offerHead']
            number=data['number']
            project_id=data['project_id']
            user=data['editor']

            pdf = HTML(string=h).write_pdf(stylesheets=[CSS(string='@page { size: A4; margin-top: 5mm; margin-left: 10mm; margin-right: 10mm; margin-bottom: 3mm; }')])
            resp = web.StreamResponse(headers={
            'CONTENT-DISPOSITION': 'inline'
            })
            resp.content_type ="application/pdf"
            await resp.prepare(request)
            await resp.write(pdf)
            file = bytes(pdf)
            number_of_pages=0
            pdf_file = io.BytesIO(file)
            read_pdf = PyPDF2.PdfFileReader(pdf_file)
            number_of_pages = read_pdf.getNumPages()
            # pages=data['number']
            added=strftime("%d-%m-%Y %H:%M:%S", localtime())
            web.json_response(await Docs.add_pdf(h, date, offerHead, number, added, number_of_pages, project_id, user))
            # print('getDocs:'+pid)
            
            for client in ws_clients:
                await client.send_str('print:'+forPreview+':'+offerHead+':'+number)
                await client.send_str('getDocs:'+pid)

        if addPdf == 'separator':
            date=data['date']
            offerHead=data['offerHead']
            number=data['number']
            project_id=data['project_id']
            user=data['editor']
            docs = ''

            resp = web.StreamResponse(headers={
                'CONTENT-DISPOSITION': 'inline'
            })
            resp.content_type ="application/pdf"
            await resp.prepare(request)
            for index, page in enumerate(h.split('<html>')):
                if index > 0:
                    part = '<html>'+page

                    pdf = HTML(string=part).write_pdf(stylesheets=[CSS(string='@page { size: A4; margin-top: 5mm; margin-left: 10mm; margin-right: 10mm; margin-bottom: 3mm; }')])
                   
                    resp.write(pdf)
                    
                    file = bytes(pdf)
                    number_of_pages=0
                    pdf_file = io.BytesIO(file)
                    read_pdf = PyPDF2.PdfFileReader(pdf_file)
                    number_of_pages = read_pdf.getNumPages()
                    # pages=data['number']
                    added=strftime("%d-%m-%Y %H:%M:%S", localtime())
                    web.json_response(await Docs.add_pdf(part, date, offerHead, number+'#'+str(index), added, number_of_pages, project_id, user))
                    docs = docs + number+'#'+str(index)+' '
            for client in ws_clients:
                await client.send_str('print:'+forPreview+':'+offerHead+':'+docs)
                await client.send_str('getDocs:'+pid)

        if addPdf == 'false':
            pdf = HTML(string=h).write_pdf()
            resp = web.StreamResponse(headers={
            'CONTENT-DISPOSITION': 'inline'
            })
            resp.content_type ="application/pdf"
            await resp.prepare(request)
            await resp.write(pdf)

        # print(forPreview)
            for client in ws_clients:
                await client.send_str('preview:'+forPreview)

                # await client.send_str('getDocs')
                # await client.send_str('getProjectDetail')

        return resp
    
    def nulsformat(val):
        num=''
        nuls = (int(4)-int(len(str(val))))
        for x in range(0, int(nuls)):
            num = str(num)+'0'
        return num