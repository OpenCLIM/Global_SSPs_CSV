# Global_SSPs_CSV
The model should suceed the Global_SSPS: Inputs and Global_SSPS: Clip & Aggregate models after they have been run for all five ssp scenarios.The Urban Development Model (UDM) pulls changes in population and creates new land use maps with developed areas to capture changes in population density. UDM pulls data from a csv file showing the demography changes. This model creates that file for the selected country.

## Description
Data is transformed from a .gpkg file to a csv file needed by the UDM model. 

## Input Parameters
* Country
  * Description: The country of interest. Only needed if not preceeded by the other Global SSP models.
* LAD_Name
  * Description: Future models need to know the name of the column from the dataset of Local Authority polygons which contains the name of each LAD. Only needed if not preceeded by the other Global SSP models.
* LAD_Code
  * Description: Future models need to know the name of the column from the dataset of Local Authority polygons which contains the code of each LAD. Only needed if not preceeded by the other Global SSP models.


## Input Files (data slots)
* LAD data
  * Description: A .gpkg file with the projected population changes per LAD. Only needed if not preceeded by the other Global SSP models.
  * Location: /data/inputs/
* Parameters
  * Description: A .csv file detailing the selected parameters - taken from the preceeding Global_SSPS:Inputs model.
  * Location: /data/inputs/parameters


## Outputs
* CSV Results
  * Description: Contains a single .csv file with the population changes per LAD in csv format.
  * Location: /data/outputs/
* Parameters
  * Description: All parameters and their values are stored in a csv file.
  * Location: /data/outputs/parameters
