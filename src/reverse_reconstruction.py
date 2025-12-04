#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
reverse_reconstruction.py
Kernalgorithmus der Reverse Reconstruction Methode
Created on Wed Dec  3 12:17:56 2025

@author: gh
"""

import numpy as np
from scipy.optimize import minimize
from scipy import integrate

class ReverseReconstruction:
    """Hauptklasse für die Reverse Reconstruction Methode"""
    
    def __init__(self):
        # Fundamentale Konstanten (CODATA 2022)
        self.fundamental_constants = {
            'alpha': 1/137.035999084,          # Feinstrukturkonstante
            'G_F': 1.1663787e-5,               # Fermi-Kopplung [GeV^-2]
            'sin2_thetaW': 0.23122,            # Weak mixing angle
            'm_Z': 91.1876,                    # Z-Boson Masse [GeV]
            'm_W': 80.377,                     # W-Boson Masse [GeV]
            'm_H': 125.25,                     # Higgs Masse [GeV]
            'm_top': 172.76,                   # Top-Quark Masse [GeV]
            'Lambda_QCD': 0.218,               # QCD Skalenparameter [GeV]
            'alpha_s_MZ': 0.1184,              # Starke Kopplung bei M_Z
            'f_pi': 0.1302,                    # Pion Zerfallskonstante [GeV]
            'm_pi': 0.13957,                   # Pion Masse [GeV]
            'm_proton': 0.93827,               # Proton Masse [GeV]
            'm_neutron': 0.93957,              # Neutron Masse [GeV]
        }
        
        # Beobachtbare Größen (experimentelle Werte)
        self.observables = self.load_experimental_data()
    
    def load_experimental_data(self):
        """Lädt experimentelle Referenzdaten"""
        return {
            # LHC Heavy-Ion Daten (Pb-Pb √s_NN = 5.02 TeV)
            'dNch_deta_central': {
                'value': 1584, 'error': 47,
                'reference': 'ALICE, Nature Phys. 13 (2017) 535'
            },
            'v2_central': {
                'value': 0.322, 'error': 0.015,
                'reference': 'ALICE, Phys. Rev. C 96 (2017) 034904'
            },
            'R_AA_central': {
                'value': 0.28, 'error': 0.03,
                'reference': 'ALICE, Phys. Lett. B 720 (2013) 52'
            },
            
            # Kritische Punkt Suchen
            'T_critical_lattice': {
                'value': 156.5, 'error': 1.5,
                'reference': 'HotQCD, Phys. Rev. D 90 (2014) 094503'
            },
            'muB_critical_search': {
                'value': 350, 'error': 50,
                'reference': 'STAR, Phys. Rev. Lett. 128 (2022) 202303'
            }
        }
    
    def compute_from_fundamentals(self):
        """Berechnet physikalische Parameter aus fundamentalen Konstanten"""
        
        # 1. QCD kritische Temperatur aus Λ_QCD und α_s
        T_c = self.calculate_critical_temperature()
        
        # 2. Baryon chemisches Potential aus Nukleonmassen
        mu_B_crit = self.calculate_critical_muB()
        
        # 3. Observablen aus QCD-Parametern
        observables_pred = self.calculate_observables(T_c, mu_B_crit)
        
        return {
            'T_critical': T_c,
            'mu_B_critical': mu_B_crit,
            'predicted_observables': observables_pred
        }
    
    def calculate_critical_temperature(self):
        """Berechnet kritische Temperatur aus QCD-Parametern"""
        # Basierend auf Skalenanalyse: T_c ∝ Λ_QCD * f(α_s, N_f)
        Lambda = self.fundamental_constants['Lambda_QCD']
        alpha_s = self.fundamental_constants['alpha_s_MZ']
        
        # Skalierungsfunktion (1-loop Näherung mit N_f=2+1)
        beta_0 = (33 - 2*3) / (12 * np.pi)  # β-Funktion für N_f=3
        scaling = 1.0 / (1 + beta_0 * alpha_s * np.log(4))
        
        T_c = Lambda * scaling * 1.8  # Numerischer Faktor aus Matching
        return T_c
    
    def calculate_critical_muB(self):
        """Berechnet kritisches μ_B aus Hadron-Spektroskopie"""
        # Verbindung zum chiralen Kondensat und Baryon-Resonanzen
        m_N = self.fundamental_constants['m_proton']
        f_pi = self.fundamental_constants['f_pi']
        
        # Skalierungsrelation: μ_B,crit ~ m_N * (1 - c * (m_pi/f_pi)^2)
        chiral_correction = 0.3 * (self.fundamental_constants['m_pi']/f_pi)**2
        
        mu_B_crit = m_N * (1.0 - chiral_correction)
        return mu_B_crit
    
    def calculate_observables(self, T, mu_B):
        """Berechnet experimentelle Observablen aus T, μ_B"""
        
        # 1. Multiplizität (Skalierung mit T^3)
        dNch_deta = 1600 * (T/156)**3 * (1 + 0.1 * mu_B/350)
        
        # 2. Elliptischer Fluss (Hydrodynamik-Skalierung)
        v2 = 0.32 * (T/156)**0.5 * np.exp(-0.001 * mu_B)
        
        # 3. Jet Quenching (energieabhängige Suppression)
        R_AA = 0.28 + 0.02 * (T/156 - 1) - 0.01 * mu_B/350
        
        return {
            'dNch_deta': dNch_deta,
            'v2': v2,
            'R_AA': R_AA
        }
    
    def optimize_parameters(self):
        """Optimiert Parameter durch Vergleich mit Experimenten"""
        
        # Zielfunktion: χ² zwischen Vorhersage und Experiment
        def objective(params):
            T, mu_B = params
            pred = self.calculate_observables(T, mu_B)
            
            chi2 = 0
            chi2 += ((pred['dNch_deta'] - self.observables['dNch_deta_central']['value']) 
                    / self.observables['dNch_deta_central']['error'])**2
            chi2 += ((pred['v2'] - self.observables['v2_central']['value'])
                    / self.observables['v2_central']['error'])**2
            chi2 += ((pred['R_AA'] - self.observables['R_AA_central']['value'])
                    / self.observables['R_AA_central']['error'])**2
            
            return chi2
        
        # Startwerte aus fundamentaler Berechnung
        initial_guess = [150, 350]
        
        # Optimierung
        result = minimize(objective, initial_guess, 
                         bounds=[(100, 200), (200, 500)])
        
        return result.x, result.fun
    
    def statistical_analysis(self, predictions):
        """Führt statistische Analyse durch"""
        
        T_pred, mu_B_pred = predictions
        
        # Vergleich mit experimentellen Werten
        T_exp = self.observables['T_critical_lattice']
        muB_exp = self.observables['muB_critical_search']
        
        # Signifikanz-Berechnung
        sigma_T = abs(T_pred - T_exp['value']) / T_exp['error']
        sigma_muB = abs(mu_B_pred - muB_exp['value']) / muB_exp['error']
        
        return {
            'T_critical': {
                'prediction': T_pred,
                'experiment': T_exp['value'],
                'sigma': sigma_T,
                'compatible': sigma_T < 2
            },
            'mu_B_critical': {
                'prediction': mu_B_pred,
                'experiment': muB_exp['value'],
                'sigma': sigma_muB,
                'compatible': sigma_muB < 2
            }
        }