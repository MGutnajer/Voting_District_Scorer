# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 15:20:18 2022

@author: tug67775
"""
import os 

'''
The get_folder_csv function pulls the file path and name from the folder location
and then appends the path + name to a list to be fed into the geutil function  
'''      

def get_folder_csv(folder_location) :
    ''' Produces list of folder path and file names needed for 
        the creation of the assignment file data frame.
    

    Parameters
    ----------
    folder_location : String  
        The path to the folder containing the assignment files.

    Returns
    -------
    afiles : List 
        List of assignment file + File Paths 
    '''
    afiles = []
    for path, subdirs, files in os.walk(folder_location):
        for x in files:
            if x.endswith(".csv"):
                afiles.append(str(os.path.join(path, x)))
    return afiles



 

                    
