#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def calculate_mean(data_frame, col_name):
    import pandas as pd
    import numpy as np
    ### Check if data_frame is a pandas DataFrame
    if not isinstance(data_frame, pd.DataFrame):
        raise ValueError("Error: The first argument must be a pandas DataFrame.")
    
    ### Check if col_name is a string
    if not isinstance(col_name, str):
        raise ValueError("Error: The column name must be a string.")
    
    try:
        ### Check if column exists in the DataFrame
        if col_name not in data_frame.columns:
            raise KeyError("Error: The specified column name does not exist in the DataFrame.")
        
        ### Check if the data in the column is numeric
        if not pd.api.types.is_numeric_dtype(data_frame[col_name]):
            raise TypeError("Error: The data in the specified column is not numerical.")
        
        return data_frame[col_name].mean()
    
    except KeyError as ke:
        raise ValueError(ke)
    except TypeError as te:
        raise ValueError(te)
    except Exception as e:
        raise ValueError(f"Error: {e}")


# In[ ]:


def calculate_std_dev(data_frame, col_name):
    import pandas as pd
    import numpy as np
    # Check if data_frame is a pandas DataFrame
    if not isinstance(data_frame, pd.DataFrame):
        raise ValueError("Error: The first argument must be a pandas DataFrame.")
    
    # Check if col_name is a string
    if not isinstance(col_name, str):
        raise ValueError("Error: The column name must be a string.")
    
    try:
        # Check if column exists in the DataFrame
        if col_name not in data_frame.columns:
            raise KeyError("Error: The specified column name does not exist in the DataFrame.")
        
        # Check if the data in the column is numeric
        if not pd.api.types.is_numeric_dtype(data_frame[col_name]):
            raise TypeError("Error: The data in the specified column is not numerical.")
        
        return data_frame[col_name].std()
    
    except KeyError as ke:
        raise ValueError(ke)
    except TypeError as te:
        raise ValueError(te)
    except Exception as e:
        raise ValueError(f"Error: {e}")


# In[ ]:


import pandas as pd
import numpy as np
def calculate_portfolio_stats(stock_returns_list):
    stats = {
        "Stock": [],
        "Mean Return": [],
        "Risk (Std Dev)": []
    }
    
    try:
        for i, returns in enumerate(stock_returns_list, start=1):
            mean = calculate_mean(returns)
            std_dev = calculate_std_dev(returns)
            
            stats["Stock"].append(f"Stock {i}")
            stats["Mean Return"].append(mean)
            stats["Risk (Std Dev)"].append(std_dev)
            df_stats = pd.DataFrame(stats)
        return df_stats
    
    except ValueError as ve:
        raise ve
    except Exception as e:
        raise ValueError(f"Error calculating portfolio stats: {e}")


# In[ ]:


"""
Simulates a specified number of random portfolios based on the provided list of asset return data frames,
and calculates their respective returns, risks, and Sharpe ratios.

** Parameters ** :
asset_data_list (list): A list of pandas DataFrame objects, where each DataFrame contains the return data for a single asset.
num_portfolios (int): The number of portfolios to simulate.
risk_free_rate (float): The risk-free rate used to calculate the Sharpe ratio. Default is 0.0.

** Returns **:
results_df (pandas.DataFrame): A DataFrame containing the simulated portfolios' returns, risks (standard deviations), 
                               and Sharpe ratios, with columns named 'Return', 'Risk', and 'Sharpe'.
weights_record (list): A list of arrays, where each array contains the asset weights for a corresponding simulated portfolio.
##################################################################################################################
##################################################################################################################
Detailed Steps:  #
#################
1. Determine the number of assets by the length of the asset_data_list.

2. Combine the individual asset return data frames into a single DataFrame named combined_data, aligning them column-wise.

3. Rename the columns of combined_data to 'Asset_1', 'Asset_2', ..., reflecting the number of risky assets for clarity.

4. Calculate the mean returns of each asset using the calculate_mean function, storing the results in mean_returns array.

5. Compute the covariance matrix of the asset returns using combined_data.cov() and store it in cov_matrix.

6. Initialize an array named results to store the simulation results, with each row representing a portfolio and columns 
   for portfolio return, standard deviation (risk), and Sharpe ratio.

7. Initialize an empty list named weights_record to store the asset weights for each simulated portfolio.

8. For each portfolio simulation (up to num_portfolios):
   a. Generate a random array of weights for the assets and normalize it so that the weights sum to 1.
   b. Record the generated weights in weights_record.
   c. Calculate the portfolio return as the dot product of weights and mean_returns.
   d. Calculate the portfolio standard deviation (risk) as the square root of the weighted sum of cov_matrix.
   e. Compute the Sharpe ratio by dividing the portfolio return minus the risk-free rate by the portfolio standard deviation.
   f. Store the portfolio return, standard deviation, and Sharpe ratio in the results array.

9. Convert the results array into a pandas DataFrame named results_df with columns 'Return', 'Risk', and 'Sharpe' for easier plotting and analysis.

10. Return results_df and weights_record, providing the calculated portfolio performance metrics and their respective asset allocations.


# In[ ]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def simulate_portfolios(asset_data_list, num_portfolios, risk_free_rate=0.2):
    try:
        ###### Validate inputs
        ###  If errors is not correct
        if not isinstance(asset_data_list,list):
            raise ValueError("Error: asset_data_list must be a list of pandas DataFrames.")
        if not all(isinstance(series, pd.Series) for series in asset_data_list):
            raise ValueError("Error: All elements in asset_data_list must be pandas Series.")
        if not isinstance(num_portfolios, int) or num_portfolios <= 0:
            raise ValueError("Error: num_portfolios must be a positive integer.")
        if not isinstance(risk_free_rate, (int, float)):
            raise ValueError("Error: risk_free_rate must be a numeric value.")
        ### If no error
        num_assets = len(asset_data_list)
        
        ### Combine data into a single DataFrame
        combined_data = pd.concat(asset_data_list, axis=1)
        
        ### Rename columns to reflect the number of risky assets
        combined_data.columns = [f'Asset_{i+1}' for i in range(num_assets)]
        
        ### Calculate mean returns and covariance matrix
        mean_returns = np.array([calculate_mean(combined_data, col) for col in combined_data.columns])
        cov_matrix = combined_data.cov()
        
        ### Arrays to store simulation results
        results = np.zeros((num_portfolios, 3))  # [portfolio_return, portfolio_std_dev, sharpe_ratio]
        weights_record = []
        
        for i in range(num_portfolios):
            ### Generate random weights
            weights = np.random.random(num_assets)
            weights /= np.sum(weights)
            
            ### Record weights
            weights_record.append(weights)
            
            ### Portfolio return and standard deviation
            portfolio_return = np.dot(weights, mean_returns)
            portfolio_std_dev = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
            
            ### Sharpe ratio
            sharpe_ratio = (portfolio_return - risk_free_rate) / portfolio_std_dev
            
            ### Store the results
            results[i, 0] = portfolio_return
            results[i, 1] = portfolio_std_dev
            results[i, 2] = sharpe_ratio
        
        ### Convert to DataFrame for easier plotting
        results_df = pd.DataFrame(results, columns=['Return', 'Risk', 'Sharpe'])
        
        return results_df, weights_record
    
    except Exception as e:
        print(f"An error occurred: {e}")
        raise


# In[ ]:


def plot_simulate_portfolios(asset_data_list, num_portfolios, risk_free_rate=0.2):
    results_df, weights_record = simulate_portfolios(asset_data_list, num_portfolios=100,risk_free_rate=0.05)
    # Plotting the efficient frontier
    plt.figure(figsize=(10, 7))
    plt.scatter(results_df['Risk'], results_df['Return'], c=results_df['Sharpe'], cmap='viridis', marker='o')
    plt.colorbar(label='Sharpe Ratio')
    plt.title('Efficient Frontier')
    plt.xlabel('Risk (Standard Deviation)')
    plt.ylabel('Return')
    plt.show()

