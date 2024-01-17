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
from gs_api.dictionary import Docs, Customer
###
import asyncio
import nest_asyncio
nest_asyncio.apply()
class language:
    @classmethod
    async def pdf(cls, request, data, ws_clients):
        result =  (await Docs.select_template(data['selected_docs_list']))

        docs = ''.join(map(str, result))
        docs = re.sub("\\s+", " ", docs.replace("'}{'template': '", '<div style="page-break-before:always;"></div>').replace("{'template': '", '').replace("'}", '').replace("\\n", '').replace("\\t", '').replace("\\", ""))
        template = Template(docs)
   
        # objs = await Docs.select_image_damage_pdf(json.loads(data['loadDamages']))
        # images_for_pdf = await Docs.images_for_pdf(152)
        # print(data['tables'])
        tables=json.loads(data['tables'])
        # print(tables)
        imagesForPdf=[]
        for table in tables:
            for damage in table['parts']['damage_content']:
                image={}
                image['content'] = b64encode(await Docs.images_for_pdf(damage['imgId'])).decode()
                #image['content'] = await Docs.images_for_pdf(damage['imgId'])
                #im = Image.open(io.BytesIO(image['content']))
                # im.thumbnail((100,100), Image.ANTIALIAS)
                #stream = io.BytesIO()
                #im.save(stream, "JPEG", quality=10)
                
                #image['content'] = im

                image['name'] = damage['name']
                image['desc'] = damage['desc']
                # image['rotate'] = damage['rotate']
                # print(image)
                imagesForPdf.append(image)


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

        # allhours = 0
        # allhoursPrint=''
        # for damage in objs:
        #     hours= datetime(1, 1, 1, 0, 0)-datetime(1, 1, 1, 0, 0)
        #     for task in damage['tasks']:
        #         date = task['data_time_start'].split(' ')
        #         y=int(date[0].split('-')[0])
        #         m=int(date[0].split('-')[1])
        #         d=int(date[0].split('-')[2])
        #         h=int(date[1].split(':')[0])
        #         mm=int(date[1].split(':')[1])

        #         if 2 < len(date[1].split(':')):
        #             s=int(date[1].split(':')[2])
        #         else:
        #             s=0
        #         dts = datetime(y, m, d, h, m, s)

        #         date = task['data_time_end'].split(' ')
        #         y=int(date[0].split('-')[0])
        #         m=int(date[0].split('-')[1])
        #         d=int(date[0].split('-')[2])
        #         h=int(date[1].split(':')[0])
        #         mm=int(date[1].split(':')[1])

        #         if 2 < len(date[1].split(':')):
        #             s=int(date[1].split(':')[2])
        #         else:
        #             s=0
        #         dtf = datetime(y, m, d, h, m, s)
        #         result = (dtf-dts)
        #         diftime = (dtf-dts)
                
        #         # result = str(round(result, 2))
        #         cW=1
        #         if not task['workers']==None:
        #             cW = len(task['workers'].split(','))
                
        #         hours = hours + diftime * cW
        #         task['data_time_end']=format_seconds_to_hhmmss(diftime.total_seconds())
        #     damage['hours']= format_seconds_to_hhmmss(hours.total_seconds())
        #     allhours=allhours+(hours.total_seconds())
        #     allhoursPrint = format_seconds_to_hhmmss(allhours)
        
        if '' == data['date']:
            skontodate = 'not set'
            date = 'not set'
        else:
            skontodate = (datetime.strptime(data['date'], '%d.%m.%Y') + timedelta(days=14)).strftime('%d.%m.%Y')
            date = data['date']
        
        # print(data['stworks'])
        # print(data['fworks'])
        
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
            threText='',
            fourText='',
            fiveText='',
            sixText='',
            summ=data['summ'],
            summ1=data['summ1'],
            customercontract = data['customerСontract'],
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
            tables=json.loads(data['tables']),
            comment=data['comment'],
            prices='',
            date_logo = date_logo['date_logo'],
            date_logo_head = date_logo['date_logo_head'],
            date_logo_address = date_logo['date_logo_address'],
            date_logo_image = date_logo['date_logo_image']
            )

        # print(data['addPdf'])
        if data['addPdf'] == 'true':
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
            pages=data['number']
            added=strftime("%d-%m-%Y %H:%M:%S", localtime())
            web.json_response(await Docs.add_pdf(h, date, offerHead, number, added, number_of_pages, project_id, user))
            for client in ws_clients:
                await client.send_str('getDocs')

        if data['addPdf'] == 'separator':
            date=data['date']
            offerHead=data['offerHead']
            number=data['number']
            project_id=data['project_id']
            user=data['editor']

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
                    pages=data['number']
                    added=strftime("%d-%m-%Y %H:%M:%S", localtime())


                    web.json_response(await Docs.add_pdf(part, date, offerHead, number, added, number_of_pages, project_id, user))

            for client in ws_clients:
                await client.send_str('getDocs')

        if data['addPdf'] == 'false':
            pdf = HTML(string=h).write_pdf()
            resp = web.StreamResponse(headers={
            'CONTENT-DISPOSITION': 'inline'
            })
            resp.content_type ="application/pdf"
            await resp.prepare(request)
            await resp.write(pdf)

            # for client in ws_clients:
            #     await client.send_str('getDocs')
            #     await client.send_str('getProjectDetail')

        return resp