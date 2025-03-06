#=========================================================================================
# This file contains the main functions that implement estimation 
# of pooled prevalence and its confidence interval following ISMS method. 
# Reference: ISMS_Birth_Prevalence_Pooled_Estimate_TEMPLATE_2023.07.27_CB_archived.xlsx
#=========================================================================================

import pandas as pd
import numpy as np
import scipy
from scipy import stats
import math



#--------------------------------------------------------------
# Simulate input data
#--------------------------------------------------------------

input_df = pd.DataFrame({
    'author and year': ['Poupetova, 2010', 'Dionisi-Vici, 2002', 'Poorthuis, 1999', 'Hult, 2014', 'Czatoryska, 1993', 'Smith, 2011', 'Applegarth, 1999', 'Chin, 2022'],
    'case': [8, 22, 30, 10, 11, 33, 3, 13],
    'population': [3362889, 7173959, 7358444, 2080791, 11951872, 15192000, 1035816, 3693759],
})

input_df.head()


#--------------------------------------------------------------
# Calculate point birth prevalence
#--------------------------------------------------------------
def cal_birth_prevalence(df):
    df['birth_prevalence'] = df['case'] / df['population']
    df['birth_prevalence_100k'] = df['birth_prevalence'] * 100000
    return df

#--------------------------------------------------------------
# Calculate margin of error of birth prevalence 
#--------------------------------------------------------------
def cal_margin_of_error(df):
    df['margin_of_error'] = 1.96 * np.sqrt(df['birth_prevalence'] * (1 - df['birth_prevalence']) / df['population'])
    df['margin_of_error_100k'] = df['margin_of_error'] * 100000
    return df

# cal_birth_prevalence(input_df)
# cal_margin_of_error(input_df)