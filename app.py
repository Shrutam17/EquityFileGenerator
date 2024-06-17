import streamlit as st
import pandas as pd

# st.image("C:\\Users\\Shrutam Shah\\Desktop\\SIHL\\logo.png", width=200)  # Adjust the width as needed
st.title("Welcome to SIHL's Equity File Generator")

def update_equity_file(df_equity, df_trade, df_block):
    required_trade_columns = ['ClientID', 'BuySell', 'No. Of Blocks']
    required_block_columns = ['Code', 'Symbol', 'Qty','Price']
    
    if all(column in df_trade.columns for column in required_trade_columns) and \
       all(column in df_block.columns for column in required_block_columns):

        rows_to_add = []
        for i, trade_row in df_trade.iterrows():
            for j, block_row in df_block.iterrows():
                new_row = {
                    'Code': block_row['Code'],
                    'ClientID': trade_row['ClientID'],
                    'BuySell': trade_row['BuySell'],
                    'Symbol': block_row['Symbol'],
                    'Price': block_row['Price'],
                    'Qty': block_row['Qty'] * trade_row['No. Of Blocks'],
                    'Exchange':'NseCm',
                    'Series':'EQ',
                    'ProtectionPercent':'1',
                    'ProCli':'Cli',
                    'Book':'RL',
                    'Trigger':'0',
                    'DiscQty':'0',
                    'Errors':'None',
                    'ValidityDays':'0',
                    'Product':trade_row['Product'],
                    'Special':'None',
                    'ExitTrigger':'0',
                    'ExitPrice':'0',
                    'TargetPrice':'0',
                    'OrderType':'Day',
                    
                }
                rows_to_add.append(new_row)

        df_equity_updated = pd.concat([df_equity, pd.DataFrame(rows_to_add)], ignore_index=True)
        return df_equity_updated
    else:
        st.error("Error: Missing required columns in df_trade or df_block")
        return pd.DataFrame()


trade_file = st.file_uploader("Upload Trade File (CSV)", type="csv")
if trade_file:
    df_trade = pd.read_csv(trade_file)
    # st.write("Trade File:")
    # st.write(df_trade)


block_file = st.file_uploader("Upload Block File (CSV)", type="csv")
if block_file:
    df_block = pd.read_csv(block_file)
    # st.write("Block File:")
    # st.write(df_block)
    
equity_file = st.file_uploader("Upload Reference File", type="csv")
if equity_file:
    df_equity = pd.read_csv(equity_file)
    # st.write("Reference File:")
    # st.write(df_equity)


if st.button("Generate Equity File"):
    if trade_file and block_file and equity_file:
        df_equity_updated = update_equity_file(df_equity, df_trade, df_block)
        # st.write("Updated Equity Trade File:")
        # st.write(df_equity_updated)
        
        st.download_button(
            label="Download Equity File",
            data=df_equity_updated.to_csv(index=False).encode('utf-8'),
            file_name='Updated_Equity_TradeFile.csv',
            mime='text/csv',
        )
    else:
        st.error("Please upload Trade, Block, and Existing Equity Trade files to update the Equity file.")
