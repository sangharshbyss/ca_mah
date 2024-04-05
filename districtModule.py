"""
1. module of ws2.py
2. will create csv once records are available for cases.


Further Actions:
1. module names as per style guide
2. use classes to by more pythonic - object oriented
3. change file structure.


"""

import os
import time
import logging
import ws_module_v1
import pageScrolModule
import copyingwholetable

from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from ws_module_proxy_v1 import list_of_proxies

logger = logging.getLogger(__name__)
# 1.a base directory
base_directory = r'/home/sangharsh/Documents/PoA/data/FIR/y_23'

# 1. constants
# 1.b logging

# 1.c url of basic page
main_url = r'https://citizen.mahapolice.gov.in/Citizen/MH/PublishedFIRs.aspx'

# 1.d lists for taking cvs output
poa_dir_district = []
poa_dir_police = []
poa_dir_year = []
poa_dir_FIR = []
poa_dir_date = []
poa_dir_sec = []
# 1.f ist of districts
ALL_Districts = ['AHMEDNAGAR', 'AKOLA', 'AMRAVATI CITY', 'AMRAVATI RURAL', 'BEED', 'BHANDARA', 'BULDHANA',
                 'CHANDRAPUR', 'CHHATRAPATI SAMBHAJINAGAR CITY', 'CHHATRAPATI SAMBHAJINAGAR (RURAL)',
                 'DHARASHIV', 'DHULE', 'GADCHIROLI', 'GONDIA', 'HINGOLI', 'JALGAON', 'JALNA',
                 'KOLHAPUR', 'LATUR', 'Mira-Bhayandar, Vasai-Virar Police Commissioner',
                 'NAGPUR CITY', 'NAGPUR RURAL', 'NANDED', 'NANDURBAR',
                 'NASHIK CITY', 'NASHIK RURAL', 'NAVI MUMBAI', 'PALGHAR', 'PARBHANI',
                 'PIMPRI-CHINCHWAD', 'PUNE CITY', 'PUNE RURAL', 'RAIGAD',
                 'RAILWAY MUMBAI', 'RAILWAY NAGPUR', 'RAILWAY PUNE', 'RATNAGIRI', 'SANGLI', 'SATARA',
                 'SINDHUDURG', 'SOLAPUR CITY', 'SOLAPUR RURAL', 'THANE CITY', 'THANE RURAL', 'WARDHA',
                 'WASHIM', 'YAVATMAL']


def districtWithProblem(name_of_problem, from_date, to_date):
    def open_page():
        """
        open page and refresh it. without refreshing it dose not work
        """
        driver.get(main_url)
        driver.refresh()

    logger.warning(f"start {from_date}")
    # constant for outer loop
    # download directory path
    download_directory = os.path.join(base_directory,
                                      "copies", f'{from_date} _ {to_date}')
    # create directory if not available.
    if not download_directory:
        os.mkdir(download_directory)

    # 3. inner loop for each district
    for name in ALL_Districts[ALL_Districts.index(name_of_problem):] :
        # variables
        number_of_cases_on_all_pages = []
        # set profile for saving directly without pop-up ref -
        # https://stackoverflow.com/a/29777967
        options = Options()
        options.set_preference("browser.download.panel.shown", False)
        options.set_preference("browser.download.manager.showWhenStarting", False)
        # profile.set_preference("browser.helperApps.neverAsk.openFile","application/pdf")
        options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
        options.set_preference("browser.download.folderList", 2)
        options.set_preference("browser.download.dir", download_directory)
        # to go undetected
        options.set_preference("general.useragent.override",
                               "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:82.0) "
                               "Gecko/20100101 Firefox/82.0")
        options.set_preference("dom.webdriver.enabled", False)
        options.set_preference('useAutomationExtension', False)
        options.set_preference("pdfjs.disabled", True)
        service = Service('C:\\BrowserDrivers\\geckodriver.exe')
        options.headless = True

        # change IP
        myProxy = list_of_proxies()
        proxy = Proxy({
            'proxyType': ProxyType.MANUAL,
            'httpProxy': myProxy[ALL_Districts.index(name)],
            'ftpProxy': myProxy[ALL_Districts.index(name)],
            'sslProxy': myProxy[ALL_Districts.index(name)],
            'noProxy': ''  # set this value as desired
        })
        #check - pycharm saying argument 'proxy' is unexpected
        try:
            driver = webdriver.Firefox(options=options, proxy=proxy)
            open_page()
            time.sleep(3)
            # enter the date
            ws_module_v1.enter_date(date1=from_date, date2=to_date, driver=driver)
            # logging
            logger.info(f"entered date {from_date}")
            time.sleep(2)
            # enter district
            ws_module_v1.district_selection(name, driver=driver)
            logger.info(f'after error, starting with  {name}')
            # creation of list. These lists will be converted to dictionary to write to csv
            # call the value of records to view @ 50
            time.sleep(5)
            ws_module_v1.view_record(driver)
            # call search
            ws_module_v1.search(driver=driver)
            # view 50 records, that is max, per page
            record = ws_module_v1.number_of_records(driver=driver)
            if record != '':
                pass
            else:
                logger.info(f"completed {name}\n")
                driver.close()
                continue
            scroll_pages = pageScrolModule.scrollPages(
                record=record, name=name, driver=driver)
            if scroll_pages:
                continue
            else:
                logger.warning(f"{name} catched error. "
                               f"second time in {from_date} to {to_date} breaking everything")
                # return the District name where it failed.
                # this district name will be used as argument in next function.
                return (name, from_date, to_date)
        except Exception as e:
            logger.warning(f"{name} catched error. "
                           f"second time in {from_date} to {to_date} breaking everything")
            # return the District name where it failed.
            # this district name will be used as argument in next function.
            return (name, from_date, to_date)

# seperate function for writing to file



# Press the green button in the gutter to run the script.
