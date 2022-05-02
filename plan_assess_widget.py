# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 21:46:10 2022

@author: gkecsk02
"""

import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
import pandas as pd
import geopandas as gpd
import os
from geoutil import *
from get_folder_csv import *
from measure import *


#model class to populate QTableView
class PandasTableModel(qtg.QStandardItemModel):
    def __init__(self, data, parent=None):
        qtg.QStandardItemModel.__init__(self, parent)
        self._data = data
        for col in data.columns:
            data_col = [qtg.QStandardItem("{}".format(x)) for x in data[col].values]
            self.appendColumn(data_col)
        return

    def rowCount(self, parent=None):
        return len(self._data.values)

    def columnCount(self, parent=None):
        return self._data.columns.size

    def headerData(self, x, orientation, role):
        if orientation == qtc.Qt.Horizontal and role == qtc.Qt.DisplayRole:
            return self._data.columns[x]
        if orientation == qtc.Qt.Vertical and role == qtc.Qt.DisplayRole:
            return self._data.index[x]
        return None

#WIDGETS AND LAYOUT
class DialogApp(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Files and measures')
        self.resize(800, 800)
        
        #create widgets
        self.button_shp = qtw.QPushButton ('Load spatial layer')
        self.button_shp.clicked.connect(self.get_shp_file)
        
        self.button_csv = qtw.QPushButton('Load .csv file')
        self.button_csv.clicked.connect(self.get_csv_file)
        
        self.button_dir= qtw.QPushButton('Load .csv Folder')
        self.button_dir.clicked.connect(self.get_folder)
        
        greeting_text= '''Welcome to our district scoring application.
        1. To begin, load your spatial and assignment files.
        2. Select the appropriate attributes to select and compile your data. 
        3. Select the measures you wish to calculate.
        4. Click "Run" to initiate the calculations. 
        5. You will receive a glimpse into the results as a tabl.
        6. And you can save the results.'''
        self.greeting_text= qtw.QLabel(greeting_text)
        
        #shp upload widgets
        self.label_shp_path= qtw.QLabel('Your file path:') 
        self.shp_path_disp= qtw.QLineEdit("file path", self)
        self.label_shp_colslct= qtw.QLabel('Select column to join on:')
        self.label_dissolve_colslct= qtw.QLabel('Select column to dissolve on:')
        
        #csv upload widgets
        self.label_csv_path= qtw.QLabel('Your file path:')
        self.csv_path_disp= qtw.QLineEdit("file path", self)
        self.label_csv_colslct= qtw.QLabel('Select column to join:')
        
        #folder upload widgets
        self.label_dir_path= qtw.QLabel('Your folder path:')
        self.label_choose_file= qtw.QLabel('For a single .csv file:')
        self.label_choose_dir= qtw.QLabel('For a folder of .csv files:')
        
        
        #comboboxes
        self.column_list_shp= qtw.QComboBox()
        self.dissolve_column_list= qtw.QComboBox()
        self.column_list_csv= qtw.QComboBox()
        self.select_splits_column= qtw.QComboBox()
                
        self.checkbox_C_PP= qtw.QCheckBox('Pollsby-Popper')
        self.checkbox_C_Swbg= qtw.QCheckBox('Schwartzberg')
        self.checkbox_splits= qtw.QCheckBox('Splits count')
        
        
        self.label_choice= qtw.QLabel('Select the measures you want to scored')
        self.label_splits_column= qtw.QLabel('choose counties column')
        self.run_button= qtw.QPushButton("Run", clicked=self.calculate_measures)
       
        
        #table display for results
        self.table_display = qtw.QTableView()
       
        
        #save results message widget
        self.save_result_label= qtw.QLabel('Save your results')
        self.save_result_btn= qtw.QPushButton('Save', clicked= self.save_files)
        
        ##grid layout
        main_layout= qtw.QVBoxLayout()
        self.setLayout(main_layout)
        main_layout.addWidget(self.greeting_text)
        
        #spatial layer load layout
        self.shp_toolbox= qtw.QGroupBox('If you have a geography file', checkable=True, checked= False, flat=False)
        main_layout.addWidget(self.shp_toolbox)
        shp_toolbox_layout= qtw.QGridLayout()
        self.shp_toolbox.setLayout(shp_toolbox_layout) 
        shp_toolbox_layout.addWidget(self.button_shp,0,0,1,1)
        shp_toolbox_layout.addWidget(self.label_shp_colslct,0,3,1,1)
        shp_toolbox_layout.addWidget(self.column_list_shp,0,4,1,1)
        shp_toolbox_layout.addWidget(self.label_shp_path,1,0,1,1)
        shp_toolbox_layout.addWidget(self.shp_path_disp,1,1,1,4)
        
            
        #csv load layout
        csv_toolbox= qtw.QGroupBox('If you have CSV file/s...', checkable=True, checked= False, flat=False) 
        main_layout.addWidget(csv_toolbox)
        csv_toolbox_layout= qtw.QGridLayout()
        csv_toolbox.setLayout(csv_toolbox_layout)
        csv_toolbox_layout.addWidget(self.label_choose_file,0,0,1,1)
        csv_toolbox_layout.addWidget(self.button_csv,0,1,1,1)
        csv_toolbox_layout.addWidget(self.label_choose_dir,1,0,1,1)
        csv_toolbox_layout.addWidget(self.button_dir,1,1,1,1)
        csv_toolbox_layout.addWidget(self.label_csv_colslct,0,3,1,1)
        csv_toolbox_layout.addWidget(self.column_list_csv,0,4,1,1)
        csv_toolbox_layout.addWidget(self.label_dissolve_colslct,1,3,1,1)
        csv_toolbox_layout.addWidget(self.dissolve_column_list,1,4,1,1)
        csv_toolbox_layout.addWidget(self.label_csv_path,2,0,1,1)
        csv_toolbox_layout.addWidget(self.csv_path_disp,2,1,1,4)
                
        #calculation choices layout
        calculator_toolbox= qtw.QGroupBox('Select and calculate measures', checkable= True, checked= False, flat= False)
        main_layout.addWidget(calculator_toolbox)
        calc_toolbox_layout= qtw.QGridLayout()
        calculator_toolbox.setLayout(calc_toolbox_layout)
        calc_toolbox_layout.addWidget(self.label_choice,0,0,1,2)
        calc_toolbox_layout.addWidget(self.checkbox_C_PP,2,0,1,1)
        calc_toolbox_layout.addWidget(self.checkbox_C_Swbg,3,0,1,1)
        calc_toolbox_layout.addWidget(self.checkbox_splits,1,0,1,1)
        calc_toolbox_layout.addWidget(self.label_splits_column,1,1,1,1)
        calc_toolbox_layout.addWidget(self.select_splits_column, 1,2,1,1)
        calc_toolbox_layout.addWidget(self.run_button,4,1,1,1)
        
        
        #table display layout
        results_display= qtw.QGroupBox('Results', flat= False)
        main_layout.addWidget(results_display)
        results_display_layout= qtw.QHBoxLayout()
        results_display.setLayout(results_display_layout)
        results_display_layout.addWidget(self.table_display)
        right_display_layout= qtw.QVBoxLayout()
        results_display_layout.addLayout(right_display_layout)
        right_display_layout.addWidget(self.save_result_label)
        right_display_layout.addWidget(self.save_result_btn)
        
        
    
##OPERATIONAL FUNCTIONS
    #slot for Select button
    def get_shp_file(self):
        shp_filename, _ = qtw.QFileDialog.getOpenFileName(
            self,
            'Select a Shapefile to open…',
            qtc.QDir.homePath(),
            'Shapefiles (*.shp)',
            #qtw.QFileDialog.DontUseNativeDialog |
            #qtw.QFileDialog.DontResolveSymlinks
        )
        
        if shp_filename:
            #set interaction
            self.shp_path_disp.setText(shp_filename)
            gdf=gpd.read_file(shp_filename) 
            shp_column_list= list(gdf.head(0)) #or gdf[0]? but this
            self.column_list_shp.clear()
            self.column_list_shp.addItems(shp_column_list)
            #set the column selection
            self.select_splits_column.clear() #I wanted to do this where I check it but could not work with the variable
            self.select_splits_column.addItems(shp_column_list)

            
     #slot for Select button 
    def get_csv_file(self):
        csv_filename, _ = qtw.QFileDialog.getOpenFileName(
            self,
            'Select a CSV file to open…',
            qtc.QDir.homePath(),
            'CSV Files (*.csv);; All Files (*):: Directory',
            #qtw.QFileDialog.DontUseNativeDialog |
            #qtw.QFileDialog.DontResolveSymlinks
        )
        
        if csv_filename:
            #set interaction
            self.csv_path_disp.setText(csv_filename)
            df=pd.read_csv(csv_filename, nrows=1) #nrows=# of rows of file to read. Useful for reading pieces of large files.
            self.column_list_csv.clear()
            self.column_list_csv.addItems(df.columns)
            self.dissolve_column_list.clear()
            self.dissolve_column_list.addItems(df.columns)
            csv_path= csv_filename #to help the mutual function
       
              
    #slot for Select button
    def get_folder(self):
        folder_path= qtw.QFileDialog.getExistingDirectory(
            self,
            "Choose Directory",
            #"C:\\"
        )
        
        if folder_path:
            #set interaction
            self.csv_path_disp.setText(folder_path)
            #select a single file from the directory; is there a better solution instead of listdir()[0]???
            dir_file_path= os.path.join(folder_path,os.listdir(folder_path)[0])
            if str(dir_file_path).endswith('csv') == True:
                #select the column names from the csv file
                df_folder=pd.read_csv(dir_file_path, nrows=1)
                #enter column names into column list groupbox
                self.column_list_csv.clear()
                self.column_list_csv.addItems(df_folder)
                self.dissolve_column_list.clear()
                self.dissolve_column_list.addItems(df_folder)
            
            else:
                qtw.QMessageBox.critical(self, 'Error:', 'Wrong file type.\n Please select a folder with .csv files in it.')
           
   
            
    #slot for Run button 
    def calculate_measures(self):
        #set variables from GUI
        afile_on= self.column_list_csv.currentText()
        spatial_layer_on= self.column_list_shp.currentText()
        splits_column= self.select_splits_column.currentText()
        dissolve_col= self.dissolve_column_list.currentText()
        county_col=splits_column
        spatial_layer= self.shp_path_disp.text()
        folder_location= self.csv_path_disp.text()
        
        #select measures + compile dataframe columns
        chosen_measures= ['Plan']
        if self.checkbox_C_PP.isChecked():
            chosen_measures.append('Polsby_Popper_mean')
            chosen_measures.append('Polsby_Popper_Min')
        if self.checkbox_C_Swbg.isChecked():
            chosen_measures.append('Schwartzberg_mean')
            chosen_measures.append('Schwartzberg_min')
        if self.checkbox_splits.isChecked():
            chosen_measures.append('Split_Counties')
            chosen_measures.append('Total_Splits')
        #check that at least 1 columns has been added
        if len(chosen_measures) == 1:
            qtw.QMessageBox.critical(self, 'Error:', 'You will need to select some measures to proceed')
        
        #set columns
        final_report= pd.DataFrame(columns= chosen_measures)
        ##Run through loop. See detailed documentation in measure.py 
        filelist = get_folder_csv(folder_location)
        for afile in filelist:   
            geodf_merge = geoutil(spatial_layer, afile, spatial_layer_on, afile_on)
            districts_gdf = dissolver(geodf_merge, dissolve_col)
            final_report_dict= {'Plan': afile}
            if 'Split_Counties' in final_report:
                total_split = find_split_sum(geodf_merge, county_col, dissolve_col)
                split_county_sum = find_split_counties(geodf_merge, county_col, dissolve_col)
                final_report_dict.update({'Split_Counties': split_county_sum})
                final_report_dict.update({'Total_Splits': total_split})
            if 'Polsby_Popper_mean' in final_report:
                pp_mean = find_polsby_mean(districts_gdf)
                pp_min = find_polsby_min(districts_gdf)
                final_report_dict.update({'Polsby_Popper_mean': pp_mean})
                final_report_dict.update({'Polsby_Popper_Min': pp_min})
            if 'Schwartzberg_mean' in final_report:
                s_mean = find_schwartzberg_mean(districts_gdf)
                s_min = find_schwartzberg_min(districts_gdf)
                final_report_dict.update({'Schwartzberg_mean': s_mean})
                final_report_dict.update({'Schwartzberg_min': s_min})
            final_report = final_report.append(final_report_dict, ignore_index=True)
        
        #engage table model
        print(final_report.dtypes)
        self.model = PandasTableModel(final_report)
        self.table_display.setModel(self.model)
        #global file_content
        self.file_content= final_report
    
    
    #slot for Save button
    def save_files(self):
        #file dialog wedget for locating directory and saving file
        final_file_name, _ = qtw.QFileDialog.getSaveFileName(
            self,
            "Save results",
            "your_file_name.csv",
            ".csv files (*.csv)", 
            options= qtw.QFileDialog.Options()|qtw.QFileDialog.DontUseNativeDialog)
        if not final_file_name.endswith('.csv'):
            final_file_name += '.csv'
        #converting dataframe into .csv
        self.file_content.to_csv(final_file_name, index=False)
                
            
          
        
if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    w = DialogApp()
    w.show()
    sys.exit(app.exec_())
