import argparse
import pandas as pd
import numpy as np
from functions import estimate_ci, cal_average_birth_prev, estimate_pooled_birth_prev_inverse, cal_Q_I2

def main():
    parser = argparse.ArgumentParser(description='Birth Prevalence Estimation Tool')
    
    # Add arguments
    parser.add_argument('input_file', type=str, help='Input file path')
    parser.add_argument('output_file', type=str, help='Output file path')
    
    # Parse arguments
    args = parser.parse_args()

    # Read input file
    input_df = pd.read_csv(args.input_file)

    # Estimate 95% CI
    df_estimate_ci = estimate_ci(input_df)

    # Calculate average birth prevalence
    avg_birth_prev_df = cal_average_birth_prev(df_estimate_ci)
    avg_birth_prev_df.to_csv(args.output_file, index=False)

    # Estimate pooled birth prevalence using inverse variance method
    inverse_df = estimate_pooled_birth_prev_inverse(avg_birth_prev_df)
    inverse_df.to_csv(args.output_file, index=False)

    # Calculate I2
    q_i2_df = cal_Q_I2(inverse_df)
    q_i2_df.to_csv(args.output_file, index=False)

# Call main function
if __name__ == '__main__':
    main()