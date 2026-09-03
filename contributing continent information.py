##Note: This code is used for extracting the information of contributing continents of a publication. Please save the data download from WOSCC in txt format as “data.txt”

#start
import pandas as pd
import numpy as np
import re
import io


def clean_word(x):
    while x[0]==' ':
        x=x[1:]
    while x[-1]==' ':
        x=x[:-1]
    while x[-1]=='.':
        x=x[:-1]
    return x

def authorlist(data):
    AU_list = []
    for i in data.index:
        if data.loc[i,'total_author_num']>0:
            au_list = pd.DataFrame()
            au_list['au_S'] = data.loc[i, 'AU'].split('; ')
            au_list['au_F'] = data.loc[i, 'AF'].split('; ')
            au_list['doc_id'] = data.loc[i, 'doc_id']
            au_list['au_seq'] = list(range(1, len(au_list) + 1))
            AU_list.append(au_list)
    AU_list_pd=pd.concat(AU_list).reset_index(drop=True)
    AU_list_pd['au_S']=AU_list_pd['au_S'].apply(lambda x:clean_word(x))
    AU_list_pd['au_F'] = AU_list_pd['au_F'].apply(lambda x: clean_word(x))
    return AU_list_pd

def addlist(data):
    add = []
    for i in data.index:
        print('i=' + str(i))
        if data.loc[i, 'len_add'] > 0:
            if '[' in data.loc[i, 'C1']:
                add1 = re.split(r';\s*(?=\[)', data.loc[i, 'C1'])
                li = []
                for t in range(len(add1)):
                    if '[' in add1[t]:
                        au_F = re.findall(r'\[(.*?)\]', add1[t])[0].split('; ')
                    else:
                        au_F = ['unknown']
                    au_F_add = re.sub(r'\[.*?\]', '', add1[t]).strip().split('; ')
                    au_add1 = pd.merge(pd.DataFrame(data=au_F, columns=['au_F']),
                                       pd.DataFrame(data=au_F_add, columns=['add']), how='cross')
                    au_add1['add_seq'] = t + 1
                    au_add1['doc_id'] = data.loc[i, 'doc_id']
                    li.append(au_add1)
                au_add = pd.concat(li).reset_index(drop=True)
                add.append(au_add)
            else:
                au_add1 = pd.DataFrame()
                au_add1['add'] = data.loc[i, 'C1'].split('; ')
                au_add1['add_seq'] = list(range(1, len(au_add1) + 1))
                au_add1['au_F'] = 'unknown'
                au_add1['doc_id'] = data.loc[i, 'doc_id']
                add.append(au_add1)
    add_pd = pd.concat(add).reset_index(drop=True)
    add_pd['au_F'] = add_pd['au_F'].apply(lambda x: clean_word(x))
    add_pd['add'] = add_pd['add'].apply(lambda x: clean_word(x))
    return add_pd

def RPadd_list(data):
    RP_add = []
    for i in data.index:
        if data.loc[i, 'len_RP_add']>0:
            if ')' in data.loc[i, 'RP']:
                add1 = data.loc[i, 'RP'].split(';')
                li = []
                t = 1
                for k in add1:
                    if ')' in k:
                        li.append([k.split('(')[0], k.split('), ')[1],t])
                        t=t+1
                    else:
                        li.append([k, np.nan,np.nan])
                cor_author1 = pd.DataFrame(data=li, columns=['au_S', 'RP_add','RP_add_seq'])
                cor_author1 = cor_author1.fillna(method='backfill')
                cor_author1['doc_id']=data.loc[i,'doc_id']
                RP_add.append(cor_author1)
            else:
                cor_author1=pd.DataFrame()
                cor_author1['RP_add']=data.loc[i, 'RP'].split(';')
                cor_author1['au_S']='unknown'
                cor_author1['RP_add_seq']=list(range(1, len(cor_author1) + 1))
                cor_author1['doc_id'] = data.loc[i, 'doc_id']
                RP_add.append(cor_author1)
    RP_add_pd=pd.concat(RP_add).reset_index(drop=True)
    RP_add_pd['au_S']=RP_add_pd['au_S'].apply(lambda x:clean_word(x))
    RP_add_pd['RP_add'] = RP_add_pd['RP_add'].apply(lambda x: clean_word(x))
    return RP_add_pd

def country_info(x):
    if type(x)==str:
        a=x.split(',')[-1]
        if 'usa' in a.lower():
            return 'usa'
        elif a[-1] in [str(i) for i in list(range(10))]:
            return 'usa'
        elif len(a)==2:
            return 'usa'
        elif 'china' in a.lower():
            return 'china'
        else:
            if a.lower()[0]==' ':
                return a.lower()[1:]
            else:
                return a.lower()
    else:
        return np.nan


country_to_region='''
country,region
angola,Africa
burundi,Africa
benin,Africa
burkina faso,Africa
botswana,Africa
cent afr republ,Africa
cote ivoire,Africa
cameroon,Africa
dem rep congo,Africa
rep congo,Africa
comoros,Africa
cape verde,Africa
djibouti,Africa
algeria,Africa
egypt,Africa
eritrea,Africa
ethiopia,Africa
gabon,Africa
ghana,Africa
guinea,Africa
gambia,Africa
guinea bissau,Africa
equat guinea,Africa
kenya,Africa
liberia,Africa
libya,Africa
lesotho,Africa
morocco,Africa
madagascar,Africa
mali,Africa
mozambique,Africa
mauritania,Africa
mauritius,Africa
malawi,Africa
namibia,Africa
niger,Africa
nigeria,Africa
rwanda,Africa
sudan,Africa
senegal,Africa
st helena,Africa
sierra leone,Africa
somalia,Africa
south sudan,Africa
sao tome & prin,Africa
eswatini,Africa
seychelles,Africa
chad,Africa
togo,Africa
tunisia,Africa
tanzania,Africa
uganda,Africa
south africa,Africa
zambia,Africa
zimbabwe,Africa
anguilla,North America
argentina,South America
antigua & barbu,North America
bahamas,North America
st barthelemy,North America
belize,North America
bermuda,North America
bolivia,South America
brazil,South America
barbados,North America
canada,North America
chile,South America
colombia,South America
costa rica,North America
cuba,North America
curacao,North America
cayman islands,North America
dominica,North America
dominican rep,North America
ecuador,South America
falkland island,South America
grenada,North America
greenland,North America
guatemala,North America
french guiana,South America
guyana,South America
honduras,North America
haiti,North America
jamaica,North America
st kitts & nevi,North America
st lucia,North America
mexico,North America
nicaragua,North America
panama,North America
peru,South America
paraguay,South America
el salvador,North America
suriname,South America
sint maarten,North America
turks & caicos,North America
trinidad tobago,North America
uruguay,South America
usa,North America
st vincent,North America
venezuela,South America
british virgin isl,North America
afghanistan,Asia
u arab emirates,Asia
armenia,Asia
azerbaijan,Asia
bangladesh,Asia
bahrain,Asia
brunei,Asia
bhutan,Asia
china,Asia
hong kong,Asia
taiwan,Asia
cyprus,Asia
georgia,Asia
indonesia,Asia
india,Asia
iran,Asia
iraq,Asia
israel,Asia
jordan,Asia
japan,Asia
kazakhstan,Asia
kyrgyzstan,Asia
cambodia,Asia
north korea,Asia
kuwait,Asia
laos,Asia
lebanon,Asia
sri lanka,Asia
maldives,Asia
myanmar,Asia
mongolia,Asia
malaysia,Asia
nepal,Asia
oman,Asia
pakistan,Asia
philippines,Asia
south korea,Asia
palestine,Asia
qatar,Asia
saudi arabia,Asia
singapore,Asia
syria,Asia
thailand,Asia
tajikistan,Asia
timor-leste,Asia
turkey,Asia
turkiye,Asia
uzbekistan,Asia
vietnam,Asia
yemen,Asia
albania,Europe
andorra,Europe
austria,Europe
belgium,Europe
bulgaria,Europe
bosnia & herceg,Europe
belarus,Europe
switzerland,Europe
czech republic,Europe
germany,Europe
denmark,Europe
spain,Europe
estonia,Europe
finland,Europe
france,Europe
faroe islands,Europe
england,Europe
north ireland,Europe
scotland,Europe
wales,Europe
gibraltar,Europe
greece,Europe
croatia,Europe
hungary,Europe
ireland,Europe
iceland,Europe
italy,Europe
liechtenstein,Europe
lithuania,Europe
luxembourg,Europe
latvia,Europe
monaco,Europe
moldova,Europe
macedonia,Europe
north macedonia,Europe
malta,Europe
montenegro,Europe
netherlands,Europe
norway,Europe
poland,Europe
portugal,Europe
kosovo,Europe
romania,Europe
russia,Europe
serbia,Europe
slovakia,Europe
slovenia,Europe
sweden,Europe
ukraine,Europe
australia,Oceania
cook islands,Oceania
fiji,Oceania
micronesia,Oceania
kiribati,Oceania
marshall island,Oceania
new caledonia,Oceania
niue,Oceania
new zealand,Oceania
palau,Oceania
papua n guinea,Oceania
solomon islands,Oceania
tonga,Oceania
tuvalu,Oceania
vanuatu,Oceania
samoa,Oceania'''

country_code=pd.read_csv(io.StringIO(country_to_region),sep=',')

del country_to_region

#read data
out=pd.read_table('data.txt')





out['doc_id']=list(range(1,len(out)+1))
out['total_author_num']=out['AU'].apply(lambda x:x.count('; ')+1 if type(x)==str else 0)
out['len_add']=out['C1'].apply(lambda x:len(x) if type(x)==str else 0)
out['len_RP_add']=out['RP'].apply(lambda x:len(x) if type(x)==str else 0)

AU_list=authorlist(out)  #author list
ADD_list=addlist(out)   #address list of all authors
RP_ADD_list=RPadd_list(out)   #address list of corresponding authors


#all contributing continents
full_add1=pd.concat([ADD_list[['add','doc_id']],RP_ADD_list[['RP_add','doc_id']].rename(columns={'RP_add':'add'})])
full_add1=full_add1.drop_duplicates()

full_add1=pd.merge(full_add1,out[['doc_id','UT']],on='doc_id',how='outer')
full_add1['country']=full_add1['add'].apply(lambda x:country_info(x))
full_add2=pd.merge(full_add1[['UT','country']],country_code,on='country',how='left')
full_add=full_add2.groupby(['UT'])['region'].unique().to_frame().reset_index()


#leading continents
li=[]
#Group1: If the publication has no author information, get the first address
G1=ADD_list.loc[ADD_list['doc_id'].isin(out.loc[out['total_author_num']==0,'doc_id'])]
li.append(G1.loc[G1['add_seq']==1,['add','doc_id']])

#Group2: If the publication has only one author, get all addresses
G2=ADD_list.loc[ADD_list['doc_id'].isin(out.loc[out['total_author_num']==1,'doc_id'])]
li.append(G2[['add','doc_id']])

#Group3: If the publication has many authors and addresses are linked with author names, get the addresses linked to the first author
G3=ADD_list.loc[(ADD_list['doc_id'].isin(out.loc[out['total_author_num']>1,'doc_id'])) & (ADD_list['au_F']!='unknown')]
AU3=AU_list.loc[AU_list['doc_id'].isin(G3['doc_id'])]
G3_merge=pd.merge(G3,AU3,on=['au_F','doc_id'],how='outer')
li.append(G3_merge.loc[G3_merge['au_seq']==1,['add','doc_id']])

#Group4: If the publication has many authors but addresses are not linked with author names, get the first address
G4=ADD_list.loc[(ADD_list['doc_id'].isin(out.loc[out['total_author_num']>1,'doc_id'])) & (ADD_list['au_F']=='unknown')]
li.append(G4.loc[G4['add_seq']==1,['add','doc_id']])

#include all addresses from the corresponding authors
li.append(RP_ADD_list[['RP_add','doc_id']].rename(columns={'RP_add':'add'}))


leading_add1=pd.concat(li).reset_index(drop=True)
leading_add1=leading_add1.drop_duplicates()
leading_add1.sort_values(by='doc_id',ascending=True,inplace=True)
leading_add1.reset_index(drop=True,inplace=True)

leading_add1=pd.merge(leading_add1,out[['doc_id','UT']],on='doc_id',how='outer')
leading_add1['country']=leading_add1['add'].apply(lambda x:country_info(x))
leading_add2=pd.merge(leading_add1[['UT','country']],country_code,on='country',how='left')
leading_add=leading_add2.groupby(['UT'])['region'].unique().to_frame().reset_index()

del G1,G2,G3,G3_merge,AU3,G4,li, ADD_list, AU_list, RP_ADD_list,full_add2,full_add1,leading_add1,leading_add2,country_code,out

full_add.to_excel('all contributing continents.xlsx')
leading_add.to_excel('leading continents.xlsx')
#end


