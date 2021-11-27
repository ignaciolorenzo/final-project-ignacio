# **Real Estate investing. A data driven approach to buy & rent operations.**

## 0. Why are we here:
**Problem:**
Lack of structured granular data* impedes having a data driven approach to Real Estate investing for individual investors. 

**Solution:**
Structure online available data so users can make data-driven decisions in their Real Estate investments.

**Approach:**
Web scraping data from RE directories to find the obtain:
1. Predicted profitabilities for listed properties
2. Scarcity of properties for rent
So investors can decide where to invest and which kind of properties to look for.

## 1. Data:
We have two different types of data:
- Properties data
- Geographical data

### 1.1. Properties data:
In this project we scrape website data from a relevant spanish Real Estate directory. We get data from properties listed for rent and for sale.
- For rent data: we will use it to train a model that predicts rent prices.
- For sale data: we will predict the rent price for properties for sale to then calculate the predicted profitabilities.

### 1.1.1. Relevant aspects of how the data is gathered:
Properties are extracted from the RE website. Not all properties have all the features that the model is trained on, so the dataset size is sacrified for the sake of improving the information we have about each property. Properties with insufficient information are excluded from the dataset which trains the model.

Also, a feature is generated to improve our model: 'hood_price_m2'. We calculate the average price per sqm for each neighborhood, a feature which will help us predict rent prices.

### 1.1.2. Data cleaning:
The data cleaning of the data we work with includes:
- Filtering out towns in which there are less than 10 listed properties.
- Replacing nulls if possible or droping rows with null values if they are not replaceable.
- Converting object columns to numericals for those cases in which the import reads values as dtypes other than ints.

## 1.2. Geographical data:
To get accurate geographical data we combine information from CCAA, provinces and towns gathered from the spanish statistics national institute, INE (https://www.ine.es/daco/daco42/codmun/cod_ccaa_provincia.htm).

Then, we merge it with the towns that have properties listed in the RE website.

