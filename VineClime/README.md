pyrus277gmail.com  
Capstone Project     
Updated 1/11/23  

VineClime is a project that models California wine production and flavor characteristics along with climate change in California wine producing regions.  Among its abilities, VineClime can identify the counties most sensitive to changing climate features and factors these features into a predictive time series models.  It also uses 25+ years of wine review text data and Natural Language Processing to see how climate features relate to the actual flavors consumers ascribe to wines.


#### The main project files are:  
- `1_Wrangling.ipynb`  
- `2_EDA.ipynb`  
- `3_Modeling.ipynb`  
They are intended to be read in that order.  
  
#### Not every cell in `1_Wrangling.ipynb` can be run, because there's some interplay with the web scrapers, and those take hours to complete. The web scrapers are:  
- scraper_google.py  
- scraper_winery_sage.py  
  
#### Simple webapp made with Streamlit to streamline the use of the Prophet model from the modeling notebook:
- forecast_webapp.py
To run this program, just navigate to its location on the command line and run: `$ streamlit run forecast_webapp.py`
    
#### For the shelve files to be brought in, the following must be in your working directory.  
 These shelve files were used in the web scraping in wrangling.ipynb:     
- wineries.bak  
- wineries.dat  
- wineries.dir  
 These shelve files hold the base dataframes for the analysis used in eda.ipynm and modeling.ipynb:  
- capstone_dataframes.bak  
- capstone_dataframes.dat  
- capstone_dataframes.dir  
    
#### Original Data Files:    
- Californa_Wine_Production_1980_2020.csv  
- winemag-data-130k-v2.csv  
- winemag-data-2017-2020.csv  
- county_climate folder includes individual climate data files  
  
#### Text files used to create the custom flavor word vocabularies are:  
- base_list.txt     
- selected_list.txt  
  
#### Report files include:  
- capstone_report.pdf  
- capstone_presentation.pdf  

