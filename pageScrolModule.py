"""
1. Note this change: if records on page are 0, this function need not reach and the loop will continue
so the function starts with checking the act directly.
2. I think there will be some issue with file writing in csv which can be resolved later.
"""

import ws_module_v1
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


def scrollPages(record, name, driver, from_date, to_date):
    number_of_cases_on_all_pages = []
    # this if at first time can be deleted as
    # the function will reach only if there is some record

    poa_cases, df = ws_module_v1.check_the_act(driver, poa_dir_district,
                                               poa_dir_police,
                                               poa_dir_year,
                                               poa_dir_FIR,
                                               poa_dir_date,
                                               poa_dir_sec)
    logger.info('trying to create file')
    ws_module_v1.df_to_file(df=df, name=name, from_date=from_date, to_date=to_date)
    logger.info('file created')
    try:

        if not poa_cases:
            number_of_cases_on_all_pages.append(0)
            logger.info(f"no PoA{name} page 1")
        else:
            number_of_cases_on_page = int(len(poa_cases))
            number_of_cases_on_all_pages.append(number_of_cases_on_page)
            ws_module_v1.download_repeat(poa_cases, driver,
                                         )
            logger.info("finished p1, with PoA")
        if int(record) > 50:
            # p2
            ws_module_v1.second_page(driver)
            poa_cases, df = ws_module_v1.check_the_act(driver, poa_dir_district,
                                                       poa_dir_police,
                                                       poa_dir_year,
                                                       poa_dir_FIR,
                                                       poa_dir_date,
                                                       poa_dir_sec)
            logger.info('trying to create file of cases')
            ws_module_v1.df_to_file(df=df, name=name, from_date=from_date, to_date=to_date)
            logger.info('file created')
            if not poa_cases:
                number_of_cases_on_all_pages.append(0)
                logger.info("finished p2")
            else:
                number_of_cases_on_page = int(len(poa_cases))
                number_of_cases_on_all_pages.append(number_of_cases_on_page)
                ws_module_v1.download_repeat(poa_cases, driver)
                logger.info("finished p2, with PoA")
        else:
            # logging
            logger.warning(f"{name} finished\n")
            driver.close()
            # tell the outer program, all went well.
            return True

        if int(record) > 100:
            # opening p3
            ws_module_v1.third_page(driver)
            # checking if PoA is available
            poa_cases, df = ws_module_v1.check_the_act(driver, poa_dir_district,
                                                   poa_dir_police,
                                                   poa_dir_year,
                                                   poa_dir_FIR,
                                                   poa_dir_date,
                                                   poa_dir_sec)
            logger.info('trying to create file of cases')
            ws_module_v1.df_to_file(df=df, name=name, from_date=from_date, to_date=to_date)
            logger.info('file created for all cases')
            if not poa_cases:
                number_of_cases_on_all_pages.append(0)
                # logging
                logger.info("finished p3")
            else:
                number_of_cases_on_page = int(len(poa_cases))
                number_of_cases_on_all_pages.append(number_of_cases_on_page)
                ws_module_v1.download_repeat(poa_cases, driver)
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
            ws_module_v1.forth_page(driver)
            poa_cases, df = ws_module_v1.check_the_act(driver, poa_dir_district,
                                                   poa_dir_police,
                                                   poa_dir_year,
                                                   poa_dir_FIR,
                                                   poa_dir_date,
                                                   poa_dir_sec)
            logger.info('trying to create file of cases')
            ws_module_v1.df_to_file(df=df, name=name, from_date=from_date, to_date=to_date)
            logger.info('file created')
            if not poa_cases:
                number_of_cases_on_all_pages.append(0)
                # logging
                logger.info('p4 finished with PoA')

            else:
                number_of_cases_on_page = int(len(poa_cases))
                number_of_cases_on_all_pages.append(number_of_cases_on_page)
                # downloading FIR
                ws_module_v1.download_repeat(poa_cases, driver)
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
            ws_module_v1.fifth_page(driver)
            # cheking for PoA
            poa_cases, df = ws_module_v1.check_the_act(driver, poa_dir_district,
                                                   poa_dir_police,
                                                   poa_dir_year,
                                                   poa_dir_FIR,
                                                   poa_dir_date,
                                                   poa_dir_sec)
            logger.info('trying to create file of cases')
            ws_module_v1.df_to_file(df=df, name=name, from_date=from_date, to_date=to_date)
            logger.info('file created')
            if not poa_cases:
                number_of_cases_on_all_pages.append(0)
            else:
                number_of_cases_on_page = int(len(poa_cases))
                number_of_cases_on_all_pages.append(number_of_cases_on_page)
                # downloading FIR
                ws_module_v1.download_repeat(poa_cases, driver,
                                             )
                # logging
                logger.info("finished p5, with PoA")
        else:
            # logging
            logger.warning(f"{name} finished\n")
            driver.close()
            # tell the outer program, all went well.
            return True

        if int(record) > 250:
            # p6
            ws_module_v1.sixth_page(driver)
            # cheking for PoA
            poa_cases, df = ws_module_v1.check_the_act(driver, poa_dir_district,
                                                   poa_dir_police,
                                                   poa_dir_year,
                                                   poa_dir_FIR,
                                                   poa_dir_date,
                                                   poa_dir_sec)
            logger.info('trying to create file of cases')
            ws_module_v1.df_to_file(df=df, name=name, from_date=from_date, to_date=to_date)
            logger.info('file for all cass created')
            if not poa_cases:
                number_of_cases_on_all_pages.append(0)
            else:
                number_of_cases_on_page = int(len(poa_cases))
                number_of_cases_on_all_pages.append(number_of_cases_on_page)
                # downloading FIR
                ws_module_v1.download_repeat(poa_cases, driver,
                                             )
                # logging
                logger.info("finished p6, with PoA")
        else:
            # logging
            logger.warning(f"{name} finished\n")
            driver.close()
            # tell the outer program, all went well.
            return True

        if int(record) > 300:
            # p7
            ws_module_v1.seventh_page(driver)
            # cheking for PoA
            poa_cases, df = ws_module_v1.check_the_act(driver, poa_dir_district,
                                                   poa_dir_police,
                                                   poa_dir_year,
                                                   poa_dir_FIR,
                                                   poa_dir_date,
                                                   poa_dir_sec)
            logger.info('trying to create file of cases')
            ws_module_v1.df_to_file(df=df, name=name, from_date=from_date, to_date=to_date)
            logger.info('file for all cass created')
            if not poa_cases:
                number_of_cases_on_all_pages.append(0)
            else:
                number_of_cases_on_page = int(len(poa_cases))
                number_of_cases_on_all_pages.append(number_of_cases_on_page)
                # downloading FIRs
                ws_module_v1.download_repeat(poa_cases, driver,
                                             )
                # logging
                logger.info("finished p7, with PoA")
        else:
            # loggingg
            logger.warning(f"{name} finished\n")
            driver.close()
            # tell the outer program, all went well.
            return True

        if int(record) > 350:
            # p8
            ws_module_v1.eightth_page(driver)
            poa_cases, df = ws_module_v1.check_the_act(driver, poa_dir_district,
                                                   poa_dir_police,
                                                   poa_dir_year,
                                                   poa_dir_FIR,
                                                   poa_dir_date,
                                                   poa_dir_sec)
            logger.info('trying to create file of cases')
            ws_module_v1.df_to_file(df=df, name=name, from_date=from_date, to_date=to_date)
            logger.info('file for all cass created')
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
                ws_module_v1.download_repeat(poa_cases, driver,
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
    except:
        logger.warning(f"{name} failed. start new program", exc_info=True)
        return False
