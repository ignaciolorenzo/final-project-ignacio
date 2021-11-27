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

## 1.2. Geographical data:
To get accurate geographical data we combine information from CCAA, provinces and towns gathered from the spanish statistics national institute, INE (https://www.ine.es/daco/daco42/codmun/cod_ccaa_provincia.htm).
