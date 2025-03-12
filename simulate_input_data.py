#--------------------------------------------------------------
# Simulate input data
#--------------------------------------------------------------

input_df = pd.DataFrame({
    'author and year': ['Poupetova, 2010', 'Dionisi-Vici, 2002', 'Poorthuis, 1999', 'Hult, 2014', 'Czatoryska, 1993', 'Smith, 2011', 'Applegarth, 1999', 'Chin, 2022'],
    'case': [8, 22, 30, 10, 11, 33, 3, 13],
    'population': [3362889, 7173959, 7358444, 2080791, 11951872, 15192000, 1035816, 3693759],
})

input_df.head()

input_df.to_csv('input.csv', index=False)