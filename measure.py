# -*- coding: utf-8 -*-
"""
Created on Sat Apr 16 10:41:13 2022

@author: tug67775
"""
import pandas  as pd 
import geopandas as gpd
import numpy

''' 
    The functions in this python file calculate the measurements of the merged plan and geodata files.
    The functions below count the number of splits, the number of split counties
    , Polsby Popper mean, min and Schwartzberg mean, min.
    These measurements make up the scores of the final report dataframe.
'''    


def find_split_sum(geodf_merge, county_col, dissolve_col):
    '''  Calculates the total number of splits that occur in the geodf_merge DataFrame
    

    Parameters
    ----------
    geodf_merge : DataFrame 
        The merged geodataframe between the dfmap and dfplan..
    county_col : String
        The column where the county ID is located.
    dissolve_col : String
        The column that identifies the district.

    Returns
    -------
    total_split_sum : int64
        The total number of splits in the geodf_merge.

    '''
    split_count_df = geodf_merge.groupby([county_col],as_index=False)[dissolve_col].nunique()
    split_count_df['Split_Counties'] = split_count_df[dissolve_col].apply(lambda x: 0 if (x<= 1) else 1)
    split_count_df['Total_Split'] = split_count_df[dissolve_col].apply(lambda x: 0 if (x<= 1) else x - 1)
    total_split_sum = split_count_df['Total_Split'].sum()
    return total_split_sum

def find_split_counties(geodf_merge, county_col, dissolve_col):
    ''' Calculates the total number of counties that are split 
    

    Parameters
    ----------
    geodf_merge : Dataframe 
        The merged geodataframe between the dfmap and dfplan.
    county_col : String
        The column where the county ID is located.
    dissolve_col : string
        The column that identifies the district.

    Returns
    -------
    total_split_counties : int64
        The number of split counties in the geodf_merge.

    '''    
    total_split_count_df = geodf_merge.groupby([county_col],as_index=False)[dissolve_col].nunique()
    total_split_count_df['Split_Counties'] = total_split_count_df[dissolve_col].apply(lambda x: 0 if (x<= 1) else 1)
    total_split_count_df['Total_Split'] = total_split_count_df[dissolve_col].apply(lambda x: 0 if (x<= 1) else x - 1)
    total_split_counties = total_split_count_df['Split_Counties'].sum()
    return total_split_counties

def find_polsby_mean(districts_gdf):
    ''' Calculates the Polsby Popper Score of every district in the districts_gdf and calculates the mean
    

    Parameters
    ----------
    districts_gdf : Dataframe
        The Geo Data Frame product of the dissolve function on the merge Geo Data Frame.

    Returns
    -------
    pp_mean : Float
        The Polsby Popper Mean.

    '''
    length = districts_gdf.length
    area = districts_gdf.area
    Polsby_Series = ((4*numpy.pi*area)/(length*length))
    pp_mean =Polsby_Series.iloc[1:1000].mean()     
    return pp_mean

def find_polsby_min(districts_gdf):
    ''' Finds the minimum value of the Polsby Popper Scores  
    

    Parameters
    ----------
    districts_gdf : DataFrame 
         The Geo Data Frame product of the dissolve function on the merge Geo Data Frame.

    Returns
    -------
    pp_min : Float
        The Polsby Popper minimum value.

    '''
    pp_length = districts_gdf.length
    pp_area = districts_gdf.area
    pp_Polsby_Series = ((4*numpy.pi*pp_area)/(pp_length*pp_length))
    pp_min = pp_Polsby_Series.iloc[1:1000].min()
    return pp_min                 

def find_schwartzberg_mean(districts_gdf):
    ''' Calculates the Schwartzberg score for every district and calculates the mean 
    

    Parameters
    ----------
    districts_gdf : DataFrame
         The Geo Data Frame product of the dissolve function on the merge Geo Data Frame.

    Returns
    -------
    s_mean : float 
        The Schwartzberg mean value.

    '''
    length = districts_gdf.length
    area = districts_gdf.area
    area = pd.to_numeric(area, errors='coerce')
    radius = numpy.sqrt(area /numpy.pi)
    circum = 2 * numpy.pi * radius 
    Schwartzberg_Score = 1/(length/circum)  
    s_mean = Schwartzberg_Score.iloc[1:1000].mean()
    return s_mean

def find_schwartzberg_min(districts_gdf):
    ''' Calculates the Schwartzberg score for every district in the district_gdf and finds the minimum value
    

    Parameters
    ----------
    districts_gdf : DataFrame
        The Geo DataFrame product of the dissolve function on the merge Geo Data Frame.

    Returns
    -------
    s_min : float
        The Schwartzberg minimum score value.

    '''
    length = districts_gdf.length
    area = districts_gdf.area
    area = pd.to_numeric(area, errors='coerce')
    radius = numpy.sqrt(area /numpy.pi)
    circum = 2 * numpy.pi * radius 
    Schwartzberg_Score = 1/(length/circum)  
    s_min = Schwartzberg_Score.iloc[1:1000].min()
    return s_min

