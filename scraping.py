# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    news_title, news_paragraph = mars_news(browser)
    # Run all scraping functions and store results in dictionary
    data = {
      "news_title": news_title,
      "news_paragraph": news_paragraph,
      "featured_image": featured_image(browser),
      "facts": mars_facts(),
      "hemisphere" : hemispheres(browser),
      "last_modified": dt.datetime.now()
    }
    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
    
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)
    # Convert the browser to html to a soup object and then quit browswer
    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    try:
        slide_elem = news_soup.select_one('div.list_text')

        slide_elem.find('div', class_='content_title')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        news_title

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
        news_p
    except AttributeError:
        return None, None    
    return news_title, news_p



# Function to get image
def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    try:

        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        
    except AttributeError:
        return None    

        # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
        
    return img_url
        
# Function to get Mars Facts

def mars_facts():
    try:
        # use 'read_html" to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None
    
    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)
    
    # Covert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

# Function to get images of four Mars hemispheres
def hemispheres(browser):
    # Visit URL for the different hemispheres of Mars
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # Index the website to make it easier to find the right tags
    browser.visit(url + 'index.html')

    # Create empy list variable and empty dictionary for image url and titles
    hemisphere_list = []
    web_pair = {}

    # Loop through images by finding links - 
    # Scrape full resolution image and title
    # store image link and title pair in dictionary
    # return to main webiste
    # Append dictionary to list
    for i in range (4):
        browser.find_by_css("a.product-item img")[i].click()
        html = browser.html
        img = soup(html, 'html.parser') 
        image_url_rel = img.find('img', class_='wide-image').get('src')
        full_url = f'https://marshemispheres.com/{image_url_rel}'
        title = img.find('h2', class_='title').text
        browser.back()
        web_pair = {}
        web_pair['img_url']= full_url
        web_pair['title'] = title
        hemisphere_list.append(web_pair)

    return(hemisphere_list)






if __name__ == "__main__":
    
    # If running as script, print scraped data
    print(scrape_all())