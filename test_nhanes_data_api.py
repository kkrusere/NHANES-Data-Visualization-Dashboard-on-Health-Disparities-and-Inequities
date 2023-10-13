import unittest
import pandas as pd
import numpy as np

from NHANES_data_API import NHANESDataAPI

class TestNHANESDataAPI(unittest.TestCase):
    def setUp(self):
        # Initialize the NHANESDataAPI with a specific data category for testing
        self.api = NHANESDataAPI(data_category='demographics')

    def test_list_data_file_descriptions(self):
        # Test the list_data_file_descriptions method
        descriptions = self.api.list_data_file_descriptions()
        self.assertTrue(isinstance(descriptions, (list, np.ndarray)))
        self.assertTrue(len(descriptions) > 0)
    

    def test_list_variables(self):
        # Test the list_variables method
        variables = self.api.list_variables(cycle_year='1999-2000', data_file_description='Demographic Variables & Sample Weights')
        self.assertIsInstance(variables, dict)
        self.assertTrue(len(variables) > 0)

    def test_list_data_files(self):
        # Test the list_data_files method
        data_files = self.api.list_data_files()
        self.assertIsInstance(data_files, dict)
        self.assertTrue(len(data_files) > 0)

    def test_get_data_filename(self):
        # Test the get_data_filename method 
        filename = self.api.get_data_filename(cycle_year='1999-2000', data_file_description='Demographic Variables & Sample Weights')
        self.assertIsInstance(filename, str)
        self.assertTrue(len(filename) > 0)

    def test_common_variables(self):
        # Test the common_variables method
        common_vars, uncommon_vars, var_cycles = self.api.common_variables(cycle_years=['1999-2000', '2001-2002'])
        self.assertIsInstance(common_vars, list)
        self.assertIsInstance(uncommon_vars, list)
        self.assertIsInstance(var_cycles, dict)
        self.assertTrue(len(common_vars) > 0)
        self.assertTrue(len(uncommon_vars) >= 0)  # uncommon_vars can be an empty list
        self.assertTrue(len(var_cycles) > 0)

    def test_check_cycle(self):
        # Test the check_cycle method
        valid_cycles = self.api.check_cycle('1999-2000')
        self.assertIsInstance(valid_cycles, list)
        self.assertEqual(len(valid_cycles), 1)
        invalid_cycles = self.api.check_cycle('InvalidCycle')
        self.assertIsInstance(invalid_cycles, list)
        self.assertEqual(len(invalid_cycles), 0)

    def test_get_data_valid(self):
        # Test when requesting valid data
        cycle_year = '1999-2000'
        data_category = 'demographics'
        data_file_description = 'Demographic Variables & Sample Weights'
        df = self.api.get_data(cycle_year, data_category, data_file_description)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertTrue(len(df) > 0)

 


if __name__ == '__main__':
    unittest.main()