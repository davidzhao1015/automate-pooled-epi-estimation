import argparse
from functions import estimate_ci, cal_average_birth_prev, estimate_pooled_birth_prev_inverse, cal_Q_I2

def main():
    parser = argparse.ArgumentParser(description='Birth Prevalence Estimation Tool')
    parser.add_argument('input_file', type=str, help='Input file path')
    parser.add_argument('output_file', type=str, help='Output file path')
    args = parser.parse_args()

    input_df = pd.read_csv(args.input_file)
    df_estimate_ci = estimate_ci(input_df)
    avg_birth_prev_df = cal_average_birth_prev(df_estimate_ci)
    avg_birth_prev_df.to_csv(args.output_file, index=False)

    inverse_df = estimate_pooled_birth_prev_inverse(avg_birth_prev_df)
    inverse_df.to_csv(args.output_file, index=False)

    q_i2_df = cal_Q_I2(inverse_df)
    q_i2_df.to_csv(args.output_file, index=False)

if __name__ == '__main__':
    main()