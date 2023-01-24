# -*- coding: utf-8 -*-
"""
Created on Wed May 25 00:20:08 2022

@author: Owner
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy as sp
from scipy import stats
import os
import glob
from datetime import datetime
from dateutil.relativedelta import relativedelta
import numpy as np
from sklearn.metrics import confusion_matrix
import sklearn.metrics as metrics
#from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
dfont = {'fontname':'David'}


average_volume_per_year = {'bas':17.26, 'gob':14.75,'roi':9.2, 'zin':0.76} #Mm^3/year


# Nash-Sutcliffe-Efficiency is a common metric. It has a value of 1 with a perfect match.
# A value higher than 0 means the model is more efficient than predicting the mean observed.
# A negative value means the model is worse than prediction of the mean, i.e., the model has no skill 

def calc_nse(obs, preds):
    nse = 1 - np.sum((preds - obs) ** 2) / np.sum((obs - np.mean(obs)) ** 2)
    return nse

def magnitude(bfast, mag, hydro):
    
    

    day = list(mag['Y'])
    df_mag = pd.DataFrame(mag)
    magnitude = {}
    c=0
    j=0
    
    #without negative values:
    for  i in bfast['Y']:
        if c in day:
            #mag_points = abs(df_mag['X3'][j])
            mag_points = df_mag['X3'][j]
            if mag_points >0:
                date =bfast['date'][c]
                magnitude[date] = mag_points
                c+=1
                j+=1
            else:
               c+=1 
               j+=1
        else:
                c+=1
    #with negative magnitudes as absoult values:
    '''
    for  i in bfast['Y']:      
        if c in day:
            mag_points = abs(df_mag['X3'][j])
            #mag_points = df_mag['X3'][j]
            date =bfast['date'][c]
            magnitude[date] = mag_points
            c+=1
            j+=1
        else:
                c+=1
    '''
    df_mag = pd.DataFrame(magnitude.items(), columns=['date', 'Magnitude']) 
    df_mag['date'] = pd.to_datetime(df_mag['date'])
    df_mag['year'] =  pd.DatetimeIndex(df_mag['date']).year
    df_mag['month'] =  pd.DatetimeIndex(df_mag['date']).month
    j=0
    for i in df_mag['month']:
        if i == 11 or i == 12:
            change = int( df_mag['year'][j])+1
            df_mag['year'][j]= change
            j+=1
        else:
            j+=1
            
    hydro.columns = [ 'year','Qp','volume','duration']        
    break_list = list(df_mag['year'])
    volume_list = []
    Qp_list =[]
    duration_list =[]
    c=0
    for i in hydro['year']:
        if i in break_list:
            volume_list.append(hydro['volume'][c])
            Qp_list.append(hydro['Qp'][c])
            duration_list.append(hydro['duration'][c])
            c+=1
        else:
            c+=1 
    grouped_df = df_mag.groupby("year")
    maximums = grouped_df.max()
    df_mag = maximums.reset_index()
    df_mag['volume'] = volume_list
    df_mag['Qp'] = Qp_list
    df_mag['duration'] = duration_list

  
    return df_mag


def read_directory(directory, vi):
    os.chdir(directory)
    path = os.getcwd()
    csv_files = sorted(glob.glob(os.path.join(path, "*.csv")))
    
    dict_dfs ={}
    c=1
    for f in csv_files:
        df = pd.read_csv(f)
        dict_dfs[c] = df
        c+=1
    return dict_dfs



vi = ['ndvi','msavi','ndwi' ]
satel = ['mod', 'land','avh']
dict_df={}
c=1
for v in vi:
    for s in satel:
            directory = 'G:/.shortcut-targets-by-id/1sUX8T9nhBa6xjqe6YGVrNhmGMD6VCbho/hydrology/datasets/'+v+'/'+s+'/bfast'
            dict_vi_satel = read_directory(directory, v)
            
            #prepare bas data
            hydro_bas= pd.read_csv("G:/.shortcut-targets-by-id/1sUX8T9nhBa6xjqe6YGVrNhmGMD6VCbho/hydrology/datasets/hydro_data/annual/bastrow_annual3.csv")
            hydro_bas['Qp(cfs/sec)']= hydro_bas['Qp(cfs/sec)']* 0.0283168
            #hydro['volume']=( hydro['volume']* 0.0283168 * 365*3600*24)/1000000
            df_bas = magnitude(dict_vi_satel[1],dict_vi_satel[2],hydro_bas)        
            df_bas['satellite'] = s
            df_bas['location'] = 'Bastrow'
            
            #prepare gob data
            hydro_gob= pd.read_csv("G:/.shortcut-targets-by-id/1sUX8T9nhBa6xjqe6YGVrNhmGMD6VCbho/hydrology/datasets/hydro_data/annual/gobabeb_annual.csv")
            df_gob = magnitude(dict_vi_satel[3],dict_vi_satel[4],hydro_gob)
            df_gob['satellite'] = s
            df_gob['location'] = 'Gobabeb'
            
            df_gob = df_gob.set_index('year', drop = False)
            for i in df_gob['year']:
                if i == 2008 or i == 2007 or i == 2010 or i > 2011:
                    df_gob = df_gob.drop(i)
                else:
                    continue
            df_gob = df_gob.reset_index(drop=True)
     
            #prepare roi data
            hydro_roi= pd.read_csv("G:/.shortcut-targets-by-id/1sUX8T9nhBa6xjqe6YGVrNhmGMD6VCbho/hydrology/datasets/hydro_data/annual/rooibank_annual.csv")
            df_roi = magnitude(dict_vi_satel[5],dict_vi_satel[6],hydro_roi)
            df_roi['satellite'] = s
            df_roi['location'] = 'Rooibank'
            
            df_roi = df_roi.set_index('year', drop = False)
            for i in df_roi['year']:
                if i == 2008 or i == 2007 or i == 2010 or i > 2011:
                    df_roi = df_roi.drop(i)
                else:
                    continue
            df_roi = df_roi.reset_index(drop=True)
            
            #prepare zin data
            hydro_zin= pd.read_csv("G:/.shortcut-targets-by-id/1sUX8T9nhBa6xjqe6YGVrNhmGMD6VCbho/hydrology/datasets/hydro_data/annual/zin_annual.csv")
            df_zin = magnitude(dict_vi_satel[7],dict_vi_satel[8],hydro_zin)
            df_zin['satellite'] = s
            df_zin['location'] = 'Zin'
            
            
            df=[df_bas, df_gob , df_roi, df_zin]
            df = pd.concat(df)
            dict_df[c] = df
            c+=1

#####divide LANDSAT & AVHRR to MODIS period and pre MODIS period:
dict_df_pre = {}
df_list = [2,3,5,6,8]
j=1
for i in df_list:
    mask = dict_df[i]['year'] >= 2002
    dict_df_pre[j] = dict_df[i][~mask] 
    dict_df[i] = dict_df[i][mask]
    j+=1
      


'''
#############################################################
#####plot combine satellites data(best results per years)####
#############################################################
colors_mod = {'Bastrow':'darkgreen', 'Gobabeb':'forestgreen', 'Rooibank':'limegreen', 'Zin':'palegreen'}
colors_land = {'Bastrow':'saddlebrown', 'Gobabeb':'chocolate', 'Rooibank':'sandybrown', 'Zin':'peachpuff'}
colors_avh = {'Bastrow':'navy', 'Gobabeb':'royalblue', 'Rooibank':'cornflowerblue', 'Zin':'skyblue'}

avh = dict_df[3]
avh = avh.drop(avh[avh.year >2001].index)

land = dict_df[2]
land = land.drop(land[land.year >2001].index)

mod = dict_df[1]

df_comb=[avh, mod]
df_comb = pd.concat(df_comb)

d= df_comb
x = d["Magnitude"]
y= d["volume"]

slope, intercept, r_value, p_value, std_err = stats.linregress(x,y) 
r2 =  round(r_value**2,3)
y_pred = intercept + slope * x
rmse = mean_squared_error(y_true=y, y_pred=y_pred, squared=False)
fig, ax = plt.subplots( figsize=(6,5))
ax = sns.regplot(x, y ,color="g", scatter_kws={'s':0}).set(title='MODIS (01 - 21) & LANDSAT (85-01) - NDVI ') #plot the regline only
#sns.scatterplot(data=d, x="Magnitude", y="volume",hue="location",  s=100) #plot points in different color
#sns.scatterplot(data=d, x="Magnitude", y="volume",hue="location", style ='satellite', s=100, legend=False) #plot points in different color and shapes
ax = sns.scatterplot(data=d, x="Magnitude", y="volume",hue="location",  s=100,palette=colors_mod,style="satellite", markers={'mod':'o','land': '^' ,'avh':'s'})
ax.set_xlabel('Magnitude', fontsize = 16,**dfont)
ax.set_ylabel('Volume (Mm$^3$/year)', fontsize = 16,**dfont);
#ax.set(xlabel=None)
#ax.set(ylabel=None)

ax.xaxis.set_tick_params(labelsize=12)
ax.yaxis.set_tick_params(labelsize=12)

props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
textstr = '\n'.join((
"R$^2$={:.2f}".format(r2),
"RMSE={:.2f}".format(rmse)
))
ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=12,**dfont,
verticalalignment='top', bbox=props)
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles=handles[1:5], labels=labels[1:5],loc='upper right', fontsize=8)
'''





###########
##ploting##
###########
#dict_df[2].corr(method='spearman') #spearman option gives no linear correlation





colors_mod = {'Bastrow':'darkgreen', 'Gobabeb':'forestgreen', 'Rooibank':'limegreen', 'Zin':'palegreen'}
colors_land = {'Bastrow':'saddlebrown', 'Gobabeb':'chocolate', 'Rooibank':'sandybrown', 'Zin':'peachpuff'}
colors_avh = {'Bastrow':'navy', 'Gobabeb':'royalblue', 'Rooibank':'cornflowerblue', 'Zin':'skyblue'}
char_list= ['volume', 'duration']
df_corr = pd.DataFrame()
df_corr_pre = pd.DataFrame()

for char in char_list:
    fig, ((ax1, ax2, ax3), (ax4, ax5, ax6), (ax7, ax8, ax9)) = plt.subplots(3,3,sharex=True, sharey=True, figsize=(10,9))
#fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(10,10))

    for i in range(1,9):
    
    #char= 'volume'
        d= dict_df[i]
        x = dict_df[i]["Magnitude"]
        y= dict_df[i][char]
        
        slope, intercept, r_value, p_value, std_err = stats.linregress(x,y) 
        r2 =  round(r_value**2,3)
        p_value = round(p_value,2)
        y_pred = intercept + slope * x
        rmse = mean_squared_error(y_true=y, y_pred=y_pred, squared=False)
        list_corr = [r2, rmse, p_value]
        dict_df[i][char+'_pred'] = y_pred
        
        
        plt.subplot(3, 3, i)
        if i == 1:
            df_corr['MODIS '+char] =  list_corr
            ax = sns.regplot(x, y , scatter_kws={'s':0,'clip_on': False},color="g") #plot the regline only
            ax = sns.scatterplot(data=d, x="Magnitude", y=char,hue="location",  s=80,palette=colors_mod,style="satellite", markers=[ 'o'] )
        if i == 2:
            df_corr['LANDSAT '+char] =  list_corr
            ax = sns.regplot(x, y , scatter_kws={'s':0},color="brown") #plot the regline only
            ax = sns.scatterplot(data=d, x="Magnitude", y=char,hue="location",  s=100,palette=colors_land,style="satellite", markers=[ 'o'] )
        if i == 3:
            df_corr['AVHRR '+char] =  list_corr
            ax = sns.regplot(x, y , scatter_kws={'s':0},color="b") #plot the regline only
            ax = sns.scatterplot(data=d, x="Magnitude", y=char,hue="location",  s=100,palette=colors_avh,style="satellite", markers=[ 'o'] )
        if i == 4:
            df_corr['MODIS2 '+char] =  list_corr
            ax = sns.regplot(x, y , scatter_kws={'s':0},color="g") #plot the regline only
            ax = sns.scatterplot(data=d, x="Magnitude", y=char,hue="location",  s=100,palette=colors_mod,style="satellite", markers=[ 's'] )
        if i == 5:
            df_corr['LANDSAT2 '+char] =  list_corr
            ax = sns.regplot(x, y , scatter_kws={'s':0},color="brown") #plot the regline only
            ax = sns.scatterplot(data=d, x="Magnitude", y=char,hue="location",  s=100,palette=colors_land,style="satellite", markers=[ 's'] )
        if i == 6:
            df_corr['AVHRR2 '+char] =  list_corr
            ax = sns.regplot(x, y , scatter_kws={'s':0},color="b") #plot the regline only
            ax = sns.scatterplot(data=d, x="Magnitude", y=char,hue="location",  s=100,palette=colors_avh,style="satellite", markers=[ 's'] )
        if i == 7:
            df_corr['MODIS3 '+char] =  list_corr
            ax = sns.regplot(x, y , scatter_kws={'s':0},color="g") #plot the regline only
            ax = sns.scatterplot(data=d, x="Magnitude", y=char,hue="location",  s=100,palette=colors_mod,style="satellite", markers=[ '^'] )
        if i == 8:
            df_corr['LANDSAT3 '+char] =  list_corr
            ax = sns.regplot(x, y , scatter_kws={'s':0},color="brown") #plot the regline only
            ax = sns.scatterplot(data=d, x="Magnitude", y=char,hue="location",  s=100,palette=colors_land,style="satellite", markers=[ '^'] )
        
        
        df_corr['parameter'] = ['r2','rmse','p_value']
        df_corr = df_corr.set_index('parameter')
        ax.set_xlabel('Magnitude', fontsize = 16,**dfont)
        if char == 'duration':
            ax.set_ylabel('Duration (days)', fontsize = 16,**dfont);
        elif char == 'volume':
            ax.set_ylabel('Volume (Mm$^3$/year)', fontsize = 16,**dfont);
        #ax.set(xlabel=None)
        #ax.set(ylabel=None)
        
        ax.xaxis.set_tick_params(labelsize=12)
        ax.yaxis.set_tick_params(labelsize=12)
        
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        textstr = '\n'.join((
        "R$^2$={:.2f}".format(r2),
        "RMSE={:.2f}".format(rmse)
        ))
        ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=12,**dfont,
            verticalalignment='top', bbox=props)
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles=handles[1:5], labels=labels[1:5],loc='upper right', fontsize=8)
     


        plt.subplots_adjust(wspace=0.4, hspace=0.3)
        fig.show()
   
        
#####ploting the pre MODIS period:
for char in char_list:   
    fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3,2,sharex=True, sharey=True, figsize=(10,9))


    for i in range(1,6):
    
    #char= 'volume'
        d= dict_df_pre[i]
        x = dict_df_pre[i]["Magnitude"]
        y= dict_df_pre[i][char]
        
        slope, intercept, r_value, p_value, std_err = stats.linregress(x,y) 
        r2 =  round(r_value**2,3)
        p_value = round(p_value,2)
        y_pred = intercept + slope * x
        rmse = mean_squared_error(y_true=y, y_pred=y_pred, squared=False)
        list_corr = [r2, rmse, p_value]
        dict_df_pre[i][char+'_pred'] = y_pred
        
        plt.subplot(3, 2, i)
        if i == 1:
            df_corr_pre['LANDSAT '+char] =  list_corr
            ax = sns.regplot(x, y , scatter_kws={'s':0,'clip_on': False},color="brown") #plot the regline only
            ax = sns.scatterplot(data=d, x="Magnitude", y=char,hue="location",  s=80,palette=colors_land,style="satellite", markers=[ 'o'] )
        if i == 2:
            df_corr_pre['AVHRR '+char] =  list_corr
            ax = sns.regplot(x, y , scatter_kws={'s':0},color="b") #plot the regline only
            ax = sns.scatterplot(data=d, x="Magnitude", y=char,hue="location",  s=100,palette=colors_avh,style="satellite", markers=[ 'o'] )
        if i == 3:
            df_corr_pre['LANDSAT2 '+char] =  list_corr
            ax = sns.regplot(x, y , scatter_kws={'s':0},color="brown") #plot the regline only
            ax = sns.scatterplot(data=d, x="Magnitude", y=char,hue="location",  s=100,palette=colors_land,style="satellite", markers=[ 's'] )
        if i == 4:
            df_corr_pre['AVHRR2 '+char] =  list_corr
            ax = sns.regplot(x, y , scatter_kws={'s':0},color="b") #plot the regline only
            ax = sns.scatterplot(data=d, x="Magnitude", y=char,hue="location",  s=100,palette=colors_avh,style="satellite", markers=[ 's'] )
        if i == 5:
            df_corr_pre['LANDSAT3 '+char] =  list_corr
            ax = sns.regplot(x, y , scatter_kws={'s':0},color="brown") #plot the regline only
            ax = sns.scatterplot(data=d, x="Magnitude", y=char,hue="location",  s=100,palette=colors_land,style="satellite", markers=[ '^'] )

        
        df_corr_pre['parameter'] = ['r2','rmse','p_value']
        df_corr_pre = df_corr_pre.set_index('parameter')
        ax.set_xlabel('Magnitude', fontsize = 16,**dfont)
        if char == 'duration':
            ax.set_ylabel('Duration (days)', fontsize = 16,**dfont);
        elif char == 'volume':
            ax.set_ylabel('Volume (Mm$^3$/year)', fontsize = 16,**dfont);
        #ax.set(xlabel=None)
        #ax.set(ylabel=None)
        
        ax.xaxis.set_tick_params(labelsize=12)
        ax.yaxis.set_tick_params(labelsize=12)
        
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        textstr = '\n'.join((
        "R$^2$={:.2f}".format(r2),
        "RMSE={:.2f}".format(rmse)
        ))
        ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=12,**dfont,
            verticalalignment='top', bbox=props)
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles=handles[1:5], labels=labels[1:5],loc='upper right', fontsize=8)
     
#fig.text(0.5, 0.0001, 'Magnitude', ha='center',fontsize=20)
#fig.text(0.01, 0.5, 'Volume (Mm$^3$/year)', va='center', rotation='vertical', fontsize=20,**dfont)    
#fig.tight_layout()

        plt.subplots_adjust(wspace=0.4, hspace=0.3)


###################################################################################
###########################CONFUSION MATRIX########################################
###################################################################################

#we do three numpy arrays: 1)y_label_all=avh. 2)y_label_mod 3) y_label_land
#thats because each satellite has different range of active years

hydro_bas['location'] = 'Bastrow'
hydro_gob['location'] = 'Gobabeb'
hydro_roi['location'] = 'Rooibank'
hydro_zin['location'] = 'Zin'
hydro_all = [ hydro_bas, hydro_gob ,hydro_roi ,hydro_zin]
hydro_all =  pd.concat(hydro_all)
hydro_all.drop(hydro_all.index[0], inplace=True)
hydro_all = hydro_all.reset_index()
hydro_all['label'] = 0
c=0

for i in hydro_all['volume']:
    if i>0.7:                      #0.7
       hydro_all['label'][c] = 1
       c+=1
    else:
       hydro_all['label'][c] = 0 
       c+=1

'''
#if you want normalize by basin size:
for i in hydro_all['volume']:
    if hydro_all['location'][c]=='Zin':
        if i>0.7:
            hydro_all['label'][c] = 1
            c+=1
        else:
            hydro_all['label'][c] = 0 
            c+=1
    else:
        if i>7:                           #the basin size of kuiseb and mojave is 10 time of zin
            hydro_all['label'][c] = 1
            c+=1
        else:
            hydro_all['label'][c] = 0 
            c+=1
'''

hydro_all = hydro_all.drop(hydro_all[(hydro_all['location'].str.match('Gobabeb') == True) & (hydro_all['year'] >2011)].index)
hydro_all = hydro_all.drop(hydro_all[(hydro_all['location'].str.match('Rooibank') == True) & (hydro_all['year'] >2011)].index)
y_label_all = list(hydro_all['label'])
y_label_all = np.array(y_label_all)


hydro_all_mod = hydro_all.drop(hydro_all[hydro_all['year'] <=2000].index)
y_label_mod = list(hydro_all_mod['label'])
y_label_mod = np.array(y_label_mod)


hydro_all_land = hydro_all.drop(hydro_all[hydro_all['year'] <=1984].index)
y_label_land = list(hydro_all_land['label'])
y_label_land = np.array(y_label_land)

hydro_all_after = hydro_all.drop(hydro_all[hydro_all['year'] <=2000].index)
y_label_after = list(hydro_all_after['label'])
y_label_after = np.array(y_label_after)


hydro_all_pre_avh = hydro_all.drop(hydro_all[hydro_all['year'] >=2002].index)
y_label_pre_avh = list(hydro_all_pre_avh['label'])
y_label_pre_avh = np.array(y_label_pre_avh)

hydro_all_pre_land = hydro_all_pre_avh.drop(hydro_all_pre_avh[hydro_all_pre_avh['year'] <=1984].index)
y_label_pre_land = list(hydro_all_pre_land['label'])
y_label_pre_land = np.array(y_label_pre_land)

#we do function of confusion matrix:
def cf_matrix(y_label, y_pred,colors):
    cf_matrix = confusion_matrix(y_label, y_pred)

    print(cf_matrix)

    group_counts = ['{0:0.0f}'.format(value) for value in
                cf_matrix.flatten()]
    group_percentages = ['{0:.2%}'.format(value) for value in
                     cf_matrix.flatten()/np.sum(cf_matrix)]
    labels = [f'{v1}\n{v2}' for v1, v2 in
          zip(group_counts,group_percentages)]
    labels = np.asarray(labels).reshape(2,2)
    ax = sns.heatmap(cf_matrix, annot=labels, annot_kws={'size': 15}, fmt='', cmap=colors)

    #ax.set_title('Confusion Matrix - NDVI from MODIS - BFAST' , fontsize = 28,**dfont);
    ax.set_xlabel('\nPredicted Values', fontsize = 22,**dfont)
    ax.set_ylabel('Actual Values ', fontsize = 22,**dfont);

    Accuracy= round(metrics.accuracy_score(y_label, y_pred),2)
    Precision = round(metrics.precision_score(y_label, y_pred),2)
    Recall = round(metrics.recall_score(y_label, y_pred),2)
    f1 = round(metrics.f1_score(y_label, y_pred),2)
    
    ## Ticket labels - List must be in alphabetical order
    ax.xaxis.set_ticklabels(['Nagative','Positive'], fontsize = 18,**dfont)
    ax.yaxis.set_ticklabels(['Nagative','Positive'], fontsize = 18,**dfont)
    ax.xaxis.set_tick_params(labelsize=18)
    ax.yaxis.set_tick_params(labelsize=18)
    ax.text(3,8, f'Accuracy = {Accuracy}', ha="center", va="center", fontsize=12,**dfont, bbox={"facecolor":"orange", "alpha":0})
    

    ## Display the visualization of the Confusion Matrix
    list_accur = [Accuracy,Precision,Recall, f1]
    return list_accur
    print(Accuracy)
    print(Precision)
    print(Recall)
    print(f1)

#for each satellite we do function that print its own confusion matrix:
    
def avh(y_label,df,cmap):   #avhrr before modis period
    y_pred_avh = np.empty(0)
    dict_place = {0: 'Bastrow', 1: 'Gobabeb', 2: 'Rooibank', 3: 'Zin'}
    for i in range(0,4):
        if i == 0 or i == 3:
            for year in range(1981, 2002):
                Slice=df.loc[(df['location'] == dict_place[i]),  
    
                                       ["year"]]
            
                lis = list(Slice['year'])
                if year in lis:
                    y_pred_avh =np. append( y_pred_avh,1)
                else:
                    y_pred_avh =np. append( y_pred_avh,0)
        elif i == 1 or i == 2:
            for year in range(1981, 2002):
                Slice=df.loc[(df['location'] == dict_place[i]),  
    
                                       ["year"]]
            
                lis = list(Slice['year'])
                if year in lis :
                    y_pred_avh =np. append( y_pred_avh,1)
                else:
                    y_pred_avh =np. append( y_pred_avh,0)

    list_accur = cf_matrix(y_label_pre_avh, y_pred_avh,cmap)
    return list_accur

def after(y_label,df,cmap):   #avhrr and landsat in modis period
    y_pred_avh = np.empty(0)
    dict_place = {0: 'Bastrow', 1: 'Gobabeb', 2: 'Rooibank', 3: 'Zin'}
    for i in range(0,4):
        if i == 0 or i == 3:
            for year in range(2001, 2022):
                Slice=df.loc[(df['location'] == dict_place[i]),  
    
                                       ["year"]]
            
                lis = list(Slice['year'])
                if year in lis:
                    y_pred_avh =np. append( y_pred_avh,1)
                else:
                    y_pred_avh =np. append( y_pred_avh,0)
        elif i == 1 or i == 2:
            for year in range(2001, 2012):
                Slice=df.loc[(df['location'] == dict_place[i]),  
    
                                       ["year"]]
            
                lis = list(Slice['year'])
                if year in lis :
                    y_pred_avh =np. append( y_pred_avh,1)
                else:
                    y_pred_avh =np. append( y_pred_avh,0)

    list_accur = cf_matrix(y_label_after, y_pred_avh,cmap)
    return list_accur

def mod(y_label,df,cmap):
    y_pred_mod = np.empty(0)
    dict_place = {0: 'Bastrow', 1: 'Gobabeb', 2: 'Rooibank', 3: 'Zin'}
    for i in range(0,4):
        if i == 0 or i == 3:
            for year in range(2001, 2022):
                Slice=df.loc[(df['location'] == dict_place[i]),  
    
                                       ["year"]]
            
                lis = list(Slice['year'])
                if year in lis :
                    y_pred_mod =np. append( y_pred_mod,1)
                else:
                    y_pred_mod =np. append( y_pred_mod,0)
        elif i == 1 or i == 2:
            for year in range(2001, 2012):
                Slice=df.loc[(df['location'] == dict_place[i]),  
    
                                       ["year"]]
            
                lis = list(Slice['year'])
                if year in lis :
                    y_pred_mod =np. append( y_pred_mod,1)
                else:
                    y_pred_mod =np. append( y_pred_mod,0)

    list_accur = cf_matrix(y_label_mod, y_pred_mod,cmap)
    return list_accur

def land(y_label,df,cmap):
    y_pred_land = np.empty(0)
    dict_place = {0: 'Bastrow', 1: 'Gobabeb', 2: 'Rooibank', 3: 'Zin'}
    for i in range(0,4):
        if i == 0 or i == 3:
            for year in range(1985, 2002):
                Slice=df.loc[(df['location'] == dict_place[i]),  
    
                                       ["year"]]
            
                lis = list(Slice['year'])
                if year in lis :
                    y_pred_land =np. append( y_pred_land,1)
                else:
                    y_pred_land =np. append( y_pred_land,0)
        elif i == 1 or i == 2:
            for year in range(1985, 2002):
                Slice=df.loc[(df['location'] == dict_place[i]),  
    
                                       ["year"]]
            
                lis = list(Slice['year'])
                if year in lis :
                    y_pred_land =np. append( y_pred_land,1)
                else:
                    y_pred_land =np. append( y_pred_land,0)

    list_accur = cf_matrix(y_label_pre_land, y_pred_land,cmap)
    return list_accur
#plot all the matrix together for MODIS period:
df_accur = pd.DataFrame()
df_accur_pre = pd.DataFrame()
            
fig, ((ax1, ax2, ax3), (ax4, ax5, ax6), (ax7, ax8, ax9)) = plt.subplots(3,3,sharex=True, sharey=True, figsize=(10,9))                
for i in range(1,9):
    plt.subplot(3, 3, i)
    
    if i == 1:
        cmap = 'Greens'
        list_accur = mod(y_label_mod,dict_df[1],cmap )
        df_accur['MODIS'] =  list_accur
    if i == 2:
        cmap = 'Reds'
        list_accur = after(y_label_after,dict_df[2],cmap )
        df_accur['LANDSAT'] =  list_accur
    if i == 3:
        cmap = 'Blues'
        list_accur = after(y_label_after,dict_df[3],cmap )
        df_accur['AVHRR'] =  list_accur
    if i == 4:
        cmap = 'Greens'
        list_accur = mod(y_label_mod,dict_df[4],cmap )
        df_accur['MODIS2'] =  list_accur
    if i == 5:
        cmap = 'Reds'
        list_accur = after(y_label_after,dict_df[5],cmap )
        df_accur['LANDSAT2'] =  list_accur
    if i == 6:
        cmap = 'Blues'
        list_accur = after(y_label_after,dict_df[6],cmap )
        df_accur['AVHRR2'] =  list_accur
    if i == 7:
        cmap = 'Greens'
        list_accur = mod(y_label_mod,dict_df[7],cmap )
        df_accur['MODIS3'] =  list_accur
    if i == 8:
        cmap = 'Reds'
        list_accur = after(y_label_after,dict_df[8],cmap )
        df_accur['LANDSAT3'] =  list_accur
 
    
#plot all the matrix together for pre-MODIS period:
         
fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3,2,sharex=True, sharey=True, figsize=(10,9))
for i in range(1,6):
    plt.subplot(3, 2, i)
    
    if i == 1:
        cmap = 'Reds'
        list_accur = land(y_label_pre_land,dict_df_pre[1],cmap )
        df_accur_pre['LANDSAT'] =  list_accur
    if i == 2:
        cmap = 'Blues'
        list_accur = avh(y_label_pre_avh,dict_df_pre[2],cmap )
        df_accur_pre['AVHRR'] =  list_accur
    if i == 3:
        cmap = 'Reds'
        list_accur = land(y_label_pre_land,dict_df_pre[3],cmap )
        df_accur_pre['LANDSAT2'] =  list_accur
    if i == 4:
        cmap = 'Blues'
        list_accur = avh(y_label_pre_avh,dict_df_pre[4],cmap )
        df_accur_pre['AVHRR2'] =  list_accur
    if i == 5:
        cmap = 'Reds'
        list_accur = land(y_label_pre_land,dict_df_pre[5],cmap )
        df_accur_pre['LANDSAT3'] =  list_accur

#plot one confusion matrix at a time: (need to change the matrix function so it will add the accuracy to the plot)

#fig, ax = plt.subplots(sharex=True, sharey=True, figsize=(8,6))  

#cmap = 'Greens'
#avh(y_label_all,df_comb,cmap)
    

            
###########################################################################################            
            
            
###################
#####Fourier#######
###################
st=1
place = ['bas','gob','roi','zin']
satellite = ['mod', 'land','avh']
vin = [ 'ndvi','msavi','ndwi' ] 

def read_directory(directory, vi):
    os.chdir(directory)
    path = os.getcwd()
    csv_files = sorted(glob.glob(os.path.join(path, "*.csv")))
    
    dict_df_fouriers ={}
    c=1
    for f in csv_files:
        df = pd.read_csv(f)
        dict_df_fouriers[c] = df
        c+=1
    return dict_df_fouriers


def forier(df,hydro) :
           
    df_1 = pd.merge(df, hydro, on='year')
    

    df_1 = df_1.reset_index(drop= True)
  
    for index, row in df_1.iterrows():
        if row['std'] < st:
            df_1.drop(index, inplace=True)
   
    return df_1


dict_df_fourier={}
dict_df_fourier_confusion={}
c=1
for v in vin:
    for s in satellite:
            directory = 'G:/.shortcut-targets-by-id/1sUX8T9nhBa6xjqe6YGVrNhmGMD6VCbho/hydrology/datasets/'+v+'/'+s+'/fourier'
            dict_vi_satel = read_directory(directory, v)
            
            #prepare bas data
            hydro_bas= pd.read_csv("G:/.shortcut-targets-by-id/1sUX8T9nhBa6xjqe6YGVrNhmGMD6VCbho/hydrology/datasets/hydro_data/annual/bastrow_annual3.csv")
            hydro_bas['Qp(cfs/sec)']= hydro_bas['Qp(cfs/sec)']* 0.0283168
            #hydro['volume']=( hydro['volume']* 0.0283168 * 365*3600*24)/1000000
            hydro_bas.columns = [ 'year','Qp','volume','duration']
            df_bas = forier(dict_vi_satel[1],hydro_bas)        
            df_bas['satellite'] = s
            df_bas['location'] = 'Bastrow'
            
            #prepare gob data
            hydro_gob= pd.read_csv("G:/.shortcut-targets-by-id/1sUX8T9nhBa6xjqe6YGVrNhmGMD6VCbho/hydrology/datasets/hydro_data/annual/gobabeb_annual.csv")
            hydro_gob.columns = [ 'year','Qp','volume','duration']
            df_gob = forier(dict_vi_satel[2],hydro_gob) 
            df_gob['satellite'] = s
            df_gob['location'] = 'Gobabeb'
            
            df_gob = df_gob.set_index('year', drop = False)
            for i in df_gob['year']:
                if i == 2008 or i == 2007 or i == 2010 or i > 2011:
                    df_gob = df_gob.drop(i)
                else:
                    continue
            df_gob = df_gob.reset_index(drop=True)
     
            #prepare roi data
            hydro_roi= pd.read_csv("G:/.shortcut-targets-by-id/1sUX8T9nhBa6xjqe6YGVrNhmGMD6VCbho/hydrology/datasets/hydro_data/annual/rooibank_annual.csv")
            hydro_roi.columns = [ 'year','Qp','volume','duration']
            df_roi = forier(dict_vi_satel[3],hydro_roi) 
            df_roi['satellite'] = s
            df_roi['location'] = 'Rooibank'
            
            df_roi = df_roi.set_index('year', drop = False)
            for i in df_roi['year']:
                if i == 2008 or i == 2007 or i == 2010 or i > 2011:
                    df_roi = df_roi.drop(i)
                else:
                    continue
            df_roi = df_roi.reset_index(drop=True)
            
            #prepare zin data
            hydro_zin= pd.read_csv("G:/.shortcut-targets-by-id/1sUX8T9nhBa6xjqe6YGVrNhmGMD6VCbho/hydrology/datasets/hydro_data/annual/zin_annual.csv")
            hydro_zin.columns = [ 'year','Qp','volume','duration']
            df_zin = forier(dict_vi_satel[4],hydro_zin) 
            df_zin['satellite'] = s
            df_zin['location'] = 'Zin'
            
            
            df=[df_bas, df_gob , df_roi, df_zin]
            df = pd.concat(df)
            dict_df_fourier[c] = df
            c+=1
            
#####divide LANDSAT & AVHRR to MODIS period and pre MODIS period:
dict_df_fourier_pre = {}
df_list = [2,3,5,6,8]
j=1
for i in df_list:
    mask = dict_df_fourier[i]['year'] >= 2002
    dict_df_fourier_pre[j] = dict_df_fourier[i][~mask] 
    dict_df_fourier[i] = dict_df_fourier[i][mask]
    j+=1
      

 
''' 
#############################################################
#####plot combine satellites data(best results per years)####
#############################################################
colors_ndvi = {'Bastrow':'darkgreen', 'Gobabeb':'forestgreen', 'Rooibank':'limegreen', 'Zin':'palegreen'}
colors_msavi = {'Bastrow':'saddlebrown', 'Gobabeb':'chocolate', 'Rooibank':'sandybrown', 'Zin':'peachpuff'}
colors_ndwi = {'Bastrow':'navy', 'Gobabeb':'royalblue', 'Rooibank':'cornflowerblue', 'Zin':'skyblue'}

avh = dict_df_fourier[3]
avh = avh.drop(avh[avh.year >2001].index)

land = dict_df_fourier[2]
land = land.drop(land[land.year >2001].index)

mod = dict_df_fourier[1]

df_comb=[land, mod]
df_comb = pd.concat(df_comb)

d= df_comb
x = d["std"]
y= d["volume"]

slope, intercept, r_value, p_value, std_err = stats.linregress(x,y) 
r2 =  round(r_value**2,3)
y_pred = intercept + slope * x
rmse = mean_squared_error(y_true=y, y_pred=y_pred, squared=False)
fig, ax = plt.subplots( figsize=(6,5))
ax = sns.regplot(x, y ,color="g", scatter_kws={'s':0}).set(title='MODIS - NDVI(01-21)') #plot the regline only
#sns.scatterplot(data=d, x="Magnitude", y="volume",hue="location",  s=100) #plot points in different color
#sns.scatterplot(data=d, x="Magnitude", y="volume",hue="location", style ='satellite', s=100, legend=False) #plot points in different color and shapes
ax = sns.scatterplot(data=d, x="std", y="volume",hue="location",  s=100,palette=colors_ndvi,style="satellite", markers={'mod':'o','land': '^' ,'avh':'s'})
ax.set_xlabel('std', fontsize = 16,**dfont)
ax.set_ylabel('Volume (Mm$^3$/year)', fontsize = 16,**dfont);
#ax.set(xlabel=None)
#ax.set(ylabel=None)

ax.xaxis.set_tick_params(labelsize=12)
ax.yaxis.set_tick_params(labelsize=12)

props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
textstr = '\n'.join((
"R$^2$={:.2f}".format(r2),
"RMSE={:.2f}".format(rmse)
))
ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=12,**dfont,
verticalalignment='top', bbox=props)
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles=handles[1:5], labels=labels[1:5],loc='upper right', fontsize=8)

'''

###########
##ploting##
###########           
  
 
charc = 'duration'
valu= 'area'



d= dict_df_fourier[1]
x = dict_df_fourier[1][valu]
y= dict_df_fourier[1][charc]

colors_mod = {'Bastrow':'darkgreen', 'Gobabeb':'forestgreen', 'Rooibank':'limegreen', 'Zin':'palegreen'}
colors_land = {'Bastrow':'saddlebrown', 'Gobabeb':'chocolate', 'Rooibank':'sandybrown', 'Zin':'peachpuff'}
colors_avh = {'Bastrow':'navy', 'Gobabeb':'royalblue', 'Rooibank':'cornflowerblue', 'Zin':'skyblue'}
char_list= ['volume', 'duration']
df_corr = pd.DataFrame()
df_corr_pre = pd.DataFrame()

for char in char_list:
    fig, ((ax1, ax2, ax3), (ax4, ax5, ax6), (ax7, ax8, ax9)) = plt.subplots(3,3,sharex=True, sharey=True, figsize=(10,9))
#fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(10,10))
    for i in range(1,9):
        d= dict_df_fourier[i]
        x = dict_df_fourier[i][valu]
        y= dict_df_fourier[i][char]
        
        slope, intercept, r_value, p_value, std_err = stats.linregress(x,y) 
        r2 =  round(r_value**2,3)
        p_value = round(p_value,3)
        y_pred = intercept + slope * x
        rmse = mean_squared_error(y_true=y, y_pred=y_pred, squared=False)
        list_corr = [r2, rmse, p_value]
        dict_df_fourier[i][char+'_pred'] = y_pred
        
        plt.subplot(3, 3, i)
        if i == 1:
            df_corr['MODIS '+char] =  list_corr
            ax = sns.regplot(x, y , scatter_kws={'s':0,'clip_on': False},color="g") #plot the regline only
            ax = sns.scatterplot(data=d, x=valu, y=char,hue="location",  s=80,palette=colors_mod,style="satellite", markers=[ 'o'] )
        if i == 2:
            df_corr['LANDAT '+char] =  list_corr
            ax = sns.regplot(x, y , scatter_kws={'s':0},color="brown") #plot the regline only
            ax = sns.scatterplot(data=d, x=valu, y=char,hue="location",  s=100,palette=colors_land,style="satellite", markers=[ 'o'] )
        if i == 3:
            df_corr['AVHRR '+char] =  list_corr
            ax = sns.regplot(x, y , scatter_kws={'s':0},color="b") #plot the regline only
            ax = sns.scatterplot(data=d, x=valu, y=char,hue="location",  s=100,palette=colors_avh,style="satellite", markers=[ 'o'] )
        if i == 4:
            df_corr['MODIS2 '+char] =  list_corr
            ax = sns.regplot(x, y , scatter_kws={'s':0},color="g") #plot the regline only
            ax = sns.scatterplot(data=d, x=valu, y=char,hue="location",  s=100,palette=colors_mod,style="satellite", markers=[ 's'] )
        if i == 5:
            df_corr['LANDSAT2 '+char] =  list_corr
            ax = sns.regplot(x, y , scatter_kws={'s':0},color="brown") #plot the regline only
            ax = sns.scatterplot(data=d, x=valu, y=char,hue="location",  s=100,palette=colors_land,style="satellite", markers=[ 's'] )
        if i == 6:
            df_corr['AVHRR2 '+char] =  list_corr
            ax = sns.regplot(x, y , scatter_kws={'s':0},color="b") #plot the regline only
            ax = sns.scatterplot(data=d, x=valu, y=char,hue="location",  s=100,palette=colors_avh,style="satellite", markers=[ 's'] )
        if i == 7:
            df_corr['MODIS3 '+char] =  list_corr
            ax = sns.regplot(x, y , scatter_kws={'s':0},color="g") #plot the regline only
            ax = sns.scatterplot(data=d, x=valu, y=char,hue="location",  s=100,palette=colors_mod,style="satellite", markers=[ '^'] )
        if i == 8:
            df_corr['LANDSAT3 '+char] =  list_corr
            ax = sns.regplot(x, y , scatter_kws={'s':0},color="brown") #plot the regline only
            ax = sns.scatterplot(data=d, x=valu, y=char,hue="location",  s=100,palette=colors_land,style="satellite", markers=[ '^'] )
        
        df_corr['parameter'] = ['r2','rmse','p_value']
        df_corr = df_corr.set_index('parameter')
        ax.set_xlabel('GSI$_a$$_n$$_o$$_m$', fontsize = 16,**dfont)
        if char == 'duration':
            ax.set_ylabel('Duration (days)', fontsize = 16,**dfont);
        elif char == 'volume':
            ax.set_ylabel('Volume (Mm$^3$/year)', fontsize = 16,**dfont);
        #ax.set(xlabel=None)
        #ax.set(ylabel=None)
        
        ax.xaxis.set_tick_params(labelsize=12)
        ax.yaxis.set_tick_params(labelsize=12)
        
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        textstr = '\n'.join((
        "R$^2$={:.2f}".format(r2),
        "RMSE={:.2f}".format(rmse)
        ))
        ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=12,**dfont,
            verticalalignment='top', bbox=props)
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles=handles[1:5], labels=labels[1:5],loc='upper right', fontsize=8)
     
    #fig.text(0.5, 0.0001, 'Magnitude', ha='center',fontsize=20)
    #fig.text(0.01, 0.5, 'Volume (Mm$^3$/year)', va='center', rotation='vertical', fontsize=20,**dfont)    
    #fig.tight_layout()
    
    plt.subplots_adjust(wspace=0.4, hspace=0.3)
            
        
#####ploting the pre MODIS period:
for char in char_list:   
    fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3,2,sharex=True, sharey=True, figsize=(10,9))


    for i in range(1,6):
    
    #char= 'volume'
        d= dict_df_fourier_pre[i]
        x = dict_df_fourier_pre[i][valu]
        y= dict_df_fourier_pre[i][char]
        
        slope, intercept, r_value, p_value, std_err = stats.linregress(x,y) 
        r2 =  round(r_value**2,3)
        p_value = round(p_value,2)
        y_pred = intercept + slope * x
        rmse = mean_squared_error(y_true=y, y_pred=y_pred, squared=False)
        list_corr = [r2, rmse, p_value]
        dict_df_fourier_pre[i][char+'_pred'] = y_pred
        
        plt.subplot(3, 2, i)
        if i == 1:
            df_corr_pre['LANDSAT '+char] =  list_corr
            ax = sns.regplot(x, y , scatter_kws={'s':0,'clip_on': False},color="brown") #plot the regline only
            ax = sns.scatterplot(data=d, x=valu, y=char,hue="location",  s=80,palette=colors_land,style="satellite", markers=[ 'o'] )
        if i == 2:
            df_corr_pre['AVHRR '+char] =  list_corr
            ax = sns.regplot(x, y , scatter_kws={'s':0},color="b") #plot the regline only
            ax = sns.scatterplot(data=d, x=valu, y=char,hue="location",  s=100,palette=colors_avh,style="satellite", markers=[ 'o'] )
        if i == 3:
            df_corr_pre['LANDSAT2 '+char] =  list_corr
            ax = sns.regplot(x, y , scatter_kws={'s':0},color="brown") #plot the regline only
            ax = sns.scatterplot(data=d, x=valu, y=char,hue="location",  s=100,palette=colors_land,style="satellite", markers=[ 's'] )
        if i == 4:
            df_corr_pre['AVHRR2 '+char] =  list_corr
            ax = sns.regplot(x, y , scatter_kws={'s':0},color="b") #plot the regline only
            ax = sns.scatterplot(data=d, x=valu, y=char,hue="location",  s=100,palette=colors_avh,style="satellite", markers=[ 's'] )
        if i == 5:
            df_corr_pre['LANDSAT3 '+char] =  list_corr
            ax = sns.regplot(x, y , scatter_kws={'s':0},color="brown") #plot the regline only
            ax = sns.scatterplot(data=d, x=valu, y=char,hue="location",  s=100,palette=colors_land,style="satellite", markers=[ '^'] )

        
        df_corr_pre['parameter'] = ['r2','rmse','p_value']
        df_corr_pre = df_corr_pre.set_index('parameter')
        ax.set_xlabel('GSI$_a$$_n$$_o$$_m$', fontsize = 16,**dfont)
        if char == 'duration':
            ax.set_ylabel('Duration (days)', fontsize = 16,**dfont);
        elif char == 'volume':
            ax.set_ylabel('Volume (Mm$^3$/year)', fontsize = 16,**dfont);
        #ax.set(xlabel=None)
        #ax.set(ylabel=None)
        
        ax.xaxis.set_tick_params(labelsize=12)
        ax.yaxis.set_tick_params(labelsize=12)
        
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        textstr = '\n'.join((
        "R$^2$={:.2f}".format(r2),
        "RMSE={:.2f}".format(rmse)
        ))
        ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=12,**dfont,
            verticalalignment='top', bbox=props)
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles=handles[1:5], labels=labels[1:5],loc='upper right', fontsize=8)
     
#fig.text(0.5, 0.0001, 'Magnitude', ha='center',fontsize=20)
#fig.text(0.01, 0.5, 'Volume (Mm$^3$/year)', va='center', rotation='vertical', fontsize=20,**dfont)    
#fig.tight_layout()

        plt.subplots_adjust(wspace=0.4, hspace=0.3)
          


###################################################################################
###########################CONFUSION MATRIX########################################
###################################################################################

#we do three numpy arrays: 1)y_label_all=avh. 2)y_label_mod 3) y_label_land
#thats because each satellite has different range of active years

hydro_bas['location'] = 'Bastrow'
hydro_gob['location'] = 'Gobabeb'
hydro_roi['location'] = 'Rooibank'
hydro_zin['location'] = 'Zin'
hydro_all = [ hydro_bas, hydro_gob ,hydro_roi ,hydro_zin]
hydro_all =  pd.concat(hydro_all)
hydro_all.drop(hydro_all.index[0], inplace=True)
hydro_all = hydro_all.reset_index()
hydro_all['label'] = 0
c=0

for i in hydro_all['volume']:
    if i>0.7:                      #0.7
       hydro_all['label'][c] = 1
       c+=1
    else:
       hydro_all['label'][c] = 0 
       c+=1
'''
#if you want normalize by basin size:
for i in hydro_all['volume']:
    if hydro_all['location'][c]=='Zin':
        if i>0.5:
            hydro_all['label'][c] = 1
            c+=1
        else:
            hydro_all['label'][c] = 0 
            c+=1
    else:
        if i>5:                           #the basin size of kuiseb and mojave is 10 time of zin
            hydro_all['label'][c] = 1
            c+=1
        else:
            hydro_all['label'][c] = 0 
            c+=1
'''
hydro_all = hydro_all.drop(hydro_all[(hydro_all['location'].str.match('Gobabeb') == True) & (hydro_all['year'] >2011)].index)
hydro_all = hydro_all.drop(hydro_all[(hydro_all['location'].str.match('Rooibank') == True) & (hydro_all['year'] >2011)].index)
y_label_all = list(hydro_all['label'])
y_label_all = np.array(y_label_all)


hydro_all_mod = hydro_all.drop(hydro_all[hydro_all['year'] <=2000].index)
y_label_mod = list(hydro_all_mod['label'])
y_label_mod = np.array(y_label_mod)

hydro_all_land = hydro_all.drop(hydro_all[hydro_all['year'] <=1984].index)
y_label_land = list(hydro_all_land['label'])
y_label_land = np.array(y_label_land)

hydro_all_after = hydro_all.drop(hydro_all[hydro_all['year'] <=2000].index)
y_label_after = list(hydro_all_after['label'])
y_label_after = np.array(y_label_after)


hydro_all_pre_avh = hydro_all.drop(hydro_all[hydro_all['year'] >=2002].index)
y_label_pre_avh = list(hydro_all_pre_avh['label'])
y_label_pre_avh = np.array(y_label_pre_avh)

hydro_all_pre_land = hydro_all_pre_avh.drop(hydro_all_pre_avh[hydro_all_pre_avh['year'] <=1984].index)
y_label_pre_land = list(hydro_all_pre_land['label'])
y_label_pre_land = np.array(y_label_pre_land)

#we do function of confusion matrix:
def cf_matrix(y_label, y_pred,colors):
    cf_matrix = confusion_matrix(y_label, y_pred)

    print(cf_matrix)

    group_counts = ['{0:0.0f}'.format(value) for value in
                cf_matrix.flatten()]
    group_percentages = ['{0:.2%}'.format(value) for value in
                     cf_matrix.flatten()/np.sum(cf_matrix)]
    labels = [f'{v1}\n{v2}' for v1, v2 in
          zip(group_counts,group_percentages)]
    labels = np.asarray(labels).reshape(2,2)
    ax = sns.heatmap(cf_matrix, annot=labels, annot_kws={'size': 15}, fmt='', cmap=colors)

    #ax.set_title('Confusion Matrix - NDVI from MODIS - Fourier' , fontsize = 28,**dfont);
    ax.set_xlabel('\nPredicted Values', fontsize = 22,**dfont)
    ax.set_ylabel('Actual Values ', fontsize = 22,**dfont);

    Accuracy= metrics.accuracy_score(y_label, y_pred)
    Precision = metrics.precision_score(y_label, y_pred)
    Recall = metrics.recall_score(y_label, y_pred)
    f1 = metrics.f1_score(y_label, y_pred)
    
    ## Ticket labels - List must be in alphabetical order
    ax.xaxis.set_ticklabels(['Nagative','Positive'], fontsize = 18,**dfont)
    ax.yaxis.set_ticklabels(['Nagative','Positive'], fontsize = 18,**dfont)
    ax.xaxis.set_tick_params(labelsize=18)
    ax.yaxis.set_tick_params(labelsize=18)
    ax.text(3,8, f'Accuracy = {Accuracy}', ha="center", va="center", fontsize=12,**dfont, bbox={"facecolor":"orange", "alpha":0})
    

    ## Display the visualization of the Confusion Matrix
    
    list_accur = [Accuracy,Precision,Recall, f1]
    return list_accur
    print(Accuracy)
    print(Precision)
    print(Recall)
    print(f1)

#for each satellite we do function that print its own confusion matrix:
'''    
def avh(y_label,df,cmap,std):
    df = df.drop(df[(df['location'].str.match('Gobabeb') == True) & (df['year'] >2011)].index)
    df = df.drop(df[(df['location'].str.match('Rooibank') == True) & (df['year'] >2011)].index)
    df['label'] =0
    df.loc[df['std'] >std,['label']] =1
    
    y_pred_avh = np.empty(0)
    dict_place = {0: 'Bastrow', 1: 'Gobabeb', 2: 'Rooibank', 3: 'Zin'}
    for i in range(0,4):
        if i == 0 or i == 3:
            for year in range(1981, 2022):
                Slice=df.loc[(df['location'] == dict_place[i]),  
    
                                       ["year"]]
            
                lis = list(Slice['year'])
                if year in lis:
                    y_pred_avh =np. append( y_pred_avh,1)
                else:
                    y_pred_avh =np. append( y_pred_avh,0)
        elif i == 1 or i == 2:
            for year in range(1981, 2012):
                Slice=df.loc[(df['location'] == dict_place[i]),  
    
                                       ["year"]]
            
                lis = list(Slice['year'])
                if year in lis :
                    y_pred_avh =np. append( y_pred_avh,1)
                else:
                    y_pred_avh =np. append( y_pred_avh,0)
                    

    cf_matrix(y_label_all, y_pred_avh,cmap)

def mod(y_label,df,cmap,std):
    df = df.drop(df[(df['location'].str.match('Gobabeb') == True) & (df['year'] >2011)].index)
    df = df.drop(df[(df['location'].str.match('Rooibank') == True) & (df['year'] >2011)].index)
    df['label'] =0
    df.loc[df['std'] >std,['label']] =1
    
    y_pred_mod = np.empty(0)
    dict_place = {0: 'Bastrow', 1: 'Gobabeb', 2: 'Rooibank', 3: 'Zin'}
    for i in range(0,4):
        if i == 0 or i == 3:
            for year in range(2001, 2022):
                Slice=df.loc[(df['location'] == dict_place[i]),  
    
                                       ["year"]]
            
                lis = list(Slice['year'])
                if year in lis :
                    y_pred_mod =np. append( y_pred_mod,1)
                else:
                    y_pred_mod =np. append( y_pred_mod,0)
        elif i == 1 or i == 2:
            for year in range(2001, 2012):
                Slice=df.loc[(df['location'] == dict_place[i]),  
    
                                       ["year"]]
            
                lis = list(Slice['year'])
                if year in lis :
                    y_pred_mod =np. append( y_pred_mod,1)
                else:
                    y_pred_mod =np. append( y_pred_mod,0)

    cf_matrix(y_label_mod, y_pred_mod,cmap)
    
def land(y_label,df,cmap,std):
    df = df.drop(df[(df['location'].str.match('Gobabeb') == True) & (df['year'] >2011)].index)
    df = df.drop(df[(df['location'].str.match('Rooibank') == True) & (df['year'] >2011)].index)
    df['label'] =0
    df.loc[df['std'] >std ,['label']] =1
    
    y_pred_land = np.empty(0)
    dict_place = {0: 'Bastrow', 1: 'Gobabeb', 2: 'Rooibank', 3: 'Zin'}
    for i in range(0,4):
        if i == 0 or i == 3:
            for year in range(1985, 2022):
                Slice=df.loc[(df['location'] == dict_place[i]),  
    
                                       ["year"]]
            
                lis = list(Slice['year'])
                if year in lis :
                    y_pred_land =np. append( y_pred_land,1)
                else:
                    y_pred_land =np. append( y_pred_land,0)
        elif i == 1 or i == 2:
            for year in range(1985, 2012):
                Slice=df.loc[(df['location'] == dict_place[i]),  
    
                                       ["year"]]
            
                lis = list(Slice['year'])
                if year in lis :
                    y_pred_land =np. append( y_pred_land,1)
                else:
                    y_pred_land =np. append( y_pred_land,0)
                    

    cf_matrix(y_label_land, y_pred_land,cmap)

#plot all the matrix together: (need to change the matrix function so it wont add the accuracy to the plot)  
std =1  #from wich std I want to predict flood
          
fig, ((ax1, ax2, ax3), (ax4, ax5, ax6), (ax7, ax8, ax9)) = plt.subplots(3,3,sharex=True, sharey=True, figsize=(10,9))                
for i in range(1,9):
    plt.subplot(3, 3, i)
    
    if i == 1:
        cmap = 'Greens'
        mod(y_label_mod,dict_df_fourier[1],cmap,std )
    if i == 2:
        cmap = 'Reds'
        land(y_label_land,dict_df_fourier[2],cmap,std  )
    if i == 3:
        cmap = 'Blues'
        avh(y_label_all,dict_df_fourier[3],cmap,std  )
    if i == 4:
        cmap = 'Greens'
        mod(y_label_mod,dict_df_fourier[4],cmap,std  )
    if i == 5:
        cmap = 'Reds'
        land(y_label_land,dict_df_fourier[5],cmap ,std )
    if i == 6:
        cmap = 'Blues'
        avh(y_label_all,dict_df_fourier[6],cmap,std  )
    if i == 7:
        cmap = 'Greens'
        mod(y_label_mod,dict_df_fourier[7],cmap,std  )
    if i == 8:
        cmap = 'Reds'
        land(y_label_all,dict_df_fourier[8],cmap,std  )
    
        
#plot one confusion matrix at a time: (need to change the matrix function so it will add the accuracy to the plot)

#fig, ax = plt.subplots(sharex=True, sharey=True, figsize=(8,6))  

#cmap = 'Greens'
#land(y_label_land,df_comb,cmap, 1)
'''

   
def avh(y_label,df,cmap):   #avhrr before modis period
    y_pred_avh = np.empty(0)
    dict_place = {0: 'Bastrow', 1: 'Gobabeb', 2: 'Rooibank', 3: 'Zin'}
    for i in range(0,4):
        if i == 0 or i == 3:
            for year in range(1981, 2002):
                Slice=df.loc[(df['location'] == dict_place[i]),  
    
                                       ["year"]]
            
                lis = list(Slice['year'])
                if year in lis:
                    y_pred_avh =np. append( y_pred_avh,1)
                else:
                    y_pred_avh =np. append( y_pred_avh,0)
        elif i == 1 or i == 2:
            for year in range(1981, 2002):
                Slice=df.loc[(df['location'] == dict_place[i]),  
    
                                       ["year"]]
            
                lis = list(Slice['year'])
                if year in lis :
                    y_pred_avh =np. append( y_pred_avh,1)
                else:
                    y_pred_avh =np. append( y_pred_avh,0)

    list_accur = cf_matrix(y_label_pre_avh, y_pred_avh,cmap)
    return list_accur

def after(y_label,df,cmap):   #avhrr and landsat in modis period
    y_pred_avh = np.empty(0)
    dict_place = {0: 'Bastrow', 1: 'Gobabeb', 2: 'Rooibank', 3: 'Zin'}
    for i in range(0,4):
        if i == 0 or i == 3:
            for year in range(2001, 2022):
                Slice=df.loc[(df['location'] == dict_place[i]),  
    
                                       ["year"]]
            
                lis = list(Slice['year'])
                if year in lis:
                    y_pred_avh =np. append( y_pred_avh,1)
                else:
                    y_pred_avh =np. append( y_pred_avh,0)
        elif i == 1 or i == 2:
            for year in range(2001, 2012):
                Slice=df.loc[(df['location'] == dict_place[i]),  
    
                                       ["year"]]
            
                lis = list(Slice['year'])
                if year in lis :
                    y_pred_avh =np. append( y_pred_avh,1)
                else:
                    y_pred_avh =np. append( y_pred_avh,0)

    list_accur = cf_matrix(y_label_after, y_pred_avh,cmap)
    return list_accur

def mod(y_label,df,cmap):
    y_pred_mod = np.empty(0)
    dict_place = {0: 'Bastrow', 1: 'Gobabeb', 2: 'Rooibank', 3: 'Zin'}
    for i in range(0,4):
        if i == 0 or i == 3:
            for year in range(2001, 2022):
                Slice=df.loc[(df['location'] == dict_place[i]),  
    
                                       ["year"]]
            
                lis = list(Slice['year'])
                if year in lis :
                    y_pred_mod =np. append( y_pred_mod,1)
                else:
                    y_pred_mod =np. append( y_pred_mod,0)
        elif i == 1 or i == 2:
            for year in range(2001, 2012):
                Slice=df.loc[(df['location'] == dict_place[i]),  
    
                                       ["year"]]
            
                lis = list(Slice['year'])
                if year in lis :
                    y_pred_mod =np. append( y_pred_mod,1)
                else:
                    y_pred_mod =np. append( y_pred_mod,0)

    list_accur = cf_matrix(y_label_mod, y_pred_mod,cmap)
    return list_accur

def land(y_label,df,cmap):
    y_pred_land = np.empty(0)
    dict_place = {0: 'Bastrow', 1: 'Gobabeb', 2: 'Rooibank', 3: 'Zin'}
    for i in range(0,4):
        if i == 0 or i == 3:
            for year in range(1985, 2002):
                Slice=df.loc[(df['location'] == dict_place[i]),  
    
                                       ["year"]]
            
                lis = list(Slice['year'])
                if year in lis :
                    y_pred_land =np. append( y_pred_land,1)
                else:
                    y_pred_land =np. append( y_pred_land,0)
        elif i == 1 or i == 2:
            for year in range(1985, 2002):
                Slice=df.loc[(df['location'] == dict_place[i]),  
    
                                       ["year"]]
            
                lis = list(Slice['year'])
                if year in lis :
                    y_pred_land =np. append( y_pred_land,1)
                else:
                    y_pred_land =np. append( y_pred_land,0)

    list_accur = cf_matrix(y_label_pre_land, y_pred_land,cmap)
    return list_accur
#plot all the matrix together for MODIS period:
df_accur = pd.DataFrame()
df_accur_pre = pd.DataFrame()
            
fig, ((ax1, ax2, ax3), (ax4, ax5, ax6), (ax7, ax8, ax9)) = plt.subplots(3,3,sharex=True, sharey=True, figsize=(10,9))                
for i in range(1,9):
    plt.subplot(3, 3, i)
    
    if i == 1:
        cmap = 'Greens'
        list_accur = mod(y_label_mod,dict_df_fourier[1],cmap )
        df_accur['MODIS'] =  list_accur
    if i == 2:
        cmap = 'Reds'
        list_accur = after(y_label_after,dict_df_fourier[2],cmap )
        df_accur['LANDSAT'] =  list_accur
    if i == 3:
        cmap = 'Blues'
        list_accur = after(y_label_after,dict_df_fourier[3],cmap )
        df_accur['AVHRR'] =  list_accur
    if i == 4:
        cmap = 'Greens'
        list_accur = mod(y_label_mod,dict_df_fourier[4],cmap )
        df_accur['MODIS2'] =  list_accur
    if i == 5:
        cmap = 'Reds'
        list_accur = after(y_label_after,dict_df_fourier[5],cmap )
        df_accur['LANDSAT2'] =  list_accur
    if i == 6:
        cmap = 'Blues'
        list_accur = after(y_label_after,dict_df_fourier[6],cmap )
        df_accur['AVHRR2'] =  list_accur
    if i == 7:
        cmap = 'Greens'
        list_accur = mod(y_label_mod,dict_df_fourier[7],cmap )
        df_accur['MODIS3'] =  list_accur
    if i == 8:
        cmap = 'Reds'
        list_accur = after(y_label_after,dict_df_fourier[8],cmap )
        df_accur['LANDSAT3'] =  list_accur
 
    
#plot all the matrix together for pre-MODIS period:
         
fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3,2,sharex=True, sharey=True, figsize=(10,9))
for i in range(1,6):
    plt.subplot(3, 2, i)
    
    if i == 1:
        cmap = 'Reds'
        list_accur = land(y_label_pre_land,dict_df_fourier_pre[1],cmap )
        df_accur_pre['LANDSAT'] =  list_accur
    if i == 2:
        cmap = 'Blues'
        list_accur = avh(y_label_pre_avh,dict_df_fourier_pre[2],cmap )
        df_accur_pre['AVHRR'] =  list_accur
    if i == 3:
        cmap = 'Reds'
        list_accur = land(y_label_pre_land,dict_df_fourier_pre[3],cmap )
        df_accur_pre['LANDSAT2'] =  list_accur
    if i == 4:
        cmap = 'Blues'
        list_accur = avh(y_label_pre_avh,dict_df_fourier_pre[4],cmap )
        df_accur_pre['AVHRR2'] =  list_accur
    if i == 5:
        cmap = 'Reds'
        list_accur = land(y_label_pre_land,dict_df_fourier_pre[5],cmap )
        df_accur_pre['LANDSAT3'] =  list_accur
    
##############################################################################

###################################
#######THE BEST MODEL EVER#########
###################################

df_bf_overlap_1 = pd.DataFrame()
df_bf_overlap_2 = pd.DataFrame()


##MODIS period:
    
#good accuracy:
df_best1 = dict_df_fourier[4]
df_best1 = df_best1[['year', 'volume','duration','volume_pred','duration_pred', 'satellite','location']]
df_best1 = df_best1.reset_index(drop ='True')


#good r^2:
df_best2 = dict_df[7]
df_best2 = df_best2[['year', 'volume','duration','volume_pred','duration_pred', 'satellite','location']]
df_best2 = df_best2.reset_index(drop ='True')

list_idx_overlap =[]
ra1 = len(df_best1)
ra2 = len(df_best2)
for c in range(0,ra1):
    for i in range(0,ra2):
        if df_best1.iloc[c]['year'] == df_best2.iloc[i]['year'] and df_best1.iloc[c]['location'] == df_best2.iloc[i]['location']:
           df_best1 = df_best1.replace({df_best1.iloc[c]['volume_pred']: df_best2.iloc[i]['volume_pred'], df_best1.iloc[c]['duration_pred']: df_best2.iloc[i]['duration_pred']})
           
           
           df_bf_overlap_1 =df_bf_overlap_1.append(df_best2.iloc[i])
           list_idx_overlap.append(i)
        else:
        
            continue
df_bf_1 = df_best2
df_bf_1.drop(list_idx_overlap, axis=0, inplace=True)

df_best_modis_both = [df_best1,df_bf_1]
df_best_modis_both = pd.concat(df_best_modis_both) 


'''        
for i in list_idx:
    df_best2.drop([i], inplace=True)

df= [df_best1,df_best2]
df_best1 = pd.concat(df)
'''
df_best1['volume_pred'][df_best1['volume_pred'] < 0] = 0
df_best1['duration_pred'][df_best1['duration_pred'] < 0] = 0

df_best_modis_both['volume_pred'][df_best_modis_both['volume_pred'] < 0] = 0
df_best_modis_both['duration_pred'][df_best_modis_both['duration_pred'] < 0] = 0

colors_ndvi = {'Bastrow':'darkgreen', 'Gobabeb':'forestgreen', 'Rooibank':'limegreen', 'Zin':'palegreen'}
colors_msavi = {'bas':'saddlebrown', 'gob':'chocolate', 'roi':'sandybrown', 'zin':'peachpuff'}
colors_ndwi = {'bas':'navy', 'gob':'royalblue', 'roi':'cornflowerblue', 'zin':'skyblue'}
color_best = {'Bastrow':'black', 'Gobabeb':'dimgray', 'Rooibank':'darkgray', 'Zin':'silver'}

for char in char_list:
    
    d= df_bf_1
    x = d[char+"_pred"]
    y= d[char]
    
    slope, intercept, r_value, p_value, std_err = stats.linregress(x,y) 
    r2 =  round(r_value**2,3)
    y_pred = intercept + slope * x
    rmse = mean_squared_error(y_true=y, y_pred=y_pred, squared=False)
    
    fig, ax = plt.subplots( figsize=(6,5))
    ax = sns.regplot(x, y ,color="black", scatter_kws={'s':0}).set(title='01-21') #plot the regline only
    #sns.scatterplot(data=d, x="Magnitude", y="volume",hue="location",  s=100) #plot points in different color
    #sns.scatterplot(data=d, x="Magnitude", y="volume",hue="location", style ='satellite', s=100, legend=False) #plot points in different color and shapes
    ax = sns.scatterplot(data=d, x=char+"_pred", y=char,hue="location",  s=100,palette=color_best, style="satellite", markers={'mod':'o','land': '^' ,'avh':'s'})
    if char == 'volume':
        ax.set_xlabel('volume_pred (Mm$^3$/year)', fontsize = 16,**dfont)
        ax.set_ylabel('Volume_obs (Mm$^3$/year)', fontsize = 16,**dfont);
        
    elif char == 'duration':
         ax.set_xlabel('Duration_pred (days/year)', fontsize = 16,**dfont)
         ax.set_ylabel('Duration_obs (days/year)', fontsize = 16,**dfont);
    #ax.set(xlabel=None)
    #ax.set(ylabel=None)
    
    #ax.set_ylim(1, 175)
    #ax.set_xlim(1, 175)
    #set(xlim=(0,int(df_best1['volume'].max())))
    #ax.set_xticks(range(0,int(df_best1['volume'].max())))
    ax.xaxis.set_tick_params(labelsize=12)
    ax.yaxis.set_tick_params(labelsize=12)
    
    
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    textstr = '\n'.join((
    "R$^2$={:.2f}".format(r2),
    "RMSE={:.2f}".format(rmse)
    ))
    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=12,**dfont,
    verticalalignment='top', bbox=props)
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles=handles[1:5], labels=labels[1:5],loc='lower right', fontsize=10)
    
    if char == 'volume':
        ax.plot([0, int(d['volume_pred'].max())+10], [0, int(d['volume_pred'].max())+10], linewidth=1.5, ls="--", color = 'black', alpha = 0.7)
        
    elif char == 'duration':
        ax.plot([0, int(d['duration_pred'].max())+3], [0, int(d['duration_pred'].max())+3], linewidth=1.5, ls="--", color = 'black', alpha = 0.7)

#################################################################################
###PRE-MODIS period:

#good accuracy:
list_idx_overlap2 = []
df_best4 = dict_df_fourier_pre[3]
df_best4 = df_best4[['year', 'volume','duration','volume_pred','duration_pred', 'satellite','location']]
df_best4 = df_best4.reset_index()

#good r^2 volume:
df_best5 = dict_df_pre[2]
df_best5 = df_best5[['year', 'volume','duration','volume_pred','duration_pred', 'satellite','location']]
df_best5 = df_best5.reset_index()


for c in range(0,len(df_best4)):
    for i in range(0,len(df_best5)):
        if df_best4.iloc[c]['year'] == df_best5.iloc[i]['year'] and df_best4.iloc[c]['location'] == df_best5.iloc[i]['location']:
           df_best4 = df_best4.replace({df_best4.iloc[c]['volume_pred']: df_best5.iloc[i]['volume_pred']  })
           df_bf_overlap_2 =df_bf_overlap_2.append(df_best5.iloc[i])
           list_idx_overlap2.append(i)
        else:
          
            continue
df_bf_2 = df_best5
df_bf_2.drop(list_idx_overlap2, axis=0, inplace=True)

df_best_pre_modis_both = [df_best4,df_bf_2]
df_best_pre_modis_both = pd.concat(df_best_pre_modis_both) 

'''
#good r^2 duration:
df_best6 = dict_df_pre[2]
df_best6 = df_best6[['year', 'volume','duration','volume_pred','duration_pred', 'satellite','location']]
df_best6 = df_best6.reset_index()


        
for c in range(0,len(df_best4)):
    for i in range(0,len(df_best6)):
        if df_best4.iloc[c]['year'] == df_best6.iloc[i]['year'] and df_best4.iloc[c]['location'] == df_best6.iloc[i]['location']:
           df_best4 = df_best4.replace({ df_best4.iloc[c]['duration_pred']: df_best6.iloc[i]['duration_pred']})
        else:
            continue
'''
        
df_best4['volume_pred'][df_best4['volume_pred'] < 0] = 0
df_best4['duration_pred'][df_best4['duration_pred'] < 0] = 0

df_best5['volume_pred'][df_best5['volume_pred'] < 0] = 0
df_best5['duration_pred'][df_best5['duration_pred'] < 0] = 0

df_best_pre_modis_both['volume_pred'][df_best_pre_modis_both['volume_pred'] < 0] = 0
df_best_pre_modis_both['duration_pred'][df_best_pre_modis_both['duration_pred'] < 0] = 0 

#df_best4.drop([1], inplace=True)
colors_ndvi = {'Bastrow':'darkgreen', 'Gobabeb':'forestgreen', 'Rooibank':'limegreen', 'Zin':'palegreen'}
colors_msavi = {'bas':'saddlebrown', 'gob':'chocolate', 'roi':'sandybrown', 'zin':'peachpuff'}
colors_ndwi = {'bas':'navy', 'gob':'royalblue', 'roi':'cornflowerblue', 'zin':'skyblue'}
color_best = {'Bastrow':'black', 'Gobabeb':'dimgray', 'Rooibank':'darkgray', 'Zin':'silver'}

for char in char_list:
    
    d= df_best5
    x = d[char+"_pred"]
    y= d[char]

    slope, intercept, r_value, p_value, std_err = stats.linregress(x,y) 
    r2 =  round(r_value**2,3)
    y_pred = intercept + slope * x
    rmse = mean_squared_error(y_true=y, y_pred=y_pred, squared=False)
    
    fig, ax = plt.subplots( figsize=(6,5))
    ax = sns.regplot(x, y ,color="black", scatter_kws={'s':0}).set(title='81-01') #plot the regline only
    #sns.scatterplot(data=d, x="Magnitude", y="volume",hue="location",  s=100) #plot points in different color
    #sns.scatterplot(data=d, x="Magnitude", y="volume",hue="location", style ='satellite', s=100, legend=False) #plot points in different color and shapes
    ax = sns.scatterplot(data=d, x=char+"_pred", y=char,hue="location",  s=100,palette=color_best, style="satellite", markers={'mod':'o','land': '^' ,'avh':'s'})
    if char == 'volume':
        ax.set_xlabel('volume_pred (Mm$^3$/year)', fontsize = 16,**dfont)
        ax.set_ylabel('Volume_obs (Mm$^3$/year)', fontsize = 16,**dfont);
        
    elif char == 'duration':
         ax.set_xlabel('Duration_pred (days/year)', fontsize = 16,**dfont)
         ax.set_ylabel('Duration_obs (days/year)', fontsize = 16,**dfont);
    #ax.set(xlabel=None)
    #ax.set(ylabel=None)
    
    #ax.set_xlim(1, 175)
    #set(xlim=(0,int(df_best1['volume'].max())))
    #ax.set_xticks(range(0,int(df_best1['volume'].max())))
    ax.xaxis.set_tick_params(labelsize=12)
    ax.yaxis.set_tick_params(labelsize=12)
    
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    textstr = '\n'.join((
    "R$^2$={:.2f}".format(r2),
    "RMSE={:.2f}".format(rmse)
    ))
    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=12,**dfont,
    verticalalignment='top', bbox=props)
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles=handles[1:5], labels=labels[1:5],loc='lower right', fontsize=10)
    
    if char == 'volume':
        ax.plot([0, int(d['volume_pred'].max())+10], [0, int(d['volume_pred'].max())+10], linewidth=1.5, ls="--", color = 'black', alpha = 0.7)
        
    elif char == 'duration':
        ax.plot([0, int(d['duration_pred'].max())+3], [0, int(d['duration_pred'].max())+3], linewidth=1.5, ls="--", color = 'black', alpha = 0.7)

#################################################################################
###all years
df_best_all=[df_best_modis_both, df_best_pre_modis_both]
df_best_all = pd.concat(df_best_all)  

df_best_all = df_best_all[df_best_all['satellite'] != 'land']
df_bf_all=[df_bf_1, df_bf_2]
df_bf_all = pd.concat(df_bf_all)  
    
for char in char_list:
    
    d= df_best_all
    x = d[char+"_pred"]
    y= d[char]
    
    slope, intercept, r_value, p_value, std_err = stats.linregress(x,y) 
    r2 =  round(r_value**2,3)
    y_pred = intercept + slope * x
    equation = str(round(intercept,2))+' + '+ str(round(slope,2))+'x'
    rmse = mean_squared_error(y_true=y, y_pred=y_pred, squared=False)
    nse = calc_nse(y, y_pred)
    
    fig, ax = plt.subplots( figsize=(8,7))
    ax = sns.regplot(x, y ,color="black", scatter_kws={'s':0}).set(title='81-21') #plot the regline only
    #sns.scatterplot(data=d, x="Magnitude", y="volume",hue="location",  s=100) #plot points in different color
    #sns.scatterplot(data=d, x="Magnitude", y="volume",hue="location", style ='satellite', s=100, legend=False) #plot points in different color and shapes
    ax = sns.scatterplot(data=d, x=char+"_pred", y=char,hue="location",  s=200,palette=color_best) #, style="satellite", markers={'mod':'^','land': '^' ,'avh':'o'}
    if char == 'volume':
        ax.set_xlabel('volume_pred (Mm$^3$/year)', fontsize = 22,**dfont)
        ax.set_ylabel('Volume_obs (Mm$^3$/year)', fontsize = 22,**dfont);
        
    elif char == 'duration':
         ax.set_xlabel('Duration_pred (days/year)', fontsize = 22,**dfont)
         ax.set_ylabel('Duration_obs (days/year)', fontsize = 22,**dfont);
    #ax.set(xlabel=None)
    #ax.set(ylabel=None)
    
    #ax.set_xlim(1, 175)
    #set(xlim=(0,int(df_best1['volume'].max())))
    #ax.set_xticks(range(0,int(df_best1['volume'].max())))
    ax.xaxis.set_tick_params(labelsize=20)
    ax.yaxis.set_tick_params(labelsize=20)

    
    #props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    textstr = '\n'.join((
    "R$^2$={:.2f}".format(r2),
    "RMSE={:.2f}".format(rmse) #,
    #"NSE={:.2f}".format(nse),
    #equation
    ))
    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=20,**dfont,
    verticalalignment='top', bbox=props)
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles=handles[1:5], labels=labels[1:5],loc='lower right', fontsize=14)
    
    if char == 'volume':
        ax.plot([0, int(d['volume_pred'].max())+10], [0, int(d['volume_pred'].max())+10], linewidth=1.5, ls="--", color = 'black', alpha = 0.7)
        
    elif char == 'duration':
        ax.plot([0, int(d['duration_pred'].max())+3], [0, int(d['duration_pred'].max())+3], linewidth=1.5, ls="--", color = 'black', alpha = 0.7)

###################
#CM all

def al(y_label,df,cmap):   #all years
    y_pred_avh = np.empty(0)
    dict_place = {0: 'Bastrow', 1: 'Gobabeb', 2: 'Rooibank', 3: 'Zin'}
    for i in range(0,4):
        if i == 0 or i == 3:
            for year in range(1981, 2022):
                Slice=df.loc[(df['location'] == dict_place[i]),  
    
                                       ["year"]]
            
                lis = list(Slice['year'])
                if year in lis:
                    y_pred_avh =np. append( y_pred_avh,1)
                else:
                    y_pred_avh =np. append( y_pred_avh,0)
        elif i == 1 or i == 2:
            for year in range(1981, 2012):
                Slice=df.loc[(df['location'] == dict_place[i]),  
    
                                       ["year"]]
            
                lis = list(Slice['year'])
                if year in lis :
                    y_pred_avh =np. append( y_pred_avh,1)
                else:
                    y_pred_avh =np. append( y_pred_avh,0)

    list_accur = cf_matrix(y_label_all, y_pred_avh,cmap)
    return list_accur

final_accur = al(y_label_all, df_best_all, 'Greys')
 
 
'''   
dict_place = {0: 'Bastrow', 1: 'Gobabeb', 2: 'Rooibank', 3: 'Zin'}
for i in range(0,4):
    Slice1=df_best1.loc[(df_best1['location'] == dict_place[i]),  
    
                                       ["year"]]
    lis1 = list(Slice1['year'])
    Slice2=df_best2.loc[(df_best2['location'] == dict_place[i]),  
    
                                     ["year"]]
    lis2 = list(Slice2['year']) 
    for y in lis1:
        if y in lis2:
            
            
df_best1.loc[df_best1.year.isin(df_best2.year), ['volume_pred', 'duration_pred']] = df_best2[['volume_pred', 'duration_pred']]
'''    

sum_all = hydro_all.groupby(['location']).sum()

list_accur = mod(y_label_mod,dict_df_fourier[4],cmap )
