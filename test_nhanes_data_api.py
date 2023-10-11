import unittest
import pandas as pd
from NHANES_data_API import NHANESDataAPI

class TestNHANESDataAPI(unittest.TestCase):
    def setUp(self):
        # Initialize the NHANESDataAPI object for testing
        self.api = NHANESDataAPI(data_category='demographic')  # Replace with the correct data category

    def test_list_data_file_descriptions(self):
        # Test the list_data_file_descriptions method
        descriptions = self.api.list_data_file_descriptions()
        self.assertIsInstance(descriptions, np.ndarray)  # Adjust for NumPy array
        self.assertGreater(len(descriptions), 0)

    def test_list_variables(self):
        # Test the list_variables method
        variables = self.api.list_variables(cycle_year='2009-2010', data_file_description='Demographic Variables & Sample Weights')
        self.assertIsInstance(variables, dict)
        # Add more specific test cases based on your implementation

    def test_list_data_files(self):
        # Test the list_data_files method
        data_files = self.api.list_data_files()
        self.assertIsInstance(data_files, dict)
        # Add more specific test cases based on your implementation

    def test_get_data_filename(self):
        # Test the get_data_filename method
        data_file_name = self.api.get_data_filename(cycle_year='2009-2010', data_file_description='Demographic Variables & Sample Weights')
        self.assertIsInstance(data_file_name, str)
        # Add more specific test cases based on your implementation

    def test_get_data(self):
        # Test the get_data method
        data = self.api.get_data(cycle_year='2009-2010', data_category="Demographics", data_file_description='Demographic Variables & Sample Weights')
        self.assertIsInstance(data, pd.DataFrame)
        # Add more specific test cases based on your implementation

    def test_join_data(self):
        # Test the join_data method
        joined_data = self.api.join_data(cycle_year='2009-2010', data_category1="demographics", data_file_name1='Demo_F', data_category2="questionnaire", data_file_name2="ACQ_F")
        self.assertIsInstance(joined_data, pd.DataFrame)
        # Add more specific test cases based on your implementation

if __name__ == '__main__':
    unittest.main()