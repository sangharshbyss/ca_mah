"""
1. re-birth of MainModule2.py
2. change: it checks if the page has really turned.
If not it goes for next district and it merges check_act and download
"""
import logging
import time
from pathlib import Path

import pandas as pd
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec, expected_conditions
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

# for logging
logger = logging.getLogger(__name__)


# 1
def enter_date(date1, date2, driver):
    WebDriverWait(driver, 160).until(
        ec.presence_of_element_located((By.CSS_SELECTOR,
                                        '#ContentPlaceHolder1_txtDateOfRegistrationFrom')))

    from_date_field = driver.find_element(By.ID, "ContentPlaceHolder1_txtDateOfRegistrationFrom")

    to_date_field = driver.find_element(By.ID, "ContentPlaceHolder1_txtDateOfRegistrationTo")

    ActionChains(driver).click(from_date_field).send_keys(
        date1).move_to_element(to_date_field).click().send_keys(
        date2).perform()


# 2 select district and enter
def district_selection(dist_name, driver):
    dist_list = Select(driver.find_element(By.CSS_SELECTOR,
                                           "#ContentPlaceHolder1_ddlDistrict"))

    dist_list.select_by_visible_text(dist_name)


# 3. List police station (currently unused)
def police_stations(driver):
    WebDriverWait(driver, 160).until(
        ec.presence_of_element_located((By.CSS_SELECTOR,
                                        '#ContentPlaceHolder1_ddlPoliceStation')))
    select_box = driver.find_element(By.CSS_SELECTOR, "#ContentPlaceHolder1_ddlPoliceStation")
    all_police_stations = [
        x.text for x in select_box.find_elements_by_tag_name("option") if x.text != "Select"]
    return all_police_stations


# 4. select police station
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


# 6. function for click on search
def search(driver):
    driver.find_element(By.CSS_SELECTOR, '#ContentPlaceHolder1_btnSearch').click()
    time.sleep(4)


# 7. number of records
def number_of_records(driver):
    total_number = driver.find_element(By.CSS_SELECTOR,
                                       '#ContentPlaceHolder1_lbltotalrecord').text
    logger.info(f'Total number of Cases: {total_number}')
    return total_number


def df_to_file(driver, name, from_date, to_date):
    data = WebDriverWait(driver, 20).until(ec.presence_of_element_located((
        By.CSS_SELECTOR, "#ContentPlaceHolder1_gdvDeadBody"))).get_attribute("outerHTML")
    all_df = pd.read_html(data)
    # 1. select 1st table as our intended dataframe
    # 2. drop last two rows as they are unnecessary
    # 3. drop column download as it has dyanamic link and not readable data.
    # 4. take df as output for next function.
    df_with_last_rows = all_df[0].drop(columns="Download")
    df = df_with_last_rows.drop(df_with_last_rows.tail(2).index)
    file_name = f'{name}_{from_date}_{to_date}.csv'
    dir_name = Path(f'/home/sangharsh/Documents/PoA/data/FIR/y_23/all_cases/{from_date}_{to_date}')
    dir_name.mkdir(parents=True, exist_ok=True)
    df.to_csv(dir_name / file_name, index=False, mode='a', header=False)
    # poa file
    poa_df = df[df['Sections'].str.contains("अनुसूचीत जाती आणि अनुसूचीत")]
    print(poa_df)
    if len(poa_df.index) > 0:
        poa_file = f'poa_{name}_{from_date}_{to_date}.csv'
        poa_dir_name = Path(f'/home/sangharsh/Documents/PoA/data/FIR/y_23/'
                            f'poa_cases/{from_date}_{to_date}')
        poa_dir_name.mkdir(parents=True, exist_ok=True)
        poa_df.to_csv(poa_dir_name / poa_file, index=False, mode='a', header=False)
    else:
        pass


# 9. check if it has PoA if yes, create a list of how many cases
def check_the_act(driver):
    logger.info("check_the_act Module called")
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
                download_link = row.find_element(By.TAG_NAME, "input")
                download_link.click()

    # logging
    logger.info("checking finished\n", exc_info=True)


# 10. for downloading PoA FIR
# not in use in ws3/AllPages2
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
                    print(row.text)
                    new_list.append(download_link)
                else:
                    continue
        new_list[i].click()
        time.sleep(3)
        i += 1
        # logging
        logger.info("downloaded", exc_info=True)


# 11. Go to next page
def second_page(driver):
    p2 = driver.find_element(By.XPATH,
                             '/html/body/form/div[4]/table/tbody/tr[4]/td/div[2]/div/table/'
                             'tbody/tr/td/table[2]/tbody/tr/td/div[3]/div[1]/table/tbody/tr[52]'
                             '/td/table/tbody/tr/td[2]/a')
    p2.click()
    end_time = time.time() + 20
    while time.time() < end_time:
        new_page_check = driver.find_element(By.ID, 'ContentPlaceHolder1_gdvDeadBody_lblSrNo_0')
        if new_page_check.text == '51':
            logger.info('p2 loaded')
            return True
        else:
            time.sleep(2)
            continue




# 12. Go to next page
def third_page(driver):
    # logging
    p3 = driver.find_element(By.XPATH,
                             "/html/body/form/div[4]/table/tbody/tr[4]/td/div[2]/div/"
                             "table/tbody/tr/td/table[2]/tbody/tr/td/div[3]/div[1]/table"
                             "/tbody/tr[52]/td/table/tbody/tr/td[3]/a"
                             )
    p3.click()
    end_time = time.time() + 20
    while time.time() < end_time:
        new_page_check = driver.find_element(By.ID, 'ContentPlaceHolder1_gdvDeadBody_lblSrNo_0')
        if new_page_check.text == '101':
            logger.info('p3 loaded')
            return True
        else:
            time.sleep(2)
            continue


# 13. Go to next page
def forth_page(driver):
    p4 = driver.find_element(By.XPATH,
                             "/html/body/form/div[4]/table/tbody/tr[4]/td/div[2]/div/table"
                             "/tbody/tr/td/table[2]/tbody/tr/td/div[3]/div[1]/table/tbody"
                             "/tr[52]/td/table/tbody/tr/td[4]/a"
                             )
    p4.click()
    end_time = time.time() + 20
    while time.time() < end_time:
        new_page_check = driver.find_element(By.ID, 'ContentPlaceHolder1_gdvDeadBody_lblSrNo_0')
        if new_page_check.text == '151':
            logger.info('p4 loaded')
            return True
        else:
            time.sleep(2)
            continue


# 14. Go to next page
def fifth_page(driver):
    p5 = driver.find_element(By.XPATH,
                             "/html/body/form/div[4]/table/tbody/tr[4]/td/div[2]/div/table"
                             "/tbody/tr/td/table[2]/tbody/tr/td/div[3]/div[1]/table/tbody"
                             "/tr[52]/td/table/tbody/tr/td[5]/a"
                             )
    p5.click()
    end_time = time.time() + 20
    while time.time() < end_time:
        new_page_check = driver.find_element(By.ID, 'ContentPlaceHolder1_gdvDeadBody_lblSrNo_0')
        if new_page_check.text == '201':
            logger.info('p5 loaded')
            return True
        else:
            time.sleep(2)
            continue


# 15. Go to next page
def sixth_page(driver):
    p6 = driver.find_element(By.XPATH,
                             "/html/body/form/div[4]/table/tbody/tr[4]/td/div[2]/div/table"
                             "/tbody/tr/td/table[2]/tbody/tr/td/div[3]/div[1]/table/tbody"
                             "/tr[52]/td/table/tbody/tr/td[6]/a"
                             )
    p6.click()
    end_time = time.time() + 20
    while time.time() < end_time:
        new_page_check = driver.find_element(By.ID, 'ContentPlaceHolder1_gdvDeadBody_lblSrNo_0')
        if new_page_check.text == '251':
            logger.info('p6 loaded')
            return True
        else:
            time.sleep(2)
            continue


# 16. Go to next page
def seventh_page(driver):
    p7 = driver.find_element(By.XPATH,
                             "/html/body/form/div[4]/table/tbody/tr[4]/td/div[2]/div/table/"
                             "tbody/tr/td/table[2]/tbody/tr/td/div[3]/div[1]/table/tbody"
                             "/tr[52]/td/table/tbody/tr/td[7]/a"
                             )
    p7.click()
    end_time = time.time() + 20
    while time.time() < end_time:
        new_page_check = driver.find_element(By.ID, 'ContentPlaceHolder1_gdvDeadBody_lblSrNo_0')
        if new_page_check.text == '301':
            logger.info('p7 loaded')
            return True
        else:
            time.sleep(2)
            continue


# 17. Go to next page
def eighth_page(driver):
    p8 = driver.find_element(By.XPATH,
                             "/html/body/form/div[4]/table/tbody/tr[4]/td/div[2]/div/table"
                             "/tbody/tr/td/table[2]/tbody/tr/td/div[3]/div[1]/table/tbody"
                             "/tr[52]/td/table/tbody/tr/td[8]/a"
                             )
    p8.click()
    end_time = time.time() + 20
    while time.time() < end_time:
        new_page_check = driver.find_element(By.ID, 'ContentPlaceHolder1_gdvDeadBody_lblSrNo_0')
        if new_page_check.text == '351':
            logger.info('p8 loaded')
            return True
        else:
            time.sleep(2)
            continue


# 18. Go to next page
def ninenth_page(driver):
    p9 = driver.find_element(By.XPATH,
                             "/html/body/form/div[4]/table/tbody/tr[4]/td/div[2]/div/table"
                             "/tbody/tr/td/table[2]/tbody/tr/td/div[3]/div[1]/table/tbody"
                             "/tr[52]/td/table/tbody/tr/td[9]/a"
                             )
    p9.click()
    end_time = time.time() + 20
    while time.time() < end_time:
        new_page_check = driver.find_element(By.ID, 'ContentPlaceHolder1_gdvDeadBody_lblSrNo_0')
        if new_page_check.text == '401':
            logger.info('p9 loaded')
            return True
        else:
            time.sleep(2)
            continue
