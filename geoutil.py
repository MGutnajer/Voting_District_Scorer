# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 17:53:27 2022

@author: tug67775
"""
import pandas as pd 
import geopandas as gpd
 
'''
    The functions in this file load the assignment file plan and geo data into dataframes
    and then merge the data based on user selected columns. The merged data frame is then dissolved 
    Through the use of the pandas built in dissolver to create the districts adta frame 
    
'''    
def geoutil(spatial_layer, afile, spatial_layer_on, afile_on):
    ''' Creates the geodf_merge dataframe from the user selected spatial layer, and assignment file.
    

    Parameters
    ----------
    spatial_layer : String  
        File path to spatial layer being used .
    afile : String
        File within the afiles list of file pathways to assignment files.
    spatial_layer_on : String 
        User selected column in the spatial layer data frame that the join 
        with the assignment file data frame will be joined on.
    afile_on : String
        User selected column in the assignment data frame that the join with 
        the spatial layer data frame will be based on .

    Returns
    -------
    geodf_merge : Data Frame 
        The product of the merge between the Spatial Layer and assignment file data frames.

    '''
    dfmap = gpd.read_file(spatial_layer)
    dfplan = pd.read_csv(afile)
    dfmap[spatial_layer_on]=dfmap[spatial_layer_on].astype(str)
    dfplan[afile_on]=dfplan[afile_on].astype(str)
    geodf_merge = pd.merge(dfmap,dfplan,left_on = spatial_layer_on, right_on = afile_on)
    return geodf_merge

def dissolver(merge_df, dissolve_col):
    '''Creates the Districts Geo Data Frame from the merge_df 
        that has broken the data down to districts to be measured 
    

    Parameters
    ----------
    merge_df : Data Frame
        The Data Frame created by the function geoutil, the merged assignment df and spatial df.
    dissolve_col : String
        The column associated with the District ID.

    Returns
    -------
    districts_gdf : Data Frame 
        The Districts Geo Data Frame that is the product of dissolving the merge_df on the Districts column.

    '''
    districts_gdf = merge_df.dissolve(by=dissolve_col)
    return districts_gdf


    