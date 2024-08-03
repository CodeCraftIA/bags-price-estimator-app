import undetected_chromedriver as uc
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common import TimeoutException
import time
from tqdm import tqdm
import re
import pandas as pd
import xlsxwriter
import requests
import urllib.request
import os

options = uc.ChromeOptions()
driver = uc.Chrome(options=options)

url = "https://www.vestiairecollective.com/"

driver.get(url)

time.sleep(30)

#URL convert to imgbb url
'''
def upload_image_to_imgbb(image_path, api_key):
    """
    Uploads an image file to imgbb and returns the URL of the uploaded image.

    Args:
        image_path (str): The path to the image file.
        api_key (str): The API key for imgbb.

    Returns:
        str: The URL of the uploaded image.
    """
    try:
        # Prepare the upload URL and parameters
        upload_url = "https://api.imgbb.com/1/upload"
        files = {"image": (image_path, open(image_path, "rb"))}
        params = {"key": api_key}

        response = requests.post(upload_url, files=files, params=params)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Extract the URL of the uploaded image from the response JSON
            uploaded_url = response.json()['data']['url']
            return uploaded_url
        else:
            print(f"Image upload failed: {response.text}")
            return ""
    except Exception as e:
        print(f"Error uploading image to imgbb: {e}")
        return ""

def image_url_from_url(original_url, api_key):
    """
    Uploads an image from a given URL to imgbb and returns its URL.
    
    Args:
        original_url (str): The URL of the original image.
        api_key (str): The API key for imgbb.

    Returns:
        str: The URL of the uploaded image.
    """
    try:
        headers = {
            'Sec-Ch-Ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
        }
        # Create a request with headers to mimic a browser request
        request = urllib.request.Request(original_url, headers=headers)
        
        # Open the URL and read the image content
        with urllib.request.urlopen(request) as response:
            image_content = response.read()
        
        # Prepare a temporary file with a .jpg extension
        temp_image_path = "temp_image.jpg"
        
        # Write the image content to the temporary file
        with open(temp_image_path, "wb") as file:
            file.write(image_content)
        
        # Upload the image to imgbb
        uploaded_url = upload_image_to_imgbb(temp_image_path, api_key)
        
        # Remove the temporary image file
        os.remove(temp_image_path)
        
        return uploaded_url
    except Exception as e:
        print(f"Error converting image URL: {e}")
        return ""
'''
#URL of image convert to image file
def image_from_url(original_url, index):
    """
    Downloads an image from a given URL and saves it to a file.
    
    Args:
        original_url (str): The URL of the original image.
        index (int): The index number to be added to the filename.

    Returns:
        str: The filename of the downloaded image if successful, otherwise an empty string.
    """
    try:
        headers = {
            'Sec-Ch-Ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
        }
        # Create a request with headers to mimic a browser request
        request = urllib.request.Request(original_url, headers=headers)
        
        # Open the URL and read the image content
        with urllib.request.urlopen(request) as response:
            image_content = response.read()
        
        filename = f"lv{index}.jpg"
        # Prepare a temporary file with a .jpg extension
        temp_image_path = os.path.join("lv_bags", filename)
        
        # Write the image content to the temporary file
        with open(temp_image_path, "wb") as file:
            file.write(image_content)
        
        # Check if the file was successfully created
        if os.path.exists(temp_image_path):
            return filename  # Return the filename if the image was generated successfully
        else:
            print("Error: Image file was not created.")
            return ""  # Return an empty string if the file was not created
        
    except Exception as e:
        print(f"Error converting URL to image: {e}")
        return ""


def scrape(url, index):
    time.sleep(1.5)
    driver.get(url)
    time.sleep(7)
    try:
        # Scroll to find_stores element using JavaScript
        driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(By.CLASS_NAME, "swiper-wrapper"))
        wrapper = driver.find_element(By.CLASS_NAME, "swiper-wrapper")
        content_text = wrapper.get_attribute("outerHTML")
        
        # Find all image elements under the wrapper
        #image_elements = wrapper.find_elements((By.CLASS_NAME, "vc-images_imageContainer__D7OIG"))
        pattern = r' src="(.*?)"'
        # Extract src attribute using regex
        matches = re.findall(pattern, content_text)
        firstM = matches[0]
        rep = firstM.replace(',','')
        photos = rep.strip()
        '''
        print(len(matches))
        # Extract first image link from srcset attribute
        image_links = set()  # Using a set to ensure distinct links
        for link in matches:
            # Remove leading and trailing whitespaces
            clean_link = link.strip()
            # Remove commas and other unwanted characters
            clean_link = clean_link.replace(',', '').replace('\n', '')
            image_links.add(clean_link)
        # Join all the image links separated by commas
        photos = " | ".join(image_links)

        print("############################")
        print(photos)
        '''
    except Exception as e:
        photos = ""

    #api_key = "bdd26e9f158f7cc5388aa0db861ec735"  # Your imgbb API key

    #imgbb_url = image_url_from_url(photos, api_key)
    filename = image_from_url(photos, index)

    driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(By.CSS_SELECTOR, "div.hero-pdp-details_heroPdpDetails__rj3Sw.hero-pdp-details_heroPdpDetails--recirculation__Rl5lk"))
    details = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div.hero-pdp-details_heroPdpDetails__rj3Sw.hero-pdp-details_heroPdpDetails--recirculation__Rl5lk"))
    )
    if details:
        try:
            header = details.find_element(By.CSS_SELECTOR, "h1.hero-pdp-header_heroPDPHeader__brand__eoJCT.vc-title-s")
            model = header.find_element(By.CSS_SELECTOR,"p.hero-pdp-header_heroPDPHeader__productName__hjUQ4").text.strip() 
        except Exception as e:
            model = ""
        try:
            con = details.find_element(By.CSS_SELECTOR,"div.hero-pdp-product-details_heroPDPProductDetails__TZgTl.hero-pdp-details_heroPdpDetails__productDetails__X4LTF")
            # Find the first p element within the div
            condition_color = con.find_elements(By.TAG_NAME, "p")

            # Extract the text from the first p element
            condition = condition_color[0].text
            color_material = condition_color[1].text
            if "," in color_material:
                color, material = color_material.split(", ")
            else:
                color = color_material
                material = ""
        except Exception as e:
            condition = ""
            color_material = ""
        try:
            price = details.find_element(By.CSS_SELECTOR,"div.product-price_productPrice__YKAe0").text.strip() 
            price = price.replace('Sold at', '').strip()
        except Exception as e:
            price = ""
    '''
    # Define the JavaScript code to scroll the page
    scroll_script = """
        window.scrollBy(0, window.innerHeight);
    """

    # Scroll the page slowly with a delay of 0.5 seconds between each scroll
    for _ in range(4):
        driver.execute_script(scroll_script)
        time.sleep(0.5)

    # Scroll to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2)")

    time.sleep(3)
    '''
    # Locate the ul element
    try:
        driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(By.CLASS_NAME, "product-description-list_descriptionList__list__FJb05"))
        time.sleep(2)
        ul_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "product-description-list_descriptionList__list__FJb05"))
        )
        date=""
        location=""
        seller=""
        # Get all li elements under the ul
        li_elements = ul_element.find_elements(By.TAG_NAME, "li")
        for li in li_elements:
            tag = li.find_element(By.CSS_SELECTOR, "span.product-description-list_descriptionList__property__MPK2a")
            if tag.text.strip() =="Online since:":
                date = li.find_element(By.CSS_SELECTOR, "span.product-description-list_descriptionList__value__lJeA_").text.strip()
            elif tag.text.strip() =="Location:":
                location = li.find_element(By.CSS_SELECTOR, "span.product-description-list_descriptionList__value__lJeA_").text.strip()
        if ', from the seller' in location:
            location, seller = location.split(', from the seller ')
            location = location.replace("Vestiaire Collective", "")
        else:
            location = location.replace("Vestiaire Collective", "")
            seller = ""  # If the 'from the seller' part is not present
    except Exception as e:
        date=""
        location=""
        seller=""
    
    # Locate the ul element
    try:
        driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(By.CSS_SELECTOR, "div.product-description-list_descriptionList__column__ndidZ.product-description-list_descriptionList__column--right___eWRs"))
        time.sleep(1)
        div_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.product-description-list_descriptionList__column__ndidZ.product-description-list_descriptionList__column--right___eWRs"))
        )
        ul_element = div_element.find_element(By.CSS_SELECTOR, "ul.product-description-list_descriptionList__list__FJb05")
        # Get all li elements under the ul
        li_elements = ul_element.find_elements(By.TAG_NAME, "li")
        list_mes=[]
        for i,li in enumerate(li_elements):
            text = li.find_element(By.CSS_SELECTOR, "span.product-description-list_descriptionList__value__lJeA_").text.strip()
            list_mes.append(text)
        measurments = " - ".join(list_mes)
    except Exception as e:
        measurments = ""
    

        

    # Return a simplified dictionary for this example
    return {
        'URL of item': url,
        'Original Photo': photos,
        'Filename': filename,
        'Brand': "Louis Vuitton",
        'Model': model,
        'Condition': condition,
        #'Color & material': color_material,
        'Color': color,
        'Material': material,
        'Measurements (Width - Height - Depth) or (Width - Height)': measurments,
        'Location (Only from Europe)': location,
        'Seller name': seller,
        'Sold at/Selling price': price,
        'Date': date,
    }

def extract_lines(input_file_path, start_line, end_line, output_file_path):
    try:
        with open(input_file_path, 'r', encoding='utf-8') as input_file, open(output_file_path, 'w', encoding='utf-8') as output_file:
            lines = input_file.readlines()
            # Adjusting start_line and end_line to be within the valid range
            start_line = max(1, min(start_line, len(lines)))
            end_line = max(start_line, min(end_line, len(lines)))

            # Writing the selected lines to the output file
            output_file.writelines(lines[start_line - 1:end_line])

        print(f"Lines {start_line} to {end_line} extracted and saved to {output_file_path}")

    except Exception as e:
        print(f"Error: {e}")

def iterate_names(file_path, index):
    # Read URLs from the file
    with open(file_path, 'r', encoding='utf-8') as file:
        names = file.read().splitlines()
    # Scrape data for each URL
    results = []
    i=index
    for name in tqdm(names):
        try:
            data = scrape(name, i)
            results.append(data)
        except Exception as e:
            print(f"Error scraping data for title: {name}\nError: {e}")
            # Write the error URL to errors.txt
            with open('errors_bags_lv.txt', 'a', encoding='utf-8') as error_file:
                error_file.write(name + '\n')
        i+=1
    return results

def write_excel(items, path):
    if len(items) == 0:
        return

    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(items)
    # Write DataFrame to Excel
    with pd.ExcelWriter(path, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')

start=7801
finish=8000
extract_lines('lv_bags_urls.txt', start, finish, 'file.txt')

# Example usage:
names_file_path = 'file.txt'
output_csv_path = 'lv25.xlsx'

# Get scraped data for each URL
scraped_data = iterate_names(names_file_path, start)

# Close the browser
driver.quit()

# Write the results to a CSV file
write_excel(scraped_data, output_csv_path)