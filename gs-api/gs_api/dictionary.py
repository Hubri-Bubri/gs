from sqlbuilder.smartsql import Q, T
from sqlbuilder.smartsql.dialects import mysql
from .api import Database, DictCursor
import json
from os import path

from datetime import datetime as dt
import datetime
from base64 import b64encode

import asyncio
import nest_asyncio
nest_asyncio.apply()


database = Database(
    cursor_type=DictCursor,
    compile=mysql.compile
)

class User:
    @classmethod
    async def select_by_login_password(cls, login, password):
        async with database.query() as Q:
            return await (Q()
                .tables(T.user)
                .fields(T.user.login)
                .where((T.user.login == login) & (T.user.password == password))
                .selectone())
 
    @classmethod
    async def select_by_login(cls, login):
        async with database.query() as Q:
            return await (Q()
                .tables(T.user)
                .fields(T.user.id, T.user.login, T.user.first_name, T.user.second_name, T.user.tel, T.user.fax, T.user.mail)
                .where((T.user.login == login))
                .selectone())

    @classmethod
    async def select_roles_by_login(cls, login):
        async with database.query() as Q:
            return await (Q()
                .tables((T.role & T.m2m_user_role & T.user).on(
                        (T.role.id == T.m2m_user_role.role_id) &
                        (T.user.id == T.m2m_user_role.user_id)))
                .fields(T.role.name)
                .where((T.user.login == login))
                .selectall())

    @classmethod
    async def select_profile(cls, login, company_id):
        return {
            'account': await cls.select_by_login(login),
            'roles': await cls.select_roles_by_login(login),
            'selected-company': await Company.select_by_id(company_id),
            'access-user': await PermissionSchema.select_by_login(login),
            'access-role': await PermissionSchema.select_by_login(login)
        }

class PermissionSchema:
    @classmethod
    async def select_by_login(cls, login):
        async with database.query() as Q:
            return await (Q()
                .tables((T.user & T.user_permission_schema).on(T.user.id == T.user_permission_schema.user_id))
                .fields(T.user.login,
                        T.user_permission_schema.target,
                        T.user_permission_schema.permission,
                        T.user_permission_schema.domen)
                .where(T.user.login == login)
                .selectall())


class Application:
    @classmethod
    async def select_by_company(cls, company_id):
        async with database.query() as Q:
            return await (Q()
                .tables((T.application & T.m2m_company_application).on(
                         T.application.id == T.m2m_company_application.application_id))
                .fields(T.application.name, T.application.link)
                .where(T.m2m_company_application.company_id == company_id)
                .selectall())


class Company:
    @classmethod
    async def select_by_login(cls, login):
        async with database.query() as Q:
            return await (Q()
                .tables((T.company & T.user & T.m2m_user_company).on(
                    (T.company.id == T.m2m_user_company.company_id) &
                    (T.user.id == T.m2m_user_company.user_id)
                ))
                .fields(T.company.id, T.company.name)
                .where(T.user.login == login)
                .selectall())

    @classmethod
    async def select_by_id(cls, id):
        async with database.query() as Q:
            return await (Q()
                .tables(T.company)
                .fields(T.company.name)
                .where(T.company.id == id)
                .selectone())

#####start Sub
class Sub:
    @classmethod
    async def send_price(cls, ids, names):
        #print(type, ids, names, item_id)
        # arr=[]
        # for v in ids.split(","):
        #    arr=arr+','+v
 
        async with database.query() as Q:
            items = (await (Q()
                            .tables(T.price)
                            .fields(
                                T.price.pos_num,
                                T.price.name,
                                T.price.desc,
                                T.price.unit,
                                T.price.price,
                                T.price.without,
                                T.price.percent
                            )
                            .where(T.price.id.in_(ids.split(",")))
                            .selectall()))

            for item in items:
                newPrice = item['price'].replace(',','.')
                try:
                    newPrice = float(newPrice)
                except:
                    newPrice = 0

                if item['unit']=='%':
                    item['unit'] = 'f-proc'
                    item['count'] = '1'
                else:
                    item['count'] = '0'

                for v in names.split(","):
                        await (Q(T.sub_rows_for_table)
                            .tables(T.sub_rows_for_table)
                            .insert({
                                    T.sub_rows_for_table.position_number: item['pos_num'],
                                    T.sub_rows_for_table.description_head: item['name'],
                                    T.sub_rows_for_table.description_from_price: '',
                                    T.sub_rows_for_table.unit: item['unit'],
                                    T.sub_rows_for_table.price: newPrice,
                                    T.sub_rows_for_table.without: item['without'],
                                    T.sub_rows_for_table.discount: item['percent'],
                                    T.sub_rows_for_table.table_id: v,
                                    T.sub_rows_for_table.status: 'yes',
                                    # T.rows_for_table.alttax: ,
                                    T.sub_rows_for_table.description_work: item['desc'],
                                    T.sub_rows_for_table.count: item['count'],
                                    T.sub_rows_for_table.done: ''
                            }))
        return ''

    @classmethod
    async def sub_order(cls):
        async with database.query() as Q:
            return await (Q()
                .tables(T.sub_items)
                .fields(
                    T.sub_items.id,
                    T.sub_items.project_id,
                    T.sub_items.status_set,
                    T.sub_items.number,
                    T.sub_items.date,
                    T.sub_items.other,
                    T.sub_items.place,
                    T.sub_items.insurance_number,
                    T.sub_items.work,
                    T.sub_items.type,
                    T.sub_items.tax,
                    T.sub_items.taxDub,
                    T.sub_items.taxP,
                    T.sub_items.taxPDub,
                    T.sub_items.disc,
                    T.sub_items.discP,
                    T.sub_items.butDiscPerc,
                    T.sub_items.addtaxColapse,
                    T.sub_items.dateEvent,
                    T.sub_items.dateInspect,
                    T.sub_items.ExamWorker,
                    T.sub_items.comment,
                    T.sub_items.order_id
                )
                # .where(T.sub_items.order_id == id)
                .selectall())

    @classmethod
    async def add_part(cls, part_name, item_id):
        async with database.query() as Q:
                await (Q()
                    .tables(T.sub_tables)
                    .insert({
                        T.sub_tables.name: part_name,
                        T.sub_tables.item_id: item_id,
                        T.sub_tables.obj: '',
                        T.sub_tables.selected: ''
                    }))
        return ''

    @classmethod
    async def select_project(cls, id):
        async with database.query() as Q:
            return await (Q()
                .tables(T.sub_project & T.user).on(T.sub_project.user_id == T.user.id)
                .fields(
                    T.sub_project.project_number_year,
                    T.sub_project.id,
                    T.sub_project.date,
                    T.sub_project.street,
                    T.sub_project.city,
                    T.sub_project.zip,
                    T.sub_project.customer_id,
                    T.sub_project.person_id,
                    T.sub_project.mail,
                    T.sub_project.phone,
                    T.sub_project.fax,
                    T.sub_project.other,
                    T.user.first_name,
                    T.user.second_name,
              
                ).where(T.sub_project.id == id)
                .selectone())

    @classmethod
    async def select_projects(cls, page):
        # print(page)
        async with database.query() as Q:
            result = (await (Q(T.sub_project)
                             .fields(
                                 T.sub_project.project_number_year,
                                 T.sub_project.date,
                                 T.sub_project.street,
                                 T.sub_project.city,
                                 T.sub_project.zip,
                                 T.sub_project.status_set,
                                 T.sub_project.id,
                                 T.sub_project.other
                            )[:int(page) * 30].selectall()))
            for item in result:
                subItem = (await (Q(T.sub_items)
                            .fields(
                                 T.sub_items.status_set,
                            )
                            .where((T.sub_items.project_id == item['id'])&(T.sub_items.type != 3))
                            .selectall()))
                count = 0
                for status in subItem:
                    # print(status['status_set'])
                    if status['status_set']=='Done':
                        count = count + 1

                if (len(subItem)!=0):
                    if (count==len(subItem)):
                        item['_rowVariant']='warning'
                    else:
                        item['_rowVariant']=''
                else:
                    item['_rowVariant']=''
            # page= int(page) * 30
            # print(page)
# [:int(page)]
        return result




    @classmethod
    async def update_table_data(cls, id, fild, data):
        async with database.query() as Q:
            # print(id, fild, data)
            # if fild == 'without':
            #     if data == true:
            #         data
            #     else:
            if data=='Null':
                data = ''
            return await (Q()
                .tables(T.sub_rows_for_table)
                .where(T.sub_rows_for_table.id == id)
                .update({
                    T.sub_rows_for_table[fild]: data
                }))

    @classmethod
    async def update(cls, id, data, fild):
        async with database.query() as Q:
              return await (Q()
                .tables(T.sub_project)
                .where(T.sub_project.id == id)
                .update({
                    T.sub_project[fild]: data
                }))

    @classmethod
    async def update_item(cls, val, type, id):
        async with database.query() as Q:
                 await (Q()
                     .tables(T.sub_items)
                     .where(T.sub_items.id == id)
                     .update({
                         T.sub_items[type]: val
                     }))
        return ''

    @classmethod
    async def select_project_new(cls, id):
        async with database.query() as Q:
            result = (await (Q()
                .tables(T.sub_items & T.type_for_table).on(T.sub_items.type == T.type_for_table.id)
                .fields(
                    T.sub_items.id,
                    T.sub_items.number,
                    T.sub_items.date,
                    T.sub_items.other,
                    T.sub_items.place,
                    T.sub_items.insurance_number,
                    T.sub_items.work,
                    T.sub_items.status_set,
                    T.type_for_table.type,
                    T.sub_items.tax,
                    T.sub_items.taxDub,
                    T.sub_items.taxP,
                    T.sub_items.taxPDub,
                    T.sub_items.disc,
                    T.sub_items.discP,
                    T.sub_items.butDiscPerc,
                    T.sub_items.addtaxColapse,
                    T.sub_items.dateEvent,
                    T.sub_items.dateInspect,
                    T.sub_items.ExamWorker
                )
                .where(T.sub_items.project_id == id)
                .selectall()))

            result1 = ( await (Q()
                .tables(T.sub_items )
                .fields(
                    T.sub_items.id,
                    T.sub_items.number
                )
                .selectall()))

            balance = ( await (Q()
                .tables(T.rows_for_balance)
                .fields(
                    T.rows_for_balance.id,
                    T.rows_for_balance.type,
                    T.rows_for_balance.value,
                    T.rows_for_balance.date,
                    T.rows_for_balance.invoice_id
                )
                .selectall()))
            for item in result:
                
                if (item['type'] == 'Damage Description'):
                   # print(item['type'])
                   result.remove(item)

            for item in result:
                id =  item['number'].split(' ')
                if len(id)==2:
                    for number in result1:
                        if int(id[1]) == number['id']: 
                            item['contract_number']=number['number']

            for item in result:
                ops=[]
                for bal in balance:
                    if item['id']==bal['invoice_id']: 
                        ops.append({'type':bal['type'], 'value':bal['value'], 'date':bal['date'], 'id':bal['id']})
                item['op'] = ops
 
            cOffer=0
            cCounract=0
            cDamage=0

            for item in result:    
                if item['tax']==None:
                    item['tax']='0,0'
                if item['taxDub']==None:
                    item['taxDub']='0,0'
                if item['taxP']==None:
                    item['taxP']='0,0'
                if item['taxPDub']==None:
                    item['taxPDub']='0,0'
                if item['disc']==None:
                    item['disc']='0,0'
                if item['discP']==None:
                    item['discP']='0,0'
                if item['butDiscPerc']==None:
                    item['butDiscPerc']='%'
                if item['addtaxColapse']==None:
                    item['addtaxColapse']='false'

                tax=(item['tax'].replace(',', '.'))
                taxDub=(item['taxDub'].replace(',', '.'))
                taxP=(item['taxP'].replace(',', '.'))
                taxPDub=(item['taxPDub'].replace(',', '.'))
                disc=(item['disc'].replace(',', '.'))
                discP=(item['discP'].replace(',', '.'))
                butDiscPerc=item['butDiscPerc']
                addtaxColapse=item['addtaxColapse']

                netto = 0
                addt = 0
                addt2 = 0
                tables =(await (Q()
                        .tables(T.sub_tables)
                        .fields(
                            T.sub_tables.id,
                            T.sub_tables.name
                        )
                        .where(T.sub_tables.item_id == item['id'])
                        .selectall()))
                add = 0
                for val in tables:
                    rows =(await (Q()
                                .tables(T.sub_rows_for_table)
                                .fields(
                                    T.sub_rows_for_table.count,
                                    T.sub_rows_for_table.price,
                                    T.sub_rows_for_table.summa,
                                    T.sub_rows_for_table.status,
                                    T.sub_rows_for_table.alttax,
                                    T.sub_rows_for_table.without,
                                    T.sub_rows_for_table.unit
                                )
                                .where(T.sub_rows_for_table.table_id == val['id'])
                                .selectall()))
                    
                    for row in rows:
                        if row['count']==None:
                            row['count'] = '0'
                        if row['price']==None:
                            row['price'] = '0'

                        if row['unit']=='%':
                                row['count']=1
                        if row['status']=='yes':
                            
                            try:
                               a = float(row['price'])
                            except ValueError:
                               row['price'] = 0
                            netto += (float(row['count'])*float(row['price']))
                            if row['without']=='true':
                                add += (float(row['count'])*float(row['price']) / 100) * float(discP)

                            # print(row['alttax'])
                            if row['alttax']!='true':
                                addt += (float(row['count'])*float(row['price']))
                            else:
                                addt2 += (float(row['count'])*float(row['price']))
                            


           
                if netto==0:
                    netto=1
                if butDiscPerc=='%':
                    # print(netto, add)
                    # netto = netto + add
                    item['netto']=str(netto-(netto/100*float(discP)))
                    # print(item['netto'])
                    item['netto']=float(item['netto'])+add
                    # print(item['netto'], add)

                    addt = addt-(addt/100)*float(discP)
                    addt2 = addt2-(addt2/100)*float(discP)
                
                else:

                    item['netto']=str(netto-float(discP))
                    
                    addt = addt-(addt/100)*float(discP)*100/netto
                    addt2 = addt2-(addt2/100)*float(discP)*100/netto
                
                #addt = addt2 = 0
                # item['netto']=0

                #tmpTax = (addt * (float(taxP) / 100))
                #tmpTax2= (addt2 * (float(taxPDub) / 100))
    
                item['brutto']=str(float(item['netto'])+(addt * (float(taxP) / 100))+(addt2 * (float(taxPDub) / 100)))
                
                if (item['type'] == 'Offers'):
                    cOffer=cOffer+1
                    if(len(str(cOffer))<2):
                        nOffer = '0'+str(cOffer)
                    item['number'] = item['number'] + '-' + nOffer
                
                if (item['type'] == 'Contracts'):
                    cCounract=cCounract+1
                    if(len(str(cCounract))<2):
                        nCounract = '0'+str(cCounract)
                    item['number'] = item['number'] + '-' + nCounract

                        
                if (item['type'] == 'Damage Description'):
                    cDamage=cDamage+1
                    item['number']=item['number'].split(' ')[0]
                    if(len(str(cDamage))<2):
                        nDamage = '0'+str(cDamage)
                    item['number'] = item['number'] + '-' + nDamage


                # item['brutto']=str(item['brutto']).replace('.',',')
                # item['netto']=str(item['netto']).replace('.',',')
            # print(result)
            return result


    @classmethod
    async def del_row_from_table(cls, id):
        async with database.query() as Q:
            return await (Q(T.sub_rows_for_table)
                    .where(T.sub_rows_for_table.id == id)
                    .delete())

    classmethod #first function on python
    async def change(old, new):
        async with database.query() as Q:
                await (Q()
                            .tables(T.sub_rows_for_table)
                            .where(T.sub_rows_for_table.id == old)
                            .update({
                                T.sub_rows_for_table.id: 999999999
                            }))
                await (Q()
                            .tables(T.sub_rows_for_table)
                            .where(T.sub_rows_for_table.id == new)
                            .update({
                                T.sub_rows_for_table.id: old
                            }))
                await (Q()
                            .tables(T.sub_rows_for_table)
                            .where(T.sub_rows_for_table.id == 999999999)
                            .update({
                                T.sub_rows_for_table.id: new
                            }))
    @classmethod
    async def update_id_in_one_table(cls, newIndex, oldIndex, newPart):
        async with database.query() as Q:
            table =(await (Q()
                    .tables(T.sub_tables)
                    .fields(
                        T.sub_tables.id,
                        T.sub_tables.obj,
                        T.sub_tables.selected
                    )
                    .where((T.sub_tables.id == newPart))
                    .selectone()))


            # print(table)
            table['selected'] = table['selected'].replace('|', '"], ')
            table['selected'] = '{'+table['selected'].replace(':', '":[')+'"]}'
            table['selected'] = table['selected'].replace('in', '"in')
            table['selected'] = table['selected'].replace('temp', '"')
            table['selected'] = table['selected'].replace(',"', '","')
            
            # befor_selected = table['selected']
            if table['selected'] != '{"]}':
                befor_selected = json.loads(table['selected'])
            else:
                befor_selected = ''       
            after_selected = ''
            # print(oldIndex, newIndex)
            for index, selected_group in enumerate(befor_selected):
                selected_group_new = ''
                for i, selected in enumerate(befor_selected[selected_group]):
                    old_select_index = int(selected) - 1
                    if i == 0:
                        if (int(newIndex) <= old_select_index) & (int(oldIndex) > old_select_index):
                            old_select_index = old_select_index + 1
                        if (int(newIndex) >= old_select_index) & (int(oldIndex) < old_select_index):
                            old_select_index = old_select_index - 1
                    else:
                        if int(oldIndex) == old_select_index:
                            old_select_index = int(newIndex)
                    
                    new_select_index = old_select_index + 1

                    selected_group_new = selected_group_new + ',temp'+str(new_select_index)
                
                if index == 0:
                    add = ''
                else:
                    add = '|'

                after_selected = after_selected + add +'in' + str(index) + ':' + str(selected_group_new)
                after_selected = after_selected.replace(':,', ':')
                after_selected = after_selected.replace(':,', ':')

            await (Q()
                     .tables(T.sub_tables)
                     .where(T.sub_tables.id == newPart)
                     .update({
                         T.sub_tables.selected: after_selected
                     }))

            oldrows =(await (Q()
                .tables(T.sub_rows_for_table)
                .fields(
                    T.sub_rows_for_table.id,
                    T.sub_rows_for_table.without
                )
                .where((T.sub_rows_for_table.table_id == newPart))
                .selectall()))

            new = (oldrows[int(newIndex)]['id'])
            old = (oldrows[int(oldIndex)]['id'])
  
            await Sub.change(old, new)

            newrows =(await (Q()
                .tables(T.sub_rows_for_table)
                .fields(
                    T.sub_rows_for_table.id,
                    T.sub_rows_for_table.count
                )
                .where((T.sub_rows_for_table.table_id == newPart))
                .selectall()))

            newx = (newrows[int(newIndex)]['id'])

            if((int(oldIndex)-int(newIndex))!=1):
                if oldIndex>newIndex:
                    start = int(newIndex)
                    end = int(oldIndex)
                else:
                    start = int(oldIndex)
                    end = int(newIndex)
                for  x in range(start, end):
        
                    if oldIndex>newIndex:
                        if ((((int(oldIndex)!=0) * (int(oldIndex)!=(len(oldrows))-1)) + ((int(newIndex)!=0) * (int(newIndex)!=(len(oldrows))-1)))==2):
                            approx = int(newIndex)-2
                            index = (len(oldrows)-x+approx)
                            move = -1
                        else:
                            approx = int(newIndex)-1
                            index = (len(oldrows)-x+approx)
                            move = -1
                            if ((int(newIndex)==0) & (int(oldIndex)!=(len(oldrows)-1))):
                                index=index-(len(oldrows)-int(oldIndex))+1
                    else:
                        index = x
                        move =  1

                    old = (newrows[index]['id'])
                    new = ((oldrows[index+move]['id']))

                    if ((newx!=newrows[index]['id']) & (newx!=(oldrows[index+move]['id']))):
                        await Sub.change(old, new)

        return ''

    @classmethod
    async def update_id(cls, newIndex, newPart, oldIndex, oldPart):
        async with database.query() as Q:

            table =(await (Q()
                    .tables(T.sub_tables)
                    .fields(
                        T.sub_tables.id,
                        T.sub_tables.obj,
                        T.sub_tables.selected
                    )
                    .where((T.sub_tables.id == oldPart))
                    .selectone()))

            el = int(oldIndex)+1
            el = ',temp' + str(el)
            oldselected = str(table['selected'])
            after_selected = oldselected.replace(el, '')
            # print(after_selected)

            await (Q()
                     .tables(T.sub_tables)
                     .where(T.sub_tables.id == oldPart)
                     .update({
                         T.sub_tables.selected: after_selected
                     }))

            newrows =(await (Q()
                .tables(T.sub_rows_for_table)
                .fields(
                    T.sub_rows_for_table.id,
                    T.sub_rows_for_table.count
                )
                .where((T.sub_rows_for_table.table_id == newPart))
                .selectall()))

            oldrows =(await (Q()
                .tables(T.sub_rows_for_table)
                .fields(
                    T.sub_rows_for_table.id
                )
                .where((T.sub_rows_for_table.table_id == oldPart))
                .selectall()))

            try:
                newrows[int(newIndex)]
            except IndexError:
                new = (oldrows[int(oldIndex)]['id'])
            else:
                new = (newrows[int(newIndex)]['id'])

            old = (oldrows[int(oldIndex)]['id'])

            await (Q()
                 .tables(T.sub_rows_for_table)
                 .where(T.sub_rows_for_table.id == old)
                 .update({
                     T.sub_rows_for_table.table_id: newPart
                 }))

            after_add =(await (Q()
                .tables(T.sub_rows_for_table)
                .fields(
                    T.sub_rows_for_table.id
                )
                .where((T.sub_rows_for_table.table_id == newPart))
                .selectall()))
            new = (after_add[int(newIndex)]['id'])
            await Sub.change(old, new)
            newTable = (await (Q()
                .tables(T.sub_rows_for_table)
                .fields(
                    T.sub_rows_for_table.id,
                    T.sub_rows_for_table.count
                )
                .where((T.sub_rows_for_table.table_id == newPart))
                .selectall()))


            for index, row in enumerate(newTable):
                if (int(index) > (int(newIndex)+1)):
                        old = int(newrows[index-1]['id'])
                        new = int(row['id'])
                        # print(newrows[index-1]['count']+'->'+row['count'])
                        await Sub.change(old, new)
                if (int(index) < (int(newIndex)-1)):
                        old = int(newrows[index]['id'])
                        new = int(row['id'])
                        # print(newrows[index]['count']+'->'+row['count'])
                        await Sub.change(old, new)

        return ''


    @classmethod
    async def update_id_table(cls, newIndex, oldIndex, id):
        async with database.query() as Q:

            rows =(await (Q()
                .tables(T.sub_tables)
                .fields(
                    T.sub_tables.id,
                )
                .where((T.sub_tables.item_id == id))
                .selectall()))
            # print(newIndex, oldIndex)
            old = (rows[int(oldIndex)]['id'])
            new = (rows[int(newIndex)]['id'])

            await (Q()
                 .tables(T.sub_rows_for_table)
                 .where(T.sub_rows_for_table.table_id == old)
                 .update({
                     T.sub_rows_for_table.table_id : 999999999
                 }))
            await (Q()
                 .tables(T.sub_rows_for_table)
                 .where(T.sub_rows_for_table.table_id == new)
                 .update({
                     T.sub_rows_for_table.table_id : old
                 }))
            await (Q()
                 .tables(T.sub_rows_for_table)
                 .where(T.sub_rows_for_table.table_id == 999999999)
                 .update({
                     T.sub_rows_for_table.table_id : new
                 }))

            await (Q()
                 .tables(T.sub_tables)
                 .where(T.sub_tables.id == old)
                 .update({
                     T.sub_tables.id: 999999999
                 }))
            await (Q()
                 .tables(T.sub_tables)
                 .where(T.sub_tables.id == new)
                 .update({
                     T.sub_tables.id: old
                 }))
            await (Q()
                 .tables(T.sub_tables)
                 .where(T.sub_tables.id == 999999999)
                 .update({
                     T.sub_tables.id: new
                 }))
        return ''

    @classmethod
    async def get_tables(cls, id):
        async with database.query() as Q:
            item = (await (Q()
            .tables(T.sub_items)
            .fields(
                    T.sub_items.tax,
                    T.sub_items.taxDub,
                    T.sub_items.taxP,
                    T.sub_items.taxPDub,
                    T.sub_items.disc,
                    T.sub_items.discP,
                    T.sub_items.butDiscPerc,
                    T.sub_items.addtaxColapse

                )
            .where(T.sub_items.id == id)
            .selectone()))

            if item['tax']==None:
                    item['tax']='0,0'
            if item['taxDub']==None:
                    item['taxDub']='0,0'
            if item['taxP']==None:
                    item['taxP']='0,0'
            if item['taxPDub']==None:
                    item['taxPDub']='0,0'
            if item['disc']==None:
                    item['disc']='0,0'
            if item['discP']==None:
                    item['discP']='0,0'
            if item['butDiscPerc']==None:
                    item['butDiscPerc']='%'
            if item['addtaxColapse']==None:
                    item['addtaxColapse']='false'

            tax=(item['tax'].replace(',', '.'))
            taxDub=(item['taxDub'].replace(',', '.'))
            taxP=(item['taxP'].replace(',', '.'))
            taxPDub=(item['taxPDub'].replace(',', '.'))
            disc=(item['disc'].replace(',', '.'))
            discP=(item['discP'].replace(',', '.'))
            butDiscPerc=item['butDiscPerc']
            addtaxColapse=item['addtaxColapse']

         


            partx = []
            tables =(await (Q()
                    .tables(T.sub_tables)
                    .fields(
                        T.sub_tables.id,
                        T.sub_tables.name,
                        T.sub_tables.obj,
                        T.sub_tables.selected
                    )
                    .where(T.sub_tables.item_id == id)
                    .selectall()))
             
            for val in tables:                
                rows =(await (Q()
                            .tables(T.sub_rows_for_table)
                            .fields(
                                T.sub_rows_for_table.id,
                                T.sub_rows_for_table.table_id,
                                T.sub_rows_for_table.count,
                                T.sub_rows_for_table.status,
                                T.sub_rows_for_table.alttax,
                                T.sub_rows_for_table.summa,
                                T.sub_rows_for_table.unit,
                                T.sub_rows_for_table.without,
                                T.sub_rows_for_table.done,
                                T.sub_rows_for_table.description_head,
                                T.sub_rows_for_table.description_work,
                                T.sub_rows_for_table.description_from_price,
                                T.sub_rows_for_table.discount,
                                T.sub_rows_for_table.position_number,
                                T.sub_rows_for_table.description_from_price,
                                T.sub_rows_for_table.price,
                                T.sub_rows_for_table.id
                            )
                            .where(T.sub_rows_for_table.table_id == val['id'])
                            .selectall()))
                
                
                flavours={}
                objNone={}
                disable=[]
                selResults={}
                if val['obj'] is not None:
                    
                    for obj in val['obj'].split(','):
                        count=0
                        objs=[]

                        for row in rows:
                            row['upHere']=False
                            count=count+1
                            objs.append('temp'+str(count))

                            if row['done']==None:
                                row['done']=''
                            if row['done']=='false':
                                row['done']=''
                            if row['alttax']=='true':
                                row['alttax']=True
                            if row['alttax']=='false':
                                row['alttax']=False

                            if row['without']=='true':
                                row['without']=True
                            else:
                                row['without']=False
                           
                        flavours[obj]=objs
                        objNone[obj]=False

                    selResults={}
                    for sel in val['selected'].split('|'):

                        select = sel.split(':')
                        if len(select)==2:
                            if select[1]=='':
                                select=''

                            selResults[select[0]]=select[1].split(',')
                            for dis in select[1].split(','):
                                disRow = dis.split('temp')[1]
                                disRow = select[0]+'-'+str(int(disRow)-1)
                                disable.append(disRow)

                        else:
                            flavours={}
                            objNone={}
                # print(disable)
                # print(flavours)
                partx.append({'parts':{'id': val['id'], 'part_name': val['name'], 'toggle': False,
                                        'checkbox_list':{
                                            'disable':disable,
                                            'flavours':flavours,
                                            'selected':selResults,
                                            'allSelected':objNone,
                                            'indeterminate':objNone
                                        },
                                        'part_content':rows}})
            #print(item['butDiscPerc'])
            partx.append({'taxs' : item})
            return partx

    @classmethod
    async def update_checkbox_table(cls, id, fild, data):
        string = ''
        objs = json.loads(data)
        counObj=0
        objstring=''
        for obj in objs:
            if counObj==0:
                separator = ''
                sepObj = ''
            else:
                separator = '|'
                sepObj = ','
            counObj=counObj+1
            string=string+separator+obj+':'
            objstring=objstring+sepObj+obj

            count=0
            for item in objs[obj]:
                count=count+1
                if count==len(objs[obj]):
                    separator = ''
                else:
                    separator = ','
                numberForItem = int(item.split('temp')[1])
                item = 'temp'+str(numberForItem)
                string = string+item+separator

        async with database.query() as Q:
            await (Q()
                     .tables(T.sub_tables)
                     .where(T.sub_tables.id == id)
                     .update({
                         T.sub_tables[fild]: string,
                         T.sub_tables.obj: objstring
                     }))

        return ''


    @classmethod
    async def get_damage(cls, id):
        async with database.query() as Q:
                damages=(await (Q()
                    .tables(T.sub_group_for_damages)
                    .fields(
                        T.sub_group_for_damages.id,
                        T.sub_group_for_damages.name
                    )
                    .where(T.sub_group_for_damages.item_id == id)
                    .selectall()))

                for val in damages:
                    imamges = (await (Q()
                    .tables(T.sub_group_for_damages)
                    .fields(
                        T.sub_group_for_damages.id,
                        T.sub_group_for_damages.file_name,
                        T.sub_group_for_damages.date,
                        T.sub_group_for_damages.desc
                    )
                    .where(T.sub_group_for_damages.group_id == val['id'])
                    .selectall()))
                    tasks = (await (Q()
                    .tables(T.sub_task_for_damages)
                    .fields(
                        T.sub_task_for_damages.id,
                        T.sub_task_for_damages.name,
                        T.sub_task_for_damages.data_time_start,
                        T.sub_task_for_damages.data_time_end,
                        T.sub_task_for_damages.workers
                    )
                    .where(T.sub_task_for_damages.table_id == val['id'])
                    .selectall()))
                    val['up']=False
                    val['images']=imamges
                    val['tasks']=tasks

                
                return damages

    @classmethod
    async def get_damage_images(cls, id, project):
        async with database.query() as Q:
                items =  (await (Q()
                    .tables(T.sub_items & T.sub_tables  & T.type_for_table).on((T.sub_items.id == T.sub_tables.item_id) & (T.sub_items.type == T.type_for_table.id))
                    .fields(
                        T.type_for_table.type,
                        T.sub_tables.id,
                        T.sub_tables.name
                    )
                    .where(T.sub_items.project_id == id)
                    .selectall()))

                # print(items)    

                result = list()              
                files=(await (Q()
                    .tables(T.files)
                    .fields(
                        T.files.id,
                        T.files.name,
                        # T.files.html,
                        T.files.number,
                        T.files.id,
                        # T.files.pages,
                        T.files.group,
                        T.files.added,
                        T.files.user
                    )
                    .where(T.files.number == project)
                    .selectall()))
                for val in files:
                    # print(val)
                    if val['name'].split('.')[1]!='pdf':
                        fild_from='Project'
                        fild_type={'id':0}

                        for it in items:
                            if (str(it['id'])==str(val['group'])):
                                fild_from=it['name']
                                fild_type= it['type']
                        
                        if val['user']==None:
                            user = 'Undefind'
                        else:
                            user =  val['user']
                        img={'id':'/image?id='+str(val['id']), 'file_name':val['name'], 'date':val['added'], 'desc':'', 'from':fild_from, 'type':fild_type, 'user':user}
                        result.append(img)
                # print(files, project)

         
                damages=(await (Q()
                    .tables(T.sub_items)
                    .fields(
                        T.sub_items.id
                    )
                    .where((T.sub_items.project_id == id) & (T.sub_items.type == 4))
                    .selectall()))

                for val in damages:
                    group=(await (Q()
                    .tables(T.sub_group_for_damages)
                    .fields(
                        T.sub_group_for_damages.id,
                        T.sub_group_for_damages.name
                    )
                    .where(T.sub_group_for_damages.item_id == val['id'])
                    .selectall()))


                    for val in group:
                        images=(await (Q()
                        .tables(T.sub_group_for_damages)
                        .fields(
                            T.sub_group_for_damages.id,
                            T.sub_group_for_damages.file_name,
                            T.sub_group_for_damages.date,
                            T.sub_group_for_damages.desc
                        )
                        .where(T.sub_group_for_damages.group_id == val['id'])
                        .selectall()))

                        for img in images:
                            img['id'] = '/image_damage?id='+str(img['id'])
                            img['from']=val['name']
                            img['type']='Damage'
                            # print(img)
                            result.append(img)

                # result = list(filter(None, result))
                # print(result)
                return result

    @classmethod
    async def get_images(cls, id):
        async with database.query() as Q:
              return await (Q()
                    .tables(T.sub_group_for_damages)
                    .fields(
                        T.sub_group_for_damages.id,
                        T.sub_group_for_damages.file_name,
                        T.sub_group_for_damages.date,
                        T.sub_group_for_damages.desc
                        # T.sub_group_for_damages.content
                    )
                    .where(T.sub_group_for_damages.group_id == id)
                    .selectall())
              
    @classmethod
    async def add_project(cls, year, date, country, area, city, street, zip):
        async with database.query() as Q:
              await (Q()
                  .tables(T.sub_project)
                  .insert({
                  T.sub_project.project_number_year: year,
                  T.sub_project.date: date,
                  T.sub_project.user_id: '1', 
                  T.sub_project.street: street,
                  T.sub_project.country: country,
                  T.sub_project.area: area,
                  T.sub_project.city: city,
                  T.sub_project.zip: zip,
                  }))
              return await (Q(T.sub_project)
                .fields(
                    T.sub_project.project_number_year,
                    T.sub_project.date,
                    T.sub_project.street,
                    T.sub_project.city,
                    T.sub_project.zip,
                    T.sub_project.status_set,
                    T.sub_project.id,
                    T.sub_project.other
                ).selectall())

    @classmethod
    async def get_workers(cls):
        async with database.query() as Q:
            result =( await (Q()
                        .tables(T.personal_sub)
                        .fields(
                            T.personal_sub.name,
                            T.personal_sub.short_name,
                            T.personal_sub.id
                        )
                        .where(T.personal_sub.item_id == 129)
                        .selectall())
            )
            return result

    @classmethod
    async def changeDisableTableAfterDell(cls, timestam, ws_clients):
        await asyncio.sleep(15)
        async with database.query() as Q:
            await (Q(T.changeDisableTableSub)
                 .where((T.changeDisableTableSub.time == timestam))
                 .delete())
            for client in ws_clients:
                await client.send_str('getLoocksSub')

            # return web.json_response('')
            # ioloop.run_until_complete(wait_tasks)
            # ioloop.close()
            return ''
    # @classmethod
    # async def foo(cls):
    #     print('Running in foo')
    #     await asyncio.sleep(0)
    #     print('Explicit context switch to foo again')

    # @classmethod
    # async def bar(cls):
    #     print('Explicit context to bar')
    #     await asyncio.sleep(0)
    #     print('Implicit context switch back to bar')

    @classmethod
    async def changeDisableTable(cls, type_operation, fild, id, user, ws_clients):
        async with database.query() as Q:
            timestam = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if type_operation=='f':
                await (Q()
                     .tables(T.changeDisableTableSub)
                     .insert({
                       T.changeDisableTableSub.fild: fild,
                       T.changeDisableTableSub.rows_id: id,
                       T.changeDisableTableSub.user: user,
                       T.changeDisableTableSub.time: timestam
                }))


                ioloop = asyncio.get_event_loop()
                tasks = [ioloop.create_task(Sub.changeDisableTableAfterDell(timestam, ws_clients))]
                # wait_tasks = asyncio.wait(tasks)
                # ioloop.run_until_complete(wait_tasks)
                # ioloop.close()

                # del_id = (await (Q()
                # .tables(T.changeDisableTable)
                # .fields(T.changeDisableTable.id)
                # .where(T.changeDisableTable.time == timestam)
                # .selectone()))



                # await Projects.changeDisableTableAfterDell(timestam)
             # 
                # await Projects.say_after(30, 'world')
            if type_operation=='b':
                await (Q(T.changeDisableTableSub)
                        .where((T.changeDisableTableSub.fild == fild) & (T.changeDisableTableSub.rows_id == id))
                        .delete())
        return ''


    @classmethod
    async def getLoocks(cls):
        async with database.query() as Q:
            return await (Q()
                .tables(T.changeDisableTableSub)
                .fields(T.changeDisableTableSub.id, T.changeDisableTableSub.fild, T.changeDisableTableSub.rows_id, T.changeDisableTableSub.user)
                .selectall())

    @classmethod
    async def change_type(cls, id, type):
        async with database.query() as Q:
            number=(await (Q()
                    .tables(T.sub_items)
                    .fields(
                        T.sub_items.number
                    )
                    .where(T.sub_items.id == id)
                    .selectone()))
            type_id =(await (Q()
                    .tables(T.type_for_table)
                    .fields(
                        T.type_for_table.id
                    )
                    .where(T.type_for_table.type == type)
                    .selectone()))
            return await (Q()
                .tables(T.sub_items)
                .where(T.sub_items.id == id)
                .update({
                    T.sub_items.type: type_id['id']
                }))


    @classmethod
    async def updateProjectTaxs(cls, id, tax, taxDub, taxP, taxPDub, disc, discP, butDiscPerc, addtaxColapse):
        async with database.query() as Q:
              return await (Q()
                .tables(T.sub_items)
                .where(T.sub_items.id == id)
                .update({
                    T.sub_items.tax: tax,
                    T.sub_items.taxDub: taxDub,
                    T.sub_items.taxP: taxP,
                    T.sub_items.taxPDub: taxPDub,
                    T.sub_items.disc: disc,
                    T.sub_items.discP: discP,
                    T.sub_items.butDiscPerc: butDiscPerc,
                    T.sub_items.addtaxColapse: addtaxColapse
                }))


class SubOffer:
    @classmethod
    async def select_offer(cls, id):
        async with database.query() as Q:
            return await (Q()
                .tables(T.sub_offer)
                .fields(T.sub_offer.offer_number, T.sub_offer.status_set, T.sub_offer.other)
                .where(T.sub_offer.project_id == id)
                .selectall())

class SubInvoice:
    @classmethod
    async def select_invoice(cls, id):
        async with database.query() as Q:
            return await (Q()
                .tables(T.sub_invoice)
                .fields(
                    T.sub_invoice.invoice_number,
                    T.sub_invoice.status_set,
                    T.sub_invoice.other,
                    T.sub_invoice.id,
                    T.sub_invoice.year
                    )
                .where(T.sub_invoice.project_id == id)
                .selectall())

    @classmethod
    async def detect_invoice(cls):
        async with database.query() as Q:
            ids=(
                await (Q()
                    .tables(T.number_for_invoice)
                    .fields(
                        T.number_for_invoice.id
                        )
                    .selectall())
                )
            for id in ids:
                maxId=id['id']

            diff=[]
            try:
                for diffId in range(1, (maxId+1)):
                    sub = 0
                    for id in ids:
                        result = (id['id']==diffId)
                        if result==True:
                            sub = 1
                        
                    if result==False:
                        if sub == 0:
                            diff.append(diffId)
            except:
                maxId = 0
            diff.append((maxId+1))
            # print(diff)
            return(diff)

    @classmethod
    async def get_reports(cls, id):
        async with database.query() as Q:
            result = (await (Q()
                .tables(T.sub_items)
                .fields(
                    T.sub_items.id,
                    T.sub_items.number,
                    T.sub_items.date,
                    T.sub_items.other,
                    T.sub_items.place,
                    T.sub_items.insurance_number,
                    T.sub_items.work,
                    T.sub_items.status_set,
                    T.sub_items.tax,
                    T.sub_items.taxDub,
                    T.sub_items.taxP,
                    T.sub_items.taxPDub,
                    T.sub_items.disc,
                    T.sub_items.discP,
                    T.sub_items.butDiscPerc,
                    T.sub_items.addtaxColapse,
                    T.sub_items.dateEvent,
                    T.sub_items.dateInspect,
                    T.sub_items.ExamWorker
                )
                .selectall()))
            sendResult=[]

            index = 0
            for res in result:
                
                if id in res['number']:
                    index = int(index)+1
                    res['number'] = index
                    sendResult.append(res)
        return sendResult

    @classmethod
    async def add_invoice(cls, id, type, number):
        async with database.query() as Q:
            types = ( await (Q()
                .tables(T.type_for_table)
                .fields(
                    T.type_for_table.id 
                    )
                .where(T.type_for_table.type == type)
                .selectone())
             )

            result = ( await (Q()
                .tables(T.sub_items)
                .fields(
                    T.sub_items.project_id,
                    T.sub_items.number,
                    T.sub_items.date,
                    T.sub_items.status_set,
                    T.sub_items.other,
                    T.sub_items.place,
                    T.sub_items.insurance_number,
                    T.sub_items.work,
                    T.sub_items.type,
                    T.sub_items.id,
                    T.sub_items.tax,
                    T.sub_items.taxDub,
                    T.sub_items.taxP,
                    T.sub_items.taxPDub,
                    T.sub_items.disc,
                    T.sub_items.discP,
                    T.sub_items.butDiscPerc,
                    T.sub_items.addtaxColapse
                    )
                .where(T.sub_items.id == id)
                .selectone())
             )
            

            await (Q()
                     .tables(T.sub_items)
                     .insert({
                       T.sub_items.project_id : result['project_id'],
                       T.sub_items.number : result['number']+' '+str(result['id']),
                       T.sub_items.date : datetime.datetime.now().strftime("%Y-%m-%d"),
                       T.sub_items.status_set : result['status_set'],
                       T.sub_items.other : result['other'],
                       T.sub_items.place : result['place'],
                       T.sub_items.insurance_number : result['insurance_number'],
                       T.sub_items.work : result['work'],
                       T.sub_items.type: types['id'],
                       T.sub_items.tax: result['tax'],
                       T.sub_items.taxDub: result['taxDub'],
                       T.sub_items.taxP: result['taxP'],
                       T.sub_items.taxPDub: result['taxPDub'],
                       T.sub_items.disc: result['disc'],
                       T.sub_items.discP: result['discP'],
                       T.sub_items.butDiscPerc: result['butDiscPerc'],
                       T.sub_items.addtaxColapse: result['addtaxColapse']
                       # T.sub_items.year: datetime.datetime.now().strftime("%Y"),
                    }))

            invoiceIdx = ( await (Q()
                .tables(T.sub_items)
                .fields(
                    T.sub_items.id
                    )
                .where(T.sub_items.number == (result['number']+' '+str(result['id'])))
                .selectall())
             )
            invoiceId = invoiceIdx[len(invoiceIdx)-1]
            if type=='Invoices':
                await (Q()
                        .tables(T.sub_number_for_invoice)
                        .insert({
                            T.sub_number_for_invoice.item_id : invoiceId['id'],
                            T.sub_number_for_invoice.name : number
                        }))
            
                numberInvoice = ( await (Q()
                    .tables(T.sub_number_for_invoice)
                    .fields(
                        T.sub_number_for_invoice.name
                        )
                    .where(T.sub_number_for_invoice.item_id == invoiceId['id'])
                    .selectone())
                )

                await (Q()
                        .tables(T.sub_items)
                        .where(T.sub_items.number == (result['number']+' '+str(result['id'])))
                        .update({
                            T.sub_items.number: result['number']+' '+str(numberInvoice['name'])+' '+str(result['id'])
                        }))
            resultTables = ( await (Q()
                .tables(T.sub_tables)
                .fields(
                    T.sub_tables.id,
                    T.sub_tables.name,
                    T.sub_tables.obj,
                    T.sub_tables.selected
                    )
                .where(T.sub_tables.item_id == id)
                .selectall()))

            for val in resultTables:
                    resultData = ( await (Q()
                    .tables(T.sub_rows_for_table)
                    .fields(
                        T.sub_rows_for_table.count,
                        T.sub_rows_for_table.status,
                        T.sub_rows_for_table.alttax,
                        T.sub_rows_for_table.summa,
                        T.sub_rows_for_table.unit,
                        T.sub_rows_for_table.without,
                        T.sub_rows_for_table.done,
                        T.sub_rows_for_table.description_head,
                        T.sub_rows_for_table.description_work,
                        T.sub_rows_for_table.description_from_price,
                        T.sub_rows_for_table.discount,
                        T.sub_rows_for_table.position_number,
                        T.sub_rows_for_table.description_from_price,
                        T.sub_rows_for_table.price,
                        T.sub_rows_for_table.id
                        )
                    .where(T.sub_rows_for_table.table_id == val['id'])
                    .selectall())
                    )

                    if type == 'Damage Description':
                        sel = number.split(',')

                        await (Q()
                             .tables(T.sub_group_for_damages)
                             .insert({
                               T.sub_group_for_damages.name : val['name'],
                               T.sub_group_for_damages.item_id : invoiceId['id'],
                        }))

                        gropupId = (await (Q()
                            .tables(T.sub_group_for_damages)
                            .fields(
                                T.sub_group_for_damages.id
                            )
                            .where((T.sub_group_for_damages.name == val['name']) & (T.sub_group_for_damages.item_id == invoiceId['id']))
                            .selectone())
                        )

                        for index, row in enumerate(resultData):
                            number = number.replace(' ', '')
                            val['name'] = val['name'].replace(' ', '')
                            sel = number.split(',')

                            for sindex, i in enumerate(sel):
                                item = i.split('-')
                                if ((val['name']==str(item[0])) & (index == int(item[1]))):
                                    await (Q()
                                        .tables(T.sub_task_for_damages)
                                        .insert({
                                            T.sub_task_for_damages.name : row['description_head'],
                                            T.sub_task_for_damages.table_id : gropupId['id']
                                        }))
                    else:
                        await (Q()
                             .tables(T.sub_tables)
                             .insert({
                               T.sub_tables.name : val['name'],
                               T.sub_tables.item_id : invoiceId['id'],
                               T.sub_tables.obj: val['obj'],
                               T.sub_tables.selected: val['selected']
                               # T.sub_items.year: datetime.datetime.now().strftime("%Y"),
                            }))

                        tableId = ( await (Q()
                        .tables(T.sub_tables)
                        .fields(
                            T.sub_tables.id
                            )
                        .where((T.sub_tables.name == val['name']) & (T.sub_tables.item_id == invoiceId['id']))
                        .selectone())
                        )

                        resultFiles = ( await (Q()
                        .tables(T.files)
                        .fields(
                            T.files.content,
                            T.files.name,
                            T.files.number,
                            T.files.pages,
                            T.files.resp,
                            T.files.html,
                            T.files.added
                            )
                        .where(T.files.group == val['id'])
                        .selectall())
                         )
                        for file in resultFiles:
                            await (Q()
                            .tables(T.files)
                            .insert({
                                T.files.content: file['content'],
                                T.files.name: file['name'],
                                T.files.number: file['number'],
                                T.files.pages: file['pages'],
                                T.files.resp: file['resp'],
                                T.files.html: file['html'],
                                T.files.added: file['added'],
                                T.files.group: tableId['id']
                            }))
                        for row in resultData:
                                await (Q()
                                .tables(T.sub_rows_for_table)
                                .insert({
                                    T.sub_rows_for_table.count : row['count'],
                                    T.sub_rows_for_table.status : row['status'],
                                    T.sub_rows_for_table.alttax : row['alttax'],
                                    T.sub_rows_for_table.summa : row['summa'],
                                    T.sub_rows_for_table.unit : row['unit'],
                                    T.sub_rows_for_table.without : row['without'],
                                    T.sub_rows_for_table.done : row['done'],
                                    T.sub_rows_for_table.description_head : row['description_head'],
                                    T.sub_rows_for_table.description_work : row['description_work'],
                                    T.sub_rows_for_table.description_from_price : row['description_from_price'],
                                    T.sub_rows_for_table.discount : row['discount'],
                                    T.sub_rows_for_table.position_number : row['position_number'],
                                    T.sub_rows_for_table.price : row['price'],
                                    T.sub_rows_for_table.table_id : tableId['id']
                                }))

        return ''

    @classmethod
    async def select_invoices(cls, id):
        async with database.query() as Q:
            return await (Q()
                .tables(T.sub_invoice)
                .fields(
                    T.sub_invoice.inoice_number,
                    T.sub_invoice.date,
                    T.sub_invoice.status_set,
                    T.sub_invoice.other,
                    T.sub_invoice.place,
                    T.sub_invoice.insurance_number,
                    T.sub_invoice.work,
                    T.sub_invoice.offer_id,
                    T.sub_invoice.id,
                    T.sub_invoice.year
                    )
                .where(T.sub_invoice.project_id == id)
                .selectall())


class add_same_sub:
    @classmethod
    async def add_same(cls, add_number, add_work, add_insurance_number, add_place, add_comment, add_project_id, order_id, type):
            async with database.query() as Q:
                type_id = (await (Q()
                    .tables(T.type_for_table)
                    .fields(
                        T.type_for_table.id
                        )
                    .where(T.type_for_table.type == type)
                    .selectone()))
                return await (Q()
                    .tables(T.sub_items)
                    .insert({
                        T.sub_items.discP:0,
                        T.sub_items.disc:0,
                        T.sub_items.taxP:19,
                        T.sub_items.taxDub:0.0,
                        T.sub_items.tax:0.00,
                        T.sub_items.taxPDub:0,
                        T.sub_items.work: add_work,
                        T.sub_items.place: add_place,
                        T.sub_items.insurance_number:add_insurance_number,
                        T.sub_items.other: add_comment, 
                        T.sub_items.number: add_number,
                        T.sub_items.date: datetime.datetime.now().strftime("%Y-%m-%d"),
                        T.sub_items.status_set: 'Open',
                        T.sub_items.project_id: add_project_id,
                        T.sub_items.order_id: order_id,
                        T.sub_items.type: type_id['id']
                    }))
class Del_offer_sub:
    @classmethod
    async def del_item(cls, id):
        async with database.query() as Q:
            tables = (
                await (Q(T.sub_tables)
                    .fields(
                        T.sub_tables.id)
                    .where(T.sub_tables.item_id == id)
                    .selectall())
                    )

            for table in tables:
                rows = (await (Q(T.sub_rows_for_table)
                .fields(
                    T.sub_rows_for_table.id)
                .where(T.sub_rows_for_table.table_id == table['id'])
                .selectall())
                )
                for row in rows:
                    await (Q(T.sub_rows_for_table)
                        .where(T.sub_rows_for_table.id == row['id'])
                        .delete())

            await (Q(T.sub_tables)
                .where(T.sub_tables.item_id == id)
                .delete())

            number_invoice = (await (Q(T.sub_items)
                    .fields(T.sub_items.id)
                    .where(T.sub_items.id == id)
                    .selectone())
                )
           
            await (Q(T.number_for_invoice)
                .where(T.number_for_invoice.item_id == number_invoice['id'])
                .delete())
                
            
            await (Q(T.sub_items)
                .where(T.sub_items.id == id)
                .delete())



#####end Sub
class Project:

    @classmethod
    async def update_id_in_prise(cls, newid, oldid):
        async with database.query() as Q:
            row= (await (Q()
                            .tables(T.price)
                            .fields(
                                T.price.id,
                                T.price.pos_num,
                                T.price.name,
                                T.price.item_id,
                                T.price.desc,
                                T.price.unit,
                                T.price.price,
                                T.price.without,
                                T.price.percent
                      
                            ).where(T.price.id == oldid)
                            .selectone()))

            await (Q(T.price)
                .where(T.price.id == oldid)
                .delete())

            await (Q()
                     .tables(T.price)
                     .where(T.price.id == newid)
                     .update({
                         T.price.id: oldid
                     }))

            return await (Q()
                    .tables(T.price)
                    .insert({
                        T.price.id:newid,
                        T.price.pos_num:row['pos_num'],
                        T.price.name:row['name'],
                        T.price.item_id:row['item_id'],
                        T.price.desc:row['desc'],
                        T.price.unit:row['unit'],
                        T.price.price:row['price'],
                        T.price.without:row['without'],
                        T.price.percent:row['percent']
                    }))


        return ''

    @classmethod
    async def get_addresbook(cls):
        async with database.query() as Q:
            return await(Q()
                .tables(T.addresbook)
                .fields(T.addresbook.mail)
                .selectall()
                )
    
    @classmethod
    async def get_units(cls):
        async with database.query() as Q:
            allResult = (await(Q()
                .tables(T.price)
                .fields(T.price.unit)
                .selectall()
                ))

            result = []
            
            for res in allResult:
                same = 0
                for resafter in result:
                    if resafter==res['unit']:
                        same = 1

                if same==0:
                    result.append(res['unit'])

        return result

    @classmethod
    async def select_project(cls, id):
        async with database.query() as Q:
            result= (await (Q()
                .tables((T.project & T.user & T.customer & T.person))
                .on((T.project.user_id == T.user.id) & (T.project.customer_id == T.customer.id) & (T.project.person_id == T.person.person))
                .fields(
                    T.project.project_number_year,
                    T.project.id,
                    T.project.project_number,
                    T.project.date,
                    T.project.edate,
                    T.project.street1,
                    T.project.city1,
                    T.project.zip1,
                    T.customer.street,
                    T.customer.city,
                    T.customer.zip,
                    T.project.area,
                    T.project.country,
                    T.project.customer_id,
                    T.project.person_id,
                    T.project.mail,
                    T.project.phone,
                    T.project.other,
                    T.user.first_name,
                    T.user.second_name,
                    T.customer.name,
                    T.person.appeal,
                    T.person.names
                ).where(T.project.id == id)
                .selectone()))
            # print (result)
            return (result)

    @classmethod
    async def updateProjectTaxs(cls, id, tax, taxDub, taxP, taxPDub, disc, discP, butDiscPerc, addtaxColapse):
        async with database.query() as Q:
              return await (Q()
                .tables(T.items)
                .where(T.items.id == id)
                .update({
                    T.items.tax: tax,
                    T.items.taxDub: taxDub,
                    T.items.taxP: taxP,
                    T.items.taxPDub: taxPDub,
                    T.items.disc: disc,
                    T.items.discP: discP,
                    T.items.butDiscPerc: butDiscPerc,
                    T.items.addtaxColapse: addtaxColapse
                }))
    
    @classmethod
    async def update(cls, id, data, fild):
        async with database.query() as Q:
              return await (Q()
                .tables(T.project)
                .where(T.project.id == id)
                .update({
                    T.project[fild]: data
                }))

    @classmethod
    async def table_data(cls, id):
        async with database.query() as Q:
              return await (Q()
                .tables(T.table_data)
                .fields(
                    T.table_data.part_name,
                    T.table_data.count,
                    T.table_data.status,
                    T.table_data.alttax,
                    T.table_data.summa,
                    T.table_data.unit,
                    T.table_data.done,
                    T.table_data.description_head,
                    T.table_data.description_work,
                    T.table_data.description_from_price,
                    T.table_data.discount,
                    T.table_data.position_number,
                    T.table_data.price,
                    T.table_data.id,
                    T.table_data.item_id
                )
                .where(T.table_data.item_id == id)
                .selectall())

    @classmethod
    async def invoice_data_table(cls, id):
        async with database.query() as Q:
              return await (Q()
                .tables(T.invoice_data_table)
                .fields(
                    T.invoice_data_table.part_name,
                    T.invoice_data_table.count,
                    T.invoice_data_table.status,
                    T.invoice_data_table.alttax,
                    T.invoice_data_table.summa,
                    T.invoice_data_table.unit,
                    T.invoice_data_table.done,
                    T.invoice_data_table.description_head,
                    T.invoice_data_table.description_work,
                    T.invoice_data_table.description_from_price,
                    T.invoice_data_table.discount,
                    T.invoice_data_table.position_number,
                    T.invoice_data_table.price,
                    T.invoice_data_table.id,
                    T.invoice_data_table.item_id
                )
                .where(T.invoice_data_table.item_id == id)
                .selectall())

    @classmethod
    async def update_table_data(cls, id, fild, data):
        async with database.query() as Q:
            # print(id, fild, data)
            # if fild == 'without':
            #     if data == true:
            #         data
            #     else:
            if data=='Null':
                data = ''
            return await (Q()
                .tables(T.rows_for_table)
                .where(T.rows_for_table.id == id)
                .update({
                    T.rows_for_table[fild]: data
                }))

    @classmethod
    async def add_part_form_price(cls, part_name, type,
        item_id, position_number, description_head, description_work,
        description_from_price, count, discount, price, status, alttax,
        summa, unit, without):
        if type=='invoice':
           table='invoice_data_table'
        else:
           table='table_data'
        async with database.query() as Q:
            return await (Q()
                .tables(T(table))
                .insert({
                    T(table).part_name: part_name,
                    T(table).item_id: item_id,
                    T(table).position_number: position_number,
                    T(table).description_head: description_head,
                    T(table).description_work: description_work,
                    T(table).description_from_price: description_from_price,
                    T(table).count: count,
                    T(table).discount: discount,
                    T(table).price: price,
                    T(table).status: status,
                    T(table).alttax: alttax,
                    T(table).summa: summa,
                    T(table).unit: unit,
                    T(table).without: without
                }))

    @classmethod
    async def add_contact(cls, type, val, person, sel, project):
        async with database.query() as Q:
             await (Q()
                .tables(T(type))
                .insert({
                    T(type)[type]: val,
                    T(type).person: person
                }))
             return await (Q()
                .tables(T.project)
                .where(T.project.id == project)
                .update({
                    T.project[type]: sel
                }))

  
    @classmethod
    async def add_person(cls, name, other, appeal, dep, pos, firm, fax, phone, mail):
        async with database.query() as Q:
            await (Q()
                .tables(T.person)
                .insert({
                    T.person.names: name,
                    T.person.other: other,
                    T.person.appeal: appeal,
                    T.person.dep: dep,
                    T.person.pos: pos,
                    T.person.data: datetime.datetime.now().strftime("%Y-%m-%d"),
                    T.person.customer_group: firm
                }))
            person = (await (Q()
                    .tables(T.person)
                    .fields(
                      T.person.person
                    )
                    .where(T.person.names==name)
                    .selectone())
            )
            if fax!='':
                for f in fax.split(","):
                    await (Q()
                        .tables(T.fax)
                        .insert({
                            T.fax.fax: f,
                            T.fax.person: person['person']
                        }))
            if phone!='':
                for f in phone.split(","):
                    await (Q()
                        .tables(T.phone)
                        .insert({
                            T.phone.phone: f,
                            T.phone.person: person['person']
                        }))
            if mail!='':
                for f in mail.split(","):
                    await (Q()
                        .tables(T.mail)
                        .insert({
                            T.mail.mail: f,
                            T.mail.person: person['person']
                        }))
            return ''
    @classmethod
    async def add_custom(cls, name, zip, city, tax, web, bic, iban, other, mail, phone, fax, street):

        async with database.query() as Q:
            await (Q()
                    .tables(T.customer)
                    .insert({
                        T.customer.name: name,
                        T.customer.zip: zip,
                        T.customer.city: city,
                        T.customer.street: street,
                        T.customer.tax: tax,
                        T.customer.web: web,
                        T.customer.bic: bic,
                        T.customer.iban: iban,
                        T.customer.other: other,
                        T.customer.data: datetime.datetime.now().strftime("%Y-%m-%d")
                    }))
            customer = (await (Q()
                    .tables(T.customer)
                    .fields(
                      T.customer.id
                    )
                    .where(T.customer.name==name)
                    .selectone())
            )
            
            if fax!='':
                for f in fax.split(","):
                    await (Q()
                        .tables(T.fax)
                        .insert({
                            T.fax.fax: f,
                            T.fax.customer: customer['id']
                        }))

            if phone!='':
                for f in phone.split(","):
                    await (Q()
                        .tables(T.phone)
                        .insert({
                            T.phone.phone: f,
                            T.phone.customer: customer['id']
                        }))

            if mail!='':
                for f in mail.split(","):
                    # print('!')
                    await (Q()
                        .tables(T.mail)
                        .insert({
                            T.mail.mail: f,
                            T.mail.customer: customer['id']
                        }))
            return customer

    @classmethod



    async def select_customers(cls, old):
        async with database.query() as Q:
            result=( await (Q()
                .tables(T.customer & T.person)
                .on(T.customer.id == T.person.customer_group)
                .fields(
                    # T.customer.name,
                    T.customer.id,
                    # T.customer.zip,
                    # T.customer.city,
                    # T.customer.street,
                    T.person.names,
                    T.person.person
                ).where((T.person.old != old) & (T.customer.old != old))
                .selectall()))


            return result

    @classmethod
    async def select_person_date(cls, old):
        async with database.query() as Q:
            result=[]
            customers = ( await (Q()
                .tables(T.customer & T.person)
                .on(T.customer.id == T.person.customer_group)
                .fields(
                    T.customer.zip,
                    T.customer.city,
                    T.customer.street,
                    T.customer.name,
                    T.customer.id,
                    T.person.names,
                    T.person.person
                ).where((T.person.old != old) & (T.customer.old != old) & (T.customer.type == None))
                .selectall()))
            for customer in customers:
                mail = (await (Q()
                    .tables(T.mail)
                    .fields(
                        T.mail.mail
                    ).where(T.mail.person == customer['person'])
                    .selectall()))
                phone = (await (Q()
                    .tables(T.phone)
                    .fields(
                        T.phone.phone
                    ).where( T.phone.person == customer['person'])
                    .selectall()))
                fax = (await (Q()
                    .tables(T.fax)
                    .fields(
                        T.fax.fax
                    ).where( T.fax.person == customer['person'])
                    .selectall()))
                coutn_much = -1
                for idx, much in enumerate(result):
                    if much['name'] == customer['name']:
                        coutn_much=idx
                if coutn_much==-1:
                    result.append({'id': customer['id'], 'name': customer['name'], 'adress':customer['street'],
                        'adress1':customer['zip']+' '+customer['city'], 'persons': [{'label': customer['names'],
                        'mail': mail, 'tel' : phone, 'fax': fax, 'id' : customer['person']}]})
                else:
                    result[coutn_much]['persons'].append({'label': customer['names'], 'mail': mail, 'tel' : phone, 'fax': fax, 'id' : customer['person']})
            # print(result)
            return  result

    @classmethod
    async def select_mails(cls, id):
        async with database.query() as Q:
            return await (Q()
                .tables(T.mail)
                .fields(
                    T.mail.mail
                ).where(T.mail.person == id)
                .selectall())

    @classmethod
    async def select_phons(cls, id):
        async with database.query() as Q:
            return await (Q()
                .tables(T.phone)
                .fields(
                    T.phone.phone
                ).where( T.phone.person == id)
                .selectall())

    @classmethod
    async def select_faxs(cls, id):
        async with database.query() as Q:
            return await (Q()
                .tables(T.fax)
                .fields(
                    T.fax.fax
                ).where( T.fax.person == id)
                .selectall())

    @classmethod
    async def add_part(cls, part_name, item_id):
        async with database.query() as Q:
                await (Q()
                    .tables(T.tables)
                    .insert({
                        T.tables.name: part_name,
                        T.tables.item_id: item_id,
                        T.tables.obj: '',
                        T.tables.selected: ''
                    }))
        return ''

    @classmethod
    async def update_part(cls, part_name, id):
        async with database.query() as Q:
                await (Q()
                     .tables(T.tables)
                     .where(T.tables.id == id)
                     .update({
                         T.tables.name: part_name
                     }))
        return ''

    @classmethod
    async def updateNameDevice(cls, device_name, id):
        async with database.query() as Q:
                await (Q()
                     .tables(T.tables)
                     .where(T.tables.id == id)
                     .update({
                         T.tables.device: device_name
                     }))
        return ''

    @classmethod
    async def del_part(cls, id):
        async with database.query() as Q:
                await (Q(T.tables)
                    .where(T.tables.id == id)
                    .delete())
        return ''

    @classmethod
    async def add_group_damage(cls, item_id):
        async with database.query() as Q:
                await (Q()
                    .tables(T.group_for_damages)
                    .insert({
                        T.group_for_damages.item_id: item_id,
                        T.group_for_damages.name: 'New Position'
                    }))
        return ''
    @classmethod
    async def damage_update(cls, fild, event, id):
        if fild=='imageDesc':
            table='images_for_group_damages'
            column='desc'
        if fild=='name':
            table='group_for_damages'
            column='name'
        async with database.query() as Q:
                 await (Q()
                     .tables(T(table))
                     .where(T(table).id == id)
                     .update({
                         T(table)[column]: event
                     }))
        return ''

    @classmethod
    async def update_item(cls, val, type, id):
        async with database.query() as Q:
                 await (Q()
                     .tables(T.items)
                     .where(T.items.id == id)
                     .update({
                         T.items[type]: val
                     }))
        return ''
    
    @classmethod
    async def updatefilename(cls, val, type, id):
        async with database.query() as Q:
                 await (Q()
                     .tables(T.files)
                     .where(T.files.id == id)
                     .update({
                         T.files[type]: val
                     }))
        return ''

    @classmethod
    async def updatefilename_company(cls, val, type, id):
        async with database.query() as Q:
                 await (Q()
                     .tables(T.files_to_company)
                     .where(T.files_to_company.id == id)
                     .update({
                         T.files_to_company[type]: val
                     }))
        return ''

    @classmethod
    async def updatefilename_customer(cls, val, type, id):
        async with database.query() as Q:
                 await (Q()
                     .tables(T.files_to_customer)
                     .where(T.files_to_customer.id == id)
                     .update({
                         T.files_to_customer[type]: val
                     }))
        return ''

    @classmethod
    async def updatefilename_person(cls, val, type, id):
        async with database.query() as Q:
                 await (Q()
                     .tables(T.files_to_person)
                     .where(T.files_to_person.id == id)
                     .update({
                         T.files_to_person[type]: val
                     }))
        return ''


    @classmethod
    async def updatefilename_sub(cls, val, type, id):
        async with database.query() as Q:
                 await (Q()
                     .tables(T.files_to_sub)
                     .where(T.files_to_sub.id == id)
                     .update({
                         T.files_to_sub[type]: val
                     }))
        return ''

    @classmethod
    async def updatefilename_sperson(cls, val, type, id):
        async with database.query() as Q:
                 await (Q()
                     .tables(T.files_to_sperson)
                     .where(T.files_to_sperson.id == id)
                     .update({
                         T.files_to_sperson[type]: val
                     }))
        return ''

    @classmethod
    async def updatedocname(cls, val, type, id):
        async with database.query() as Q:
                 await (Q()
                     .tables(T.docs)
                     .where(T.docs.id == id)
                     .update({
                         T.docs[type]: val
                     }))
        return ''

    @classmethod
    async def get_workers(cls):
        async with database.query() as Q:
            result =( await (Q()
                        .tables(T.personal)
                        .fields(
                            T.personal.name,
                            T.personal.short_name,
                            T.personal.id
                        )
                        .where(T.personal.item_id == 137)
                        .selectall())
            )
            return result

    @classmethod
    async def workers_task(cls, workers, id):
        if workers == 'Null':
           workers = None
        async with database.query() as Q:
                 await (Q()
                     .tables(T.task_for_damages)
                     .where(T.task_for_damages.id == id)
                     .update({
                         T.task_for_damages.Workers: workers
                     }))
        return ''
    @classmethod
    async def get_type_works(cls):
        async with database.query() as Q:
            return await (Q()
                        .tables(T.type_works)
                        .fields(
                            T.type_works.value,
                            T.type_works.text
                        )
                        .selectall())


class Projects:
    @classmethod
    async def variables(cls):
        async with database.query() as Q:
            return await (Q()
                        .tables(T.content_for_factory)
                        .fields(T.content_for_factory.content)
                        .where((T.content_for_factory.id == 2))
                        .selectall())

    @classmethod
    async def select_projects(cls, param):
    # async def select_projects(cls, page):
        # print(page)
        async with database.query() as Q:
            done = param[0]
            notdone = param[1]
            # print(done+' '+notdone)

            n_result = []
            result = (await (Q(T.project)
                             .fields(
                                 T.project.project_number_year,
                                 T.project.date,
                                 T.project.edate,
                                 T.project.street1,
                                 T.project.city1,
                                 T.project.zip1,
                                 T.project.status_set,
                                 T.project.id,
                                 T.project.project_number,
                                 T.project.other,
                                 T.project.user,
                                 T.project.datacomment
                            ).order_by(T.project.id.desc()).selectall()))
                            # ).order_by(T.project.id.desc()).selectall()))
                            # ).order_by(T.project.id.desc())[:int(page) * 30].selectall()))

            for index, item in enumerate(result):
                # print(str(index)+' - '+str(item['id']))
                subItem = (await (Q(T.items)
                            .fields(
                                 T.items.status_set,
                                 T.items.type,
                                 T.items.project_id #del
                                 # T.items.id #del
                            )
                            .where(T.items.project_id==item['id'])
                            .selectall()))

                count = 0
                lencount = len(subItem)

                for status in subItem:
                    # if (status['type']==1):
                        # lencount = lencount + 1
                    if (status['type']==3):
                        lencount = lencount - 1

                    if (status['type']==6):
                        lencount = lencount - 1

                    if (status['type']==4):
                        lencount = lencount - 1

                    if status['status_set']=='Done':
                        if (status['type']!=3):
                            if (status['type']!=6):
                                if (status['type']!=4):
                                    count = count + 1
                                

                # print('('+str(count)+'/'+str(lencount)+') '+str(item['id']))

                if (lencount!=0):
                    if (count>=lencount):
                        if (done==str(1)):
                            item['_rowVariant']='warning'
                            n_result.append(item)
                    else:
                        if (notdone==str(1)):
                            item['_rowVariant']=''
                            n_result.append(item)
                else:
                    if (notdone==str(1)):
                        item['_rowVariant']=''
                        n_result.append(item)
            # page= int(page) * 30
            # print(page)
# [:int(page)]
        # print(result)
        return n_result

    @classmethod
    async def select_project_new(cls, id):
        async with database.query() as Q:
            result = (await (Q()
                .tables(T.items & T.type_for_table).on(T.items.type == T.type_for_table.id)
                .fields(
                    T.items.id,
                    T.items.number,
                    T.items.date,
                    T.items.other,
                    T.items.place,
                    T.items.insurance_number,
                    T.items.insurname,
                    T.items.work,
                    T.items.status_set,
                    T.type_for_table.type,
                    T.items.tax,
                    T.items.taxDub,
                    T.items.taxP,
                    T.items.taxPDub,
                    T.items.disc,
                    T.items.discP,
                    T.items.butDiscPerc,
                    T.items.addtaxColapse,
                    T.items.dateEvent,
                    T.items.dateInspect,
                    T.items.ExamWorker,
                    T.items.comment
                )
                .where(T.items.project_id == id)
                .selectall()))

            result1 = ( await (Q()
                .tables(T.items )
                .fields(
                    T.items.id,
                    T.items.number
                )
                .selectall()))

            balance = ( await (Q()
                .tables(T.rows_for_balance)
                .fields(
                    T.rows_for_balance.id,
                    T.rows_for_balance.type,
                    T.rows_for_balance.value,
                    T.rows_for_balance.date,
                    T.rows_for_balance.invoice_id
                )
                .selectall()))
            for item in result:
                
                if (item['type'] == 'Damage Description'):
                   # print(item['type'])
                   result.remove(item)

            for item in result:
                id =  item['number'].split(' ')
                if len(id)==2:
                    for number in result1:
                        if int(id[1]) == number['id']: 
                            item['contract_number']=number['number']

            for item in result:
                ops=[]
                for bal in balance:
                    if int(item['id']) == int(bal['invoice_id']): 
                        ops.append({'type':bal['type'], 'value':bal['value'], 'date':bal['date'], 'id':bal['id']})
                item['op'] = ops
 
            cOffer=0
            cCounract=0
            cDamage=0

            for item in result:    
                if item['tax']==None:
                    item['tax']='0,0'
                if item['taxDub']==None:
                    item['taxDub']='0,0'
                if item['taxP']==None:
                    item['taxP']='0,0'
                if item['taxPDub']==None:
                    item['taxPDub']='0,0'
                if item['disc']==None:
                    item['disc']='0,0'
                if item['discP']==None:
                    item['discP']='0,0'
                if item['butDiscPerc']==None:
                    item['butDiscPerc']='%'
                if item['addtaxColapse']==None:
                    item['addtaxColapse']='false'

                tax=(item['tax'].replace(',', '.'))
                taxDub=(item['taxDub'].replace(',', '.'))
                taxP=(item['taxP'].replace(',', '.'))
                taxPDub=(item['taxPDub'].replace(',', '.'))
                disc=(item['disc'].replace(',', '.'))
                discP=(item['discP'].replace(',', '.'))
                butDiscPerc=item['butDiscPerc']
                addtaxColapse=item['addtaxColapse']

                netto = 0
                addt = 0
                addt2 = 0
                tables =(await (Q()
                        .tables(T.tables)
                        .fields(
                            T.tables.id,
                            T.tables.name,
                            T.tables.obj,
                            T.tables.selected
                        )
                        .where(T.tables.item_id == item['id'])
                        .selectall()))
                add = 0

                for subIndex, val in enumerate(tables):
                    rows =(await (Q()
                                .tables(T.rows_for_table)
                                .fields(
                                    T.rows_for_table.count,
                                    T.rows_for_table.price,
                                    T.rows_for_table.summa,
                                    T.rows_for_table.status,
                                    T.rows_for_table.alttax,
                                    T.rows_for_table.without,
                                    T.rows_for_table.unit
                                )
                                .where(T.rows_for_table.table_id == val['id'])
                                .selectall()))

                    for row in rows:
                        if row['count']==None:
                            row['count'] = '0'
                        if row['price']==None:
                            row['price'] = '0'

                        if row['unit']=='%':
                            # if row['count']==None:
                            #     row['count']=1
                            # if row['count']=='0':
                            #     row['count']=1
                            row['price']=0
                            summax = 0

                            for obj in val['obj'].split(','):
                                selected = ['']
                                if not '|' in val["selected"]:
                                    selected = json.loads('{"'+val["selected"].replace(':', '":"')+'"}')
                                    if ('temp' + str(subIndex + 1)) in selected[obj]:

                                        for val in selected[obj].split(','):

                                            val = val.split('temp')
                                            val[1]=int(val[1])-1

                                            countx = 0
                                            pricex = 0
                                            
                                            countx = rows[val[1]]['count'] 
                                            pricex = rows[val[1]]['price']

                                            summax += float(countx) * float(pricex)
                               
                            row['price']=persent_from_summa = (float(summax / 100) * float(row['count']))
                            # print(persent_from_summa)
                            # print(persent_from_summa / float(rows[(subIndex)]['count']))
                                
                            # print(rows[(subIndex)]['price'])
                            
                            row['count']=1
                        if row['status']=='yes':
                            
                            try:
                               a = float(row['price'])
                            except ValueError:
                               row['price'] = 0
                            netto += (float(row['count'])*float(row['price']))






                                # print(str(row['count'])+'*'+str(row['price'])+'='+str(float(row['count'])*float(row['price'])))


                            if row['without']=='true':
                                add += (float(row['count'])*float(row['price']) / 100) * float(discP)

                            # print(row['alttax'])
                            if row['alttax']!='true':
                                addt += (float(row['count'])*float(row['price']))
                            else:
                                addt2 += (float(row['count'])*float(row['price']))



           
                if netto==0:
                    netto=1
                if butDiscPerc=='%':
                    # print(netto, add)
                    # netto = netto + add

                    item['netto']=str(netto-(netto/100*float(discP)))
                    # print(item['netto'])
                    item['netto']=float(item['netto'])+add
                    # print(item['netto'], add)

                    addt = addt-(addt/100)*float(discP)
                    addt2 = addt2-(addt2/100)*float(discP)
                
                else:

                    item['netto']=str(netto-float(discP))
                    
                    addt = addt-(addt/100)*float(discP)*100/netto
                    addt2 = addt2-(addt2/100)*float(discP)*100/netto
                
                #addt = addt2 = 0
                # item['netto']=0

                #tmpTax = (addt * (float(taxP) / 100))
                #tmpTax2= (addt2 * (float(taxPDub) / 100))
    
                item['brutto']=str(float(item['netto'])+(addt * (float(taxP) / 100))+(addt2 * (float(taxPDub) / 100)))
                
                if (item['type'] == 'Offers'):
                    cOffer=cOffer+1
                    if(len(str(cOffer))<2):
                        nOffer = '0'+str(cOffer)
                    item['number'] = item['number'] + '-' + nOffer
                
                if (item['type'] == 'Contracts'):
                    cCounract=cCounract+1
                    if(len(str(cCounract))<2):
                        nCounract = '0'+str(cCounract)
                    item['number'] = item['number'] + '-' + nCounract

                        
                if (item['type'] == 'Damage Description'):
                    cDamage=cDamage+1
                    item['number']=item['number'].split(' ')[0]
                    if(len(str(cDamage))<2):
                        nDamage = '0'+str(cDamage)
                    item['number'] = item['number'] + '-' + nDamage


                # item['brutto']=str(item['brutto']).replace('.',',')
                # item['netto']=str(item['netto']).replace('.',',')
            # print(result)
            return result

    @classmethod
    async def del_row_from_table(cls, id):
        async with database.query() as Q:
            return await (Q(T.rows_for_table)
                    .where(T.rows_for_table.id == id)
                    .delete())

    classmethod #first function on python
    async def change(old, new):
        async with database.query() as Q:
                await (Q()
                            .tables(T.rows_for_table)
                            .where(T.rows_for_table.id == old)
                            .update({
                                T.rows_for_table.id: 999999999
                            }))
                await (Q()
                            .tables(T.rows_for_table)
                            .where(T.rows_for_table.id == new)
                            .update({
                                T.rows_for_table.id: old
                            }))
                await (Q()
                            .tables(T.rows_for_table)
                            .where(T.rows_for_table.id == 999999999)
                            .update({
                                T.rows_for_table.id: new
                            }))
    @classmethod
    async def update_id_in_one_table(cls, newIndex, oldIndex, newPart):
        async with database.query() as Q:
            table =(await (Q()
                    .tables(T.tables)
                    .fields(
                        T.tables.id,
                        T.tables.obj,
                        T.tables.selected
                    )
                    .where((T.tables.id == newPart))
                    .selectone()))


            # print(table)
            table['selected'] = table['selected'].replace('|', '"], ')
            table['selected'] = '{'+table['selected'].replace(':', '":[')+'"]}'
            table['selected'] = table['selected'].replace('in', '"in')
            table['selected'] = table['selected'].replace('temp', '"')
            table['selected'] = table['selected'].replace(',"', '","')
            
            # befor_selected = table['selected']
            if table['selected'] != '{"]}':
                befor_selected = json.loads(table['selected'])
            else:
                befor_selected = ''       
            after_selected = ''
            # print(oldIndex, newIndex)
            for index, selected_group in enumerate(befor_selected):
                selected_group_new = ''
                for i, selected in enumerate(befor_selected[selected_group]):
                    old_select_index = int(selected) - 1
                    if i == 0:
                        if (int(newIndex) <= old_select_index) & (int(oldIndex) > old_select_index):
                            old_select_index = old_select_index + 1
                        if (int(newIndex) >= old_select_index) & (int(oldIndex) < old_select_index):
                            old_select_index = old_select_index - 1
                    else:
                        if int(oldIndex) == old_select_index:
                            old_select_index = int(newIndex)
                    
                    new_select_index = old_select_index + 1

                    selected_group_new = selected_group_new + ',temp'+str(new_select_index)
                
                if index == 0:
                    add = ''
                else:
                    add = '|'

                after_selected = after_selected + add +'in' + str(index) + ':' + str(selected_group_new)
                after_selected = after_selected.replace(':,', ':')
                after_selected = after_selected.replace(':,', ':')

            await (Q()
                     .tables(T.tables)
                     .where(T.tables.id == newPart)
                     .update({
                         T.tables.selected: after_selected
                     }))

            oldrows =(await (Q()
                .tables(T.rows_for_table)
                .fields(
                    T.rows_for_table.id,
                    T.rows_for_table.without
                )
                .where((T.rows_for_table.table_id == newPart))
                .selectall()))

            new = (oldrows[int(newIndex)]['id'])
            old = (oldrows[int(oldIndex)]['id'])
  
            await Projects.change(old, new)

            newrows =(await (Q()
                .tables(T.rows_for_table)
                .fields(
                    T.rows_for_table.id,
                    T.rows_for_table.count
                )
                .where((T.rows_for_table.table_id == newPart))
                .selectall()))

            newx = (newrows[int(newIndex)]['id'])

            if((int(oldIndex)-int(newIndex))!=1):
                if oldIndex>newIndex:
                    start = int(newIndex)
                    end = int(oldIndex)
                else:
                    start = int(oldIndex)
                    end = int(newIndex)
                for  x in range(start, end):
        
                    if oldIndex>newIndex:
                        if ((((int(oldIndex)!=0) * (int(oldIndex)!=(len(oldrows))-1)) + ((int(newIndex)!=0) * (int(newIndex)!=(len(oldrows))-1)))==2):
                            approx = int(newIndex)-2
                            index = (len(oldrows)-x+approx)
                            move = -1
                        else:
                            approx = int(newIndex)-1
                            index = (len(oldrows)-x+approx)
                            move = -1
                            if ((int(newIndex)==0) & (int(oldIndex)!=(len(oldrows)-1))):
                                index=index-(len(oldrows)-int(oldIndex))+1
                    else:
                        index = x
                        move =  1

                    old = (newrows[index]['id'])
                    new = ((oldrows[index+move]['id']))

                    if ((newx!=newrows[index]['id']) & (newx!=(oldrows[index+move]['id']))):
                        await Projects.change(old, new)

        return ''

    @classmethod
    async def update_id(cls, newIndex, newPart, oldIndex, oldPart):
        async with database.query() as Q:

            table =(await (Q()
                    .tables(T.tables)
                    .fields(
                        T.tables.id,
                        T.tables.obj,
                        T.tables.selected
                    )
                    .where((T.tables.id == oldPart))
                    .selectone()))

            el = int(oldIndex)+1
            el = ',temp' + str(el)
            oldselected = str(table['selected'])
            after_selected = oldselected.replace(el, '')
            # print(after_selected)

            await (Q()
                     .tables(T.tables)
                     .where(T.tables.id == oldPart)
                     .update({
                         T.tables.selected: after_selected
                     }))

            newrows =(await (Q()
                .tables(T.rows_for_table)
                .fields(
                    T.rows_for_table.id,
                    T.rows_for_table.count
                )
                .where((T.rows_for_table.table_id == newPart))
                .selectall()))

            oldrows =(await (Q()
                .tables(T.rows_for_table)
                .fields(
                    T.rows_for_table.id
                )
                .where((T.rows_for_table.table_id == oldPart))
                .selectall()))

            try:
                newrows[int(newIndex)]
            except IndexError:
                new = (oldrows[int(oldIndex)]['id'])
            else:
                new = (newrows[int(newIndex)]['id'])

            old = (oldrows[int(oldIndex)]['id'])

            await (Q()
                 .tables(T.rows_for_table)
                 .where(T.rows_for_table.id == old)
                 .update({
                     T.rows_for_table.table_id: newPart
                 }))

            after_add =(await (Q()
                .tables(T.rows_for_table)
                .fields(
                    T.rows_for_table.id
                )
                .where((T.rows_for_table.table_id == newPart))
                .selectall()))
            new = (after_add[int(newIndex)]['id'])
            await Projects.change(old, new)
            newTable = (await (Q()
                .tables(T.rows_for_table)
                .fields(
                    T.rows_for_table.id,
                    T.rows_for_table.count
                )
                .where((T.rows_for_table.table_id == newPart))
                .selectall()))


            for index, row in enumerate(newTable):
                if (int(index) > (int(newIndex)+1)):
                        old = int(newrows[index-1]['id'])
                        new = int(row['id'])
                        # print(newrows[index-1]['count']+'->'+row['count'])
                        await Projects.change(old, new)
                if (int(index) < (int(newIndex)-1)):
                        old = int(newrows[index]['id'])
                        new = int(row['id'])
                        # print(newrows[index]['count']+'->'+row['count'])
                        await Projects.change(old, new)

        return ''


    @classmethod
    async def update_id_table(cls, newIndex, oldIndex, id):
        async with database.query() as Q:

            rows =(await (Q()
                .tables(T.tables)
                .fields(
                    T.tables.id,
                )
                .where((T.tables.item_id == id))
                .selectall()))
            # print(newIndex, oldIndex)
            old = (rows[int(oldIndex)]['id'])
            new = (rows[int(newIndex)]['id'])

            await (Q()
                 .tables(T.rows_for_table)
                 .where(T.rows_for_table.table_id == old)
                 .update({
                     T.rows_for_table.table_id : 999999999
                 }))
            await (Q()
                 .tables(T.rows_for_table)
                 .where(T.rows_for_table.table_id == new)
                 .update({
                     T.rows_for_table.table_id : old
                 }))
            await (Q()
                 .tables(T.rows_for_table)
                 .where(T.rows_for_table.table_id == 999999999)
                 .update({
                     T.rows_for_table.table_id : new
                 }))

            await (Q()
                 .tables(T.tables)
                 .where(T.tables.id == old)
                 .update({
                     T.tables.id: 999999999
                 }))
            await (Q()
                 .tables(T.tables)
                 .where(T.tables.id == new)
                 .update({
                     T.tables.id: old
                 }))
            await (Q()
                 .tables(T.tables)
                 .where(T.tables.id == 999999999)
                 .update({
                     T.tables.id: new
                 }))
        return ''

    @classmethod
    async def get_tables(cls, id):
        async with database.query() as Q:
            item = (await (Q()
            .tables(T.items)
            .fields(
                    T.items.tax,
                    T.items.taxDub,
                    T.items.taxP,
                    T.items.taxPDub,
                    T.items.disc,
                    T.items.discP,
                    T.items.butDiscPerc,
                    T.items.addtaxColapse,
                    T.items.comment

                )
            .where(T.items.id == id)
            .selectone()))
            if item['tax']==None:
                    item['tax']='0,0'
            if item['taxDub']==None:
                    item['taxDub']='0,0'
            if item['taxP']==None:
                    item['taxP']='0,0'
            if item['taxPDub']==None:
                    item['taxPDub']='0,0'
            if item['disc']==None:
                    item['disc']='0,0'
            if item['discP']==None:
                    item['discP']='0,0'
            if item['butDiscPerc']==None:
                    item['butDiscPerc']='%'
            if item['addtaxColapse']==None:
                    item['addtaxColapse']='false'

            tax=(item['tax'].replace(',', '.'))
            taxDub=(item['taxDub'].replace(',', '.'))
            taxP=(item['taxP'].replace(',', '.'))
            taxPDub=(item['taxPDub'].replace(',', '.'))
            disc=(item['disc'].replace(',', '.'))
            discP=(item['discP'].replace(',', '.'))
            butDiscPerc=item['butDiscPerc']
            addtaxColapse=item['addtaxColapse']

            partx = []
            tables =(await (Q()
                    .tables(T.tables)
                    .fields(
                        T.tables.id,
                        T.tables.name,
                        T.tables.device,
                        T.tables.obj,
                        T.tables.selected
                    )
                    .where(T.tables.item_id == id)
                    .selectall()))
             
            for val in tables:                
                rows =(await (Q()
                            .tables(T.rows_for_table)
                            .fields(
                                T.rows_for_table.id,
                                T.rows_for_table.table_id,
                                T.rows_for_table.count,
                                T.rows_for_table.status,
                                T.rows_for_table.alttax,
                                T.rows_for_table.summa,
                                T.rows_for_table.unit,
                                T.rows_for_table.without,
                                T.rows_for_table.done,
                                T.rows_for_table.description_head,
                                T.rows_for_table.description_work,
                                T.rows_for_table.description_from_price,
                                T.rows_for_table.discount,
                                T.rows_for_table.position_number,
                                T.rows_for_table.description_from_price,
                                T.rows_for_table.price,
                                T.rows_for_table.id
                            )
                            .where(T.rows_for_table.table_id == val['id'])
                            .selectall()))

                rows_devices =(await (Q()
                            .tables(T.rows_for_devices)
                            .fields(
                                T.rows_for_devices.id,
                                T.rows_for_devices.table_id,
                                T.rows_for_devices.pos_num,
                                T.rows_for_devices.designation,
                                T.rows_for_devices.kilowatt,
                                T.rows_for_devices.comment,
                                T.rows_for_devices.time,
                                T.rows_for_devices.manufacturer,
                                T.rows_for_devices.serial,
                                T.rows_for_devices.order,
                                T.rows_for_devices.check_date,
                                T.rows_for_devices.next_check_date,
                                T.rows_for_devices.sdate,
                                T.rows_for_devices.sworker,
                                T.rows_for_devices.smReading,
                                T.rows_for_devices.fdate,
                                T.rows_for_devices.fworker,
                                T.rows_for_devices.fmReading,
                                T.rows_for_devices.location
                            )
                            .where(T.rows_for_devices.table_id == val['id'])
                            .selectall()))

                rows_measurement =(await (Q()
                            .tables(T.measure_protocol)
                            .fields(
                                T.measure_protocol.id,
                                T.measure_protocol.table_id,
                                T.measure_protocol.sminsurface,
                                T.measure_protocol.smaxsurface,
                                T.measure_protocol.smindepth,
                                T.measure_protocol.smaxdepth,
                                T.measure_protocol.fminsurface,
                                T.measure_protocol.fmaxsurface,
                                T.measure_protocol.fmindepth,
                                T.measure_protocol.fmaxdepth
                            )
                            .where(T.measure_protocol.table_id == val['id'])
                            .selectall()))

                rows_damage =(await (Q()
                            .tables(T.damage)
                            .fields(
                                T.damage.id,
                                T.damage.table_id,
                                T.damage.imgId,
                                T.damage.name,
                                T.damage.desc,
                                T.damage.rotate
                            )
                            .where(T.damage.table_id == val['id'])
                            .selectall()))

                flavours={}
                objNone={}
                disable=[]
                selResults={}
                if val['obj'] is not None:
                    
                    for obj in val['obj'].split(','):
                        count=0
                        objs=[]

                        for row in rows:
                            row['upHere']=False
                            count=count+1
                            objs.append('temp'+str(count))

                            if row['done']==None:
                                row['done']=''
                            if row['done']=='false':
                                row['done']=''
                            if row['alttax']=='true':
                                row['alttax']=True
                            if row['alttax']=='false':
                                row['alttax']=False

                            if row['without']=='true':
                                row['without']=True
                            else:
                                row['without']=False
                           
                        flavours[obj]=objs
                        objNone[obj]=False

                    selResults={}
                    for sel in val['selected'].split('|'):

                        select = sel.split(':')
                        if len(select)==2:
                            if select[1]=='':
                                select=''

                            selResults[select[0]]=select[1].split(',')
                            for dis in select[1].split(','):
                                disRow = dis.split('temp')[1]
                                disRow = select[0]+'-'+str(int(disRow)-1)
                                disable.append(disRow)

                        else:
                            flavours={}
                            objNone={}
                # print(disable)
                # print(flavours)

                for rowDev in rows_devices:
                    rowDev['subEquel'] = (await (Q()
                            .tables(T.measurement)
                            .fields(
                                T.measurement.id,
                                T.measurement.date,
                                T.measurement.worker,
                                T.measurement.mReading,
                            )
                            .where(T.measurement.rows_for_devices == rowDev['id'])
                            .selectall()))

                partx.append({'parts':{'id': val['id'], 'part_name': val['name'], 'part_name_device': val['device'], 'toggle': False,
                                        'checkbox_list':{
                                            'disable':disable,
                                            'flavours':flavours,
                                            'selected':selResults,
                                            'allSelected':objNone,
                                            'indeterminate':objNone
                                        },
                                        'part_content':rows,'devices_content':rows_devices,'measure_protocol':rows_measurement,'damage_content':rows_damage}})
            #print(item['butDiscPerc'])
            partx.append({'taxs' : item})
            return partx

    @classmethod
    async def update_checkbox_table(cls, id, fild, data):
        string = ''
        objs = json.loads(data)
        counObj=0
        objstring=''
        for obj in objs:
            if counObj==0:
                separator = ''
                sepObj = ''
            else:
                separator = '|'
                sepObj = ','
            counObj=counObj+1
            string=string+separator+obj+':'
            objstring=objstring+sepObj+obj

            count=0
            for item in objs[obj]:
                count=count+1
                if count==len(objs[obj]):
                    separator = ''
                else:
                    separator = ','
                numberForItem = int(item.split('temp')[1])
                item = 'temp'+str(numberForItem)
                string = string+item+separator

        async with database.query() as Q:
            await (Q()
                     .tables(T.tables)
                     .where(T.tables.id == id)
                     .update({
                         T.tables[fild]: string,
                         T.tables.obj: objstring
                     }))

        return ''

    @classmethod
    async def get_damage(cls, id):
        async with database.query() as Q:
                damages=(await (Q()
                    .tables(T.group_for_damages)
                    .fields(
                        T.group_for_damages.id,
                        T.group_for_damages.name
                    )
                    .where(T.group_for_damages.item_id == id)
                    .selectall()))

                for val in damages:
                    imamges = (await (Q()
                    .tables(T.images_for_group_damages)
                    .fields(
                        T.images_for_group_damages.id,
                        T.images_for_group_damages.file_name,
                        T.images_for_group_damages.date,
                        T.images_for_group_damages.desc
                    )
                    .where(T.images_for_group_damages.group_id == val['id'])
                    .selectall()))
                    tasks = (await (Q()
                    .tables(T.task_for_damages)
                    .fields(
                        T.task_for_damages.id,
                        T.task_for_damages.name,
                        T.task_for_damages.data_time_start,
                        T.task_for_damages.data_time_end,
                        T.task_for_damages.workers
                    )
                    .where(T.task_for_damages.table_id == val['id'])
                    .selectall()))
                    val['up']=False
                    val['images']=imamges
                    val['tasks']=tasks

                
                return damages

    @classmethod
    async def get_damage_images(cls, id, project):
        async with database.query() as Q:
                items =  (await (Q()
                    .tables(T.items & T.tables  & T.type_for_table).on((T.items.id == T.tables.item_id) & (T.items.type == T.type_for_table.id))
                    .fields(
                        T.type_for_table.type,
                        T.tables.id,
                        T.tables.name
                    )
                    .where(T.items.project_id == id)
                    .selectall()))

                result = list()              
                files=(await (Q()
                    .tables(T.files)
                    .fields(
                        T.files.id,
                        T.files.name,
                        # T.files.html,
                        T.files.number,
                        T.files.id,
                        # T.files.pages,
                        T.files.group,
                        T.files.added,
                        T.files.user
                    )
                    .where(T.files.number == project)
                    .selectall()))
                for val in files:
                    full_name = path.basename(val['name'])
                    if path.splitext(full_name)[1]!='.pdf':

                        if val['group']=='':
                            group=0
                        else:
                            group=val['group']
                        if val['user']==None:
                            user = 'Undefind'
                        else:
                            user =  val['user']
                        img={'id':'/image?id='+str(val['id']), 'file_name':val['name'], 'date':val['added'], 'desc':'', 'user':user, 'group':group, '_rowVariant':''}
                        result.append(img)
                # print(files, project)

         
                damages=(await (Q()
                    .tables(T.items)
                    .fields(
                        T.items.id
                    )
                    .where((T.items.project_id == id) & (T.items.type == 4))
                    .selectall()))

                for val in damages:
                    group=(await (Q()
                    .tables(T.group_for_damages)
                    .fields(
                        T.group_for_damages.id,
                        T.group_for_damages.name
                    )
                    .where(T.group_for_damages.item_id == val['id'])
                    .selectall()))


                    for val in group:
                        images=(await (Q()
                        .tables(T.images_for_group_damages)
                        .fields(
                            T.images_for_group_damages.id,
                            T.images_for_group_damages.file_name,
                            T.images_for_group_damages.date,
                            T.images_for_group_damages.desc
                        )
                        .where(T.images_for_group_damages.group_id == val['id'])
                        .selectall()))

                        for img in images:
                            img['id'] = '/image_damage?id='+str(img['id'])
                            img['from']=val['name']
                            img['type']='Damage'
                            # print(img)
                            result.append(img)

                # result = list(filter(None, result))
                # print(result)
                return result



    @classmethod
    async def get_damage_images_company(cls, id):
        async with database.query() as Q:


                result = list()              
                files=(await (Q()
                    .tables(T.files_to_company)
                    .fields(
                        T.files_to_company.id,
                        T.files_to_company.name,
                        T.files_to_company.html,
                        T.files_to_company.number,
                        T.files_to_company.pages,
                        T.files_to_company.group,
                        T.files_to_company.added,
                        T.files_to_company.user
                    )
                    .where(T.files_to_company.number == id)
                    .selectall()))

                for val in files:
                    full_name = path.basename(val['name'])
                    if path.splitext(full_name)[1]!='.pdf':

                    #     if val['group']=='':
                    #         group=0
                    #     else:
                    #         group=val['group']
                    #     if val['user']==None:
                    #         user = 'Undefind'
                    #     else:
                    #         user =  val['user']
                        content={'id':'/image_company?id='+str(val['id']), 'file_name':val['name'], 'date':val['added'], 'user':val['user']}
                        result.append(content)
                    else:
                        content={'id':str(val['id']), 'name':val['name'], 'added':val['added'], 'user':val['user'], 'group':'', 'html':val['html'], 'pages':val['pages']}
                        result.append(content)

                return result

    @classmethod
    async def get_damage_images_customer(cls, id):
        async with database.query() as Q:


                result = list()              
                files=(await (Q()
                    .tables(T.files_to_customer)
                    .fields(
                        T.files_to_customer.id,
                        T.files_to_customer.name,
                        T.files_to_customer.html,
                        T.files_to_customer.number,
                        T.files_to_customer.pages,
                        T.files_to_customer.group,
                        T.files_to_customer.added,
                        T.files_to_customer.user
                    )
                    .where(T.files_to_customer.number == id)
                    .selectall()))

                for val in files:
                    full_name = path.basename(val['name'])
                    if path.splitext(full_name)[1]!='.pdf':

                    #     if val['group']=='':
                    #         group=0
                    #     else:
                    #         group=val['group']
                    #     if val['user']==None:
                    #         user = 'Undefind'
                    #     else:
                    #         user =  val['user']
                        content={'id':'/image_customer?id='+str(val['id']), 'file_name':val['name'], 'date':val['added'], 'user':val['user']}
                        result.append(content)
                    else:
                        content={'id':str(val['id']), 'name':val['name'], 'added':val['added'], 'user':val['user'], 'group':'', 'html':val['html'], 'pages':val['pages']}
                        result.append(content)

                return result


    @classmethod
    async def get_damage_images_person(cls, id):
        async with database.query() as Q:


                result = list()              
                files=(await (Q()
                    .tables(T.files_to_person)
                    .fields(
                        T.files_to_person.id,
                        T.files_to_person.name,
                        T.files_to_person.html,
                        T.files_to_person.number,
                        T.files_to_person.pages,
                        T.files_to_person.group,
                        T.files_to_person.added,
                        T.files_to_person.user
                    )
                    .where(T.files_to_person.number == id)
                    .selectall()))

                for val in files:
                    full_name = path.basename(val['name'])
                    if path.splitext(full_name)[1]!='.pdf':

                    #     if val['group']=='':
                    #         group=0
                    #     else:
                    #         group=val['group']
                    #     if val['user']==None:
                    #         user = 'Undefind'
                    #     else:
                    #         user =  val['user']
                        content={'id':'/image_person?id='+str(val['id']), 'file_name':val['name'], 'date':val['added'], 'user':val['user']}
                        result.append(content)
                    else:
                        content={'id':str(val['id']), 'name':val['name'], 'added':val['added'], 'user':val['user'], 'group':'', 'html':val['html'], 'pages':val['pages']}
                        result.append(content)

                return result

    @classmethod
    async def get_damage_images_sub(cls, id):
        async with database.query() as Q:


                result = list()              
                files=(await (Q()
                    .tables(T.files_to_sub)
                    .fields(
                        T.files_to_sub.id,
                        T.files_to_sub.name,
                        T.files_to_sub.html,
                        T.files_to_sub.number,
                        T.files_to_sub.pages,
                        T.files_to_sub.group,
                        T.files_to_sub.added,
                        T.files_to_sub.user
                    )
                    .where(T.files_to_sub.number == id)
                    .selectall()))

                for val in files:
                    full_name = path.basename(val['name'])
                    if path.splitext(full_name)[1]!='.pdf':

                    #     if val['group']=='':
                    #         group=0
                    #     else:
                    #         group=val['group']
                    #     if val['user']==None:
                    #         user = 'Undefind'
                    #     else:
                    #         user =  val['user']
                        content={'id':'/image_sub?id='+str(val['id']), 'file_name':val['name'], 'date':val['added'], 'user':val['user']}
                        result.append(content)
                    else:
                        content={'id':str(val['id']), 'name':val['name'], 'added':val['added'], 'user':val['user'], 'group':'', 'html':val['html'], 'pages':val['pages']}
                        result.append(content)

                return result


    @classmethod
    async def get_damage_images_sperson(cls, id):
        async with database.query() as Q:


                result = list()              
                files=(await (Q()
                    .tables(T.files_to_sperson)
                    .fields(
                        T.files_to_sperson.id,
                        T.files_to_sperson.name,
                        T.files_to_sperson.html,
                        T.files_to_sperson.number,
                        T.files_to_sperson.pages,
                        T.files_to_sperson.group,
                        T.files_to_sperson.added,
                        T.files_to_sperson.user
                    )
                    .where(T.files_to_sperson.number == id)
                    .selectall()))

                for val in files:
                    full_name = path.basename(val['name'])
                    if path.splitext(full_name)[1]!='.pdf':

                    #     if val['group']=='':
                    #         group=0
                    #     else:
                    #         group=val['group']
                    #     if val['user']==None:
                    #         user = 'Undefind'
                    #     else:
                    #         user =  val['user']
                        content={'id':'/image_sperson?id='+str(val['id']), 'file_name':val['name'], 'date':val['added'], 'user':val['user']}
                        result.append(content)
                    else:
                        content={'id':str(val['id']), 'name':val['name'], 'added':val['added'], 'user':val['user'], 'group':'', 'html':val['html'], 'pages':val['pages']}
                        result.append(content)

                return result

    @classmethod
    async def get_images(cls, id):
        async with database.query() as Q:
              return await (Q()
                    .tables(T.images_for_group_damages)
                    .fields(
                        T.images_for_group_damages.id,
                        T.images_for_group_damages.file_name,
                        T.images_for_group_damages.date,
                        T.images_for_group_damages.desc
                        # T.images_for_group_damages.content
                    )
                    .where(T.images_for_group_damages.group_id == id)
                    .selectall())
              
    @classmethod
    async def change_type(cls, id, type):
        async with database.query() as Q:
            type_id =(await (Q()
                    .tables(T.type_for_table)
                    .fields(
                        T.type_for_table.id
                    )
                    .where(T.type_for_table.type == type)
                    .selectone()))
            return await (Q()
                .tables(T.items)
                .where(T.items.id == id)
                .update({
                    T.items.type: type_id['id']
                }))
            
            
    @classmethod
    async def get_types_for_tables(cls):
        async with database.query() as Q:
            return await (Q(T.type_for_table)
                .fields(
                    T.type_for_table.type,
                ).selectall())

    @classmethod
    async def add_project(cls, year, date, country, area, city, street, zip, user):
        async with database.query() as Q:
            nums = (await (Q(T.project)
                    .fields(
                        T.project.project_number
                    ).order_by(T.project.id.desc()).selectone()))
            await (Q()
                  .tables(T.project)
                  .insert({
                  T.project.project_number_year: year,
                  T.project.project_number: (nums['project_number']+1),
                  T.project.date: date,
                  T.project.user_id: user, 
                  T.project.street1: street,
                  T.project.country: country,
                  T.project.area: area,
                  T.project.city1: city,
                  T.project.zip1: zip,
                  T.project.status_set: 'Open',
                  T.project.mail: 0, 
                  T.project.phone: 0, 
                  T.project.fax: 0,
                  T.project.person_id: 0,
                  T.project.customer_id: 0
                  }))
            return await (Q(T.project)
                .fields(
                    T.project.project_number_year,
                    T.project.date,
                    T.project.street1,
                    T.project.city1,
                    T.project.zip1,
                    T.project.status_set,
                    T.project.id,
                    T.project.other
                ).selectall())

    @classmethod
    async def changeDisableTableAfterDell(cls, timestam, ws_clients):
        await asyncio.sleep(15)
        async with database.query() as Q:
            await (Q(T.changeDisableTable)
                 .where((T.changeDisableTable.time == timestam))
                 .delete())
            for client in ws_clients:
                await client.send_str('getLoocks')

            # return web.json_response('')
            # ioloop.run_until_complete(wait_tasks)
            # ioloop.close()
            return ''
    # @classmethod
    # async def foo(cls):
    #     print('Running in foo')
    #     await asyncio.sleep(0)
    #     print('Explicit context switch to foo again')

    # @classmethod
    # async def bar(cls):
    #     print('Explicit context to bar')
    #     await asyncio.sleep(0)
    #     print('Implicit context switch back to bar')

    @classmethod
    async def changeDisableTable(cls, type_operation, fild, id, user, ws_clients):
        async with database.query() as Q:
            timestam = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if type_operation=='f':
                await (Q()
                     .tables(T.changeDisableTable)
                     .insert({
                       T.changeDisableTable.fild: fild,
                       T.changeDisableTable.rows_id: id,
                       T.changeDisableTable.user: user,
                       T.changeDisableTable.time: timestam
                }))


                ioloop = asyncio.get_event_loop()
                tasks = [ioloop.create_task(Projects.changeDisableTableAfterDell(timestam, ws_clients))]
                # wait_tasks = asyncio.wait(tasks)
                # ioloop.run_until_complete(wait_tasks)
                # ioloop.close()

                # del_id = (await (Q()
                # .tables(T.changeDisableTable)
                # .fields(T.changeDisableTable.id)
                # .where(T.changeDisableTable.time == timestam)
                # .selectone()))



                # await Projects.changeDisableTableAfterDell(timestam)
             # 
                # await Projects.say_after(30, 'world')
            if type_operation=='b':
                await (Q(T.changeDisableTable)
                        .where((T.changeDisableTable.fild == fild) & (T.changeDisableTable.rows_id == id))
                        .delete())
        return ''

    @classmethod
    async def getLoocks(cls):
        async with database.query() as Q:
            return await (Q()
                .tables(T.changeDisableTable)
                .fields(T.changeDisableTable.id, T.changeDisableTable.fild, T.changeDisableTable.rows_id, T.changeDisableTable.user)
                .selectall())

        

class Offer:
    @classmethod
    async def select_offer(cls, id):
        async with database.query() as Q:
            return await (Q()
                .tables(T.offer)
                .fields(T.offer.offer_number, T.offer.status_set, T.offer.other)
                .where(T.offer.project_id == id)
                .selectall())

class Invoice:
    @classmethod
    async def select_invoice(cls, id):
        async with database.query() as Q:
            return await (Q()
                .tables(T.invoice)
                .fields(
                    T.invoice.invoice_number,
                    T.invoice.status_set,
                    T.invoice.other,
                    T.invoice.id,
                    T.invoice.year
                    )
                .where(T.invoice.project_id == id)
                .selectall())

    @classmethod
    async def detect_invoice(cls):
        async with database.query() as Q:
            maxId=0
            maxItem=2020
            ids=(
                await (Q()
                    .tables(T.number_for_invoice)
                    .fields(
                        T.number_for_invoice.id,
                        T.number_for_invoice.item_id
                        )
                    .selectall())
                )

            for id in ids:
                maxId=id['id']
                maxItem=id['item_id']

            lastYear = ( await (Q()
                .tables(T.items)
                .fields(
                T.items.date
                )
                .where(T.items.id == maxItem)
                .selectone())
            )      

            diff=[]
            try:
                for diffId in range(1, (maxId+1)):
                    sub = 0
                    for id in ids:
                        result = (id['id']==diffId)
                        if result==True:
                            sub = 1
                        
                    if result==False:
                        if sub == 0:
                            diff.append(diffId)
            except:
                maxId = 0
            diff.append({'lastNumber':(maxId+1), 'lastDate':lastYear})
            return(diff)

    @classmethod
    async def get_reports(cls, id):
        async with database.query() as Q:
            result = (await (Q()
                .tables(T.items)
                .fields(
                    T.items.id,
                    T.items.number,
                    T.items.date,
                    T.items.other,
                    T.items.place,
                    T.items.insurance_number,
                    T.items.work,
                    T.items.status_set,
                    T.items.tax,
                    T.items.taxDub,
                    T.items.taxP,
                    T.items.taxPDub,
                    T.items.disc,
                    T.items.discP,
                    T.items.butDiscPerc,
                    T.items.addtaxColapse,
                    T.items.dateEvent,
                    T.items.dateInspect,
                    T.items.ExamWorker
                )
                .selectall()))
            sendResult=[]

            index = 0
            for res in result:
                
                if id in res['number']:
                    index = int(index)+1
                    res['number'] = index
                    sendResult.append(res)
        return sendResult

    @classmethod
    async def add_invoice(cls, id, type, number, newRange):
        async with database.query() as Q:

            types = ( await (Q()
                .tables(T.type_for_table)
                .fields(
                T.type_for_table.id 
                )
                .where(T.type_for_table.type == type)
                .selectone())
            )         


            result = ( await (Q()
                .tables(T.items)
                .fields(
                    T.items.project_id,
                    T.items.number,
                    T.items.date,
                    T.items.status_set,
                    T.items.other,
                    T.items.place,
                    T.items.insurance_number,
                    T.items.insurname,
                    T.items.work,
                    T.items.type,
                    T.items.id,
                    T.items.tax,
                    T.items.taxDub,
                    T.items.taxP,
                    T.items.taxPDub,
                    T.items.disc,
                    T.items.discP,
                    T.items.butDiscPerc,
                    T.items.addtaxColapse
                    )
                .where(T.items.id == id)
                .selectone())
             )
            
            # number_documents = result['number']+' '+str(result['id'])
            number_documents = result['number'].split('-')[0]+'-'+datetime.datetime.now().strftime("%Y")+' '+str(result['id'])
            

            await (Q()
                     .tables(T.items)
                     .insert({
                       T.items.project_id : result['project_id'],
                       T.items.number : number_documents,
                       T.items.date : datetime.datetime.now().strftime("%Y-%m-%d"),
                       T.items.status_set : result['status_set'],
                       T.items.other : result['other'],
                       T.items.place : result['place'],
                       T.items.insurance_number : result['insurance_number'],
                       T.items.insurname : result['insurname'],
                       T.items.work : result['work'],
                       T.items.type: types['id'],
                       T.items.tax: result['tax'],
                       T.items.taxDub: result['taxDub'],
                       T.items.taxP: result['taxP'],
                       T.items.taxPDub: result['taxPDub'],
                       T.items.disc: result['disc'],
                       T.items.discP: result['discP'],
                       T.items.butDiscPerc: result['butDiscPerc'],
                       T.items.addtaxColapse: result['addtaxColapse']
                       # T.items.year: datetime.datetime.now().strftime("%Y"),
                    }))

            invoiceIdx = ( await (Q()
                .tables(T.items)
                .fields(
                    T.items.id
                    )
                .where(T.items.number == number_documents)
                .selectall())
             )
            invoiceId = invoiceIdx[len(invoiceIdx)-1]

            if type=='Invoices':

                if (newRange=='true'):
                      await (Q()
                        .tables(T.number_for_invoice)
                        .where(T.number_for_invoice.id != 0)
                        .delete())

                await (Q()
                        .tables(T.number_for_invoice)
                        .insert({
                            T.number_for_invoice.item_id : invoiceId['id'],
                            T.number_for_invoice.id : number
                        }))
            
                numberInvoice = ( await (Q()
                    .tables(T.number_for_invoice)
                    .fields(
                        T.number_for_invoice.id
                        )
                    .where(T.number_for_invoice.item_id == invoiceId['id'])
                    .selectone())
                )

                await (Q()
                        .tables(T.items)
                        .where(T.items.number == number_documents)
                        .update({
                            T.items.number: result['number'].split('-')[0]+'-'+datetime.datetime.now().strftime("%Y")+' '+str(numberInvoice['id'])+' '+str(result['id'])
                        }))
                
            if type=='SUB':
                await (Q()
                        .tables(T.items)
                        .where(T.items.number == number_documents)
                        .update({
                            T.items.number:number+' '+str(result['id'])+' '+str(result['number']),
                            T.items.status_set:'Open'
                        }))

            if type=='Sub Invoices':
                await (Q()
                        .tables(T.items)
                        .where(T.items.number == number_documents)
                        .update({
                            T.items.number:result['number']+' '+number+' '+str(result['id'])
                        }))

            resultTables = ( await (Q()
                .tables(T.tables)
                .fields(
                    T.tables.id,
                    T.tables.name,
                    T.tables.obj,
                    T.tables.selected
                    )
                .where(T.tables.item_id == id)
                .selectall()))

            for val in resultTables:
                    resultData = ( await (Q()
                    .tables(T.rows_for_table)
                    .fields(
                        T.rows_for_table.count,
                        T.rows_for_table.status,
                        T.rows_for_table.alttax,
                        T.rows_for_table.summa,
                        T.rows_for_table.unit,
                        T.rows_for_table.without,
                        T.rows_for_table.done,
                        T.rows_for_table.description_head,
                        T.rows_for_table.description_work,
                        T.rows_for_table.description_from_price,
                        T.rows_for_table.discount,
                        T.rows_for_table.position_number,
                        T.rows_for_table.description_from_price,
                        T.rows_for_table.price,
                        T.rows_for_table.id
                        )
                    .where(T.rows_for_table.table_id == val['id'])
                    .selectall())
                    )

                    if type == 'Damage Description':
                        sel = number.split(',')

                        await (Q()
                             .tables(T.group_for_damages)
                             .insert({
                               T.group_for_damages.name : val['name'],
                               T.group_for_damages.item_id : invoiceId['id'],
                        }))

                        gropupId = (await (Q()
                            .tables(T.group_for_damages)
                            .fields(
                                T.group_for_damages.id
                            )
                            .where((T.group_for_damages.name == val['name']) & (T.group_for_damages.item_id == invoiceId['id']))
                            .selectone())
                        )

                        for index, row in enumerate(resultData):
                            number = number.replace(' ', '')
                            val['name'] = val['name'].replace(' ', '')
                            sel = number.split(',')

                            for sindex, i in enumerate(sel):
                                item = i.split('-')
                                if ((val['name']==str(item[0])) & (index == int(item[1]))):
                                    await (Q()
                                        .tables(T.task_for_damages)
                                        .insert({
                                            T.task_for_damages.name : row['description_head'],
                                            T.task_for_damages.table_id : gropupId['id']
                                        }))
                    else:
                        if type!='SUB':
                            await (Q()
                                 .tables(T.tables)
                                 .insert({
                                   T.tables.name : val['name'],
                                   T.tables.item_id : invoiceId['id'],
                                   T.tables.obj: val['obj'],
                                   T.tables.selected: val['selected']
                                   # T.items.year: datetime.datetime.now().strftime("%Y"),
                                }))

                            tableId = ( await (Q()
                            .tables(T.tables)
                            .fields(
                                T.tables.id
                                )
                            .where((T.tables.name == val['name']) & (T.tables.item_id == invoiceId['id']))
                            .selectone())
                            )

                            resultFiles = ( await (Q()
                            .tables(T.files)
                            .fields(
                                T.files.content,
                                T.files.name,
                                T.files.number,
                                T.files.pages,
                                T.files.resp,
                                T.files.html,
                                T.files.added
                                )
                            .where(T.files.group == val['id'])
                            .selectall())
                             )

                            for file in resultFiles:
                                await (Q()
                                .tables(T.files)
                                .insert({
                                    T.files.content: file['content'],
                                    T.files.name: file['name'],
                                    T.files.number: file['number'],
                                    T.files.pages: file['pages'],
                                    T.files.resp: file['resp'],
                                    T.files.html: file['html'],
                                    T.files.added: file['added'],
                                    T.files.group: tableId['id']
                                }))

                            for row in resultData:
                                    await (Q()
                                    .tables(T.rows_for_table)
                                    .insert({
                                        T.rows_for_table.count : row['count'],
                                        T.rows_for_table.status : row['status'],
                                        T.rows_for_table.alttax : row['alttax'],
                                        T.rows_for_table.summa : row['summa'],
                                        T.rows_for_table.unit : row['unit'],
                                        T.rows_for_table.without : row['without'],
                                        T.rows_for_table.done : row['done'],
                                        T.rows_for_table.description_head : row['description_head'],
                                        T.rows_for_table.description_work : row['description_work'],
                                        T.rows_for_table.description_from_price : row['description_from_price'],
                                        T.rows_for_table.discount : row['discount'],
                                        T.rows_for_table.position_number : row['position_number'],
                                        T.rows_for_table.price : row['price'],
                                        T.rows_for_table.table_id : tableId['id']
                                    }))

        return ''

    @classmethod
    async def select_invoices(cls, id):
        async with database.query() as Q:
            return await (Q()
                .tables(T.invoice)
                .fields(
                    T.invoice.inoice_number,
                    T.invoice.date,
                    T.invoice.status_set,
                    T.invoice.other,
                    T.invoice.place,
                    T.invoice.insurance_number,
                    T.invoice.work,
                    T.invoice.offer_id,
                    T.invoice.id,
                    T.invoice.year
                    )
                .where(T.invoice.project_id == id)
                .selectall())


class add_same:
    @classmethod
    async def add_same(cls, add_number, add_work, add_insurance_number, add_place, add_comment, add_project_id, type):
            async with database.query() as Q:
                type_id = (await (Q()
                    .tables(T.type_for_table)
                    .fields(
                        T.type_for_table.id
                        )
                    .where(T.type_for_table.type == type)
                    .selectone()))
                return await (Q()
                    .tables(T.items)
                    .insert({
                        T.items.discP:0,
                        T.items.disc:0,
                        T.items.taxP:19,
                        T.items.taxDub:0.0,
                        T.items.tax:0.00,
                        T.items.taxPDub:0,
                        T.items.work: add_work,
                        T.items.place: add_place,
                        T.items.insurance_number:add_insurance_number,
                        T.items.other: add_comment, 
                        T.items.number: add_number,
                        T.items.date: datetime.datetime.now().strftime("%Y-%m-%d"),
                        T.items.status_set: 'Open',
                        T.items.project_id: add_project_id,
                        T.items.type: type_id['id']
                    }))
class Del_offer:
    @classmethod
    async def del_item(cls, id):
        async with database.query() as Q:
            tables = (
                await (Q(T.tables)
                    .fields(
                        T.tables.id)
                    .where(T.tables.item_id == id)
                    .selectall())
                    )

            for table in tables:
                rows = (await (Q(T.rows_for_table)
                .fields(
                    T.rows_for_table.id)
                .where(T.rows_for_table.table_id == table['id'])
                .selectall())
                )
                for row in rows:
                    await (Q(T.rows_for_table)
                        .where(T.rows_for_table.id == row['id'])
                        .delete())

            await (Q(T.tables)
                .where(T.tables.item_id == id)
                .delete())

            number_invoice = (await (Q(T.items)
                    .fields(T.items.id)
                    .where(T.items.id == id)
                    .selectone())
                )
           
            await (Q(T.number_for_invoice)
                .where(T.number_for_invoice.item_id == number_invoice['id'])
                .delete())
                
            
            await (Q(T.items)
                .where(T.items.id == id)
                .delete())



class Offers:
    @classmethod
    async def select_offers(cls, id):
        async with database.query() as Q:
            return await (Q(T.offer)
                .fields(
                    T.offer.offer_number,
                    T.offer.date,
                    T.offer.work,
                    T.offer.status_set,
                    T.offer.place,
                    T.offer.status_set,
                    T.offer.insurance_number,
                    T.offer.other,
                    T.offer.type,
                    T.offer.id)
                .where(T.offer.project_id == id)
                .selectall())


class Docs:
    @classmethod
    async def docs_menu(cls, project):
        async with database.query() as Q:
            return await (Q(T.docs_menu)
                .fields(
                    T.docs_menu.id,
                    T.docs_menu.name,
                    T.docs_menu.parrent)
                .where(T.docs_menu.project == project)
                .selectall())

    @classmethod
    async def show_docs(cls, id):
        async with database.query() as Q:
            return await (Q(T.devices)
                .fields(
                    T.devices.pos_num,
                    T.devices.designation,
                    T.devices.comment,
                    T.devices.kilowatt,
                    T.devices.time,
                    T.devices.manufacturer,
                    T.devices.serial,
                    T.devices.order,
                    T.devices.check_date,
                    T.devices.next_check_date,
                    T.devices.id
                )
                .where(T.devices.item_id == id)
                .selectall())

    @classmethod
    async def add_docs_menu(cls, parent_id, project):
        async with database.query() as Q:
            return await (Q(T.docs_menu)
                .tables(T.docs_menu)
                .insert({
                    T.docs_menu.name: 'New Part',
                    T.docs_menu.parrent: parent_id,
                    T.docs_menu.project: project
            }))

    @classmethod
    async def remove_docs_menu(cls, remove_id):
        async with database.query() as Q:
            return await (Q(T.docs_menu)
              .tables(T.docs_menu)
              .where(T.docs_menu.id == remove_id)
              .delete())

    @classmethod
    async def update_name_docs_menu(cls, name, id):
        async with database.query() as Q:
            return await (Q(T.docs_menu)
                .tables(T.docs_menu)
                .where(T.docs_menu.id == id)
                .update({
                    T.docs_menu.name: name
                }))

    @classmethod
    async def get_type_docs(cls, type):
            async with database.query() as Q:
                return await (Q(T.type_docs)
                    .fields(
                        T.type_docs.id,
                        T.type_docs.name)
                    .where(T.type_docs.type == type)
                    .selectall())

    @classmethod
    async def select_template(cls, indexses):
            async with database.query() as Q:
                result = []
                for index in indexses.split(','):
                    result.append(await (Q(T.type_docs)
                    .fields(T.type_docs.template)
                    .where(T.type_docs.id == index)
                    .selectone()))
                return result

    @classmethod
    async def date_logo(cls):
            async with database.query() as Q:
                return await (Q(T.date_logo)
                    .fields(
                        T.date_logo.date_logo,
                        T.date_logo.date_logo_head,
                        T.date_logo.date_logo_address,
                        T.date_logo.date_logo_image)
                    .where(T.date_logo.id == 1)
                    .selectone())
    @classmethod
    async def add_pdf(cls, h, date, offerHead, number, added, number_of_pages, project_id, user):
            async with database.query() as Q:
                # print('files')
                return await (Q()
                    .tables(T.docs)
                    .insert({
                        T.docs.html: h,
                        T.docs.date: date,
                        T.docs.name: 'New '+offerHead+' #'+number,
                        T.docs.number: number,
                        T.docs.pages: number_of_pages,
                        T.docs.added: added,
                        T.docs.project_id : project_id,
                        T.docs.user : user
                    }))
    @classmethod
    async def select_docs(cls, id):
            async with database.query() as Q:
                return await (Q()
                    .tables(T.docs)
                    .fields(
                        T.docs.html,
                        T.docs.added,
                        T.docs.name,
                        T.docs.number,
                        T.docs.pages,
                        T.docs.date,
                        T.docs.id,
                        T.docs.user
                    )
                    .where(T.docs.project_id==id)
                    .selectall())
    @classmethod
    async def select_files(cls, id):
            async with database.query() as Q:
                return await (Q()
                    .tables(T.files)
                    .fields(
                        T.files.name,
                        T.files.html,
                        T.files.number,
                        T.files.id,
                        T.files.pages,
                        T.files.group,
                        T.files.added,
                        T.files.user
                    )
                    .where(T.files.number==id)
                    .selectall())

    # @classmethod
    # async def select_image_damage(cls, id):
    #         async with database.query() as Q:
    #             return await (Q()
    #                 .tables(T.images_for_group_damages)
    #                 .fields(
    #                     T.images_for_group_damages.file_name,
    #                     T.images_for_group_damages.content
    #                 )
    #                 .where(T.images_for_group_damages.id==id)
    #                 .selectone())


    @classmethod
    async def select_image_damage(cls, id):
            async with database.query() as Q:
                return await (Q()
                    .tables(T.damage)
                    .fields(
                        T.damage.content
                    )
                    .where(T.damage.imgId==id)
                    .selectone())


    @classmethod
    async def select_image_damage_pdf(cls, data):
            async with database.query() as Q:
                for row in data:
                    for image in row['images']:
                        contentFromDataBase = (
                          await (Q()
                            .tables(T.images_for_group_damages)
                            .fields(
                                T.images_for_group_damages.content
                            )
                            .where(T.images_for_group_damages.id==image['id'])
                            .selectone())
                        )
                        image['content']=b64encode(contentFromDataBase['content']).decode()
                return data        

    @classmethod
    async def images_for_pdf(cls, id):
        async with database.query() as Q:
            contentFromDataBase = (
                await (Q()
                    .tables(T.damage)
                    .fields(
                        T.damage.content
                    )
                    .where(T.damage.imgId==id)
                    .selectone())
            )
            return b64encode(contentFromDataBase['content']).decode()

    @classmethod
    async def select_file(cls, id):
            async with database.query() as Q:
                return await (Q()
                    .tables(T.files)
                    .fields(
                        T.files.content,
                        T.files.name,
                        T.files.id
                    )
                    .where(T.files.id==id)
                    .selectone())

    @classmethod
    async def select_file_company(cls, id):
            async with database.query() as Q:
                return await (Q()
                    .tables(T.files_to_company)
                    .fields(
                        T.files_to_company.content,
                        T.files_to_company.name,
                        T.files_to_company.id
                    )
                    .where(T.files_to_company.id==id)
                    .selectone())

    @classmethod
    async def select_file_customer(cls, id):
            async with database.query() as Q:
                return await (Q()
                    .tables(T.files_to_customer)
                    .fields(
                        T.files_to_customer.content,
                        T.files_to_customer.name,
                        T.files_to_customer.id
                    )
                    .where(T.files_to_customer.id==id)
                    .selectone())

    @classmethod
    async def select_file_person(cls, id):
            async with database.query() as Q:
                return await (Q()
                    .tables(T.files_to_person)
                    .fields(
                        T.files_to_person.content,
                        T.files_to_person.name,
                        T.files_to_person.id
                    )
                    .where(T.files_to_person.id==id)
                    .selectone())

    @classmethod
    async def select_file_sub(cls, id):
            async with database.query() as Q:
                return await (Q()
                    .tables(T.files_to_sub)
                    .fields(
                        T.files_to_sub.content,
                        T.files_to_sub.name,
                        T.files_to_sub.id
                    )
                    .where(T.files_to_sub.id==id)
                    .selectone())

    @classmethod
    async def select_file_sperson(cls, id):
            async with database.query() as Q:
                return await (Q()
                    .tables(T.files_to_sperson)
                    .fields(
                        T.files_to_sperson.content,
                        T.files_to_sperson.name,
                        T.files_to_sperson.id
                    )
                    .where(T.files_to_sperson.id==id)
                    .selectone())
    @classmethod
    async def select_split_files(cls, indexses):
            async with database.query() as Q:
                result = []
                for index in indexses:
                    result.append(await (Q(T.files)
                    .fields(T.files.content,
                            T.files.name)
                    .where(T.files.id == index)
                    .selectone()))
                return result

    @classmethod
    async def select_doc(cls, id):
            async with database.query() as Q:
                return await (Q()
                    .tables(T.docs)
                    .fields(
                        T.docs.html
                    )
                    .where(T.docs.id==id)
                    .selectone())

    @classmethod
    async def select_split_doc(cls, indexses):
            async with database.query() as Q:
                result = []
                for index in indexses:
                    result.append(await (Q(T.docs)
                    .fields(T.docs.html,
                            T.docs.name)
                    .where(T.docs.id == index)
                    .selectone()))
                return result

    @classmethod
    async def user_pass(cls, mail):
            async with database.query() as Q:
                return await (Q()
                    .tables(T.user)
                    .fields(
                        T.user.pass_from_mail
                    )
                    .where(T.user.mail==mail)
                    .selectone())
    
    @classmethod            
    async def select_image(cls, id):
            async with database.query() as Q:
                return await (Q()
                    .tables(T.files)
                    .fields(
                        T.files.content
                    )
                    .where(T.files.id==id)
                    .selectone())
    @classmethod
    async def del_doc(cls, id, number):
        async with database.query() as Q:
             await (Q(T.docs)
                .where(T.docs.id == id)
                .delete())
             return await (Q(T.docs)
                    .fields(
                        T.docs.html,
                        T.docs.added,
                        T.docs.name,
                        T.docs.number,
                        T.docs.pages,
                        T.docs.date,
                        T.docs.id
                    )
                    .where(T.docs.number == number)
                    .selectall())


    @classmethod
    async def del_file(cls, id, number):
        async with database.query() as Q:
             await (Q(T.files)
                .where(T.files.id == id)
                .delete())
             return await (Q(T.files)
                    .fields(
                        T.files.name,
                        T.files.html,
                        T.files.number,
                        T.files.id,
                        T.files.pages,
                        T.files.group,
                        T.files.added
                    )
                    .where(T.files.number == number)
                    .selectall())

    @classmethod
    async def delfile(cls, id):
        async with database.query() as Q:
            return await (Q(T.files)
                .where(T.files.id == id)
                .delete())

    @classmethod
    async def delfile_company(cls, id):
        async with database.query() as Q:
            return await (Q(T.files_to_company)
                .where(T.files_to_company.id == id)
                .delete())
    @classmethod
    async def delfile_customer(cls, id):
        async with database.query() as Q:
            return await (Q(T.files_to_customer)
                .where(T.files_to_customer.id == id)
                .delete())
    @classmethod
    async def delfile_person(cls, id):
        async with database.query() as Q:
            return await (Q(T.files_to_person)
                .where(T.files_to_person.id == id)
                .delete())

    @classmethod
    async def delfile_sub(cls, id):
        async with database.query() as Q:
            return await (Q(T.files_to_sub)
                .where(T.files_to_sub.id == id)
                .delete())

    @classmethod
    async def delfile_sperson(cls, id):
        async with database.query() as Q:
            return await (Q(T.files_to_sperson)
                .where(T.files_to_sperson.id == id)
                .delete())



    @classmethod
    async def deldoc(cls, id):
        async with database.query() as Q:
            return await (Q(T.docs)
                .where(T.docs.id == id)
                .delete())

    @classmethod
    async def upload_doc(cls, file, name, number, number_of_pages, group, added, user, resp):
            async with database.query() as Q:
                return await (Q()
                    .tables(T.files)
                    .insert({
                        T.files.content: file,
                        T.files.name: name,
                        T.files.number: number,
                        T.files.pages: number_of_pages,
                        T.files.group: group,
                        T.files.added: added,
                        T.files.resp: resp,
                        T.files.user: user,
                        T.files.html: 'file'
                    }))

    @classmethod
    async def upload_to_company(cls, file, name, number, number_of_pages, group, added, user, resp):
            async with database.query() as Q:
                return await (Q()
                    .tables(T.files_to_company)
                    .insert({
                        T.files_to_company.content: file,
                        T.files_to_company.name: name,
                        T.files_to_company.number: number,
                        T.files_to_company.pages: number_of_pages,
                        T.files_to_company.group: group,
                        T.files_to_company.added: added,
                        T.files_to_company.resp: resp,
                        T.files_to_company.user: user,
                        T.files_to_company.html: 'company'
                    }))

    @classmethod
    async def upload_to_customer(cls, file, name, number, number_of_pages, group, added, user, resp):
            async with database.query() as Q:
                return await (Q()
                    .tables(T.files_to_customer)
                    .insert({
                        T.files_to_customer.content: file,
                        T.files_to_customer.name: name,
                        T.files_to_customer.number: number,
                        T.files_to_customer.pages: number_of_pages,
                        T.files_to_customer.group: group,
                        T.files_to_customer.added: added,
                        T.files_to_customer.resp: resp,
                        T.files_to_customer.user: user,
                        T.files_to_customer.html: 'company'
                    }))

    @classmethod
    async def upload_to_contact(cls, file, name, number, number_of_pages, group, added, user, resp):
            async with database.query() as Q:
                return await (Q()
                    .tables(T.files_to_person)
                    .insert({
                        T.files_to_person.content: file,
                        T.files_to_person.name: name,
                        T.files_to_person.number: number,
                        T.files_to_person.pages: number_of_pages,
                        T.files_to_person.group: group,
                        T.files_to_person.added: added,
                        T.files_to_person.resp: resp,
                        T.files_to_person.user: user,
                        T.files_to_person.html: 'person'
                    }))

    @classmethod
    async def upload_to_sub(cls, file, name, number, number_of_pages, group, added, user, resp):
            async with database.query() as Q:
                return await (Q()
                    .tables(T.files_to_sub)
                    .insert({
                        T.files_to_sub.content: file,
                        T.files_to_sub.name: name,
                        T.files_to_sub.number: number,
                        T.files_to_sub.pages: number_of_pages,
                        T.files_to_sub.group: group,
                        T.files_to_sub.added: added,
                        T.files_to_sub.resp: resp,
                        T.files_to_sub.user: user,
                        T.files_to_sub.html: 'sub'
                    }))

    @classmethod
    async def upload_to_sperson(cls, file, name, number, number_of_pages, group, added, user, resp):
            async with database.query() as Q:
                return await (Q()
                    .tables(T.files_to_sperson)
                    .insert({
                        T.files_to_sperson.content: file,
                        T.files_to_sperson.name: name,
                        T.files_to_sperson.number: number,
                        T.files_to_sperson.pages: number_of_pages,
                        T.files_to_sperson.group: group,
                        T.files_to_sperson.added: added,
                        T.files_to_sperson.resp: resp,
                        T.files_to_sperson.user: user,
                        T.files_to_sperson.html: 'sperson'
                    }))

    @classmethod
    async def upload_img_for_damages(cls, file, filename, group_id, added):

            # file = base64.b64encode(file)

            async with database.query() as Q:
                for val in group_id.split(','):
                    await (Q()
                        .tables(T.images_for_group_damages)
                        .insert({
                            T.images_for_group_damages.group_id: val,
                            T.images_for_group_damages.file_name: filename,
                            T.images_for_group_damages.date: added,
                            T.images_for_group_damages.content: file
                        }))

    @classmethod
    async def add_task(cls, name, id, start, end):
            async with database.query() as Q:
                if  (start=='null') | (end=='null'):
                    return await (Q()
                            .tables(T.task_for_damages)
                            .insert({
                                T.task_for_damages.name: name,
                                T.task_for_damages.table_id: id,
                                T.task_for_damages.data_time_start: datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            }))
                else:
                    return await (Q()
                            .tables(T.task_for_damages)
                            .insert({
                                T.task_for_damages.name: name,
                                T.task_for_damages.table_id: id,
                                T.task_for_damages.data_time_start: start,
                                T.task_for_damages.data_time_end: end
                            }))

    @classmethod
    async def update_task(cls, data, fild, id):
            if data=='null':
                data = None
            async with database.query() as Q:
                    return await (Q()
                            .tables(T.task_for_damages)
                            .where(T.task_for_damages.id == id)
                            .update({
                                T.task_for_damages[fild]: data
                            }))

    @classmethod
    async def task_time_damage(cls, id):
            async with database.query() as Q:
                return await (Q()
                    .tables(T.task_for_damages)
                    .where(T.task_for_damages.id == id)
                    .update({
                        T.task_for_damages.data_time_end: datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }))


    @classmethod
    async def send_replace_image(cls, data, id):
            async with database.query() as Q:
                return await (Q()
                    .tables(T.damage)
                    .where(T.damage.imgId == id)
                    .update({
                        T.damage.content: data
                    }))

class Customer:
    @classmethod
    async def detectSub(cls, name):
        print(name)
        async with database.query() as Q:
            return await (Q()
                .tables(T.customer)
                .fields(
                    # T.customer.id,
                    T.customer.name,
                    T.customer.street,
                    # T.customer.old,
                    # T.customer.status,
                    # T.customer.data,
                    T.customer.zip,
                    T.customer.city
                    # T.customer.tax,
                    # T.customer.web,
                    # T.customer.bic,
                    # T.customer.iban,
                    # T.customer.other
                ).where(T.customer.name == name)
                .selectone())

    @classmethod
    async def select_customers(cls):
        async with database.query() as Q:
            return await (Q(T.customer)
                .fields(
                    T.customer.name,
                    T.customer.old,
                    T.customer.status,
                    T.customer.data,
                    T.customer.zip,
                    T.customer.city,
                    T.customer.street,
                    T.customer.tax,
                    T.customer.web,
                    T.customer.bic,
                    T.customer.iban,
                    T.customer.other,
                    T.customer.id
                )
                .where(T.customer.type == None)
                .selectall())


    @classmethod
    async def select_customers_sub(cls):
        async with database.query() as Q:
            return await (Q(T.customer)
                .fields(
                    T.customer.name,
                    T.customer.old,
                    T.customer.status,
                    T.customer.data,
                    T.customer.zip,
                    T.customer.city,
                    T.customer.street,
                    T.customer.tax,
                    T.customer.web,
                    T.customer.bic,
                    T.customer.iban,
                    T.customer.other,
                    T.customer.id
                )
                .where(T.customer.type == 'sub')
                .selectall())

    @classmethod
    async def customer_old(cls, id, event):
        async with database.query() as Q:
                  return await (Q()
                .tables(T.customer)
                .where(T.customer.id == id)
                .update({
                    T.customer.old: event
                }))

    @classmethod
    async def add_customer_list(cls, date):
        async with database.query() as Q:
              await (Q()
                  .tables(T.customer)
                  .insert({
                  T.customer.data: date,
                  T.customer.name: 'New-Firm',
                  T.customer.old: 0
                  }))
              return await (Q(T.customer)
                .fields(
                    T.customer.name,
                    T.customer.old,
                    T.customer.status,
                    T.customer.data,
                    T.customer.zip,
                    T.customer.city,
                    T.customer.street,
                    T.customer.tax,
                    T.customer.web,
                    T.customer.bic,
                    T.customer.iban,
                    T.customer.other,
                    T.customer.id
                ).selectall())

    @classmethod
    async def add_customer_sub_list(cls, date):
        async with database.query() as Q:
              await (Q()
                  .tables(T.customer)
                  .insert({
                  T.customer.data: date,
                  T.customer.name: 'New-Firm',
                  T.customer.old: 0,
                  T.customer.type: 'sub'
                  }))
              return await (Q(T.customer)
                .fields(
                    T.customer.name,
                    T.customer.old,
                    T.customer.status,
                    T.customer.data,
                    T.customer.zip,
                    T.customer.city,
                    T.customer.street,
                    T.customer.tax,
                    T.customer.web,
                    T.customer.bic,
                    T.customer.iban,
                    T.customer.other,
                    T.customer.id
                ).selectall())

    @classmethod
    async def select_customer(cls, id):
        async with database.query() as Q:
            return await (Q()
                .tables(T.customer)
                .fields(
                    T.customer.id,
                    T.customer.name,
                    T.customer.street,
                    T.customer.old,
                    T.customer.status,
                    T.customer.data,
                    T.customer.zip,
                    T.customer.city,
                    T.customer.tax,
                    T.customer.web,
                    T.customer.bic,
                    T.customer.iban,
                    T.customer.other
                ).where(T.customer.id == id)
                .selectone())

    @classmethod
    async def select_persons(cls, id):
        async with database.query() as Q:
            return await (Q()
                .tables(T.person)
                .fields(
                    T.person.person,
                    T.person.old,
                    T.person.adress,
                    T.person.data,
                    T.person.appeal,
                    T.person.data,
                    T.person.pos,
                    T.person.dep,
                    T.person.other,
                    T.person.names,
                    T.person.customer_group
                ).where(T.person.customer_group == id)
                .selectall())

    @classmethod
    async def update(cls, id, data, fild):
        async with database.query() as Q:
              return await (Q()
                .tables(T.customer)
                .where(T.customer.id == id)
                .update({
                    T.customer[fild]: data
                }))

    @classmethod
    async def select_customer_contact(cls, fild, customer):
        async with database.query() as Q:
            return await (Q()
                .tables(T(fild))
                .fields(
                    T(fild)[fild]
                ).where(T(fild).customer == customer)
                .selectall())

    @classmethod
    async def add_customer_contact(cls, type, val, id):
            async with database.query() as Q:
                return await (Q()
                    .tables(T(type))
                    .insert({
                        T(type)[type]: val,
                        T(type).customer: id
                    }))
    @classmethod
    async def updateContact(cls, id, date, type):
        async with database.query() as Q:
            await (Q()
                    .tables(T(type))
                    .where(T(type).customer == id)
                    .delete())

            for val in date.split(","):
                await (Q()
                    .tables(T(type))
                    .insert({
                        T(type)[type]: val,
                        T(type).customer: id
                    }))

            return ''

    @classmethod
    async def updatePerson(cls, id, data, fild):
        async with database.query() as Q:
              return await (Q()
                .tables(T.person)
                .where(T.person.person == id)
                .update({
                    T.person[fild]: data
                }))

    @classmethod
    async def del_person(cls, id):
        async with database.query() as Q:
            return await (Q()
              .tables(T.person)
              .where(T.person.person == id)
              .delete())

    @classmethod
    async def get_contact_person(cls, id):
        async with database.query() as Q:
            mail = (await (Q()
                        .tables(T.mail)
                        .fields(T.mail.mail)
                        .where(T.mail.person == id)
                        .selectall())
                    )
            phone = (await (Q()
                        .tables(T.phone)
                        .fields(T.phone.phone)
                        .where(T.phone.person == id)
                        .selectall())
                    )
            fax = (await (Q()
                        .tables(T.fax)
                        .fields(T.fax.fax)
                        .where(T.fax.person == id)
                        .selectall())
                    )               
            adress = (await (Q()
                        .tables(T.adress)
                        .fields(T.adress.adress)
                        .where(T.adress.person == id)
                        .selectall())
                    )   

        return ({'mail' : mail, 'phone' : phone, 'fax' : fax, 'adress' : adress})

    @classmethod
    async def edit_contact_person(cls, fild, value, id, type):
        async with database.query() as Q:
            await (Q()
              .tables(T(fild))
              .where(T(fild)[type] == id)
              .delete())

            for v in value.split(","):
                if  v!='':
                    if  fild=='adress':
                        v = v.replace(';', ',')

                    await (Q()
                        .tables(T(fild))
                        .insert({
                        T(fild)[fild]: v,
                        T(fild)[type]: id
                    }))

            return ''

    @classmethod
    async def contact_in_person_remove_row(cls, fild, id, value, type):
        async with database.query() as Q:
            if  fild=='adress':
                        value = value.replace(';', ',')
            await (Q()
              .tables(T(fild))
              .where((T(fild)[type] == id) & (T(fild)[fild] == value))
              .delete())

class Prices:
    @classmethod
    async def select_prices(cls, id):
        async with database.query() as Q:
            return await (Q(T.price)
                .fields(
                    T.price.pos_num,
                    T.price.name,
                    T.price.desc,
                    T.price.unit,
                    T.price.price,
                    T.price.without,
                    T.price.percent,
                    T.price.id
                )
                .where(T.price.item_id == id)
                .selectall())

    @classmethod
    async def price_menu(cls):
        async with database.query() as Q:
            return await (Q(T.price_menu)
                .fields(
                    T.price_menu.id,
                    T.price_menu.name,
                    T.price_menu.parrent
                ).selectall())

    @classmethod
    async def change_parrent_menu(cls, drag1, drag2):
        async with database.query() as Q:
            return await (Q(T.price_menu)
                .tables(T.price_menu)
                .where(T.price_menu.id == drag1)
                .update({
                    T.price_menu.parrent: drag2
                }))

    @classmethod
    async def add_price_menu(cls, parent_id):
        async with database.query() as Q:
            return await (Q(T.price_menu)
                .tables(T.price_menu)
                .insert({
                    T.price_menu.name: 'New Part',
                    T.price_menu.parrent: parent_id
                })) 

   
    @classmethod
    async def remove_price_menu(cls, remove_id):
        async with database.query() as Q:
            return await (Q(T.price_menu)
              .tables(T.price_menu)
              .where(T.price_menu.id == remove_id)
              .delete())

    @classmethod
    async def update_name_price_menu(cls, name, id):
        async with database.query() as Q:
            return await (Q(T.price_menu)
                .tables(T.price_menu)
                .where(T.price_menu.id == id)
                .update({
                    T.price_menu.name: name
                }))

    @classmethod
    async def add_price(cls, id):
        async with database.query() as Q:
            return await (Q(T.price_menu)
                .tables(T.price)
                .insert({
                    T.price.item_id: id
                }))

    @classmethod
    async def remove_price(cls, id):
        async with database.query() as Q:
            return await (Q(T.price_menu)
                .tables(T.price)
                .where(T.price.id == id)
                .delete())

    @classmethod
    async def update_price(cls, data, fild, id):
        async with database.query() as Q:
            return await (Q(T.price)
                .tables(T.price)
                .where(T.price.id == id)
                .update({
                    T.price[fild]: data
                }))

    @classmethod
    async def cp_mv_to_price(cls, ids, new, op):
        async with database.query() as Q:
            if  op=='move':
                for v in ids.split(","):
                    await (Q()
                        .tables(T.price)
                        .where(T.price.id == v)
                        .update({
                              T.price.item_id: new
                        }))
            if  op=='copy':
                for v in ids.split(","):
                  item = (await (Q()
                        .tables(T.price)
                        .fields(
                            T.price.pos_num,
                            T.price.name,
                            T.price.desc,
                            T.price.unit,
                            T.price.price,
                            T.price.without,
                            T.price.percent
                        )
                        .where(T.price.id == v)
                        .selectone()))
                  await (Q(T.price_menu)
                    .tables(T.price)
                    .insert({
                            T.price.pos_num: item['pos_num'],
                            T.price.name: item['name'],
                            T.price.desc: item['desc'],
                            T.price.unit: item['unit'],
                            T.price.price: item['price'],
                            T.price.without: item['without'],
                            T.price.percent: item['percent'],
                            T.price.item_id: new
                    }))

            return ''

    @classmethod
    async def send_price(cls, ids, names):
        #print(type, ids, names, item_id)
        # arr=[]
        # for v in ids.split(","):
        #    arr=arr+','+v
 
        async with database.query() as Q:
            items = (await (Q()
                            .tables(T.price)
                            .fields(
                                T.price.pos_num,
                                T.price.name,
                                T.price.desc,
                                T.price.unit,
                                T.price.price,
                                T.price.without,
                                T.price.percent
                            )
                            .where(T.price.id.in_(ids.split(",")))
                            .selectall()))

            for item in items:
                newPrice = item['price'].replace(',','.')
                try:
                    newPrice = float(newPrice)
                except:
                    newPrice = 0

                if item['unit']=='%':
                    item['unit'] = 'f-proc'
                    item['count'] = '1'
                else:
                    item['count'] = '0'

                if item['desc']==None:
                    item['desc'] = ' '
                if item['desc']=='':
                    item['desc'] = ''

                for v in names.split(","):
                        await (Q(T.rows_for_table)
                            .tables(T.rows_for_table)
                            .insert({
                                    T.rows_for_table.position_number: item['pos_num'],
                                    T.rows_for_table.description_head: item['name'],
                                    T.rows_for_table.description_from_price: '',
                                    T.rows_for_table.unit: item['unit'],
                                    T.rows_for_table.price: newPrice,
                                    T.rows_for_table.without: item['without'],
                                    T.rows_for_table.discount: item['percent'],
                                    T.rows_for_table.table_id: v,
                                    T.rows_for_table.status: 'yes',
                                    # T.rows_for_table.alttax: ,
                                    T.rows_for_table.description_work: item['desc'],
                                    T.rows_for_table.count: item['count'],
                                    T.rows_for_table.done: ''
                            }))
        return ''





class Damage:
    @classmethod
    async def send_damage(cls, ids, names):
        #print(type, ids, names, item_id)
        # arr=[]
        # for v in ids.split(","):
        #    arr=arr+','+v
        
        async with database.query() as Q:
            items = (await (Q()
                            .tables(T.files)
                            .fields(
                                T.files.id,
                                T.files.name,
                                T.files.content
                            )
                            .where(T.files.id.in_(ids.split(",")))
                            .selectall()))
            for item in items:
                for v in names.split(","):
                    table_name = (await (Q(T.tables)
                        .fields(
                        T.tables.name
                        )
                        .where(T.tables.id == v)
                        .selectone())
                    )
                    await (Q(T.damage)
                        .tables(T.damage)
                        .insert({
                            T.damage.table_id: v,
                            T.damage.imgId: item['id'],
                            T.damage.name: table_name['name'],
                            T.damage.content: item['content'],
                            T.damage.desc: '',
                            T.damage.rotate: ''
                        }))
        return ''

    @classmethod
    async def delImageFromPart(cls, id):
        async with database.query() as Q:
                await (Q(T.damage)
                    .where(T.damage.table_id == id)
                    .delete())
        return ''

    @classmethod
    async def updateDamage(cls, newDate, fild, id):
        async with database.query() as Q:
                 await (Q()
                     .tables(T.damage)
                     .where(T.damage.id == id)
                     .update({
                         T.damage[fild]: newDate
                     }))
        return ''

    @classmethod
    async def del_row_from_damage(cls, id):
        async with database.query() as Q:
            return await (Q(T.damage)
                    .where(T.damage.id == id)
                    .delete())


class Devices:
    @classmethod
    async def addmeasrow(cls, id):
        async with database.query() as Q:
            fdate = (await (Q(T.rows_for_devices)
                .fields(
                    T.rows_for_devices.fworker,
                    T.rows_for_devices.fdate,
                    T.rows_for_devices.fmReading
                    )
                .where(T.rows_for_devices.id == id)
                .selectone())
            )

            await (Q(T.measurement)
                .tables(T.measurement)
                .insert({
                    T.measurement.date: fdate['fdate'],
                    T.measurement.mReading: fdate['fmReading'],
                    T.measurement.worker: fdate['fworker'],
                    T.measurement.rows_for_devices: id
                }))

            await (Q()
                .tables(T.rows_for_devices)
                .where(T.rows_for_devices.id == id)
                .update({
                    T.rows_for_devices.fworker:'',
                    T.rows_for_devices.fdate: '',
                    T.rows_for_devices.fmReading: ''
            }))

            return ''

    @classmethod
    async def addMeasureProtocolrow(cls, id):
        async with database.query() as Q:
            return await (Q(T.measure_protocol)
                .tables(T.measure_protocol)
                .insert({
                    T.measure_protocol.sminsurface: 0,
                    T.measure_protocol.smaxsurface: 0,
                    T.measure_protocol.smindepth: 0,
                    T.measure_protocol.smaxdepth: 0,
                    T.measure_protocol.fminsurface: 0,
                    T.measure_protocol.fmaxsurface: 0,
                    T.measure_protocol.fmindepth: 0,
                    T.measure_protocol.fmaxdepth: 0,
                    T.measure_protocol.table_id: id
                }))

    # @classmethod
    # async def delmeasrow(cls, id):
    #     async with database.query() as Q:
    #         return await (Q(T.measurement)
    #             .tables(T.measurement)
    #             .where(T.measurement.id == id)
    #             .delete())

    @classmethod
    async def measureProtocolDel(cls, id):
        async with database.query() as Q:
            return await (Q(T.measure_protocol)
                .tables(T.measure_protocol)
                .where(T.measure_protocol.id == id)
                .delete())

    @classmethod
    async def select_devices(cls, id):
        async with database.query() as Q:
            return await (Q(T.devices)
                .fields(
                    T.devices.pos_num,
                    T.devices.designation,
                    T.devices.comment,
                    T.devices.kilowatt,
                    T.devices.time,
                    T.devices.manufacturer,
                    T.devices.serial,
                    T.devices.order,
                    T.devices.check_date,
                    T.devices.next_check_date,
                    T.devices.id
                )
                .where(T.devices.item_id == id)
                .selectall())

    @classmethod
    async def devices_menu(cls):
        async with database.query() as Q:
            return await (Q(T.devices_menu)
                .fields(
                    T.devices_menu.id,
                    T.devices_menu.name,
                    T.devices_menu.parrent
                ).selectall())

    @classmethod
    async def change_parrent_menu_devices(cls, drag1, drag2):
        async with database.query() as Q:
            return await (Q(T.price_menu)
                .tables(T.price_menu)
                .where(T.price_menu.id == drag1)
                .update({
                    T.price_menu.parrent: drag2
                }))

    @classmethod
    async def add_devices_menu(cls, parent_id):
        async with database.query() as Q:
            return await (Q(T.devices_menu)
                .tables(T.devices_menu)
                .insert({
                    T.devices_menu.name: 'New Part',
                    T.devices_menu.parrent: parent_id
                })) 

   
    @classmethod
    async def remove_devices_menu(cls, remove_id):
        async with database.query() as Q:
            return await (Q(T.devices_menu)
              .tables(T.devices_menu)
              .where(T.devices_menu.id == remove_id)
              .delete())

    @classmethod
    async def update_name_devices_menu(cls, name, id):
        async with database.query() as Q:
            return await (Q(T.devices_menu)
                .tables(T.devices_menu)
                .where(T.devices_menu.id == id)
                .update({
                    T.devices_menu.name: name
                }))

    @classmethod
    async def add_devices(cls, id):
        async with database.query() as Q:
            return await (Q(T.devices_menu)
                .tables(T.devices)
                .insert({
                    T.devices.item_id: id
                }))

    @classmethod
    async def remove_devices(cls, id):
        async with database.query() as Q:
            return await (Q(T.devices_menu)
                .tables(T.devices)
                .where(T.devices.id == id)
                .delete())

    @classmethod
    async def update_devices(cls, data, fild, id):
        async with database.query() as Q:
            return await (Q(T.devices)
                .tables(T.devices)
                .where(T.devices.id == id)
                .update({
                    T.devices[fild]: data
                }))

    @classmethod
    async def cp_mv_to_devices(cls, ids, new, op):
        async with database.query() as Q:
            if  op=='move':
                for v in ids.split(","):
                    await (Q()
                        .tables(T.devices)
                        .where(T.devices.id == v)
                        .update({
                              T.devices.item_id: new
                        }))
            if  op=='copy':
                for v in ids.split(","):
                  item = (await (Q()
                        .tables(T.devices)
                        .fields(
                            T.devices.pos_num,
                            T.devices.name,
                            T.devices.desc,
                            T.devices.unit,
                            T.devices.price,
                            T.devices.without,
                            T.devices.percent
                        )
                        .where(T.devices.id == v)
                        .selectone()))
                  await (Q(T.devices_menu)
                    .tables(T.devices)
                    .insert({
                            T.devices.pos_num: item['pos_num'],
                            T.devices.name: item['name'],
                            T.devices.desc: item['desc'],
                            T.devices.unit: item['unit'],
                            T.devices.price: item['price'],
                            T.devices.without: item['without'],
                            T.devices.percent: item['percent'],
                            T.devices.item_id: new
                    }))

            return ''

    @classmethod
    async def send_devices(cls, ids, names):
        #print(type, ids, names, item_id)
        # arr=[]
        # for v in ids.split(","):
        #    arr=arr+','+v
 
        async with database.query() as Q:
            items = (await (Q()
                            .tables(T.devices)
                            .fields(
                                T.devices.pos_num,
                                T.devices.designation,
                                T.devices.comment,
                                T.devices.kilowatt,
                                T.devices.time,
                                T.devices.manufacturer,
                                T.devices.serial,
                                T.devices.order,
                                T.devices.check_date,
                                T.devices.next_check_date
                            )
                            .where(T.devices.id.in_(ids.split(",")))
                            .selectall()))

            for item in items:
                newPrice = item['kilowatt'].replace(',','.')
                try:
                    newPrice = float(newPrice)
                except:
                    newPrice = 0

                if item['comment']==None:
                    item['comment'] = ' '

                for v in names.split(","):
                        devName = (await (Q()
                        .tables(T.tables)
                        .fields(
                            T.tables.name
                        )
                        .where(T.tables.id == v)
                        .selectone()))

                        await (Q()
                        .tables(T.tables)
                        .where(T.tables.id == v)
                        .update({
                              T.tables.device: devName['name']
                        }))

                        await (Q(T.rows_for_devices)
                            .tables(T.rows_for_devices)
                            .insert({
                                    T.rows_for_devices.table_id: v,
                                    T.rows_for_devices.pos_num: item['pos_num'],
                                    T.rows_for_devices.designation: item['designation'],
                                    T.rows_for_devices.kilowatt: item['kilowatt'],
                                    T.rows_for_devices.comment: item['comment'],
                                    T.rows_for_devices.time: item['time'],
                                    T.rows_for_devices.manufacturer: item['manufacturer'],
                                    T.rows_for_devices.serial: item['serial'],
                                    T.rows_for_devices.order: item['order'],
                                    T.rows_for_devices.check_date: item['check_date'],
                                    T.rows_for_devices.next_check_date: item['next_check_date'],
                                    T.rows_for_devices.sdate: datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                                    T.rows_for_devices.fdate: (datetime.datetime.now() + datetime.timedelta(days = 7)).strftime("%Y-%m-%d %H:%M"),
                                    T.rows_for_devices.smReading: '0.00',
                                    T.rows_for_devices.fmReading: '0.00',
                                    T.rows_for_devices.location: 'Undefined'
                            }))
        return ''

    @classmethod
    async def updateDeviceList(cls, newDate, fild, id):
        async with database.query() as Q:
                 await (Q()
                     .tables(T.rows_for_devices)
                     .where(T.rows_for_devices.id == id)
                     .update({
                         T.rows_for_devices[fild]: newDate
                     }))
        return ''

    @classmethod
    async def updateDeviceIntern(cls, newDate, fild, id):
        async with database.query() as Q:
                 await (Q()
                     .tables(T.measurement)
                     .where(T.measurement.id == id)
                     .update({
                         T.measurement[fild]: newDate
                     }))
        return ''

    @classmethod
    async def updateMeasureProtocol(cls, newDate, fild, id):
        async with database.query() as Q:
                 await (Q()
                     .tables(T.measure_protocol)
                     .where(T.measure_protocol.id == id)
                     .update({
                         T.measure_protocol[fild]: newDate
                     }))
        return ''

    @classmethod
    async def del_row_from_devices(cls, id):
        async with database.query() as Q:
            return await (Q(T.rows_for_devices)
                    .where(T.rows_for_devices.id == id)
                    .delete())


class Personals:
    @classmethod
    async def get_templates_for_factory(cls):
        async with database.query() as Q:
            result = []
            templates = (
                await (Q(T.template_for_factory)
                    .fields(
                        T.template_for_factory.id,
                        T.template_for_factory.name
                    ).selectall())
            )
            for tmp in templates:
                filds = (
                    await (Q(T.filds_for_tamplate_factory)
                        .fields(
                            T.filds_for_tamplate_factory.type,
                            T.filds_for_tamplate_factory.name,
                            T.filds_for_tamplate_factory.id
                        )
                        .where(T.filds_for_tamplate_factory.template_id == tmp['id'])
                        .selectall())
                )
                result.append({'name' : tmp['name'], 'id' : tmp['id'], 'filds':filds})
            return result

    @classmethod
    async def add_row_in_template_for_factory(cls, id):
        async with database.query() as Q:
            await (Q(T.filds_for_tamplate_factory)
            .tables(T.filds_for_tamplate_factory)
            .insert({
                    T.filds_for_tamplate_factory.name: 'New Prop',
                    T.filds_for_tamplate_factory.template_id: id
            }))
        return ''

    @classmethod
    async def remove_row_in_template_for_factory(cls, id):
        async with database.query() as Q:
            await (Q()
                .tables(T.filds_for_tamplate_factory)
                .where(T.filds_for_tamplate_factory.id == id)
                .delete())
        return ''

    @classmethod
    async def update_row_in_template_for_factory(cls, id, value, type):
        # print(id, value, type)
        async with database.query() as Q:
            await (Q()
                .tables(T.filds_for_tamplate_factory)
                .where(T.filds_for_tamplate_factory.id == id)
                .update({
                    T.filds_for_tamplate_factory[type]: value
                }))
        return ''

    @classmethod
    async def add_Item_in_template_for_factory(cls):
        async with database.query() as Q:
            await (Q(T.template_for_factory)
            .tables(T.template_for_factory)
            .insert({
                    T.template_for_factory.name: 'New Item'
            }))
        return ''

    @classmethod
    async def remove_Item_in_template_for_factory(cls, id):
        async with database.query() as Q:
            await (Q()
                .tables(T.template_for_factory)
                .where(T.template_for_factory.id == id)
                .delete())
            await (Q()
                .tables(T.filds_for_tamplate_factory)
                .where(T.filds_for_tamplate_factory.template_id == id)
                .delete())
        return ''

    @classmethod
    async def update_Item_in_template_for_factory(cls, id, value):
        async with database.query() as Q:
            await (Q()
                .tables(T.template_for_factory)
                .where(T.template_for_factory.id == id)
                .update({
                    T.template_for_factory.name: value
                }))

        return ''

        
  
    @classmethod
    async def select_personals(cls, id, type):
        async with database.query() as Q:
            result = []
            if type=='part':
                personals = (await (Q()
                        .tables(T.personal)
                        .fields(
                            T.personal.id,
                            T.personal.files,
                            T.personal.salary,
                            T.personal.end_work,
                            T.personal.start_work,
                            T.personal.position,
                            T.personal.name,
                            T.personal.short_name,
                            T.personal.item_id
                        )
                        .where(T.personal.item_id == id)
                        .selectall())
                )

                for person in personals:

                    mail = (await (Q()
                                .tables(T.mail)
                                .fields(T.mail.mail)
                                .where(T.mail.personal == person['id'])
                                .selectall())
                            )
                    phone = (await (Q()
                                .tables(T.phone)
                                .fields(T.phone.phone)
                                .where(T.phone.personal == person['id'])
                                .selectall())
                            )
                    fax = (await (Q()
                                .tables(T.fax)
                                .fields(T.fax.fax)
                                .where(T.fax.personal == person['id'])
                                .selectall())
                            )               
                    adress = (await (Q()
                                .tables(T.adress)
                                .fields(T.adress.adress)
                                .where(T.adress.personal == person['id'])
                                .selectall())
                            )
                    result.append({'id' : person['id'], 'files' : person['files'], 'salary' : person['salary'],
                                'end_work' : person['end_work'], 'start_work' : person['start_work'],
                                'position' : person['position'], 'name' : person['name'],
                                'short_name' : person['short_name'], 'item_id' : person['item_id'],
                                'mail' : mail, 'phone' : phone, 'fax' : fax, 'adress' : adress})
        
                return result

            if type=='factory':
                factories = (await (Q()
                    .tables(T.factories)
                    .fields(
                        T.factories.id,
                        T.factories.files,
                        T.factories.name,
                        T.factories.option,
                        T.factories.template_id,
                        T.factories.item_id
                    )
                    .where(T.factories.item_id == id)
                        .selectall())
                )

                for factory in factories:
                    content = (await (Q()
                        .tables(T.content_for_factory)
                        .fields(T.content_for_factory.content)
                        .where(T.content_for_factory.factory_id == factory['id'])
                        .selectall())
                       
                    )
                    result.append({
                        'id' : factory['id'],
                        'files' : factory['files'],
                        'name' : factory['name'],
                        'option' : factory['option'],
                        'template_id' : factory['template_id'],
                        'item_id' : factory['item_id'],
                        'content': content
                        })
                #     mail = (await (Q()
                #                 .tables(T.mail)
                #                 .fields(T.mail.mail)
                #                 .where(T.mail.factory == factory['id'])
                #                 .selectall())
                #             )
                #     phone = (await (Q()
                #                 .tables(T.phone)
                #                 .fields(T.phone.phone)
                #                 .where(T.phone.factory == factory['id'])
                #                 .selectall())
                #             )
                #     fax = (await (Q()
                #                 .tables(T.fax)
                #                 .fields(T.fax.fax)
                #                 .where(T.fax.factory == factory['id'])
                #                 .selectall())
                #             )               
                #     adress = (await (Q()
                #                 .tables(T.adress)
                #                 .fields(T.adress.adress)
                #                 .where(T.adress.factory == factory['id'])
                #                 .selectall())
                #             )
                #     result.append({'id' : factory['id'], 'files' : factory['files'], 'salary' : factory['salary'],
                #                 'end_work' : factory['end_work'], 'start_work' : factory['start_work'],
                #                 'position' : factory['position'], 'name' : factory['name'],
                #                 'short_name' : factory['short_name'], 'item_id' : factory['item_id'],
                #                 'mail' : mail, 'phone' : phone, 'fax' : fax, 'adress' : factory})
                # print(result)
                return result

    @classmethod
    async def add_block(cls, id, l):
        async with database.query() as Q:
            for x in range(int(l)):
                 await (Q(T.content_for_factory)
                    .tables(T.content_for_factory)
                    .insert({
                        T.content_for_factory.content: '',
                        T.content_for_factory.factory_id: id
                    }))

        return ''

    @classmethod
    async def remove_block(cls, count, id, detail):
        async with database.query() as Q:
            content = (await (Q()
                    .tables(T.content_for_factory)
                    .fields(
                        T.content_for_factory.id
                    )
                    .where(T.content_for_factory.factory_id == detail)
                    .selectall())
                )
            group = -1
            for index, item in enumerate(content):
                if (index%(int(count)))==0:
                    group +=1
                if (group==int(id)):
                        await (Q()
                         .tables(T.content_for_factory)
                         .where(T.content_for_factory.id == item['id'])
                         .delete())

        return '' 

    @classmethod
    async def update_block(cls, val, count, inc, index, detail):
        async with database.query() as Q:
            content = (await (Q()
                    .tables(T.content_for_factory)
                    .fields(
                        T.content_for_factory.id
                    )
                    .where(T.content_for_factory.factory_id == detail)
                    .selectall())
                )
            group = -1
            inRow = 0
            for ind, item in enumerate(content):
                if (ind%(int(count)))==0:
                    group +=1
                if (group==int(inc)):
                    inRow +=1
                    if inRow==(int(index)+1):
                        await (Q()
                             .tables(T.content_for_factory)
                             .where(T.content_for_factory.id == item['id'])
                             .update({
                                 T.content_for_factory.content: val
                             }))
        return '' 


    @classmethod
    async def personal_menu(cls):
        async with database.query() as Q:
            result = await (Q(T.personal_menu)
                .fields(
                    T.personal_menu.id,
                    T.personal_menu.name,
                    T.personal_menu.parrent,
                    T.personal_menu.type
                ).selectall())
            # print (result)
            return result

    @classmethod
    async def change_parrent_menu_personal(cls, drag1, drag2):
        async with database.query() as Q:
            return await (Q(T.personal_menu)
                .tables(T.personal_menu)
                .where(T.personal_menu.id == drag1)
                .update({
                    T.personal_menu.parrent: drag2
                }))

    @classmethod
    async def add_personal_menu(cls, parent_id, type):
        async with database.query() as Q:
            return await (Q(T.personal_menu)
                .tables(T.personal_menu)
                .insert({
                    T.personal_menu.name: 'New '+type,
                    T.personal_menu.type: type,
                    T.personal_menu.parrent: parent_id
                })) 

    @classmethod
    async def remove_personal_menu(cls, remove_id):
        async with database.query() as Q:
            return await (Q(T.personal_menu)
              .tables(T.personal_menu)
              .where(T.personal_menu.id == remove_id)
              .delete())

    @classmethod
    async def update_name_personal_menu(cls, name, id):
        async with database.query() as Q:
            return await (Q(T.personal_menu)
                .tables(T.personal_menu)
                .where(T.personal_menu.id == id)
                .update({
                    T.personal_menu.name: name
                }))

    @classmethod
    async def add_personal(cls, id, type, option, option_id):
        async with database.query() as Q:
            if type=='part':
                type = 'personal'
                name='Name'
                return await (Q(T(type))
                .tables(T(type))
                .insert({
                    T(type).item_id: id,
                    T(type).name: 'New ' + name
                }))

            if type=='factory':
                type = 'factories'
                name='Prop'
                return await (Q(T(type))
                .tables(T(type))
                .insert({
                    T(type).item_id: id,
                    T(type).name: option,
                    T(type).option: option_id
                }))

    @classmethod
    async def remove_personal(cls, id, type):
        async with database.query() as Q:
            if type=='part':
                type = 'personal'
            if type=='factory':
                type = 'factories'
            return await (Q(T(type))
                .tables(T(type))
                .where(T(type).id == id)
                .delete())

    @classmethod
    async def update_personal(cls, data, fild, id, type):
        async with database.query() as Q:
            # print(data)
            if type=='part':
                type = 'personal'
            if type=='factory':
                type = 'factories'
            return await (Q(T(type))
                .tables(T(type))
                .where(T(type).id == id)
                .update({
                    T(type)[fild]: data
                }))

    @classmethod
    async def cp_mv_to_personal(cls, ids, new, op, type):
        async with database.query() as Q:
            if type=='part':
                type = 'personal'
            if type=='factory':
                type = 'factories'

            if  op=='move':
                for v in ids.split(","):
                    await (Q()
                        .tables(T(type))
                        .where(T(type).id == v)
                        .update({
                              T(type).item_id: new
                        }))
            if  op=='copy':
                for v in ids.split(","):
                    if type=='personal':
                        item = (await (Q()
                            .tables(T.personal)
                            .fields(
                                T.personal.id,
                                T.personal.files,
                                T.personal.salary,
                                T.personal.end_work,
                                T.personal.start_work,
                                T.personal.name,
                                T.personal.short_name,
                                T.personal.item_id
                            )
                            .where(T.personal.id == v)
                            .selectone())
                        )

                    if type=='factories':
                        item = (await (Q()
                            .tables(T.factories)
                            .fields(
                                T.factories.id,
                                T.factories.files,
                                T.factories.name,
                                T.factories.option,
                                T.factories.template_id,
                                T.factories.item_id
                            )
                            .where(T.factories.id == v)
                            .selectone())
                        )
                    
                    if type=='personal':
                        await (Q(T.personal)
                        .tables(T.personal)
                        .insert({
                            T.personal.faxs: item['faxs'],
                            T.personal.salary: item['salary'],
                            T.personal.end_work: item['end_work'],
                            T.personal.start_work: item['start_work'],
                            T.personal.position: item['position'],
                            T.personal.name: item['name'],
                            T.personal.short_name: item['short_name'],
                            T.personal.item_id: new
                        }))

                    if type=='factories':
                        await (Q(T.factories)
                        .tables(T.factories)
                        .insert({
                            T.factories.files: item['files'],
                            T.factories.name: item['name'],
                            T.factories.option: item['option'],
                            T.factories.template_id: item['template_id'],
                            T.factories.item_id: new
                        }))

            return ''

    # @classmethod
    # async def send_price(cls, ids, names):
    #     #print(type, ids, names, item_id)
    #     # arr=[]
    #     # for v in ids.split(","):
    #     #    arr=arr+','+v
 
    #     async with database.query() as Q:
    #         items = (await (Q()
    #                         .tables(T.price)
    #                         .fields(
    #                             T.price.pos_num,
    #                             T.price.name,
    #                             T.price.desc,
    #                             T.price.unit,
    #                             T.price.price,
    #                             T.price.without,
    #                             T.price.percent
    #                         )
    #                         .where(T.price.id.in_(ids.split(",")))
    #                         .selectall()))

    #         for v in names.split(","):
    #             for item in items:
    #                 await (Q(T.rows_for_table)
    #                     .tables(T.rows_for_table)
    #                     .insert({
    #                             T.rows_for_table.position_number: item['pos_num'],
    #                             T.rows_for_table.description_head: item['name'],
    #                             T.rows_for_table.description_from_price: item['desc'],
    #                             T.rows_for_table.unit: item['unit'],
    #                             T.rows_for_table.price: item['price'],
    #                             T.rows_for_table.without: item['without'],
    #                             T.rows_for_table.discount: item['percent'],
    #                             T.rows_for_table.table_id: v,
    #                             T.rows_for_table.status: 'yes',
    #                             T.rows_for_table.alttax: 'false',
    #                             T.rows_for_table.description_work: ''
    #                     }))
    #     return ''        
class Balance:

    @classmethod
    async def select_balances(cls):
        async with database.query() as Q:
            result = ( await (Q()
                .tables(T.items & T.type_for_table & T.project & T.customer & T.person)
                .on((T.items.type == T.type_for_table.id) & (T.items.project_id == T.project.id) & (T.project.customer_id == T.customer.id)  & (T.project.person_id == T.person.person))
                .fields(
                    T.items.id,
                    T.items.number,
                    T.items.date,
                    T.items.other,
                    T.items.place,
                    T.items.insurance_number,
                    T.items.work,
                    T.items.status_set,
                    T.type_for_table.type,
                    T.items.tax,
                    T.items.taxDub,
                    T.items.taxP,
                    T.items.taxPDub,
                    T.items.disc,
                    T.items.discP,
                    T.items.butDiscPerc,
                    T.items.addtaxColapse,
                    T.items.comment,
                    T.items.project_id,
                    T.project.street1,
                    T.person.names
                )
                .where((T.type_for_table.type == 'Invoices')|(T.type_for_table.type == 'Sub Invoices'))
                .selectall()))



            result1 = ( await (Q()
                .tables(T.items )
          
                .fields(
                    T.items.id,
                    T.items.number
                )
                .selectall()))

            balance = ( await (Q()
                .tables(T.rows_for_balance)
                .fields(
                    T.rows_for_balance.id,
                    T.rows_for_balance.type,
                    T.rows_for_balance.value,
                    T.rows_for_balance.date,
                    T.rows_for_balance.invoice_id
                )
                .selectall()))


            for item in result:
                id =  item['number'].split(' ')
                if len(id)==2:
                    for number in result1:
                        if int(id[1]) == number['id']: 
                            item['contract_number']=number['number']

            for item in result:
                ops=[]
                for bal in balance:
                    # print(item['id'], bal['invoice_id'])
                    if str(item['id'])==bal['invoice_id']: 
                        ops.append({'type':bal['type'], 'value':bal['value'], 'date':bal['date'], 'id':bal['id']})
                item['op'] = ops

                if item['tax']==None:
                    item['tax']='0,0'
                if item['taxDub']==None:
                    item['taxDub']='0,0'
                if item['taxP']==None:
                    item['taxP']='0,0'
                if item['taxPDub']==None:
                    item['taxPDub']='0,0'
                if item['disc']==None:
                    item['disc']='0,0'
                if item['discP']==None:
                    item['discP']='0,0'
                if item['butDiscPerc']==None:
                    item['butDiscPerc']='%'
                if item['addtaxColapse']==None:
                    item['addtaxColapse']='false'

                tax=(item['tax'].replace(',', '.'))
                taxDub=(item['taxDub'].replace(',', '.'))
                taxP=(item['taxP'].replace(',', '.'))
                taxPDub=(item['taxPDub'].replace(',', '.'))
                disc=(item['disc'].replace(',', '.'))
                discP=(item['discP'].replace(',', '.'))
                butDiscPerc=item['butDiscPerc']
                addtaxColapse=item['addtaxColapse']
                # print('start', item['number'], item['insurance_number'])
                netto = 0
                addt = 0
                addt2 = 0
                tables =(await (Q()
                        .tables(T.tables)
                        .fields(
                            T.tables.id,
                            T.tables.name,
                            T.tables.obj,
                            T.tables.selected
                        )
                        .where(T.tables.item_id == item['id'])
                        .selectall()))
                add = 0
                for subIndex, val in enumerate(tables):
                    rows =(await (Q()
                                .tables(T.rows_for_table)
                                .fields(
                                    T.rows_for_table.count,
                                    T.rows_for_table.price,
                                    T.rows_for_table.summa,
                                    T.rows_for_table.status,
                                    T.rows_for_table.alttax,
                                    T.rows_for_table.without,
                                    T.rows_for_table.unit,
                                    T.rows_for_table.done
                                )
                                .where(T.rows_for_table.table_id == val['id'])
                                .selectall()))

                    for row in rows:
                        if row['count']==None:
                            row['count'] = '0'
                        if row['price']==None:
                            row['price'] = '0'

                        if row['unit']=='%':
                            row['price']=0
                            summax = 0

                            for obj in val['obj'].split(','):
                                selected = ['']
                                if not '|' in val["selected"]:
                                    selected = json.loads('{"'+val["selected"].replace(':', '":"')+'"}')
                                    if ('temp' + str(subIndex + 1)) in selected[obj]:

                                        for val in selected[obj].split(','):

                                            val = val.split('temp')
                                            val[1]=int(val[1])-1

                                            countx = 0
                                            pricex = 0
                                            
                                            countx = rows[val[1]]['count'] 
                                            pricex = rows[val[1]]['price']

                                            summax += float(countx) * float(pricex)
                               
                            row['price']=persent_from_summa = (float(summax / 100) * float(row['count']))
                            row['count']=1
                        if row['status']=='yes':
                            

                            netto += (float(row['count'])*float(row['price']))
                            if row['without']=='true':
                                add += (float(row['count'])*float(row['price']) / 100) * float(discP)

                            # print(row['alttax'])
                            if row['alttax']!='true':
                                addt += (float(row['count'])*float(row['price']))
                            else:
                                addt2 += (float(row['count'])*float(row['price']))

                if butDiscPerc=='%':
                    # print(netto, add)
                    # netto = netto + add
                    item['netto']=str(netto-(netto/100*float(discP)))
                    # print(item['netto'])
                    item['netto']=float(item['netto'])+add
                    # print(item['netto'], add)
                    addt = addt-(addt/100)*float(discP)
                    addt2 = addt2-(addt2/100)*float(discP)
                
                else:

                    item['netto']=str(netto-float(discP))
                    addt = addt-(addt/100)*float(discP)*100/netto
                    addt2 = addt2-(addt2/100)*float(discP)*100/netto
                
                #addt = addt2 = 0
                # item['netto']=0

                #tmpTax = (addt * (float(taxP) / 100))
                #tmpTax2= (addt2 * (float(taxPDub) / 100))
                
                item['brutto']=str(float(item['netto'])+(addt * (float(taxP) / 100))+(addt2 * (float(taxPDub) / 100)))
                # print((netto-(netto/100*20)), (netto-(netto/100*20))+((netto/100)*19))
                # print(item['brutto'])

# ???????????????????????????????????????????????????????????????????????????
            # for item in sub_result:
            #     id =  item['number'].split(' ')
            #     if len(id)==2:
            #         for number in sub_result1:
            #             if int(id[1]) == number['id']: 
            #                 item['contract_number']=number['number']

            # for item in sub_result:
            #     ops=[]
            #     for bal in balance:
            #         # print(item['id'], bal['invoice_id'])
            #         if ('s'+str(item['id']))==bal['invoice_id']:
            #             ops.append({'type':bal['type'], 'value':bal['value'], 'date':bal['date'], 'id':bal['id']})
            #     item['op'] = ops

            #     if item['tax']==None:
            #         item['tax']='0,0'
            #     if item['taxDub']==None:
            #         item['taxDub']='0,0'
            #     if item['taxP']==None:
            #         item['taxP']='0,0'
            #     if item['taxPDub']==None:
            #         item['taxPDub']='0,0'
            #     if item['disc']==None:
            #         item['disc']='0,0'
            #     if item['discP']==None:
            #         item['discP']='0,0'
            #     if item['butDiscPerc']==None:
            #         item['butDiscPerc']='%'
            #     if item['addtaxColapse']==None:
            #         item['addtaxColapse']='false'

            #     tax=(item['tax'].replace(',', '.'))
            #     taxDub=(item['taxDub'].replace(',', '.'))
            #     taxP=(item['taxP'].replace(',', '.'))
            #     taxPDub=(item['taxPDub'].replace(',', '.'))
            #     disc=(item['disc'].replace(',', '.'))
            #     discP=(item['discP'].replace(',', '.'))
            #     butDiscPerc=item['butDiscPerc']
            #     addtaxColapse=item['addtaxColapse']
            #     # print('start', item['number'], item['insurance_number'])
            #     netto = 0
            #     addt = 0
            #     addt2 = 0
            #     tables =(await (Q()
            #             .tables(T.sub_tables)
            #             .fields(
            #                 T.sub_tables.id,
            #                 T.sub_tables.name
            #             )
            #             .where(T.sub_tables.item_id == item['id'])
            #             .selectall()))
            #     add = 0
            #     for val in tables:

            #         rows =(await (Q()
            #                     .tables(T.sub_rows_for_table)
            #                     .fields(
                                    
            #                         T.sub_rows_for_table.count,
            #                         T.sub_rows_for_table.price,
            #                         T.sub_rows_for_table.summa,
            #                         T.sub_rows_for_table.status,
            #                         T.sub_rows_for_table.alttax,
            #                         T.sub_rows_for_table.without,
            #                         T.sub_rows_for_table.unit
            #                     )
            #                     .where(T.sub_rows_for_table.table_id == val['id'])
            #                     .selectall()))

            #         for row in rows:
            #             if row['count']==None:
            #                 row['count'] = '0'
            #             if row['price']==None:
            #                 row['price'] = '0'

            #             if row['unit']=='%':
            #                     row['count']=1
            #             if row['status']=='yes':
                            

            #                 netto += (float(row['count'])*float(row['price']))
            #                 if row['without']=='true':
            #                     add += (float(row['count'])*float(row['price']) / 100) * float(discP)

            #                 # print(row['alttax'])
            #                 if row['alttax']!='true':
            #                     addt += (float(row['count'])*float(row['price']))
            #                 else:
            #                     addt2 += (float(row['count'])*float(row['price']))
                            


           

                # if butDiscPerc=='%':
                #     # print(netto, add)
                #     # netto = netto + add
                #     item['netto']=str(netto-(netto/100*float(discP)))
                #     # print(item['netto'])
                #     item['netto']=float(item['netto'])+add
                #     # print(item['netto'], add)
                #     addt = addt-(addt/100)*float(discP)
                #     addt2 = addt2-(addt2/100)*float(discP)
                
                # else:

                #     item['netto']=str(netto-float(discP))
                #     addt = addt-(addt/100)*float(discP)*100/netto
                #     addt2 = addt2-(addt2/100)*float(discP)*100/netto
                
                #addt = addt2 = 0
                # item['netto']=0

                #tmpTax = (addt * (float(taxP) / 100))
                #tmpTax2= (addt2 * (float(taxPDub) / 100))
    
                # item['brutto']=str(float(item['netto'])+(addt * (float(taxP) / 100))+(addt2 * (float(taxPDub) / 100)))
                # # print((netto-(netto/100*20)), (netto-(netto/100*20))+((netto/100)*19))
                # # print('end')
                # item['id'] = ('s' + str(item['id']))
                # item['brutto'] = str(-(float(item['brutto'])))
                # item['netto'] = str(-(float(item['netto'])))

                # if 'sub_result' in locals():
                #     result = result + sub_result
            # print(result)
            return result

    @classmethod
    async def add_payment(cls, id, value, type):
        async with database.query() as Q:
           return await (Q(T.rows_for_balance)
                    .tables(T.rows_for_balance)
                    .insert({
                            T.rows_for_balance.type: type,
                            T.rows_for_balance.value: value,
                            T.rows_for_balance.date: datetime.datetime.now().strftime("%Y-%m-%d"),
                            T.rows_for_balance.invoice_id: id 
                    }))

    @classmethod
    async def remove_payment(cls, id):
        async with database.query() as Q:
           return await (Q(T.rows_for_balance)
                .tables(T.rows_for_balance)
                .where(T.rows_for_balance.id == id)
                .delete())

    @classmethod
    async def update_payment(cls, id, value, fild):
        async with database.query() as Q:
           return await (Q(T.rows_for_balance)
                    .tables(T.rows_for_balance)
                    .where(T.rows_for_balance.id == id)
                    .update({
                            T.rows_for_balance[fild]: value
                    }))
    @classmethod
    async def update_comment(cls, id, value):
        async with database.query() as Q:
           return await (Q(T.items)
                    .tables(T.items)
                    .where(T.items.id == id)
                    .update({
                            T.items.comment: value
                    }))
    @classmethod
    async def update_comment_sub(cls, id, value):
        async with database.query() as Q:
           return await (Q(T.sub_items)
                    .tables(T.sub_items)
                    .where(T.sub_items.id == id)
                    .update({
                            T.sub_items.comment: value
                    }))
           