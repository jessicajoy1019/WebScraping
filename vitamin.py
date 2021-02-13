from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import csv
import re
import time


option = Options()
option.add_argument("--incognito")

driver = webdriver.Chrome(options=option)

url= "https://www.vitaminshoppe.com/c/goals/N-cp99iy?page=1"
driver.get(url)

#Close pop up
wait= WebDriverWait(driver, 15)
wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME,"ju_iframe_607875")))
driver.find_element_by_xpath("//*[@id='justuno_form']/div/div[2]/div").click()
driver.switch_to.default_content()



csv_file = open('vitaminshoppe.csv', 'w', encoding='utf-8', newline='')
writer = csv.writer(csv_file)

index = 2
url_list = []
url_list.append(url)
while index < 4:

    try:
        print("Scraping Page number " + str(index))
        url_to_add = "https://www.vitaminshoppe.com/c/goals/N-cp99iy?page=" + str(index)       
        url_list.append(url_to_add)
        index += 1
        print(url_list)

        for url_ in url_list:
            driver.get(url_)

            # Open each product in new tab
            elems = [elem.get_attribute("href") for elem in WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH, "//vshoppe-product-grid/div/div/div[2]/div/div[1]/div[1]/a")))]
            windows_before  = driver.current_window_handle

            for elem in elems:
                driver.execute_script("window.open('" +elem +"');")
                WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))

                windows_after = driver.window_handles
                new_window = [x for x in windows_after if x != windows_before][0] 
                driver.switch_to.window(new_window) 
                time.sleep(3)
                

                # Create empty dictionary to scrape product info
                product_dict={}

                try:
                    name = driver.find_element_by_xpath('//*[@id="main-body-container"]/div/div/div/div[1]/vshoppe-main-product-details-sco/div[2]/div/div/div[1]/vshoppe-product-details-upgrade/div/div/div[2]/h1').text
                except:
                    name = None

                try:
                    id_number = driver.find_element_by_xpath('//span[@class="item"]').text
                except:
                    id_number = None

                try:
                    listed_price = driver.find_element_by_xpath('//span[@class="priceCurrencyLabel sale-price-displayed"]/span[1]').text
                except:
                    try:
                        listed_price = driver.find_element_by_xpath('//span[@class="priceCurrencyLabel"]/span[1]').text
                    except:
                        name = None

                try:
                    price_per_serving = driver.find_element_by_xpath('//div[@class="pdp--priceServeRow"]/span[1]').text
                except:
                    price_per_serving = None

                try:
                    brand = driver.find_element_by_xpath('//div[@class="productBrandName"]/a[1]/span[1]').text
                except:
                    brand = None 

                try:
                    ingredients = driver.find_element_by_xpath('//div[@class="product-label"]/p[1]').text
                except:
                    ingredients

                try:
                    average_rating = driver.find_element_by_xpath("//span[@id='TTreviewSummaryAverageRating']").text
                except:
                    average_rating = None

                try: 
                    review_count = driver.find_element_by_xpath("//div[@class='TTreviewCount']").text
                except:
                    review_count = None

                try:
                    recommend_yes = driver.find_element_by_xpath('//div[@class="TTreviewDimsSingleSelectSummary"]/div[@class="TTreviewDimsSingleSelectValue"][1]').text
                except:
                    recommend_yes = None

                try:
                    recommend_no = driver.find_element_by_xpath('//div[@class="TTreviewDimsSingleSelectSummary"]/div[@class="TTreviewDimsSingleSelectValue"][2]').text
                except:
                    recommend_no = None

                
                product_dict['name'] = name
                product_dict['id_number'] = id_number
                product_dict['listed_price'] = listed_price
                product_dict['price_per_serving'] = price_per_serving
                product_dict['brand'] = brand
                product_dict['ingredients'] = ingredients
                product_dict['average_rating'] = average_rating
                product_dict['review_count'] = review_count
                product_dict['recommend_yes'] = recommend_yes
                product_dict['recommend_no'] = recommend_no

                writer.writerow(product_dict.values())

                # Close the window
                driver.close()
                driver.switch_to.window(windows_before)

    except:
        try: 
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        except: 
            csv_file.close()
            driver.close()
    break