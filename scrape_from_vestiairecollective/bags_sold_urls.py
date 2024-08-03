import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from tqdm import tqdm


url = 'https://www.vestiairecollective.com/'
options = uc.ChromeOptions()
driver = uc.Chrome(options=options)

driver.get(url)
time.sleep(20)


with open('lv_urls.txt','a') as file:
  for i in tqdm(range(1,3)):                      
    #url = "https://us.vestiairecollective.com/women-bags/p-2/#categoryParent=Bags%235_gender=Women%231_localCountries=1_condition=Very%20good%20condition%233-Good%20condition%234-Never%20worn%232-Never%20worn%2C%20with%20tag%231_brand=Louis%20Vuitton%20x%20Yayoi%20Kusama%2316561"
    url = "https://us.vestiairecollective.com/women-bags/p-" + str(i) + "/#categoryParent=Bags%235_gender=Women%231_localCountries=1_condition=Very%20good%20condition%233-Good%20condition%234-Never%20worn%232-Never%20worn%2C%20with%20tag%231_brand=Louis%20Vuitton%20x%20Yayoi%20Kusama%2316561"
  
    
    driver.get(url)
    time.sleep(7)

    wait = WebDriverWait(driver, 10)
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "product-search_catalog__flexContainer__Dg0eL")))

    # Define the JavaScript code to scroll the page
    scroll_script = """
        window.scrollBy(0, window.innerHeight);
    """

    # Scroll the page slowly with a delay of 0.5 seconds between each scroll
    for _ in range(3):
        driver.execute_script(scroll_script)
        time.sleep(1)

    # Scroll to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

    # Wait for a moment to let the page load completely
    time.sleep(5)

    # Get the page source after waiting for dynamic content to load
    html_content = driver.page_source

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    ul = soup.find('ul', class_="product-search_catalog__flexContainer__Dg0eL")

    cards = ul.find_all('div', class_="product-card_productCard__BF_Iz product-search_catalog__productCardContainer__A2YBW")
    print(len(cards))
    for card in cards:
      sold = card.find('span', "product-card_productCard__image__soldText__h_2Si")
      if sold:
        # Find the <a> tag
        a_tag = card.find('a')
        # Extract the value of the href attribute
        href = a_tag['href']
        link = "https://www.vestiairecollective.com"+href
        file.write(link+"\n")

# Close the webdriver
driver.quit()