import numpy as np
import pandas as pd
from bs4 import BeautifulSoup # this module helps in web scrapping.
import requests  # this module helps us to download a web page



def pd_read_html_test():
    URL="https://web.archive.org/web/20230902185326/https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29"

    tables = pd.read_html(URL)
    df = tables[3] # the required table will have index 2
    print(df)


# Use beautiful soup 

def ibm_test():
    url = "http://www.ibm.com" 
    data  = requests.get(url).text 
    soup = BeautifulSoup(data,"html.parser")  # create a soup object using the variable 'data'

    # Get all html links 
    for link in soup.find_all('a',href=True):
        print(link.get('href'))

    # Get all images 
    for link in soup.find_all('img'):
        print(link)
        print(link.get('src'))


def table_read():
    url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DA0321EN-SkillsNetwork/labs/datasets/HTMLColorCodes.html"
    data  = requests.get(url).text
    soup = BeautifulSoup(data,"html.parser")    

    table = soup.find('table')       # in html table is represented by the tag <table>    
    for row in table.find_all('tr'): # Get all rows in the table by looking for tag <tr>
        cols = row.find_all('td')    #    Find the cells with tag <td> 
        color_name = cols[2].string  #       third column has the color_name 
        color_code = cols[3].string  #       column 4 has the color_code
        print("{}--->{}".format(color_name,color_code))

pd_read_html_test()
ibm_test()  
table_read()  # Uncomment this line to run the table_read function