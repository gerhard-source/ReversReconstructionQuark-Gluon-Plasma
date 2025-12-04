#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_qcd_calculations.py
Created on Wed Dec  3 12:50:32 2025

@author: gh
"""

import unittest
import sys
sys.path.append('../src')

from qcd_equations import QCDEquations

class TestQCDCalculations(unittest.TestCase):
    
    def setUp(self):
        self.qcd = QCDEquations()
    
    def test_pressure_scaling(self):
        """Test ob Druck richtig mit T^4 skaliert"""
        p1 = self.qcd.pressure_ideal_qgp(T=200)
        p2 = self.qcd.pressure_ideal_qgp(T=400)
        ratio = p2 / p1
        expected = (400/200)**4
        self.assertAlmostEqual(ratio, expected, delta=0.1)
    
    def test_critical_behavior(self):
        """Test kritische Punkt Eigenschaften"""
        chi_near = self.qcd.baryon_susceptibility(T=156, mu_B=350)
        chi_far = self.qcd.baryon_susceptibility(T=200, mu_B=100)
        
        # Suszeptibilität sollte nahe am kritischen Punkt größer sein
        self.assertGreater(chi_near, chi_far)

if __name__ == '__main__':
    unittest.main()
