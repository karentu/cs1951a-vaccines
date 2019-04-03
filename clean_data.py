import numpy as np
import pandas as pd

def clean_data():
    df = pd.read_csv('./complete.csv')

    # Remove school with 0 people
    df = df[df['k12_enrollment'] != 0]
    df.to_csv('complete_cleaned.csv')


def main():
    clean_data()

if __name__ == "__main__":
    main()
