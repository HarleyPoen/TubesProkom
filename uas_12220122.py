import pandas as pd
import streamlit as st
import json

## WEB ##
st.title("Aplikasi Plot Data Minyak Mentah")
sidebar = ['Home','Jumlah Produksi Minyak','Negara dengan jumlah prduksi terbesar pada tahun T','Top N negara','Informasi']
list = st.sidebar.selectbox(label='Main Menu', options=sidebar)

## IMPORT ##
# CSV #
with open('produksi_minyak_mentah.csv') as dataminyak_csv:
    df = pd.read_csv(dataminyak_csv)

# JSON #  
KodeNegara = open ("kode_negara_lengkap.json")
buka_json = json.load(KodeNegara)
negara = []
for dc in buka_json:
    name = dc.get('name')
    alpha = dc.get('alpha-3')
    ccode = dc.get('country-code')
    region = dc.get('region')
    subregion = dc.get('sub-region')
    appenddata = [name, alpha, ccode, region, subregion]
    negara.append(appenddata)

if list == 'Home':
    st.header('Nama : Harley Poen')
    st.subheader('NIM : 12220122')
## Code Dan Grafik ##
# 1A #
elif list=='Jumlah Produksi Minyak':
    negara_nama = []
    for i in negara:
        negara_nama.append(i[0])
    nomorA = st.selectbox('Pilih negara: ',negara_nama,key = '<1>')
    for i in negara:
        if i[0]==nomorA:
            negara_alpha = i[1]
            break
    dfA = df.loc[df["kode_negara"] == negara_alpha]
    dfA = dfA[["tahun", "produksi"]] 
    #Grafik A
    st.line_chart(dfA.rename(columns={'tahun':'index'}).set_index('index'))

# 1B #
elif list == 'Negara dengan jumlah prduksi terbesar pada tahun T':
    tahun = df['tahun'].unique().tolist()
    nomorB = st.selectbox('Tahun ke berapa: ', tahun,0,key = '<2>') 
    tahun2 =df.loc[df['tahun']==nomorB] 
    banyak_negara = st.slider ('Berapa negara? ',min_value=1, max_value=136) 
    dfB = tahun2.nlargest(banyak_negara, 'produksi')
    dfB = dfB[['kode_negara', 'produksi']]
    #Grafik B
    st.bar_chart(dfB.rename(columns={'kode_negara':'Kode Negara'}).set_index('Kode Negara'))
    
# 1C #
elif list == 'Top N negara':
    top = st.slider ('Berapa negara terbesar? ',min_value=1, max_value=136) 
    grup_negara = df.groupby('kode_negara').sum().reset_index().reset_index(drop=True)
    terbesar_sort = grup_negara.nlargest(top, 'produksi')
    dfC = terbesar_sort[['kode_negara', 'produksi']]
    #Grafik C
    st.bar_chart(dfC.rename(columns={'kode_negara':'Kode Negara'}).set_index('Kode Negara'))

# 1D #
# A #
# Keseluruhan tahun #
# terbesar #
elif list == 'Informasi':
    st.subheader('Jumlah Produksi Terbesar Keseluruhan Tahun')
    df_grup = df.groupby('kode_negara').sum().reset_index().reset_index(drop=True)
    terbesar_sort2 = df_grup.nlargest(1, 'produksi')
    for i in negara:
        if i[1] == terbesar_sort2['kode_negara'].values[0]:
            terbesar_nama = i[0]
            terbesar_ccode = i[2]
            terbesar_region = i[3]
            terbesar_subregion = i[4]
            st.write(terbesar_nama)
            st.write(terbesar_ccode)
            st.write(terbesar_region)
            st.write(terbesar_subregion)
            
    # terkecil #
    st.subheader('Jumlah Produksi Terkecil Keseluruhan Tahun')
    dfD = df_grup[df_grup['produksi'] != 0]
    terkecil_sort2 = dfD.nsmallest(1, 'produksi')
    for i in negara:
        if i[1] == terkecil_sort2['kode_negara'].values[0]:
            terbesar_nama = i[0]
            terbesar_ccode = i[2]
            terbesar_region = i[3]
            terbesar_subregion = i[4]
            st.write(terbesar_nama)
            st.write(terbesar_ccode)
            st.write(terbesar_region)
            st.write(terbesar_subregion)

    # sama dengan nol #
    st.subheader('Jumlah Produksi Sama Dengan Nol Keseluruhan Tahun')
    nol1 = df_grup[df_grup['produksi'] == 0]
    hasil_nol1 = pd.DataFrame(columns = ['nama negara', 'kode negara', 'region', 'sub region'])
    for j in range(len(nol1)):
        for i in negara:
            if i[1] == nol1['kode_negara'].values[j]:
                temp = {'nama negara': i[0], 'kode negara': i[2], 'region': i[3], 'sub region': i[4]}
                hasil_nol1 = hasil_nol1.append(temp, ignore_index=True)
    st.table(hasil_nol1)

    # B #
    # Per Tahun #
    # terbesar #
    st.subheader('Jumlah Produksi Terbesar Per Tahun')
    tahun = df['tahun'].unique().tolist()
    nomorC = st.selectbox('Tahun ke berapa: ', tahun,0,key = '<3>') 
    tahun3 =df.loc[df['tahun']==nomorC] 
    terbesar_tahun3 = tahun3.nlargest(1, 'produksi')
    for i in negara:
        if i[1] == terbesar_tahun3['kode_negara'].values[0]:
            terbesar_tahun3_nama = i[0]
            terbesar_tahun3_ccode = i[2]
            terbesar_tahun3_region = i[3]
            terbesar_tahun3_subregion = i[4]
            st.write(terbesar_tahun3_nama)
            st.write(terbesar_tahun3_ccode)
            st.write(terbesar_tahun3_region)
            st.write(terbesar_tahun3_subregion)

    # terkecil #
    st.subheader('Jumlah Produksi Terkecil Per Tahun')
    tahun = df['tahun'].unique().tolist()
    nomorD = st.selectbox('Tahun ke berapa: ', tahun,0,key = '<4>') 
    tahun4 =df.loc[df['tahun']==nomorD] 
    tahun4 = tahun4[tahun4['produksi'] != 0]
    terkecil_tahun4 = tahun4.nsmallest(1, 'produksi')
    for i in negara:
        if i[1] == terkecil_tahun4['kode_negara'].values[0]:
            terbesar_tahun4_nama = i[0]
            terbesar_tahun4_ccode = i[2]
            terbesar_tahun4_region = i[3]
            terbesar_tahun4_subregion = i[4]
            st.write(terbesar_tahun4_nama)
            st.write(terbesar_tahun4_ccode)
            st.write(terbesar_tahun4_region)
            st.write(terbesar_tahun4_subregion)

    # sama dengan nol #
    st.subheader('Jumlah Produksi Sama Dengan Nol Per Tahun')
    nomorE = st.selectbox('Tahun ke berapa: ', tahun,0,key = '<5>') 
    tahun5 =df.loc[df['tahun']==nomorE] 
    nol2 = tahun5[tahun5['produksi'] == 0]
    hasil_nol2 = pd.DataFrame(columns = ['nama negara', 'kode negara', 'region', 'sub region'])
    for j in range(len(nol2)):
        for i in negara:
            if i[1] == nol2['kode_negara'].values[j]:
                temp = {'nama negara': i[0], 'kode negara': i[2], 'region': i[3], 'sub region': i[4]}
                hasil_nol2 = hasil_nol2.append(temp, ignore_index=True)
    st.table(hasil_nol2)