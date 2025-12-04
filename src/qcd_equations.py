#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
qcd_equations.py
QCD-Gleichungen und Phasenübergangs-Physik

Created on Wed Dec  3 12:21:39 2025

@author: gh
"""

import numpy as np

class QCDEquations:
    """QCD-Gleichungen für Phasenübergänge"""
    
    def __init__(self, N_c=3, N_f=2+1):
        self.N_c = N_c
        self.N_f = N_f
        
    def pressure_ideal_qgp(self, T, mu_B=0):
        """Druck des idealen Quark-Gluon-Plasmas"""
        # Gluonen: 2*(N_c^2 - 1) Freiheitsgrade
        gluon_dof = 2 * (self.N_c**2 - 1)
        gluon_pressure = gluon_dof * (np.pi**2/90) * T**4
        
        # Quarks: N_f * N_c * 2 * 2 * (7/8)
        quark_dof = self.N_f * self.N_c * 4 * (7/8)
        quark_pressure = quark_dof * (np.pi**2/90) * T**4
        
        # Baryon-Dichte Beitrag
        baryon_pressure = (1/54) * mu_B**2 * T**2
        
        return gluon_pressure + quark_pressure + baryon_pressure
    
    def pressure_hadron_gas(self, T, mu_B):
        """Druck des Hadronengases"""
        # Pionen und Kaonen (Mesonen)
        m_pi = 0.140  # GeV
        m_K = 0.494   # GeV
        
        pion_pressure = 3 * self.bose_einstein_pressure(T, m_pi)
        kaon_pressure = 4 * self.bose_einstein_pressure(T, m_K)
        
        # Nukleonen
        m_N = 0.938  # GeV
        nucleon_pressure = 4 * self.fermi_dirac_pressure(T, m_N, mu_B/3)
        
        return pion_pressure + kaon_pressure + nucleon_pressure
    
    def bose_einstein_pressure(self, T, m):
        """Druck für Bose-Einstein Statistik"""
        if T == 0:
            return 0
        return (np.pi**2/90) * T**4 * np.exp(-m/T)
    
    def fermi_dirac_pressure(self, T, m, mu):
        """Druck für Fermi-Dirac Statistik"""
        if T == 0:
            return 0
        return (7/8) * (np.pi**2/90) * T**4 * np.exp(-(m - mu)/T)
    
    def critical_point_conditions(self, T, mu_B):
        """Bedingungen für kritischen Punkt"""
        # Baryonische Suszeptibilität
        chi_B = self.baryon_susceptibility(T, mu_B)
        
        # Kurtosis (κσ²)
        kappa_sigma2 = self.kurtosis(T, mu_B)
        
        # Kritischer Punkt wenn χ_B divergiert und κσ² Vorzeichen wechselt
        return chi_B, kappa_sigma2
    
    def baryon_susceptibility(self, T, mu_B):
        """Baryonische Suszeptibilität χ_B"""
        # Vereinfachtes Modell mit kritischem Exponent
        T_c = 156  # MeV
        mu_c = 350  # MeV
        
        distance = np.sqrt((T - T_c)**2 + (mu_B - mu_c)**2)
        if distance < 1:
            return 1e6  # Divergenz am kritischen Punkt
        
        return 1.0 / distance
    
    def kurtosis(self, T, mu_B):
        """Netto-Baryon Kurtosis κσ²"""
        # Vorzeichenwechsel am kritischen Punkt
        mu_c = 350  # MeV
        if mu_B > mu_c:
            return -1.0
        else:
            return 1.0
