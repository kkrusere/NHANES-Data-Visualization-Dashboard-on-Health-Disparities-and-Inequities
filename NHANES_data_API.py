import pandas as pd
cycle_list = [  
                '1999-2000',
                '2001-2002',
                '2003-2004',
                '2005-2006',
                '2007-2008',
                '2009-2010',
                '2011-2012',
                '2013-2014',
                '2015-2016',
                '2017-2018']
data_cat_list = [
                "demographics",
                "dietary", 
                "examination", 
                "laboratory", 
                "questionnaire", 
                "limitedaccess"
            ]

class NHANESDataAPI:
    def __init__(self, data_category, data_dir="data/"):
        """
        Initialize the NHANES Data API.

        Args:
        data_category (str): The data category for which to retrieve the variable table.
        data_dir (str): Directory where data will be stored.
        """
        self.data_dir = data_dir

        # Check if the provided data category is valid
        if not self.is_valid_data_category(data_category):
            print("You have enter an Invalid data category!!!")
            print(f"Valid Data Categories: {data_cat_list}")

            raise ValueError(f"Invalid data category: {data_category}")
            

        self.variable_table = self._get_variable_table(data_category)
        self.data_file_names = self.resolve_data_file_names()
        #self.list_data_file_descriptions_for_data = self.list_data_file_descriptions()
        



    def is_valid_data_category(self, data_category):
        """
        Check if the provided data category is valid.

        Args:
        data_category (str): The data category to check.

        Returns:
        bool: True if the data category is valid, False otherwise.
        """
        valid_data_categories = data_cat_list  
        return data_category in valid_data_categories



    def resolve_data_file_names(self):
        """
        Resolve data file names for all available cycles during initialization.

        Returns:
        dict: A dictionary mapping (cycle_year, data_file_description) to data_file_name.
        """
        data_file_names = {}

        for cycle_year in cycle_list:
            for data_file_description in self.list_data_file_descriptions():
                data_file_name = self.get_data_filename(cycle_year, data_file_description)
                data_file_names[(cycle_year, data_file_description)] = data_file_name

        return data_file_names

    def _get_variable_table(self, data_category):
        """
        Retrieve the variable table for a specific data category.

        Args:
        data_category (str): The data category for which you want the variable table.

        Returns:
        pd.DataFrame: A pandas DataFrame containing the variable table.
        """
        url = f"https://wwwn.cdc.gov/nchs/nhanes/search/variablelist.aspx?Component={data_category}"
        df = pd.read_html(url)[0]  # Assuming the table is the first one on the page

        df["Years"] = df.apply(lambda row: f"{row['Begin Year']}-{row['EndYear']}", axis=1)
        df.drop(["Begin Year", "EndYear", "Component", "Use Constraints"], axis=1, inplace=True)
        df = df.loc[df["Years"].isin(cycle_list)]
        df.reset_index(drop=True, inplace=True)

        return df

    
    def list_data_file_descriptions(self):
        """
        List unique data file descriptions from the variable table.

        Returns:
        list: A list of unique data file descriptions.
        """
        data_file_descriptions = self.variable_table['Data File Description'].unique()
        return data_file_descriptions

    
    def list_variables(self, cycle_year, data_file_description):
        """
        List variables for a specific cycle year and data file description.

        Args:
        cycle_year (str): The year or cycle for which data is requested.
        data_file_description (str): The data file description.

        Returns:
        dict: A dictionary of {Variable Name: Variable Description}.
        """
        variable_dict = {}
        for i in range(len(self.variable_table)):
            if self.variable_table['Years'][i] == cycle_year and self.variable_table['Data File Description'][i] == data_file_description:
                variable_dict[self.variable_table['Variable Name'][i]] = self.variable_table['Variable Description'][i]
        return variable_dict


    def list_data_files(self):
        """
        List data files and their corresponding cycle years for each unique data file description.

        Returns:
        dict: A dictionary of {Data File Description: {Data File Name: [cycle_years]}}.
        """
        data_file_dict = {}
        for index, row in self.variable_table.iterrows():
            data_file_desc = row['Data File Description']
            data_file_name = row['Data File Name']
            cycle_year = row['Years']
            if data_file_desc not in data_file_dict:
                data_file_dict[data_file_desc] = {data_file_name: [cycle_year]}
            else:
                if data_file_name in data_file_dict[data_file_desc]:
                    data_file_dict[data_file_desc][data_file_name].append(cycle_year)
                else:
                    data_file_dict[data_file_desc][data_file_name] = [cycle_year]
        return data_file_dict

    def get_data_filename(self, cycle_year, data_file_description):
        """
        Get the data file name for a specific cycle year and data file description.

        Args:
        cycle_year (str): The year or cycle for which data is requested.
        data_file_description (str): The data file description.

        Returns:
        str: The data file name.
        """
        # for row in self.variable_table:
        #     if row['Years'] == cycle_year and row['Data File Description'] == data_file_description:
        #         return row['Data File Name']

        for i in range(len(self.variable_table)):
            if self.variable_table['Years'][i] == cycle_year and self.variable_table['Data File Description'][i] == data_file_description:
                return self.variable_table['Data File Name'][i]
            
        return None

    def common_variables(self, cycle_years):
        """
        Find common variables across multiple cycle years and create a dictionary with variable-cycles mapping.

        Args:
        cycle_years (list of str): List of cycle years.

        Returns:
        list: List of common variables.
        dict: A dictionary of {variable: [cycles]}.
        """
        common_variables = None
        variable_cycles_dict = {}

        for cycle in cycle_years:
            variables = [row['Variable Name'] for index, row in self.variable_table.iterrows() if row['Years'] == cycle]
            if common_variables is None:
                common_variables = set(variables)
            else:
                common_variables.intersection_update(variables)

            for variable in variables:
                if variable in variable_cycles_dict:
                    variable_cycles_dict[variable].append(cycle)
                else:
                    variable_cycles_dict[variable] = [cycle]

        common_variables = list(common_variables)
        return common_variables, variable_cycles_dict
    
    def check_cycle(self, input_cycle):
        """
        Check the validity of a cycle and return valid cycle(s) based on input.

        Args:
        input_cycle (str): The input cycle year or range.

        Returns:
        list: List of valid cycle(s) based on input.
        """
        if '-' in input_cycle:
            start_year, end_year = input_cycle.split('-')
            the_cyclelist = self.check_in_between_cycle(start_year, end_year, cycle_list)
            return the_cyclelist
        elif input_cycle in cycle_list:
            return [input_cycle]
        else:
            return []

    def check_in_between_cycle(self, start_year, end_year, cycle_list):
        """
        Check for valid cycles within a range.

        Args:
        start_year (str): The start year of the range.
        end_year (str): The end year of the range.
        cycle_list (list): List of available cycle years.

        Returns:
        list: List of valid cycle(s) within the range.
        """
        list_of_cycles_to_be_worked_on = []
        flager = 0
        for cycle in cycle_list:
            if start_year in cycle:
                flager = 1
            if flager == 1:
                list_of_cycles_to_be_worked_on.append(cycle)
            if end_year in cycle:
                return list_of_cycles_to_be_worked_on
        return list_of_cycles_to_be_worked_on




    def get_data(self, cycle_year, data_category, data_file_description, include_uncommon=False):
        """
        Get data for a specific cycle year, data category, and data file description.

        Args:
        cycle_year (str): The year or cycle for which data is requested.
        data_category (str): The data category.
        data_file_description (str): The data file description.
        include_uncommon (bool): Whether to include uncommon variables (default is False).

        Returns:
        pd.DataFrame: A pandas DataFrame containing the requested data.
        """
        list_of_cycles = self.check_cycle(cycle_year)

        if len(list_of_cycles) == 1:
            data_file_name = self.data_file_names.get((cycle_year, data_file_description))
            if data_file_name is not None:
                return pd.read_sas(f"https://wwwn.cdc.gov/Nchs/Nhanes/{cycle_year}/{data_file_name}")
            else:
                # Handle the case where data_file_name is not found
                print(f"Data file name not found for {cycle_year} and {data_file_description}.")
                return None

        else:
            # Initialize an empty DataFrame
            collective_data = pd.DataFrame()

            # Check commonality of variables within the cycles
            common_variables, _ = self.common_variables(list_of_cycles)

            # Prompt the user to include/exclude uncommon variables
            if include_uncommon:
                for cycle in list_of_cycles:
                    data_file_name = self.get_data_filename(cycle, data_file_description)
                    data = pd.read_sas(f"https://wwwn.cdc.gov/Nchs/Nhanes/{cycle}/{data_file_name}")
                    collective_data = collective_data.join(data)
            else:
                # Filter out uncommon variables
                common_variable_dataframes = []
                for cycle in list_of_cycles:
                    data_file_name = self.get_data_filename(cycle, data_file_description)
                    data = pd.read_sas(f"https://wwwn.cdc.gov/Nchs/Nhanes/{cycle}/{data_file_name}")

                    # Filter the DataFrame to include only common variables
                    data = data[common_variables]
                    common_variable_dataframes.append(data)

                # Join the filtered DataFrames
                collective_data = pd.concat(common_variable_dataframes, axis=1)

            return collective_data


    def join_data(self, cycle_year, data_category1, data_file_name1, data_category2, data_file_name2):
        """
        Join data from two different data files in the same cycle year.

        Args:
        cycle_year (str): The year or cycle for which data is requested.
        data_category1 (str): The data category of the first data file.
        data_file_name1 (str): The name of the first data file.
        data_category2 (str): The data category of the second data file.
        data_file_name2 (str): The name of the second data file.

        Returns:
        pd.DataFrame: A pandas DataFrame containing the joined data.
        """
        # Get data frames for the specified data categories and data files
        data_frame1 = self.get_data(cycle_year, data_category1, data_file_name1)
        data_frame2 = self.get_data(cycle_year, data_category2, data_file_name2)

        # Check if data frames exist
        if data_frame1 is None or data_frame2 is None:
            return None

        # Define the common column for joining (e.g., 'SEQN' - Respondent sequence number)
        common_column = 'SEQN'

        # Perform the join operation
        merged_data = data_frame1.merge(data_frame2, on=common_column, how='inner')

        return merged_data
