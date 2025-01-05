import pandas as pd
from prettytable import PrettyTable

def reconcile_account_history_funding(file_path):
    """
    Reconcile account transactions from a CSV file.
    
    Args:
        file_path (str): Path to the CSV file containing account transactions
        
    Returns:
        pd.DataFrame: Summary of deposits, withdrawals, and net movement
    """
    # Read the CSV file
    df = pd.read_csv(file_path, low_memory=False)
    
    # Calculate sums based on conditions
    deposits = df[
        (df['Side'].str.lower().str.strip() == 'deposit') & 
        (df['Type'].str.lower().str.strip() == 'deposit')
    ]['Amount'].sum()

    withdrawals = df[
        (df['Side'].str.lower().str.strip().str.contains('withdraw', na=False)) & 
        (df['Type'].str.lower().str.strip().str.contains('withdraw', na=False))
    ]['Amount'].sum()
    
    # Create summary DataFrame
    summary_df = pd.DataFrame({
        'Metric': ['Total Deposits', 'Total Withdrawals', 'Net Movement'],
        'Amount': [deposits, withdrawals, deposits - withdrawals]
    })
    
    return summary_df

def reconcile_spot_order_history(file_path):
    """
    Reconcile spot order history by calculating buy/sell volumes per symbol.
    
    Args:
        file_path (str): Path to the CSV file containing spot order history
        
    Returns:
        pd.DataFrame: Summary of buy volume, sell volume, and net volume per symbol
    """
    # Read the CSV file
    df = pd.read_csv(file_path)
    
    # Convert Side to uppercase and strip whitespace for consistency
    df['Side'] = df['Side'].str.upper().str.strip()
    
    # Group by symbol and side, sum the filled volumes and fees
    grouped_volume = df.groupby(['Symbol', 'Side'])['Filled Volume'].sum().unstack(fill_value=0)
    grouped_fee = df.groupby(['Symbol', 'Side'])['Fee'].sum().unstack(fill_value=0)
    
    # Rename columns for clarity
    spot_order_history_df = grouped_volume.rename(columns={
        'BUY': 'Buy Volume',
        'SELL': 'Sell Volume'
    })
    
    # Add fee columns
    spot_order_history_df['Buy Fee'] = grouped_fee['BUY']
    spot_order_history_df['Sell Fee'] = grouped_fee['SELL']
    spot_order_history_df['Total Fee'] = spot_order_history_df['Buy Fee'] + spot_order_history_df['Sell Fee']
    
    # Calculate net volume including fees: (Sell Volume + Total Fee) - Buy Volume
    spot_order_history_df['Net Volume'] = (
        spot_order_history_df['Sell Volume'] + 
        spot_order_history_df['Total Fee'] -
        spot_order_history_df['Buy Volume']
    )
    
    # Reset index to make Symbol a column
    spot_order_history_df = spot_order_history_df.reset_index()
    
    return spot_order_history_df

# Example usage:
if __name__ == "__main__":
    # Account History Funding Results
    file_path = 'combined/Account History_Funding Account-combined.csv'
    history_results = reconcile_account_history_funding(file_path)
    
    funding_table = PrettyTable()
    funding_table.field_names = ["Metric", "Amount"]
    funding_table.align = "l"  # Left align all columns
    for _, row in history_results.iterrows():
        funding_table.add_row([row['Metric'], f"${row['Amount']:,.2f}"])
    print("\nDeposit/Withdrawal History Summary:")
    print(funding_table)

    # Spot Order History Summary
    spot_results = reconcile_spot_order_history('combined/Spot Orders_Filled Orders (Show Order-Splitting)-combined.csv')
    summary_stats = {
        'Total Buy Volume': spot_results['Buy Volume'].sum(),
        'Total Sell Volume': spot_results['Sell Volume'].sum(),
        'Total Net Volume': spot_results['Net Volume'].sum(),
    }
    
    spot_table = PrettyTable()
    spot_table.field_names = ["Metric", "Value"]
    spot_table.align = "l"  # Left align all columns
    for metric, value in summary_stats.items():
        spot_table.add_row([metric, f"{value:,.2f}"])
    print("\nSpot Order History Summary:")
    print(spot_table)

    # Calculate combined net movement (calculated from Account History_Funding Account-combined.csv)
    history_net = history_results.loc[history_results['Metric'] == 'Net Movement', 'Amount'].iloc[0]
    spot_net = summary_stats['Total Net Volume']
    combined_net = history_net + spot_net

    # Display combined results
    combined_table = PrettyTable()
    combined_table.field_names = ["Metric", "Value"]
    combined_table.align = "l"
    combined_table.add_row(["Deposit/Withdrawal Net", f"${history_net:,.2f}"])
    combined_table.add_row(["Spot Net Volume", f"{spot_net:,.2f}"])
    combined_table.add_row(["-" * 20, "-" * 20])  # Add divider row
    combined_table.add_row(["Combined Net", f"{combined_net:,.2f}"])
    print("\nCombined Results ('Combined Net' shows discrepancy between deposit/withdrawls and trading losses):")
    print(combined_table)
