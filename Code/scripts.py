import pandas as pd
import os

def import_clean_epa(path, name, col_name_map):
    fullpath = os.path.join(path, name)
    df_temp = pd.read_csv(fullpath, compression='zip', low_memory=False)

    df_temp.rename_axis(col_name_map, axis=1, inplace=True)
    
    # Rather than just converting the date column to datetime, create a new column
    # that also makes use of the operating hour
    df_temp.loc[:,'OP_DATE_TIME'] = pd.to_datetime(df_temp['OP_DATE'] + 
                                                   '-' +  
                                                   df_temp['OP_HOUR'].astype(str), format='%m-%d-%Y-%H')
#    df_temp.loc[:,'OP_DATE'] = pd.to_datetime(df_temp.loc[:,'OP_DATE'], format='%m-%d-%Y')
    return df_temp


def import_group_epa(path):
    epa_df = pd.read_csv(path, parse_dates=['OP_DATE_TIME'], infer_datetime_format=True, 
                         usecols=['ORISPL_CODE', 'GLOAD (MW)', 'SLOAD (1000lb/hr)', 
                                  'CO2_MASS (tons)', 'HEAT_INPUT (mmBtu)',
                                  'OP_DATE_TIME', 'OP_TIME'])
    epa_df.loc[:,'YEAR'] = epa_df.loc[:,'OP_DATE_TIME'].dt.year.astype(int)
    epa_df.loc[:,'MONTH'] = epa_df.loc[:,'OP_DATE_TIME'].dt.month.astype(int)
    
    grouped = epa_df.groupby(['ORISPL_CODE', 'YEAR', 'MONTH']).sum()
    grouped.loc[:,'CO2_MASS (kg)'] = unit_conversion(grouped.loc[:,'CO2_MASS (tons)'], 
                                                     start_unit='tons', final_unit='kg')
    grouped.drop('CO2_MASS (tons)', inplace=True, axis=1)
    grouped.reset_index(inplace=True)
    return grouped

def unit_conversion(value, start_unit, final_unit):
    """
    Convert a value from one unit to another (e.g. short tons to kg)
    
    inputs:
        value: numeric or array-like
        start_unit: str (kg, tons, lbs)
        final_unit: str (kg, tons, lbs)
        
    returns:
        converted_value: numeric or array-like
    """
    # All values are for conversion to kg
    convert_dict = {'kg' : 1.,
                    'tons' : 907.1847,
                    'lbs' : 0.453592}
    
    # Convert inputs to kg, then to final unit type
    kg = value * convert_dict[start_unit]
    converted_value = kg / convert_dict[final_unit]
    
    return converted_value

def facility_line_to_df(line):
    """
    Takes in a line (dictionary), returns a dataframe
    """
    for key in ['latlon', 'source', 'copyright', 'iso3166',
               'description', 'name', 'start', 'end']:
        line.pop(key, None)

    # Split the series_id up to extract information
    # Example: ELEC.PLANT.GEN.388-WAT-ALL.M
    series_id = line['series_id']
    series_id_list = series_id.split('.')
    # Use the second to last item in list rather than third
    plant_fuel_mover = series_id_list[-2].split('-')
    line['plant id'] = plant_fuel_mover[0]
    line['fuel'] = plant_fuel_mover[1]
    line['prime mover'] = plant_fuel_mover[2]
    temp_df = pd.DataFrame(line)

    try:
        temp_df['year'] = temp_df.apply(lambda x: x['data'][0][:4], axis=1).astype(int)
        temp_df['month'] = temp_df.apply(lambda x: x['data'][0][-2:], axis=1).astype(int)
        temp_df['value'] = temp_df.apply(lambda x: x['data'][1], axis=1)
        temp_df.drop('data', axis=1, inplace=True)
        return temp_df
    except:
        exception_list.append(line)
        pass