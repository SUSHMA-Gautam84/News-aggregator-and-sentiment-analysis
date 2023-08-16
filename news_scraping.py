import os
import pandas as pd
import time
import random
from datetime import datetime, date
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from dateutil.relativedelta import relativedelta
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def get_links_and_dates(keyword):
    """Function : Get Links and Dates
    Input : Keyword, source and ip
    Output : link and date list"""

    try:  # source = proactive health

        text = keyword

        options = Options()
        options.add_argument("--start-minimized")
        # options.add_argument('--headless')
        options.add_argument("--incognito")
        options.add_argument('--disable-gpu')
        wd = webdriver.Chrome(
            ChromeDriverManager().install(),
            chrome_options=options
        )
        wd.get("https://www.google.com/")
        time.sleep(random.uniform(2, 5))
        # time.sleep(random.randint(8, 10))
        search_field = wd.find_element_by_name("q")
        search_field.clear()
        search_field.send_keys(text)

        search_field.send_keys(Keys.ENTER)
        time.sleep(random.uniform(5.1, 8.2))
    except:
        print("error in searching")

    # going on news element
    try:
        news_element = 2
        buttons = wd.find_elements_by_css_selector('div.hdtb-mitem')

        for i in range(len(buttons)):
            if buttons[i].text == "News":
                news_element = i + 1
        news_button = wd.find_element_by_xpath(
            '//*[@id="hdtb-msb"]/div[1]/div/div[' + str(news_element) + ']/a').click()


        time.sleep(random.uniform(5, 2))
        print("shifted to news element")
    except:
        print("error in clicking news element")
    # selecting time limit
    try:
        button_tools = wd.find_element_by_xpath("/html/body/div[6]/div/div[4]/div/div[1]/div/div[2]/div").click()
        time.sleep(random.uniform(2.1, 3.2))

        button_recent = wd.find_element_by_xpath("/html/body/div[6]/div/div[4]/div/div[2]/div/span[1]/g-popup/div[1]/div/div/div").click()
        time.sleep(random.uniform(2.1, 3.2))

        button_custom_range = wd.find_element_by_xpath("/html/body/div[6]/div/div[6]/div/g-menu/g-menu-item[8]/div/div/span").click()
        time.sleep(random.uniform(2.1, 3.2))
        text_field_1 = wd.find_element_by_xpath("/html/body/div[6]/div/div[4]/div[2]/div[2]/div[3]/form/input[7]")
        time.sleep(random.uniform(0, 1))
        text_field_1.clear()
        time.sleep(random.uniform(0, 1))
        # text_field_1.send_keys(datetime.today().strftime('%d/%m/%Y'))
        text_field_1.send_keys("")  # %mm/%dd/%yyyy
        text_field_2 = wd.find_element_by_xpath("/html/body/div[6]/div/div[4]/div[2]/div[2]/div[3]/form/input[8]")

        time.sleep(random.uniform(0,1))
        text_field_2.clear()
        time.sleep(random.uniform(0,1))
        text_field_2.send_keys("")  # %mm/%dd/%yyyy
        time.sleep(random.uniform(2.1, 3.2))

        time.sleep(random.uniform(2.1, 3.2))
        button_go = wd.find_element_by_xpath("/html/body/div[6]/div/div[4]/div[2]/div[2]/div[3]/form/g-button").click()
        time.sleep(random.uniform(2.1, 3.2))

    except:
        print("Error in setting range")

    link_list = []
    date1 = []

    for page in range(50):
        try:
            links = wd.find_elements_by_css_selector("a.WlydOe")
            dates = wd.find_elements_by_css_selector("div.OSrXXb.rbYSKb.LfVVr span")

            for i in range(len(links)):
                a = links[i].get_attribute("href")
                if a not in link_list:
                    link_list.append(a)
                    b = dates[i].text
                    if "hours" in b or 'hour' in b:
                        c = date.today()
                        date1.append(str(c))
                    elif "day" in b:
                        c = date.today()
                        c = c - datetime.timedelta(days=1)
                        date1.append(str(c))
                    elif "week" in b:
                        c = date.today()
                        c = c - datetime.timedelta(days=7)
                        date1.append(str(c))
                    elif "month" in b:
                        c = date.today()
                        c = c - relativedelta(months=1)
                        date1.append(str(c))
                    elif "year" in b:
                        c = date.today()
                        c = c - relativedelta(months=12)
                        date1.append(str(c))
                    elif "mins" in b or "min" in b:
                        c = date.today()
                        date1.append(str(c))
                    else:
                        date1.append(b)
            time.sleep(random.uniform(2.1, 5.2))

            print("LEN OF NEWS LINKS :", len(link_list))
            print("Moving to next page")
            time.sleep(random.randint(2, 5))
            try:
                next_button = wd.find_element_by_xpath("""//*[@id="pnnext"]/span[2]""")
                next_button.click()
                print(page + 1)
                time.sleep(random.uniform(2.1, 5.2))
            except:
                print("no next button")
                wd.close()
                break
        except:
            print("error in scraping dates and links")
            break
    return link_list, date1


def scraping(keyword):
    """Function : Scraping type, source, language and store scraped data to file with format keyword+source.csv in csv
    folder. File will not be scraped if source and keyword pair exists and is not populated and pushed to the dashboard
    Input : IP
    Output : None but stored file in csv folder."""

    link_list1, dates = get_links_and_dates(keyword=keyword)

    lkvndl = list(zip(link_list1, dates))
    df2 = pd.DataFrame(lkvndl, columns=['link', 'date'])
    df2['keyword'] = keyword

    if not os.path.exists("./{}_csv/".format("news_links_" + ''.join(keyword))):
        os.system("mkdir ./{}_csv/".format("news_links_" + ''.join(keyword)))
    df2.to_csv("./{}_csv/".format("news_links_" + ''.join(keyword)) + keyword + ' ' + ".csv", index=False)

    print(keyword)


if __name__ == '__main__':
    keyword_list = ['keyword_1', 'keyword_2']
    for keyword in keyword_list:
        scraping(keyword=keyword)
