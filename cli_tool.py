import argparse
import pandas as pd
import numpy as np
from functions import estimate_ci, cal_average_birth_prev, estimate_pooled_birth_prev_inverse, cal_Q_I2

def main():
    parser = argparse.ArgumentParser(description='Birth Prevalence Estimation Tool')
    
    # Add arguments
    parser.add_argument('--input_file', type=str, help='Input file path')
    parser.add_argument('--output_file', type=str, help='Output file path')
    
    # Parse arguments
    args = parser.parse_args()

    # Prompt for input file if not provided
    if not args.input_file:
        args.input_file = input("Please enter the absolute path for the input file: ")
        print(f'The input file path you enter: {args.input_file}')

    # Prompt for output file if not provided
    if not args.output_file:
        args.output_file = input("Please enter the output file name (without file extension): ")
        print(f'The output file name you enter: {args.output_file}')

    # Read input file
    input_df = pd.read_csv(args.input_file)

    # Estimate 95% CI
    df_estimate_ci = estimate_ci(input_df)

    # Calculate average birth prevalence
    avg_birth_prev_df = cal_average_birth_prev(df_estimate_ci)
    # avg_birth_prev_df.to_csv(args.output_file, index=False)

    # Estimate pooled birth prevalence using inverse variance method
    inverse_df = estimate_pooled_birth_prev_inverse(avg_birth_prev_df)
    # inverse_df.to_csv(args.output_file, index=False)

    # Calculate I2
    q_i2_df = cal_Q_I2(inverse_df)
    # q_i2_df.to_csv(args.output_file, index=False)

    # Subset columns
    target_columns = [
        "author and year",
        "case",
        "population",
    "birth_prevalence_100k",
    "95 CI, lower_bound (poisson dist)",
    "95 CI, upper_bound (poisson dist)",
    "average birth prevalence_100k",
    "95CI lower bound average",
    "95CI upper bound average",
    "pooled birth prevalence (inverse) per 100K",
    "95 CI, lower_bound (inverse)",
    "95 CI, upper_bound (inverse)",
    "Q_statistic",
    "I2_statistic"]

    q_i2_df_subset = q_i2_df[target_columns]

    # Save output
    q_i2_df_subset.to_csv(args.output_file, index=False)

# Call main function
if __name__ == '__main__':
    main()