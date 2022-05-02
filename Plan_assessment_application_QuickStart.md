# Voting District Plan Assessment Application: Quick Start

This application is designed to assess the quality of voting district plans from the perspective of compactness and split municipalities. 
[[toc]]
## Key Concepts
- **plan:** spatial configuration of planned voting districts in a redistricting proposal
- **assignment file:** the .csv file that contains the district assignments
- **measure:** the geographic and/or geometric calculations by which the plans are assessed

## Currently applied measures:
### Polsby-Popper compactness score:
- mathematical compactness measure of a shape; 
- scored between 0 (complete non compactness) and 1 (perfect geographic compactness = circle)
- calculating the ratio of the area of the district to the area of a circle whose circumference is equal to the perimeter of the district.
- code: `((4* pi* area)/ (length * length))`

### Schwartzberg compactness score:
- the ratio  of the perimeter of a district to the
to the circumference of a circle whose area is equal to the area of the district
- scored between the values of 0 (no compactness whatsoever) and 1 (maximum compactness) 
- the formula: 
1. the radius of the equal area (equal to the area of the district) circle is found  `sqrt(area / pi)`
2. the circumference of the circle is found by  multiplying 2 times pi then multiplied by  the radius created earlier.
3. with the circumference found, this is divided by the perimeter  of the district

### Split Counties score: 
- counts the number of counties that are split by voting district boundaries
- reflects the goal of keeping counties and other smaller political subdivisions, such as cities and towns, together when redistricting


|  **Measure name** |   **Associated function**    |
| ----------------- | ------------------- |
|  **Polsby-Popper minimum value** |   `measure.find_polsby_min`  |
|  **Polsby-Popper mean value**    |   `measure.find_polsby_mean` |
|  **Schwartzberg minimum value**  |   `measure.schwartzberg_min` |
|  **Schwartzberg mean value**     |   `measure.schwartzberg_mean`|
|  **Number of split counties**    |   `measure.total_split`      |

## Recommended Process:
To calculate the above measures with our application,
1. Run `plan_assess_widget.py` to open interface
2. Populate interface with appropriate information
- load your spatial layer file (currently operating with .shp format)
- load your assignment files (currently operating with .csv format)
3. Choose the appropriate columns for extracting values for conversion and calculation:
-  "Select your column to join on" selects the id field from the spatial layer's attribute table and in the assignment file
-  "Select a columns to dissolve on" selects the field on which to dissolve the spatial layer and the assignment file
-  "Select the measures you want to be scored" gives the options for the measures to be calculated
-  "Select county columns" designates the column of the county ID column for checking for split counties
4. `Run` the calculations
5. Observe the results in the table view panel
6. `Save` the results (currently operating in .csv format)

##  Caveats and Future Tasks
The application is operational, but it has multiple shortcomings that should be fixed in later revisions:
- More measures and more complicated comparisons should be added. The ultimate goal is to advance the scoring to feed into a Pareto Frontier score for the plans.
- The application should be opened up to multiple different types of file formats both on the spatial layer and the assignment files.
- The application should have a tighter process for single assignment file entries. At present, the orientation is toward working with folders full of assignment files.
- There are some guardian codes and related bells and whistles to be worked out for smooth operations, such as error reminders and splash screens and message boxes to create clearer channels of communication.
- Another display area should be created for more robust visual demonstration of the results, like charts, spatial representations, or other.