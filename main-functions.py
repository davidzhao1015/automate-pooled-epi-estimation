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
# Estimate birth prevalence and 95% CI per study
#--------------------------------------------------------------

def estimate_ci(df, dist_type=None):
    # Calculate birth prevalence
    df['birth_prevalence'] = df['case'] / df['population']
    df['birth_prevalence_100k'] = df['birth_prevalence'] * 100000

    # Calculate margin of error
    df['margin_of_error'] = 1.96 * np.sqrt(df['birth_prevalence'] * (1 - df['birth_prevalence']) / df['population'])
    df['margin_of_error_100k'] = df['margin_of_error'] * 100000

    if dist_type == 'normal':
        # Follow normal distribution 
        for i in range(len(df)):
            df.loc[i, '95 CI, lower_bound (normal dist)'] = df.loc[i, 'birth_prevalence_100k'] - df.loc[i, 'margin_of_error_100k'] if (df.loc[i, 'birth_prevalence_100k'] - df.loc[i, 'margin_of_error_100k']) > 0 else 0
            df.loc[i, '95 CI, upper_bound (normal dist)'] = df.loc[i, 'birth_prevalence_100k'] + df.loc[i, 'margin_of_error_100k']
    elif dist_type == 'poisson' or dist_type == None:
        # Follow Poisson distribution
        df['95 CI, lower_bound (poisson dist)'] = scipy.stats.poisson.ppf(0.025, df['case']) / df['population'] * 100000
        df['95 CI, upper_bound (poisson dist)'] = scipy.stats.poisson.ppf(0.975, df['case']) / df['population'] * 100000

    return df    

# estimate_ci(input_df, dist_type='normal')



#--------------------------------------------------------------
# Calculate average (pool) birth prevalence and 95% CI 
#--------------------------------------------------------------

def cal_average_birth_prev(df):
    df_estimate_ci = estimate_ci(df)

    # Calculate weights per study
    df_estimate_ci['weight per study'] = df_estimate_ci['population'] / df_estimate_ci['population'].sum()

    # Calculate weighted birth prevalence per study
    df_estimate_ci['weighted birth prevalence per study'] = df_estimate_ci['birth_prevalence'] * df_estimate_ci['weight per study']

    # Calculate average birth prevalence 
    df_estimate_ci['average birth prevalence'] = df_estimate_ci['weighted birth prevalence per study'].sum()
    df_estimate_ci['average birth prevalence_100k'] = df_estimate_ci['average birth prevalence'] * 100000

    # Calculate 95% CI lower and upper bound per study
    df_estimate_ci['95CI lower bound weighted'] = df_estimate_ci['weight per study'] * df_estimate_ci['95 CI, lower_bound (poisson dist)']
    df_estimate_ci['95CI upper bound weighted'] = df_estimate_ci['weight per study'] * df_estimate_ci['95 CI, upper_bound (poisson dist)']

    # Calculate 95% CI lower and upper bound for average birth prevalence
    df_estimate_ci['95CI lower bound average'] = df_estimate_ci['95CI lower bound weighted'].sum()
    df_estimate_ci['95CI upper bound average'] = df_estimate_ci['95CI upper bound weighted'].sum()

    return df_estimate_ci

# avg_birth_prev_df = cal_average_birth_prev(input_df)

# avg_birth_prev_df.to_csv('output.csv', index=False)



#-----------------------------------------------------------------
# Estimate pooled birth prevalence using inverse variance method
#------------------------------------------------------------------

def estimate_pooled_birth_prev_inverse(df):
    # Calculate std error per study
    df['std error per 100K'] = np.sqrt(df['birth_prevalence'] * (1 - df['birth_prevalence']) / df['population']) * 100000

    # Calculate weights per study
    df['cofficient per study'] = 1 / df['std error per 100K'] ** 2
    df['weight per study (inverse)'] = df['cofficient per study'] / df['cofficient per study'].sum()

    # Calculate weighted birth prevalence per study
    df['weighted birth prevalence per study (inverse) per 100K'] = df['birth_prevalence_100k'] * df['weight per study (inverse)'] 

    # Calculate pooled birth prevalence
    df['pooled birth prevalence (inverse) per 100K'] = df['weighted birth prevalence per study (inverse) per 100K'].sum()

    # Calculate standard error per 100K
    df['std error (inverse) per 100K'] = 1 / np.sqrt(df['cofficient per study'].sum()) 

    # Calculate margin of error
    df['margin of error (inverse) per 100K'] = 1.96 * df['std error (inverse) per 100K']

    # Calculate 95% CI lower and upper bound
    df['95 CI, lower_bound (inverse)'] = df['pooled birth prevalence (inverse) per 100K'] - df['margin of error (inverse) per 100K']
    df['95 CI, upper_bound (inverse)'] = df['pooled birth prevalence (inverse) per 100K'] + df['margin of error (inverse) per 100K']

    return df

inverse_df = estimate_pooled_birth_prev_inverse(input_df)

inverse_df.to_csv('output.csv', index=False)

#--------------------------------------------------------------
# Calculate Q and I^2 statistics
#--------------------------------------------------------------

def cal_Q_I2(df):
    df2 = cal_average_birth_prev(df)
    df_inverse = estimate_pooled_birth_prev_inverse(df2)

    # Calculate Q statistic
    df_inverse['weight_prev_square'] = df_inverse['cofficient per study'] * (df_inverse['birth_prevalence_100k'] ** 2)
    df_inverse['weight_prev'] = df_inverse['cofficient per study'] * df_inverse['birth_prevalence_100k']

    df['Q_statistic'] = df_inverse['weight_prev_square'].sum() - (df_inverse['weight_prev'].sum() ** 2/df_inverse['cofficient per study'].sum())

    df['freedom_degree'] = len(df_inverse) - 1

    # Calculate I^2 statistic
    df['I2_statistic'] = (df['Q_statistic'] - df['freedom_degree']) / df['Q_statistic'] 

    if df['I2_statistic'].values[0] < 0:
        df['I2_statistic'] = 0

    return df

# q_df = cal_Q_I2(input_df)

# q_df.to_csv('output_q.csv', index=False)