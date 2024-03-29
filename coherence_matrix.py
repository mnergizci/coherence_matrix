#!/usr/bin/env python3
import pickle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# To load the dictionary from the file
with open('av_coh.pkl', 'rb') as fp:
    av_coh_loaded = pickle.load(fp)


# To view the average coherence values for each ROI
for roi_label, date_coh_dict in av_coh_loaded.items():
    all_coh_values = []  # List to aggregate all coherence values for the current ROI
    for date_pair, coh_values in date_coh_dict.items():
        # Extend the list with all coherence values found for the current date pair
        all_coh_values.extend(coh_values)
    
    # Calculate the average coherence for the current ROI using all aggregated values
    average_coh = np.nanmean(all_coh_values) if all_coh_values else float('nan')
    print(f"Average coherence for ROI {roi_label}: {average_coh}")

# Ensure the rest of the plotting code remains unchanged


for AOI in ['A', 'B', 'C']:
    coh_data = av_coh_loaded[AOI]
    dates = set()
    for key in coh_data.keys():
        date1, date2 = key.split('_')
        dates.update([date1, date2])
    
    dates_temp = sorted(list(dates))
    start_date = '20220801'
    end_date = '20230801'
    dates = [date for date in dates_temp if start_date <= date <= end_date]
    
    if '20220919' in dates:
        dates.remove('20220919')
        dates.remove('20230318')
    
    print(f"Dates for AOI {AOI}: {dates}")
    
    # Initialize a matrix to hold the coherence values
    coh_matrix = np.full((len(dates), len(dates)), np.nan)
    
    # Populate the coherence matrix with the coherence values from the dictionary
    for i, date1 in enumerate(dates):
        for j, date2 in enumerate(dates):
            key = f'{date1}_{date2}'
            if key in coh_data and not np.isnan(coh_data[key][0]):
                coh_matrix[i, j] = coh_data[key][0]
                coh_matrix[j, i] = coh_data[key][0]  # Symmetric matrix

    # Set the diagonal values to 1 for same-day coherence
    np.fill_diagonal(coh_matrix, 1)
    
    # Mask the upper triangle, including the diagonal
    upper_tri_indices = np.triu_indices_from(coh_matrix, k=1)
    coh_matrix[upper_tri_indices] = np.nan
    
    # Adjusting the size of the plot and the font sizes
    plt.figure(figsize=(10, 10))  # Adjust the figure size as needed
    plt.imshow(coh_matrix, cmap='viridis', interpolation='none', aspect='auto')  # Let aspect ratio be 'auto'
    if AOI=='C':
        cbar = plt.colorbar(fraction=0.03, pad=0.01)
        cbar.set_label('Coherence', size=20)  # Increase the label font size
        cbar.ax.tick_params(labelsize=20)  # Increase colorbar tick font size
        
    # Set title and axis labels with a larger font size
    plt.title(f'Coherence Matrix of "{AOI}" AOI', fontsize=18)
    if AOI=='A':
        plt.xlabel('1st Epoch', fontsize=16)
        plt.ylabel('2nd Epoch', fontsize=16)
    else:
        plt.xlabel('1st Epoch', fontsize=16)
    # Format the ticks and increase font size for better readability
    plt.xticks(ticks=range(len(dates)), labels=dates, rotation=90, fontsize=12)
    plt.yticks(ticks=range(len(dates)), labels=dates, fontsize=12)
    
    # Optional: Use a DateFormatter to improve the date tick labels
    
    
    plt.grid(False)  # Keep the grid off as it's not usually needed for coherence matrices
    plt.tight_layout()  # Adjust the layout
    plt.savefig(f'coherence_mat{AOI}.png')  # Display the plot


