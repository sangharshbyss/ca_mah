"""
1. Note this change: if records on page are 0, this function need not reach and the loop will continue
so the function starts with checking the act directly.
2. I think there will be some issue with file writing in csv which can be resolved later.
"""

from modules import MainModule2
import logging

# logging
logger = logging.getLogger(__name__)
# it takes record as an argument which indicates output from other function.
# and name suggesting district name from main function
# another argument is driver - which is from main program and named same.
poa_dir_district = []
poa_dir_police = []
poa_dir_year = []
poa_dir_FIR = []
poa_dir_date = []
poa_dir_sec = []


def scrollpages(record, name, driver, from_date, to_date):
    number_of_cases_on_all_pages = []
    if int(record)> 0:
        logger.info('trying to create file for all cases')
        MainModule2.df_to_file(driver=driver, name=name,
                               from_date=from_date, to_date=to_date,)
        logger.info('file created for all cases')
        logger.info("p1")
        poa_cases = MainModule2.check_the_act(driver, poa_dir_district,
                                                  poa_dir_police,
                                                  poa_dir_year,
                                                  poa_dir_FIR,
                                                  poa_dir_date,
                                                  poa_dir_sec)

        if not poa_cases:
            number_of_cases_on_all_pages.append(0)
            logger.info(f"no PoA {name} page 1")
        else:
            number_of_cases_on_page = int(len(poa_cases))
            number_of_cases_on_all_pages.append(number_of_cases_on_page)
            MainModule2.download_repeat(poa_cases, driver,
                                        )
            logger.info("finished p1, with PoA")
    else:
        logger.info("0 cases")
    if int(record) > 50:
        # p2
        MainModule2.second_page(driver)
        logger.info("p2")
        MainModule2.df_to_file(driver=driver, name=name, from_date=from_date, to_date=to_date)
        logger.info('all cases on page 2 added')
        poa_cases = MainModule2.check_the_act(driver, poa_dir_district,
                                                  poa_dir_police,
                                                  poa_dir_year,
                                                  poa_dir_FIR,
                                                  poa_dir_date,
                                                  poa_dir_sec)
        if not poa_cases:
            number_of_cases_on_all_pages.append(0)
            logger.info("finished p2. No PoA")
        else:
            number_of_cases_on_page = int(len(poa_cases))
            number_of_cases_on_all_pages.append(number_of_cases_on_page)
            MainModule2.download_repeat(poa_cases, driver)
            logger.info("finished p2, with PoA")
    else:
        # logging
        logger.warning(f"{name} finished\n")
        driver.close()
        # tell the outer program, all went well.
        return True

    if int(record) > 100:
        # opening p3
        MainModule2.third_page(driver)
        logger.info('trying to create file of cases')
        MainModule2.df_to_file(driver=driver, name=name, from_date=from_date, to_date=to_date)
        logger.info('all cases on page 3 added\n')
        # checking if PoA is available
        poa_cases = MainModule2.check_the_act(driver, poa_dir_district,
                                                  poa_dir_police,
                                                  poa_dir_year,
                                                  poa_dir_FIR,
                                                  poa_dir_date,
                                                  poa_dir_sec)
        if not poa_cases:
            number_of_cases_on_all_pages.append(0)
            # logging
            logger.info("finished p3")
        else:
            number_of_cases_on_page = int(len(poa_cases))
            number_of_cases_on_all_pages.append(number_of_cases_on_page)
            MainModule2.download_repeat(poa_cases, driver)
            # logging
            logger.info("finished p3, with PoA")
    else:
        driver.close()
        # logging
        logger.warning(f"{name} finished\n")
        # tell the outer program, all went well.
        return True

    if int(record) > 150:
        # opening p4
        MainModule2.forth_page(driver)
        logger.info('trying to create file of cases')
        MainModule2.df_to_file(driver=driver, name=name, from_date=from_date, to_date=to_date)
        logger.info('all cases on page 4 added')
        poa_cases = MainModule2.check_the_act(driver, poa_dir_district,
                                                  poa_dir_police,
                                                  poa_dir_year,
                                                  poa_dir_FIR,
                                                  poa_dir_date,
                                                  poa_dir_sec)
        if not poa_cases:
            number_of_cases_on_all_pages.append(0)
            # logging
            logger.info('p4 finished with PoA\n')

        else:
            number_of_cases_on_page = int(len(poa_cases))
            number_of_cases_on_all_pages.append(number_of_cases_on_page)
            # downloading FIR
            MainModule2.download_repeat(poa_cases, driver)
            # logging
            logger.info("finished p4, with PoA")

    else:
        # logging
        logger.warning(f"{name} finished\n")
        driver.close()
        # tell the outer program, all went well.
        return True

    if int(record) > 200:
        # p5
        MainModule2.fifth_page(driver)
        logger.info('trying to create file of cases')
        MainModule2.df_to_file(driver=driver, name=name, from_date=from_date, to_date=to_date)
        logger.info('all cases on page 5 added\n')
        # cheking for PoA
        poa_cases = MainModule2.check_the_act(driver, poa_dir_district,
                                                  poa_dir_police,
                                                  poa_dir_year,
                                                  poa_dir_FIR,
                                                  poa_dir_date,
                                                  poa_dir_sec)
        if not poa_cases:
            number_of_cases_on_all_pages.append(0)
        else:
            number_of_cases_on_page = int(len(poa_cases))
            number_of_cases_on_all_pages.append(number_of_cases_on_page)
            # downloading FIR
            MainModule2.download_repeat(poa_cases, driver,
                                        )
            # logging
            logger.info("finished p5, with PoA\n")
    else:
        # logging
        logger.warning(f"{name} finished\n")
        driver.close()
        # tell the outer program, all went well.
        return True

    if int(record) > 250:
        # p6
        MainModule2.sixth_page(driver)
        logger.info('trying to create file of cases')
        MainModule2.df_to_file(driver=driver, name=name, from_date=from_date, to_date=to_date)
        logger.info('all cases on page 6 added')

        # cheking for PoA
        poa_cases = MainModule2.check_the_act(driver, poa_dir_district,
                                                  poa_dir_police,
                                                  poa_dir_year,
                                                  poa_dir_FIR,
                                                  poa_dir_date,
                                                  poa_dir_sec)
        if not poa_cases:
            number_of_cases_on_all_pages.append(0)
        else:
            number_of_cases_on_page = int(len(poa_cases))
            number_of_cases_on_all_pages.append(number_of_cases_on_page)
            # downloading FIR
            MainModule2.download_repeat(poa_cases, driver,
                                        )
            # logging
            logger.info("finished p6, with PoA\n")
    else:
        # logging
        logger.warning(f"{name} finished\n")
        driver.close()
        # tell the outer program, all went well.
        return True

    if int(record) > 300:
        # p7
        MainModule2.seventh_page(driver)
        logger.info('trying to create file of cases')
        MainModule2.df_to_file(driver=driver, name=name, from_date=from_date, to_date=to_date)
        logger.info('all cases on page 7 added')

        # cheking for PoA
        poa_cases = MainModule2.check_the_act(driver, poa_dir_district,
                                                  poa_dir_police,
                                                  poa_dir_year,
                                                  poa_dir_FIR,
                                                  poa_dir_date,
                                                  poa_dir_sec)
        if not poa_cases:
            number_of_cases_on_all_pages.append(0)
        else:
            number_of_cases_on_page = int(len(poa_cases))
            number_of_cases_on_all_pages.append(number_of_cases_on_page)
            # downloading FIRs
            MainModule2.download_repeat(poa_cases, driver,
                                        )
            # logging
            logger.info("finished p7, with PoA\n")
    else:
        # loggingg
        logger.warning(f"{name} finished\n")
        driver.close()
        # tell the outer program, all went well.
        return True

    if int(record) > 350:
        # p8
        MainModule2.eightth_page(driver)
        logger.info('trying to create file of cases')
        MainModule2.df_to_file(driver=driver, name=name, from_date=from_date, to_date=to_date)
        logger.info('all cases on page 8 added')
        poa_cases = MainModule2.check_the_act(driver, poa_dir_district,
                                                  poa_dir_police,
                                                  poa_dir_year,
                                                  poa_dir_FIR,
                                                  poa_dir_date,
                                                  poa_dir_sec)
        if not poa_cases:
            # taking output of 0 to list and then to csv
            number_of_cases_on_all_pages.append(0)
            driver.close()
            # logging
            logger.warning(f"{name} finished\n")
            return True
        else:
            number_of_cases_on_page = int(len(poa_cases))
            number_of_cases_on_all_pages.append(number_of_cases_on_page)
            # downloading PoA FIR
            MainModule2.download_repeat(poa_cases, driver,
                                        )
            # logging
            logger.info("finished p8, with PoA")
            # logging
            logger.warning(f"{name} finished\n")
            driver.close()
            return True
    else:
        driver.close()
        # loggingg
        logger.warning(f"{name} finished\n")
        return True
