# Import google_streetview for the api module
import google_streetview.api
import pandas as pd
import os
import glob

'''
This script is used to download streetview images from a given location.
The script will download images from the given location and save them in a folder.
The script will also save the location and the image url in a csv file.
'''

API_KEY = 'Your key' # Your Google map key
location = pd.read_excel(r"Path to the coords csv") # Path to the coords csv
location['coords'] = location['POINT_Y'].astype(str) + ', ' + location['POINT_X'].astype(str)
k = 1
headings = ['45', '90', '135', '180'] # Headings to be used, 0 is north, 90 is east, etc.
for i in location['coords']:
    for direction in headings:
        print(i)
        params = [{
            'size': '640x640', # max 640x640 pixels
            'location': i, # coords of the street view
            'heading': direction,
            'pitch': '-0.76', # -0.76 is the default pitch
            'key': API_KEY
        }]

        try:
            results = google_streetview.api.results(params) # Create a results object
            results.preview() # Preview the results
            results.download_links('downloads') # Path to the directory where you want to save the images
            os.rename('downloads\\gsv_0.jpg', f'downloads\\{k}_{direction}.jpg') # Rename the image
        except Exception:
            pass # If there is an error, do nothing
    k = k + 1
directory = "downloads" # Path to the directory where the images are saved
jpg_files = glob.glob(os.path.join(directory, "*.jpg")) # Get all the jpg files in the directory
jpg_files = [s.strip('downloads\\').strip('.jpg') for s in jpg_files] # Remove the directory and the extension from the file name
jpg_files = pd.DataFrame(jpg_files, columns=['file_name']) # Create a dataframe with the file names
jpg_files[['ID', 'Direction']] = jpg_files['file_name'].str.split('_', expand=True) # Split the file name into ID and Direction
jpg_files_list = jpg_files.groupby(['ID', 'Direction']).count().reset_index() # Group the file names by ID and Direction
jpg_files_list = jpg_files_list.pivot_table(index="ID", columns="Direction", values="file_name", aggfunc='first') # Pivot the dataframe by direction
jpg_files_list.reset_index(inplace=True) # Reset the index
jpg_files_list['ID']=jpg_files_list['ID'].astype(int) # Convert the ID to an integer
# Merge the two dataframes and save the result to an excel file
pd.merge(location, jpg_files_list, left_on='OBJECTID', right_on='ID', how='left').fillna(0).to_excel('path to the summary csv', index=False) 