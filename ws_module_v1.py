import time
import logging
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

""" 
1. re-birth of FIR_modules.py
2. number of pages reduced to 8. 
3. logging added
4. Deleting the refresh added in check available - new approach adopted in main file
By this approch - 
the while loop will be initiated again for same date range if there's any exception
"""

# for logging
logger = logging.getLogger(__name__)
def enter_date(date1, date2, driver):
    WebDriverWait(driver, 160).until(
        ec.presence_of_element_located((By.CSS_SELECTOR,
                                        '#ContentPlaceHolder1_txtDateOfRegistrationFrom')))

    from_date_field = driver.find_element(By.ID, "ContentPlaceHolder1_txtDateOfRegistrationFrom")

    to_date_field = driver.find_element(By.ID, "ContentPlaceHolder1_txtDateOfRegistrationTo")

    ActionChains(driver).click(from_date_field).send_keys(
        date1).move_to_element(to_date_field).click().send_keys(
        date2).perform()


# 3 select district and enter
def district_selection(dist_name, driver):
    dist_list = Select(driver.find_element(By.CSS_SELECTOR,
                                           "#ContentPlaceHolder1_ddlDistrict"))

    dist_list.select_by_visible_text(dist_name)


# 4. List police station
def police_stations(driver):
    WebDriverWait(driver, 160).until(
        ec.presence_of_element_located((By.CSS_SELECTOR,
                                        '#ContentPlaceHolder1_ddlPoliceStation')))
    select_box = driver.find_element(By.CSS_SELECTOR, "#ContentPlaceHolder1_ddlPoliceStation")
    all_police_stations = [
        x.text for x in select_box.find_elements_by_tag_name("option") if x.text != "Select"]
    return all_police_stations


# select police station
# unused function as of 31.03.2024
def select_police_station(selected_police, driver):
    # this will select police station as per there names listed in
    # list created by police_stations() function.
    police_list = Select(driver.find_element(By.CSS_SELECTOR,
                                             '#ContentPlaceHolder1_ddlPoliceStation'))
    police_list.select_by_visible_text(selected_police)


# 5. view 50 records at a time
def view_record(driver):
    view = Select(driver.find_element(By.ID, 'ContentPlaceHolder1_ucRecordView_ddlPageSize'))
    view.select_by_value("50")


# 4. function for click on search
def search(driver):
    driver.find_element(By.CSS_SELECTOR, '#ContentPlaceHolder1_btnSearch').click()
    time.sleep(4)


def number_of_records(driver):
    total_number = driver.find_element(By.CSS_SELECTOR,
                                       '#ContentPlaceHolder1_lbltotalrecord').text
    return total_number


# 5 check if it has PoA if yes, create a list of how many cases
def check_the_act(driver, poa_dir_district,
                  poa_dir_police,
                  poa_dir_year,
                  poa_dir_fir,
                  poa_dir_date,
                  poa_dir_sec):
    poa_list = []

    # check for PoA in table.
    # identify table first
    WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((
            By.CSS_SELECTOR, "#ContentPlaceHolder1_gdvDeadBody")))
    table = driver.find_element(By.ID, "ContentPlaceHolder1_gdvDeadBody")
    rows = table.find_elements(By.TAG_NAME, "tr")
    # iterate over each row
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        # iterate over each cell
        for cell in cells:
            cell_text = cell.text
            # if the act is found, count it. and take details.
            if "अनुसूचीत जाती आणि अनुसूचीत" in cell_text:
                poa_list.append(row.text)
                poa_dir_district.append(cells[2].text)
                poa_dir_police.append(cells[3].text)
                poa_dir_year.append(cells[4].text)
                poa_dir_fir.append(cells[5].text)
                poa_dir_date.append(cells[6].text)
                poa_dir_sec.append(cells[8].text)
    # logging
    logging.debug("checked for PoA", exc_info=True)
        
    return poa_list



def download_repeat(some_list, driver,
                    ):
    i = 0
    while i <= len(some_list) - 1:
        table = driver.find_element(By.ID, "ContentPlaceHolder1_gdvDeadBody")
        rows = table.find_elements(By.TAG_NAME, "tr")
        new_list = []
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            # iterate over each cell
            for cell in cells:
                cell_text = cell.text
                # if the act is found, count it. and take details.
                if "अनुसूचीत जाती आणि अनुसूचीत" in cell_text:
                    download_link = row.find_element(By.TAG_NAME, "input")
                    new_list.append(download_link)

                else:
                    continue

        try:
            new_list[i].click()
            time.sleep(5)
            i += 1
            # logging
            logging.debug("checked for PoA", exc_info=True)
        except:
            # logging
            logging.debug("major error", exc_info=True)
            i += 1
            continue


def second_page(driver):
    p2 = driver.find_element(By.XPATH,
                             '/html/body/form/div[4]/table/tbody/tr[4]/td/div[2]/div/table/'
                             'tbody/tr/td/table[2]/tbody/tr/td/div[3]/div[1]/table/tbody/tr[52]'
                             '/td/table/tbody/tr/td[2]/a')
    p2.click()
    # logging
    logging.debug("p2", exc_info=True)


def third_page(driver):
    p3 = driver.find_element(By.XPATH,
                             "/html/body/form/div[4]/table/tbody/tr[4]/td/div[2]/div/"
                             "table/tbody/tr/td/table[2]/tbody/tr/td/div[3]/div[1]/table"
                             "/tbody/tr[52]/td/table/tbody/tr/td[3]/a"
                             )
    p3.click()
    # logging
    logging.debug("p3", exc_info=True)


def forth_page(driver):
    p4 = driver.find_element(By.XPATH,
                             "/html/body/form/div[4]/table/tbody/tr[4]/td/div[2]/div/table"
                             "/tbody/tr/td/table[2]/tbody/tr/td/div[3]/div[1]/table/tbody"
                             "/tr[52]/td/table/tbody/tr/td[4]/a"
                             )
    p4.click()
    # logging
    logging.debug("p4", exc_info=True)


def fifth_page(driver):
    p5 = driver.find_element(By.XPATH,
                             "/html/body/form/div[4]/table/tbody/tr[4]/td/div[2]/div/table"
                             "/tbody/tr/td/table[2]/tbody/tr/td/div[3]/div[1]/table/tbody"
                             "/tr[52]/td/table/tbody/tr/td[5]/a"
                             )
    p5.click()
    # logging
    logging.debug("p5", exc_info=True)


def sixth_page(driver):
    p6 = driver.find_element(By.XPATH,
                             "/html/body/form/div[4]/table/tbody/tr[4]/td/div[2]/div/table"
                             "/tbody/tr/td/table[2]/tbody/tr/td/div[3]/div[1]/table/tbody"
                             "/tr[52]/td/table/tbody/tr/td[6]/a"
                             )
    p6.click()
    # logging
    logging.debug("p6", exc_info=True)


def seventh_page(driver):
    p7 = driver.find_element(By.XPATH,
                             "/html/body/form/div[4]/table/tbody/tr[4]/td/div[2]/div/table/"
                             "tbody/tr/td/table[2]/tbody/tr/td/div[3]/div[1]/table/tbody"
                             "/tr[52]/td/table/tbody/tr/td[7]/a"
                             )
    p7.click()
    # logging
    logging.debug("p7", exc_info=True)

def eightth_page(driver):
    p8 = driver.find_element(By.XPATH,
                             "/html/body/form/div[4]/table/tbody/tr[4]/td/div[2]/div/table"
                             "/tbody/tr/td/table[2]/tbody/tr/td/div[3]/div[1]/table/tbody"
                             "/tr[52]/td/table/tbody/tr/td[8]/a"
                             )
    p8.click()
    # logging
    logging.debug("p8", exc_info=True)


def ninenth_page(driver):
    p9 = driver.find_element(By.XPATH,
                             "/html/body/form/div[4]/table/tbody/tr[4]/td/div[2]/div/table"
                             "/tbody/tr/td/table[2]/tbody/tr/td/div[3]/div[1]/table/tbody"
                             "/tr[52]/td/table/tbody/tr/td[9]/a"
                             )
    p9.click()
    # logging
    logging.debug("p9", exc_info=True)
