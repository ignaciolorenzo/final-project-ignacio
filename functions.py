import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
import pandas as pd
import math
from bs4 import BeautifulSoup
import requests
import nums_from_string as nfs
import numpy as np
from re import search
from random import randint
from time import sleep
import openpyxl
import xlrd
import lxml
from datetime import datetime, timedelta
from collections import Counter
import re
pd.options.mode.chained_assignment = None
import seaborn as sns
from scipy import stats

def filtering_big_cities(df):
    filter_dct = dict(df['geo_town'].value_counts(normalize=True).mul(100)>50)
    for k,v in filter_dct.items():
        if v == True:
            target_town = k
    return target_town

def clean_last_update(df, c):
    for i,n in enumerate(df[c]):
        try:
            df[c][i] = int(n)
        except:
            df[c][i] = int('0')
            
def checking_nulls(df):
    # This function shows which columns have null values and returns a df with only nulls
    for c in df.columns:
        null_count = df[c].isnull().sum()
        if null_count > 0:
            print ("The column ", c, " has ", null_count, " null values")
    

def convert_to_numerical(df, list = []):
    for l in list:
        df[l] = df[l].astype('int')

def cat_exploration(df):
    # This function displays the proportion of each value type for each categorical column and its countplot
    cat = df.select_dtypes('object')
    for c in cat.columns:
        sns.set_style("darkgrid")
        print(c)
        # print(cat[c].value_counts(normalize=True).mul(100).round(1))
        fig, axes = plt.subplots(1, 1, figsize=(7, 4))
        ax = sns.countplot(cat[c],
                      color = 'gray',
                      order = cat[c].value_counts().index)
        ax.set_xticklabels(ax.get_xticklabels(),rotation = 90)
        plt.show()

def countplot(df,c = ""):
    fig, axes = plt.subplots(1, 1, figsize=(14, 5))
    ax = sns.countplot(df[c],
                       color = 'gray',
                       order = df[c].value_counts().index)
    ax.set_xticklabels(ax.get_xticklabels(),rotation = 90)
    plt.show()

def num_exploration(df):
    # This column helps us understand how are our numerical columns distributed
    num = df.select_dtypes('number')
    for c in num.columns:
        print(c)
        fig, axes = plt.subplots(1, 2, figsize=(10, 3))
        sns.set_style("dark")
        # Distribution plot to check normality
        sns.distplot(num[c], ax=axes[0],  color = 'gray')
        # box plot to check outliers
        sns.boxplot(num[c], ax=axes[1],  color = 'gray')
        plt.show()

def clean_floors(df):
    for i,v in enumerate(df['floor']):
        if df['floor'][i] == '1':
            df['floor'][i] = 'first'
        elif df['floor'][i] == '2':
            df['floor'][i] = 'second'
        elif df['floor'][i] == '3':
            df['floor'][i] = 'third'
        elif df['floor'][i] == '4':
            df['floor'][i] = 'fourth'
        elif df['floor'][i] == '5':
            df['floor'][i] = 'fifth'
        else:
            df['floor'][i] = 'sixth_or_higher'

def clean_floors2(df, column):
    for i,v in enumerate(df[column]):
        if v != None:
            try: 
                int_v = int(v)
                if int_v == 1:
                    df[column][i] = 'first'
                elif int_v == 2:
                    df[column][i] = 'second'
                elif int_v == 3:
                    df[column][i] = 'third'
                elif int_v == 4:
                    df[column][i] = 'fourth'
                elif int_v == 5:
                    df[column][i] = 'fifth'
                elif int_v > 5:
                    df[column][i] = 'sixth_or_higher'
                else:
                    df[column][i] = "empty"
            except: 
                pass

        
def get_lift_from_property_url(df):
    counter = 0
    for i,p in enumerate(df['url']):
        if df['floor'][i] == "":
            counter +=1
            if i % 100 == 0:
                print(i) 
            sleep(randint(1,3))
            r = requests.get(p)
            soup = BeautifulSoup(r.content, 'html.parser')
            details = soup.find('section', attrs={'class': 'detail'})
            details = soup.find_all('article', attrs={'class': 'has-aside'})
            variable = str(details)
            try:
                floor_text = re.findall("Planta número\s\d+", variable)[0]
                floor_num = re.findall("\d+", floor_text)[0]
                df['floor'][i] = floor_num
            except:
                df['floor'][i] = None

lst_underground_floor = ['sótano', 'sotano', 'semi sotano', 'semi sótano', 'semisotano', 'semisótano']
lst_ground_floor = ['bajo', 'bajos']
lst_first_floor = ['primera planta', 'primer piso', 'primero']
lst_second_floor = ['segunda planta', 'segundo piso', 'segundo']
lst_third_floor = ['tercera planta', 'tercer piso', 'tercero']
lst_fourth_floor = ['cuarta planta', 'cuarto piso']
lst_fifth_floor = ['quinta planta', 'quinto piso', 'quinto']
lst_sixth_floor = ['sexta planta', 'sexto piso', 'sexto']
lst_seventh_floor = ['séptima planta', 'séptimo piso', 'séptimo', 'septima planta', 'septimo piso', 'septimo']
lst_eighth_floor = ['octava planta', 'octavo piso', 'octavo']
lst_ninth_floor = ['novena planta', 'noveno piso', 'noveno']
lst_tenth_floor = ['décima planta', 'décimo piso', 'décimo', 'décima planta', 'décimo piso', 'décimo']

list_floors = [lst_underground_floor, 
               lst_ground_floor,
               lst_first_floor,
               lst_second_floor,
               lst_third_floor,
               lst_fourth_floor,
               lst_fifth_floor,
               lst_sixth_floor,
               lst_seventh_floor,
               lst_eighth_floor,
               lst_ninth_floor,
               lst_tenth_floor]

def boxcox_transform(df):
    numeric_cols = df.select_dtypes(np.number).columns
    _ci = {column: None for column in numeric_cols}
    for column in numeric_cols:
        df[column] = np.where(df[column]<=0, np.NAN, df[column]) 
        df[column] = df[column].fillna(df[column].mean())
        transformed_data, ci = stats.boxcox(df[column])
        df[column] = transformed_data
        _ci[column] = [ci] 
    return df, _ci


def remove_outliers(df, threshold=1.5, in_columns = [], skip_columns=[]):
    for column in in_columns:
        if column not in skip_columns:
            upper = np.percentile(df[column],75)
            lower = np.percentile(df[column],25)
            iqr = upper - lower
            upper_limit = upper + (threshold * iqr)
            lower_limit = lower - (threshold * iqr)
            df = df[(df[column]>lower_limit) & (df[column]<upper_limit)]
    return df

def find_floor(df, column, key_words = []):
    for i,d in enumerate(df[column]):
        for kw in key_words:
            floor = re.findall(kw, d.lower())
            if len(floor) != 0:
                df['floor'][i] = floor
                if key_words == lst_underground_floor:
                    df['floor'][i] = "underground"
                elif key_words == lst_ground_floor:
                    df['floor'][i] = "ground"
                elif key_words == lst_first_floor:
                    df['floor'][i] = "first"
                elif key_words == lst_second_floor:
                    df['floor'][i] = "second"
                elif key_words == lst_third_floor:
                    df['floor'][i] = "third"
                elif key_words == lst_fourth_floor:
                    df['floor'][i] = "fourth"
                elif key_words == lst_fifth_floor:
                    df['floor'][i] = "fifth"
                else:
                    df['floor'][i] = "sixth_or_higher"

def fill_lift_column(df):
    return df['lift'].fillna('no', inplace = True)

def plot_numericals(df, title = "Title"):
    fig, axes = plt.subplots(nrows=3, ncols=4, figsize=(18, 9))
    axes = axes.flat
    numeric_columns = df.select_dtypes(include=['float64', 'int']).columns

    for i, column in enumerate(numeric_columns):
        ii = i+i
        ie = ii-1

        sns.histplot(
            data    = df,
            x       = column,
            stat    = "count",
            kde     = True,
            color   = (list(plt.rcParams['axes.prop_cycle'])*2)[i]["color"],
            line_kws= {'linewidth': 2},
            alpha   = 0.3,
            ax      = axes[ie]
        )

        sns.boxplot(
            data    = df,
            x       = column,
            color   = (list(plt.rcParams['axes.prop_cycle'])*2)[i]["color"],
            ax      = axes[ie-1]
        )

    fig.tight_layout()
    plt.subplots_adjust(top = 0.9)
    fig.suptitle(title, fontsize = 12, fontweight = "bold")
    
def plot_categorical(df, title = "title", delete_n = [5]):
    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(22, 10))
    axes = axes.flat
    categorical_columns = df.select_dtypes(include=['object']).columns

    for i, column in enumerate(categorical_columns):
        ax = sns.countplot(
                data    = df,
                x       = column,
                color   = (list(plt.rcParams['axes.prop_cycle'])*2)[i]["color"],
                alpha   = 0.3,
                ax      = axes[i],
                order = df[column].value_counts().index,

            )
        axes[i].set_xticklabels(ax.get_xticklabels(),rotation = 90)
        axes[i].set_title(column, fontsize = 12)
        axes[i].tick_params(labelsize = 12)
        axes[i].set_xlabel("")

    plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=0.5)
    plt.subplots_adjust(top = 0.9)
    fig.suptitle(title, fontsize = 12, fontweight = "bold")
    
    for i in delete_n:
        fig.delaxes(axes[i])
        
def model_plots(test_df, title = ""):
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 8))

    sns.histplot(
        x = test_df.sort_values(by="reg_difference_%", ascending=False)['reg_difference_%'],
        stat = "count",
        kde = True,
        color = "b",
        line_kws= {'linewidth': 2},
        alpha = 0.3,
        ax = axes[0,0]
    )
    sns.histplot(
        x = test_df.sort_values(by="rf_difference_%", ascending=False)['rf_difference_%'],
        stat = "count",
        kde = True,
        color = "b",
        line_kws= {'linewidth': 2},
        alpha = 0.3,
        ax = axes[0,1]
    )
    sns.residplot(
        x=test_df.price, 
        y=test_df['reg_difference_%'], 
        lowess=True, 
        color="b",
        ax = axes[1,0]
    )
    sns.residplot(
        x=test_df.price, 
        y=test_df['rf_difference_%'], 
        lowess=True, 
        color="b",
        ax = axes[1,1]
    )

    fig.tight_layout()
    plt.subplots_adjust(top=0.9)
    fig.suptitle(title, fontsize = 12, fontweight = "bold");