import os
import glob
from glob import glob
import pandas as pd
import geopandas as gpd

### This code creates a metadata.json file which tells DAFNI what to name each output ###
def metadata_json(output_path, output_title, output_description, bbox, file_name):
    """
    Generate a metadata json file used to catalogue the outputs of the UDM model on DAFNI
    """

    # Create metadata file
    metadata = f"""{{
      "@context": ["metadata-v1"],
      "@type": "dcat:Dataset",
      "dct:language": "en",
      "dct:title": "{output_title}",
      "dct:description": "{output_description}",
      "dcat:keyword": [
        "UDM"
      ],
      "dct:subject": "Environment",
      "dct:license": {{
        "@type": "LicenseDocument",
        "@id": "https://creativecommons.org/licences/by/4.0/",
        "rdfs:label": null
      }},
      "dct:creator": [{{"@type": "foaf:Organization"}}],
      "dcat:contactPoint": {{
        "@type": "vcard:Organization",
        "vcard:fn": "DAFNI",
        "vcard:hasEmail": "support@dafni.ac.uk"
      }},
      "dct:created": "{datetime.now().isoformat()}Z",
      "dct:PeriodOfTime": {{
        "type": "dct:PeriodOfTime",
        "time:hasBeginning": null,
        "time:hasEnd": null
      }},
      "dafni_version_note": "created",
      "dct:spatial": {{
        "@type": "dct:Location",
        "rdfs:label": null
      }},
      "geojson": {bbox}
    }}
    """

    # write to file
    with open(join(output_path, '%s.json' % file_name), 'w') as f:
        f.write(metadata)
    return


# Set data paths
data_path = os.getenv('DATA','/data')

# Set up Data Input Paths
inputs_path = os.path.join(data_path, 'inputs')
parameters_path = os.path.join(inputs_path,'parameters')

# Set up and create data output paths
outputs_path = os.path.join(data_path, 'outputs')
if not os.path.exists(outputs_path):
    os.mkdir(outputs_path)

# Look to see if a parameter file has been added
parameter_file = glob(parameters_path + "/*.csv", recursive = True)

if len(parameter_file) == 1 :
    parameters = pd.read_csv(parameter_file[0])
    lad_name = parameters.loc[3][1]
    lad_code = parameters.loc[4][1]
    country = parameters.loc[0][1]

if len(parameter_file) == 0:
    country = os.getenv('COUNTRY')
    lad_name = os.getenv('LAD_NAME')
    lad_code = os.getenv('LAD_CODE')

results_name = glob(inputs_path + "/*.gpkg", recursive = True)
results = gpd.read_file(results_name[1])

csv_file = []
csv_file = pd.DataFrame()
csv_file['ID']=['xx' for n in range(len(results))]
csv_file['ID'] = csv_file.index
csv_file['Metric']='Age Structure'
csv_file['Unit'] = 'thousand people'
csv_file['Age Class'] = 'Total'
csv_file['LADCD'] = results[lad_code]

ssps = ['ssp1','ssp2','ssp3','ssp4','ssp5']

final =[]
final = pd.DataFrame()

inter = []
inter = pd.DataFrame()

for i in range(0,len(results_name)):
    if 'total' in results_name[i]:
        for j in range(0,len(ssps)):
            ssp_scen = ssps[j]
            if ssp_scen in results_name[i]:
                results = gpd.read_file(results_name[i])
                inter['LADCD'] = results[lad_code]
                inter['LADNM'] = results[lad_name]
                inter['Scenario'] = ssp_scen.upper()
                ssp_cols = [col for col in results.columns if 'ssp' in col]
                for l in range(0,len(ssp_cols)):
                    name=ssp_cols[l]
                    year = name.split('_')[2]
                    inter[year] = (results[name])/1000
        #check = pd.concat([csv_file,inter],axis=1)
        initial = pd.merge(csv_file,inter,on='LADCD',how='right')
        final = pd.concat([final,initial])

final['ID'] = final.reset_index().index

final.to_csv(
    os.path.join(outputs_path, country+'_Demography.csv'), index=False,  float_format='%g') 

title_for_output = country + ' - ' + SSP +' csv.'

description_for_data_prep = 'This dataset contains a single csv file detailing population change for ' + country + ' under the each ssp scenario. Generated using the downscaled SSP datasets (https://www.nature.com/articles/s41597-021-01052-0) data is collated at the Local Authority level selected by the user.'
# write a metadata file so outputs properly recorded on DAFNI
metadata_json(output_path=meta_outputs_path, output_title=title_for_output, output_description=description_for_data_prep, bbox=geojson, file_name='metadata_ssp_data_csv')
