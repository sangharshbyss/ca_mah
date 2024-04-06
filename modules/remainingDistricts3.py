"""
1. module of ws3.py
2. improved from remainingDistrict.py
3. adds name of problem distirct to a list
4. changes - shifted to subfoler.
"""
from pathlib import Path
import logging
import pandas as pd



logger = logging.getLogger(__name__)


def districtWithProblem(name_of_problem, from_date, to_date, record):
    dictionary = {'District': [name_of_problem],
                  'from_date': [from_date],
                  'to_date': [to_date],
                  'number_of_record': [record]}
    file_name = f'remaining_district_{from_date}_{to_date}.csv'
    dir_name = Path(f'/home/sangharsh/Documents/PoA/data/FIR/y_23/remaining_districts')
    dir_name.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame.from_dict(dictionary)
    df.to_csv(dir_name/file_name, mode='a', index=False, header=False)
    logger.info(f"{name_of_problem} added to remaining district")
