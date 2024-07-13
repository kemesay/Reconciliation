import streamlit as st
import pandas as pd
import numpy as np
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module='openpyxl')
pd.set_option('future.no_silent_downcasting', True)
# Function to filter dataframe based on start and end times

def filter_by_time(df, start_time, end_time):
    df['Authorize Date'] = pd.to_datetime(df['Authorize Date'])
    df['Time'] = df['Authorize Date'].dt.time
    filtered_df = df[(df['Time'] >= start_time) & (df['Time'] <= end_time)]
    return filtered_df.drop(columns=['Time'])

st.markdown("""
    <style>
        .main-title {
            color: #3498db;
            font-size: 30px;
            font-weight: bold;
            height: 100px;
            width: 100%;
        }
        .sub-title {
            color: #141414;
            font-size: 15px;
            font-weight: bold;
        }
        .error-message {
            color: #e74c3c;
            font-size: 20px;
        }
        .success-message {
            color: #27ae60;
            font-size: 20px;
        }
        .summary-table {
            width: 100%;
            border-collapse: collapse;
        }
        .summary-table, .summary-table th, .summary-table td {
            border: 1px solid black;
        }
        .summary-table th, .summary-table td {
            padding: 10px;
            text-align: left;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for file uploaders
if 'uploaded_file1' not in st.session_state:
    st.session_state['uploaded_file1'] = None
if 'uploaded_file2' not in st.session_state:
    st.session_state['uploaded_file2'] = None
if 'uploaded_file3' not in st.session_state:
    st.session_state['uploaded_file3'] = None
if 'uploaded_file_reference' not in st.session_state:
    st.session_state['uploaded_file_reference'] = None
if 'unique_debtors' not in st.session_state:
    st.session_state['unique_debtors'] = set()
if 'unique_creditors' not in st.session_state:
    st.session_state['unique_creditors'] = set()

st.markdown('<h1 class="main-title"> DX-Valley Reconciliation Tool For E-birr and CBO</h1>', unsafe_allow_html=True)

st.markdown('<h2 class="sub-title">Upload files that will be used in reconciliation and becare of the files since they must be relate in dates.</h2>', unsafe_allow_html=True)
uploaded_file1 = st.file_uploader("Upload the first Excel file (Last date morning)", type=["xlsx"], key='file1')
uploaded_file2 = st.file_uploader("Upload the second Excel file (Last date afternoon)", type=["xlsx"], key='file2')
uploaded_file3 = st.file_uploader("Upload the third Excel file (Today morning)", type=["xlsx"], key='file3')
uploaded_file_reference = st.file_uploader("Upload the reference Excel file", type=["xlsx"], key='file4')

if uploaded_file1 and uploaded_file2 and uploaded_file3 and uploaded_file_reference:
    st.session_state['uploaded_file1'] = uploaded_file1
    st.session_state['uploaded_file2'] = uploaded_file2
    st.session_state['uploaded_file3'] = uploaded_file3
    st.session_state['uploaded_file_reference'] = uploaded_file_reference
    
    #  Actions
    if st.button("Start Reconciliation"):
        try:
            header_keywords = [ 'Ebirr TRANSFERID', 'OPER ID']
            
            df_main1 = pd.read_excel(st.session_state['uploaded_file1'], header=None) 
            header_row_index = df_main1[df_main1.apply(lambda row: row.astype(str).str.contains('|'.join(header_keywords)).any(), axis=1)].index[0]
            df_main1 = pd.read_excel(uploaded_file1, header=header_row_index)
            df_main1 = df_main1.replace(r'^\s*$', np.nan, regex=True)
            df_main1 = df_main1.dropna(how='all')
            df_main1.drop(columns=[col for col in df_main1.columns if 'Unnamed' in col], inplace=True)
            df_main1.replace('-', 0, inplace=True)

            identifier_column = next((col for col in df_main1.columns if any(keyword in col for keyword in header_keywords)), None)
            if identifier_column:
                df_main1 = df_main1[df_main1[identifier_column].notna()]
            if identifier_column:
                df_main1[identifier_column] = pd.to_numeric(df_main1[identifier_column], errors='coerce')
                zero_index = df_main1[df_main1[identifier_column] == 0].index
                if not zero_index.empty:
                    end_of_table_index = zero_index[0]
                    df_main1 = df_main1.iloc[:end_of_table_index]
            df_main1.dropna(how='all')

            start_time1 = pd.to_datetime('00:00:00').time()
            end_time1 = pd.to_datetime('08:59:59').time()
            filtered_df1 = filter_by_time(df_main1, start_time1, end_time1)
            
            # print(filtered_df1.head(5))
            # print(filtered_df1.tail(5))            
            ##################################### Read and filter the second file (Last date afternoon)
            df_main2 = pd.read_excel(st.session_state['uploaded_file2'], header=None) 
            header_row_index = df_main2[df_main2.apply(lambda row: row.astype(str).str.contains('|'.join(header_keywords)).any(), axis=1)].index[0]
            df_main2 = pd.read_excel(uploaded_file2, header=header_row_index)
            df_main2 = df_main2.replace(r'^\s*$', np.nan, regex=True)
            df_main2 = df_main2.dropna(how='all')
            df_main2.drop(columns=[col for col in df_main2.columns if 'Unnamed' in col], inplace=True)
            df_main2.replace('-', 0, inplace=True)

            identifier_column = next((col for col in df_main2.columns if any(keyword in col for keyword in header_keywords)), None)
            if identifier_column:
                df_main2 = df_main2[df_main2[identifier_column].notna()]
            if identifier_column:
                df_main2[identifier_column] = pd.to_numeric(df_main2[identifier_column], errors='coerce')
                zero_index = df_main2[df_main2[identifier_column] == 0].index
                if not zero_index.empty:
                    end_of_table_index = zero_index[0]
                    df_main2 = df_main2.iloc[:end_of_table_index]
            df_main2.dropna(how='all')
            
            start_time2 = pd.to_datetime('09:00:00').time()
            end_time2 = pd.to_datetime('14:59:59').time()
            filtered_df2 = filter_by_time(df_main2, start_time2, end_time2)
            
            
            # print("df_main2-detail", filtered_df2.head(5))
            # print("df_main2-detail", filtered_df2.tail(5))
            ################################### Read and filter the third file (Today morning)
            df_main3 = pd.read_excel(st.session_state['uploaded_file3'], header=None)          
            header_row_index = df_main3[df_main3.apply(lambda row: row.astype(str).str.contains('|'.join(header_keywords)).any(), axis=1)].index[0]
            df_main3 = pd.read_excel(uploaded_file3, header=header_row_index)
            df_main3 = df_main3.replace(r'^\s*$', np.nan, regex=True)
            df_main3 = df_main3.dropna(how='all')
            df_main3.drop(columns=[col for col in df_main3.columns if 'Unnamed' in col], inplace=True)
            df_main3.replace('-', 0, inplace=True)

            identifier_column = next((col for col in df_main3.columns if any(keyword in col for keyword in header_keywords)), None)
            if identifier_column:
                df_main3 = df_main3[df_main3[identifier_column].notna()]
            if identifier_column:
                df_main3[identifier_column] = pd.to_numeric(df_main3[identifier_column], errors='coerce')
                zero_index = df_main3[df_main3[identifier_column] == 0].index
                if not zero_index.empty:
                    end_of_table_index = zero_index[0]
                    df_main3 = df_main3.iloc[:end_of_table_index]
            df_main3.dropna(how='all')
            

            
            start_time3 = pd.to_datetime('15:00:00').time()
            end_time3 = pd.to_datetime('23:59:59').time()
            filtered_df3 = filter_by_time(df_main3, start_time3, end_time3)
            
            # print("df_main33_detail",filtered_df3.head(5) )
            # print("df_main33_detail",filtered_df3.tail(5) )


            # Concatenate all filtered DataFrames
            df_main = pd.concat([filtered_df1, filtered_df2, filtered_df3], ignore_index=True)
            
            
            # Read the reference file of E-birr
            df_reference = pd.read_excel(st.session_state['uploaded_file_reference'], header=None) 
            header_row_index = df_reference[df_reference.apply(lambda row: row.astype(str).str.contains('|'.join(header_keywords)).any(), axis=1)].index[0]
            df_reference = pd.read_excel(uploaded_file_reference, header=header_row_index)
            df_reference = df_reference.replace(r'^\s*$', np.nan, regex=True)
            df_reference = df_reference.dropna(how='all')
            df_reference.drop(columns=[col for col in df_reference.columns if 'Unnamed' in col], inplace=True)
            df_reference.replace('-', 0, inplace=True)

            identifier_column = next((col for col in df_reference.columns if any(keyword in col for keyword in header_keywords)), None)
            if identifier_column:
                df_reference = df_reference[df_reference[identifier_column].notna()]
            if identifier_column:
                df_reference[identifier_column] = pd.to_numeric(df_reference[identifier_column], errors='coerce')
                zero_index = df_reference[df_reference[identifier_column] == 0].index
                if not zero_index.empty:
                    end_of_table_index = zero_index[0]
                    df_reference = df_reference.iloc[:end_of_table_index]
            df_reference.dropna(how='all')
            
            # print(df_reference.head(5))
            # print(df_reference.tail(5))
            
            # Change Debitor and Creditor amount ton the same data type
            df_main['Transaction Amount'] = df_main['Transaction Amount'].str.replace(',', '').astype(float)
            df_reference['CREDIT'] = df_reference['CREDIT'].astype(float)
            
            # Extract unique debtors and creditors dynamically
            if 'Debtor Institution' in df_main.columns:
                st.session_state['unique_debtors'].update(df_main['Debtor Institution'].unique())
            if 'Creditor institution' in df_main.columns:
                st.session_state['unique_creditors'].update(df_main['Creditor institution'].unique())

            unique_debtors_list = sorted(list(st.session_state['unique_debtors']))
            unique_creditors_list = sorted(list(st.session_state['unique_creditors']))

            # Perform additional analysis
            main_sum = df_main['Transaction Amount'].sum()
            reference_sum = df_reference['CREDIT'].sum()
            difference = main_sum - reference_sum
            
            # Filter debtor and creditor institutions
            debtor_institutions = df_main[df_main['Debtor Institution'].isin(unique_debtors_list)]
            creditor_institutions = df_main[df_main['Creditor institution'].isin(unique_creditors_list)]
            # Calculate outstanding values
            debtor_sum = debtor_institutions.groupby('Debtor Institution')['Transaction Amount'].sum()
            creditor_sum = creditor_institutions.groupby('Creditor institution')['Transaction Amount'].sum()
            # Perform the reconciliation
            main_cols = ['IP Original transaction ID', 'Transaction Amount']
            ref_cols = ['Bank TRANSFERID', 'CREDIT']
      
            # merged = pd.merge(df_main, df_reference, how='right', left_on=main_cols, right_on=ref_cols, indicator=True)
            # # Filter out unmatched records that exist only in df_file_two
            # matched = merged[merged['_merge'] == 'both']
            # unmatched = merged[merged['_merge'] == 'right_only']

            # # Calculate sums
            # sum_matched_credit = matched['CREDIT'].sum()
            # sum_matched_transaction_amount = matched['Transaction Amount'].sum()
            # sum_unmatched_credit = unmatched['CREDIT'].sum()
            # default_reference_records= sum_matched_transaction_amount + sum_unmatched_credit
            
            merged = pd.merge(df_main, df_reference, how='outer', left_on=main_cols, right_on=ref_cols, indicator=True)
            # Filter out unmatched records that exist only in df_file_two
            matched = merged[merged['_merge'] == 'both']
            unmatched = merged[merged['_merge'] != 'both']
            # Calculate sums
            sum_matched_credit = matched['CREDIT'].sum()
            sum_unmatched_credit = unmatched['CREDIT'].sum()
            sum_credit = sum_matched_credit + sum_unmatched_credit
            
            sum_matched_transaction_amount = matched['Transaction Amount'].sum()
            sum_unmatched_transaction_amount = unmatched['Transaction Amount'].sum()
            sum_transaction_amount = sum_matched_transaction_amount + sum_unmatched_transaction_amount
            
            sum_of_unmatched = sum_unmatched_credit + sum_unmatched_transaction_amount

            
            
            # Save the unmatched records and additional reports to an Excel file
            with pd.ExcelWriter('unmatched_records_new1.xlsx') as writer:
                unmatched.to_excel(writer, sheet_name='Unmatched Records', index=False)
                pd.DataFrame({
                    'Main Sum': [main_sum],
                    'Reference Sum': [reference_sum],
                    'Difference': [difference]
                }).to_excel(writer, sheet_name='Summary', index=False)
                debtor_sum.to_excel(writer, sheet_name='Debtor Institution Summary')
                creditor_sum.to_excel(writer, sheet_name='Creditor Institution Summary')


            # Display results in Streamlit              
            st.markdown('<h1 class="main-title">Overall Summary</h1>', unsafe_allow_html=True)
            st.markdown('<h2 class="sub-title">Unmatched Records In CSV Format and You can downlaod it</h2>', unsafe_allow_html=True)
            st.dataframe(unmatched)

            # Display additional analysis results
            col1, col2 = st.columns(2)
            with col1:
                st.markdown('<h2 class="sub-title">Before Reconsiliation Analysis </h2>', unsafe_allow_html=True)
                
                st.markdown(f"""
                    <table class="summary-table">
                        <tr>
                            <th>IPs (CBS) sum</th>
                            <td>ETB{main_sum:,.2f}</td>
                        </tr>
                        <tr>
                            <th>E-birr Sum</th>
                            <td>ETB{reference_sum:,.2f}</td>
                        </tr>
                        <tr>
                            <th>Difference Between them</th>
                            <td>ETB{difference:,.2f}</td>
                        </tr>
                    </table>
                """, unsafe_allow_html=True)
            col3, col4 = st.columns(2)
            with col3:
                st.markdown('<h2 class="sub-title">Debtor Institution Summary</h2>', unsafe_allow_html=True)
                st.write(debtor_sum)
            with col4:
                st.markdown('<h2 class="sub-title">Creditor Institution Summary</h2>', unsafe_allow_html=True)
                st.write(creditor_sum)

            # Display E-birr and IPS summaries
            st.markdown('<h2 class="sub-title" {{textAlign: center}}>After Reconsiliation Analysis \n </h2>', unsafe_allow_html=True)

            col5, col6 = st.columns(2)
            with col5:
                
                st.markdown('<h3 class="sub-title">Summary of E-birr</h3>', unsafe_allow_html=True)
                st.markdown(f"""
                    <table class="summary-table">
                        <tr>
                            <th>Sum of matched credit</th>
                            <td>ETB{sum_matched_credit:,.2f}</td>
                        </tr>
                        <tr>
                            <th>Sum of unmatched credit</th>
                            <td>ETB{sum_unmatched_credit:,.2f}</td>
                        </tr>
                        <tr>
                            <th>Sum credit</th>
                            <td>ETB{sum_credit:,.2f}</td>
                        </tr>
                    </table>
                """, unsafe_allow_html=True)
            with col6:
            # Display IPS summary in table format
                st.markdown('<h3 class="sub-title">Summary of IPS (CBO)</h3>', unsafe_allow_html=True)
                st.markdown(f"""
                    <table class="summary-table">
                        <tr>
                            <th>Sum of matched transaction amount</th>
                            <td>ETB{sum_matched_transaction_amount:,.2f}</td>
                        </tr>
                        <tr>
                            <th>Sum of unmatched transaction amount</th>
                            <td>ETB{sum_unmatched_transaction_amount:,.2f}</td>
                        </tr>
                        <tr>
                            <th>Sum of transaction amount</th>
                            <td>ETB{sum_transaction_amount:,.2f}</td>
                        </tr>
                    </table>
                """, unsafe_allow_html=True)
            # Display summary of unmatched records
            st.markdown('<h3 class="sub-title">Summary of Unmatched between two Records</h3>', unsafe_allow_html=True)
            st.markdown(f"""
                    <table class="Sum of unmatched records">
                        <tr>
                            <th>IPs (CBS) sum</th>
                            <td>ETB{sum_of_unmatched:,.2f}</td>
                        </tr>
    
                    </table>
                """, unsafe_allow_html=True)

            # Display debtor and creditor institution summaries

                
                

            # Provide a download link for the unmatched records
            with open("unmatched_records_new1.xlsx", "rb") as file:
                btn = st.download_button(
                    label="Download Unmatched Records",
                    data=file,
                    file_name="unmatched_records_new1.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            st.markdown('<p class="success-message">Unmatched records have been saved successfully.</p>', unsafe_allow_html=True)
        except Exception as e:
            st.markdown(f'<p class="error-message">An error occurred: {e}</p>', unsafe_allow_html=True)

    #Reset the fields with action button
    if st.button("Clear and Ready for next"):
        for key in st.session_state.keys():
            del st.session_state[key]

        st.rerun()
