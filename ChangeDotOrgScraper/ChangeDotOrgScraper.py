import requests
from bs4 import BeautifulSoup
import json
from tqdm import tqdm
import re
import pandas as pd
import ast


def get_soup(url):
    '''
    Gets BeautifulSoup object from the url provided by the user. 
    
    Paramters:
    - url (str): url link provided by the user

    Returns:
    - soup (BeautifulSoup obj): A beautiful object of the url provided by the user. 
    '''
    if url.endswith("&offset=0"):
        url=url[:url.find("offset=")]
        url=url+"offset="
    elif url.endswith("&offset="):
        url=url
    else:
        url=url+"&offset="
        
    # Send a GET request to the URL
    response = requests.get(url+"0")
    try:
        # Parse the HTML content of the page with Beautiful Soup
        soup = BeautifulSoup(response.text, 'html.parser')
    except:
         print("Please check the URL or change.org may have been updated such that this package is no long compatable") 
    return(soup)

def get_pages_no(soup):
    '''
    Determines the number of pages of worth of petitions within the change.org search. 

    Parameters:
    - soup (BeautifulSoup obj): A beautiful object of the existing page of in the change.org petition of interests

    Returns:
    - offset_nos (list): list of page numbers. 
    '''
    match = re.search(r'<div class="corgi-1weo53w">([\d,]+) results</div>', str(soup))

    if match:
        # Extract the matched group which contains the number of results
        num_results = match.group(1)
        # Optional: convert the string number to an integer, removing commas
        num_results_int = int(num_results.replace(',', ''))
        #print(num_results)  # This will print the string 
        #print(num_results_int)  # This will print the integer 
    else:
        print("No match found")
    offset=(num_results_int//10)*10
    offset_nos=[i for i in range(0,offset+10,10)]
    return(offset_nos)

def get_current_page(soup):
    '''
    Extracts all the petition and the corresponding creator information from the beautiful soup object. 

    Parameters:
    - soup (BeautifulSoup obj): A beautiful object of the existing page of in the change.org petition of interests

    Returns:
    - petition_info (list): a list of dictionaries containing all the information of the petitions within the existing change.org page.
    - creator_info (list): a list of dictionaries containing all the information of the corrresponding creators among the petitions within the existing change.org page. 
    '''
    filter_soup=soup.find('script', text=lambda t: '__HYDRATION_DATA__' in t)
    filter_soup=str(filter_soup)
    start_str_pos=filter_soup.find("\"prefetchedData\":{\"")
    end_str_pos=soup.find("}}}}")
    info=filter_soup[start_str_pos:end_str_pos]
    info=info.replace('</script>', '')
    info=info.replace('<script>', '')
    info=info.replace('__HYDRATION_DATA__=',"")
    
    pattern = r'\{"petition":\{"__typename":"Petition".*?"highlight"'

    # Find all instances in the text
    matches = re.findall(pattern, info, re.DOTALL)

    # Print matches
    lists_of_petitions=[]
    for match in (matches):
        lists_of_petitions.append(match)
    petition_info,creator_info=[],[]
    petition_info_pattern = r'\{"petition":\{"__typename":"Petition".*?\}\}'
    creator_info_pattern = r'"slug".*?"highlight"'
    
    for i in lists_of_petitions:
        petition_info.append(re.findall(petition_info_pattern, i, re.DOTALL))
        creator_info.append(re.findall(creator_info_pattern, i, re.DOTALL))
    petition_info=[item for sublist in petition_info for item in sublist]
    creator_info=[item for sublist in creator_info for item in sublist]
    
    for i in (range(len(lists_of_petitions))):
        petition_info[i]=petition_info[i].replace('false', 'False').replace('true', 'True').replace('null', 'None')
        petition_info[i]=ast.literal_eval(petition_info[i]+"}}")
        creator_info[i]=creator_info[i].replace(",\"highlight\"","")
        creator_info[i]="{"+creator_info[i]
#         print(creator_info[i])
        creator_info[i]= ast.literal_eval(creator_info[i].replace('false', 'False').replace('true', 'True').replace('null', 'None'))
    return(petition_info,creator_info)

def clean_info(petition_info, creator_info):
    '''
    Organizes and parses all each petition and creator information

    Parameters:
    - petition_info (list): a list of dictionaries of petitions with informations of all the petitions within a change.org page. 
    Each dictionary contains information for each petition, which was extracted from `get_current_page` function.
    - creator_info (list): a list of dictionaries with creator information from the corresponding petition in petition_info. 
    Each dictionary contains information for each creator of each corresponding petition, which was extracted from `get_current_page` function.

    Returns
    list_of_petitions (list): a list of dictionaries, with each dictionary containing information about the petition and creator from the list of petitions within one webpage. 
    These includes petition title, Description, signature count, creator name, date created, location createdd, and victory status. 
    '''
    list_of_petitions=[]
    for i,j in zip(petition_info,creator_info):
        petition_title=i["petition"]["ask"]
        petition_description=i["petition"]["description"]
        # petition_target=i["petition"]["targetingDescription"]
        petition_signatures=i["petition"]["signatureState"]["signatureCount"]["displayed"]
        petition_creator=j["user"]["displayName"]
        date_created=j['createdAt']
        location=j["user"]["formattedLocationString"]
        victory_verification_status=j['isVerifiedVictory']
        curr={"Petition title":petition_title,
             "Description":petition_description,
            #  "target":petition_target,
             "signature count":petition_signatures,
             "creator":petition_creator,
             "date created":date_created,
              "location created":location,
             "Victory verification status":victory_verification_status}
        list_of_petitions.append(curr)
    return(list_of_petitions)

def scrape_petitions(url):
    '''
    Scrapes all the petition and its corresponding details based on the url provided. 
    This encompasses going looping through all the pages automatically to extract ALL the petitions, not just the petitions listed within the page itself. 

    Parameters:
    - url (str): url from change.org upon searching for the list of petitions
    
    Returns:
    - data_of_petitions (pandas dataframe): dataset of petitions with all the relevant information, including 
    petition title, Description, target audience, signature count, creator name, date created, location createdd, and victory status. 
    '''
    soup=get_soup(url)
    # gets the list of page numbers. 
    pages=get_pages_no(soup)
    list_of_petitions=[]
    if url.endswith("&offset=0"):
        url=url[:url.find("offset=")]
        url=url+"offset="
    elif url.endswith("&offset="):
        url=url
    else:
        url=url+"&offset="
    # this for loop runs through all the pages and extracts the petitions.
    for (i) in tqdm(pages):
        #print(f"obtaining page {i} of {pages[-1]} pages")
        i=str(i)
        response = requests.get(url+i)
        try:
            # Parse the HTML content of the page with Beautiful Soup
            soup = BeautifulSoup(response.text, 'html.parser')
        except:
             print("Please check the URL or change.org may have been updated such that this package is no long compatable")
        petition_info,creator_info=get_current_page(soup)
        list_of_petitions+=clean_info(petition_info, creator_info)
    data_of_petitions=pd.DataFrame(list_of_petitions)
    return(data_of_petitions)
    
# example use case
# url = "https://www.change.org/search?q=Supplemental%20Nutrition%20Assistance%20Program&offset=0"
# SNAP_petitions=scrape_petitions(url)