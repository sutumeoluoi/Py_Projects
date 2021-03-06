'''
Process Tran2 records from csv file
'''

import csv
import pandas as pd
import numpy as np
from pathlib import Path
from io import StringIO, SEEK_SET
import pyodbc 
import matplotlib.pyplot as plt

# from MyUtils import printnl

'''
expand pandas output to full width
Use all 3 to show expand to full width without any truncate or '...'
Use ONLY 2nd expand width, but will truncate some middle cols showing '...'
'''
#===============================================================================
pd.set_option('display.max_columns', None)  #put 'display.' is optional
pd.set_option('expand_frame_repr', False)
pd.set_option('max_colwidth', -1)  
#===============================================================================


# def Reset_Csv_Pos(a_csv_r, f):
#     f.seek(0)

#===============================================================================
# io_string = '''
#     1, 3, 5.63    , 89    
#     25, 3, 6.22, 9
#     '''
# trans = str.maketrans('', '', ' \t')
# strip_io_string = io_string.translate(trans)
# # print(io_string, strip_io_string)
# #  iostring_obj = StringIO(strip_io_string) #StringIO obj using in place of file obj
# ##or
# ##############################
# iostring_obj = StringIO()
# print(iostring_obj.write(strip_io_string))  #25 chars written
# print(iostring_obj.tell())  #showing 25 which is the end.
# # iostring_obj.seek(0, SEEK_SET)  #after write(), pos cursor at the end of StringIO obj, need seek() to the top
# ##############################
# csv_r = csv.reader(iostring_obj, skipinitialspace=True)
# for item in csv_r:
#     print(csv_r.line_num, item)
# iostring_obj.close()    #need to close as if file obj
#===============================================================================

#===============================================================================
# csv_filename = Path('C:\Documents and Settings\hal\Desktop\Py CSV\Tran2-20190304-check-5.csv')
#    
# with csv_filename.open(encoding='utf-8') as f:
#     csv_r = csv.reader(f)
#     for item in csv_r:
#         print(csv_r.line_num, item)
#===============================================================================

# df = pd.read_csv('C:\Documents and Settings\hal\Desktop\Py CSV\Tran2-20190304-check-5.csv')
# df = pd.read_csv(r'C:\Documents and Settings\hal\Desktop\Py CSV\nm-0101-0311.csv', encoding='utf-16le')

# printnl(df.index, df.columns)
# printnl(df['invoice'])    #return Series (no column label/name)
# printnl(df[['vendor_code', 'invoice', 'division']].loc[:3]) ##return DataFrame of 3 columns
# printnl(df[['vendor_code']].loc[:3]) #return DataFrame of 1 column
# print(df.loc[[0, 1, 2, 3], ['vendor_code', 'invoice', 'receive_date', 'account', 'division']])
# print(df.loc[[0, 1, 2, 3], 'vendor_code'])
# print(df.loc[:3, 'vendor_code':'division'])
# print(df.loc[3, 'vendor_code':'division'])
# print(df.to_string())
# invoice = df['invoice']
# print(invoice)

sql_str = '''
    select 
        recordtype,
        reason,
        recid_notused,
        division,
        invoicedate,
        invoicenumber,
        invoiceline,
        plu,
        qty, 
        price,
        itmcost,
        newcost,
        discount
    from invbillinfo_mp
    where
        invoicedate >= '2019-03-01'
        and reason = 56
        and recordtype in (7, 207)
        and plu = 497837
    '''
       
conn = pyodbc.connect('DRIVER={Pervasive ODBC Client Interface};SERVERNAME=MASTER101;DBQ=MMV8;UID=;PWD=')
df = pd.read_sql(sql_str, conn, )
# df = df.set_index('InvoiceNumber', 'Division')
# df = df.set_index('RecID_NotUsed')
mpdck_sql = '''
    select * from nmp_daily_check_rn
    where
        invoicedate = '2019-04-02'
        and division = 28
        and mpid = 481243
        and invoicenumber = 18080607
        and recordtype = 7
    '''
df_mpdck = pd.read_sql(mpdck_sql, conn, )    
print(df)
print(df_mpdck)

 

# x = np.linspace(0, 10, 100, endpoint=True)
# plt.plot(np.exp(x), 'r+')
# df.sort(['currentdate', 'div', 'deptnum'])
# ds = df.loc[(df['deptnum']==1) & (df['div']==3),'totalsell']
# # print(ds)
# ds9 = df.loc[(df['deptnum']==1) & (df['div']==9),'totalsell']
# ds12 = df.loc[(df['deptnum']==1) & (df['div']==9),'totalsell']
# plt.plot(ds, 'g-', ds9, 'b-', ds12, 'r-')

# ts = pd.Series(np.random.randn(1000),
#                index=pd.date_range('1/1/2000', periods=1000))
# pd.DataFrame(np.random.randn(1000, 4),
#              index=ts.index, columns=list('ABCD'))
# df = df.cumsum()
# df.plot()
# plt.show()

'''https://stackoverflow.com/questions/55382525/how-to-find-the-minimum-value-of-a-list-element-which-is-based-on-unique-value-o'''
#===============================================================================
# t = '''
# SKU;price;availability;Title;Supplier
# SUV500;21,50 €;1;27-03-2019 14:46;supplier1
# MZ-76E;5,50 €;1;27-03-2019 14:46;supplier1
# SUV500;49,95 €;0;27-03-2019 14:46;supplier2
# MZ-76E;71,25 €;0;27-03-2019 14:46;supplier2
# SUV500;32,60 €;1;27-03-2019 14:46;supplier3
# '''
# # print(t)
# stio_min = StringIO(t)
# df = pd.read_csv(stio_min, delimiter=';', encoding='utf-8')
# df['f_price'] = df['price'].str.extract(r'([+-]?\d+\,\d+)', expand=False).str.replace(',', '.').astype(float)
# idx_min = df.groupby('SKU', as_index=False)['f_price'].idxmin().tolist()
# df_final = df.loc[idx_min].drop('f_price', 1)
# print(df)
# t_out = df_final.to_csv(sep=';', index=False)
# print(t_out)
#===============================================================================