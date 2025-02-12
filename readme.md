`ChangeDotOrgScraper` is an Python package that allows you to scrape online petition data from [change.org](https://www.change.org/).

[![pypi package](https://img.shields.io/badge/pypi_package-v0.0.9-brightgreen)](https://pypi.org/project/ChangeDotOrgScraper/) [![GitHub Source Code](https://img.shields.io/badge/github_source_code-source_code?logo=github&color=green)](https://github.com/cja5553/change_org_scraper) 



## Installation
To install in python, simply do the following: 
```bash
pip install ChangeDotOrgScraper
```

## Quick Start
Here we provide a quick example on how you can use `ChangeDotOrgScraper` to scrape petition data right from [change.org](https://www.change.org/). 

```python
from ChangeDotOrgScraper import scrape_petitions

# Specify the url of your scrape.org searches
## for instance, we shall scrape petitions from the search "supplemental nutrition assistance program"
url='https://www.change.org/search?q=Supplemental%20Nutrition%20Assistance%20Program&offset=0'

# scrape the petition data from change.org
SNAP_petitions_df=scrape_petitions(url)
print(SNAP_petitions_df)
```
It returns a dataframe with all the petitions data, which contains details such as the petition(s) title, description, date created, target audience signature count, location created, victory status, etc. 



## Requirements
### Required packages
To use `ChangeDotOrgScraper`, you are required to have the following packages installed:  
- `requests`
- `beautifulsoup4`    
- `tqdm`    
- `pandas`  
- `ast` (Python standard library)   
- `re` (Python standard library)   
- `json`  (Python standard library)  

If you do not have these packages installed in python, you can do the following:
```bash
pip install requests beautifulsoup4 tqdm pandas
```


## Citation
This package was made as part of a larger study on food stamps (i.e., SNAP), therefore, we do not have the paper ready just yet. 

However, if you wish to cite, you may cite:

C Alba (2024) `ChangeDotOrgScraper`: A python package to scrape petition data from change.org. PyPi. 

## Questions?
Contact me at [alba@wustl.edu](mailto:alba@wustl.edu)
