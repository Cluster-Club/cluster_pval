"""
Tests for plotting function and function calculating percent
explained variance per principal component in display module
"""
import unittest
import pandas as pd
import numpy as np

from cluster_pval.display_module.display import cluster_plot
from cluster_pval.display_module.display import pca_var_per


class PlotFunctionTest(unittest.TestCase):
    """Tests for cluster_plot function"""
    @classmethod
    def test_smoke_clusterplot(cls):
        """Smoke test to make sure function runs"""
        test_array = np.array([[3, 1, 230, 0], [6, 2, 745, 0],
                               [6, 6, 1080, 1], [4, 3, 495, 0], [2, 5, 260, 0]])
        test_df = pd.DataFrame(data=test_array, columns=['0', '1', '2', 'cluster'])
        cluster_plot(test_df)

    def test_exception_clusterplot(self):
        """Test to see if exception is raised for wrong input type"""
        test_array = np.array([[3, 1, 230, 0], [6, 2, 745, 0], [6, 6, 1080, 1],
                               [4, 3, 495, 0], [2, 5, 260, 0]])
        with self.assertRaises(ValueError):
            cluster_plot(test_array)


class VarFunctionTest(unittest.TestCase):
    """Tests for percent explained variance function"""
    @classmethod
    def test_smoke_varper(cls):
        """Smoke test to make sure function runs"""
        test_array = np.array([[3, 1, 230, 0], [6, 2, 745, 0], [6, 6, 1080, 1],
                               [4, 3, 495, 0], [2, 5, 260, 0]])
        test_df = pd.DataFrame(data=test_array, columns=['0', '1', '2', 'cluster'])
        pca_var_per(test_df)

    def test_exception_varper(self):
        """Test to see if exception is raised for wrong input type"""
        test_array = np.array([[3, 1, 230, 0], [6, 2, 745, 0], [6, 6, 1080, 1],
                               [4, 3, 495, 0], [2, 5, 260, 0]])
        with self.assertRaises(ValueError):
            pca_var_per(test_array)

    def test_output_varper(self):
        """Test to check that the output is in the form of a percentage, i.e., between 0 and 1"""
        test_array = np.array([[3, 1, 230, 0], [6, 2, 745, 0], [6, 6, 1080, 1],
                               [4, 3, 495, 0], [2, 5, 260, 0]])
        test_df = pd.DataFrame(data=test_array, columns=['0', '1', '2', 'cluster'])
        varper_output = pca_var_per(test_df)
        self.assertGreaterEqual(varper_output[0], 0)
        self.assertGreaterEqual(varper_output[1], 0)
        self.assertLessEqual(varper_output[0], 1)
        self.assertLessEqual(varper_output[1], 1)
