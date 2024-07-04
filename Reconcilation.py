# import pandas as pd
# import numpy as np

# file_path = 'CBOTest.xlsx'
# df = pd.read_excel(file_path)
# df['Authorize Date'] = pd.to_datetime(df['Authorize Date'])

# df['Authorize Date Date'] = df['Authorize Date'].dt.date
# df_2024_06_10 = df[df['Authorize Date Date'] == pd.to_datetime('2024-06-10').date()]
# df_2024_06_11 = df[df['Authorize Date Date'] == pd.to_datetime('2024-06-11').date()]
# df_2024_06_10 = df_2024_06_10.drop(columns=['Authorize Date Date'])
# df_2024_06_11 = df_2024_06_11.drop(columns=['Authorize Date Date'])
# print(df_2024_06_10.head(10))
# print(df_2024_06_11.head(10))

# # Save the filtered data to new Excel files with the original timestamps in filenames
# df_2024_06_10.to_excel('CBOTest_2024-06-10.xlsx', index=False)
# df_2024_06_11.to_excel('CBOTest_2024-06-11.xlsx', index=False)
# print("Files have been saved successfully.")


# import pandas as pd

# df_reference = pd.read_excel('Ebirr_2024-06-11.xlsx')
# df_reference['TRANSFERDATE'] = pd.to_datetime(df_reference['TRANSFERDATE'])
# df_reference['Time'] = df_reference['TRANSFERDATE'].dt.time
# start_time = pd.to_datetime('00:00:00').time()
# end_time = pd.to_datetime('08:59:59').time()

# filtered_df = df_reference[(df_reference['Time'] >= start_time) & (df_reference['Time'] <= end_time)]
# print(filtered_df.head(10))
# filtered_df = filtered_df.drop(columns=['Time'])
# filtered_df.to_excel('Filtered_Ebirr_2024_06_11.xlsx', index=False)

# # print("Filtered records have been saved successfully.")



import pandas as pd
df_main = pd.read_excel('CBOTest_2024-06-11.xlsx')
df_reference = pd.read_excel('Filtered_Ebirr_2024_06_11.xlsx')
df_main['Transaction Amount'] = df_main['Transaction Amount'].str.replace(',', '').astype(float)
df_reference['CREDIT'] = df_reference['CREDIT'].astype(float)

main_cols = ['IP Original transaction ID',  'Transaction Amount']
ref_cols = ['Bank TRANSFERID',  'CREDIT']
# print(df_main[main_cols].head(10))
# print(df_reference[ref_cols].head(10))

# Perform the reconciliation
merged = pd.merge(df_main, df_reference, how='outer', left_on=main_cols, right_on=ref_cols, indicator=True)
unmatched = merged[merged['_merge'] != 'both']
unmatched.to_excel('unmatched_records.xlsx', index=False)
print("Unmatched records have been saved successfully.")