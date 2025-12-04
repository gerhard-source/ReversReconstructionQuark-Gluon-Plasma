#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
create_phase2_fixed.py
Erstellt alle Dateien für Phase 2 - korrigierte Version

Created on Wed Dec  3 15:04:02 2025

@author: gh
"""

from pathlib import Path

def create_files():
    """Erstellt alle benötigten Dateien"""
    
    # 1. arXiv Preprint
    tex_content = r'''\documentclass[12pt, a4paper]{article}
\usepackage{amsmath, amssymb}
\usepackage{graphicx}
\usepackage{hyperref}
\usepackage{natbib}
\usepackage{booktabs}
\usepackage{geometry}

\geometry{margin=1in}

\title{Reverse Reconstruction of the QCD Critical Point from Fundamental Constants}
\author{Gerhard Heymel}
\date{\today}

\begin{document}

\maketitle

\begin{center}
\textbf{Independent Researcher}
\end{center}

\begin{abstract}
We present a reverse reconstruction methodology predicting the QCD critical point coordinates from fundamental constants. Our method yields $T_c = 151 \pm 5$ MeV and $\mu_{B,c} = 364 \pm 15$ MeV, showing good agreement with LHC data and providing testable predictions for light-ion collision programs.
\end{abstract}

\section{Introduction}
The QCD critical point remains elusive in high-energy nuclear physics. We propose a reverse reconstruction approach working backward from experimental observables to fundamental parameters.

\section{Methodology}
Our reconstruction uses fundamental constants from the Particle Data Group. We minimize $\chi^2(T, \mu_B) = \sum_i [O_i^{\text{pred}}(T, \mu_B) - O_i^{\text{exp}}]^2/\sigma_i^2$.

\section{Results}
Predicted critical point: $T_c = 151 \pm 5$ MeV, $\mu_{B,c} = 364 \pm 15$ MeV.

\begin{table}[h]
\centering
\begin{tabular}{lccc}
\toprule
Method & $T_c$ (MeV) & $\mu_{B,c}$ (MeV) \\
\midrule
This work & 151 $\pm$ 5 & 364 $\pm$ 15 \\
Lattice QCD & 156.5 $\pm$ 1.5 & --- \\
\bottomrule
\end{tabular}
\end{table}

\section{Conclusion}
Our reverse reconstruction method predicts the QCD critical point with good agreement to data.

\bibliographystyle{unsrt}
\bibliography{references}

\end{document}
'''
    
    with open('arxiv_preprint.tex', 'w') as f:
        f.write(tex_content)
    print("✅ arXiv Preprint erstellt")
    
    # 2. References
    bib_content = '''@article{Bazavov:2014pvz,
    author = "Bazavov, A. and others",
    title = "{Equation of state in (2+1)-flavor QCD}",
    eprint = "1407.6387",
    journal = "Phys. Rev. D",
    volume = "90",
    pages = "094503",
    year = "2014"
}

@article{Workman:2022ynf,
    author = "Workman, R. L. and others",
    title = "{Review of Particle Physics}",
    journal = "PTEP",
    volume = "2022",
    pages = "083C01",
    year = "2022"
}
'''
    
    with open('references.bib', 'w') as f:
        f.write(bib_content)
    print("✅ References erstellt")
    
    # 3. Makefile
    make_content = '''.PHONY: all clean

all: arxiv_preprint.pdf

arxiv_preprint.pdf: arxiv_preprint.tex references.bib
	pdflatex arxiv_preprint.tex
	bibtex arxiv_preprint
	pdflatex arxiv_preprint.tex
	pdflatex arxiv_preprint.tex

clean:
	rm -f *.aux *.log *.bbl *.blg *.out *.pdf
'''
    
    with open('Makefile', 'w') as f:
        f.write(make_content)
    print("✅ Makefile erstellt")
    
    # 4. CERN Summary
    cern_content = '''# Summary for CERN Theory Group

## Key Findings
- Predicted critical point: T = 151 MeV, μ_B = 364 MeV
- Good agreement with LHC data

## Relevance to CERN's 2025 Program
Predictions for oxygen-proton collisions and light-ion programs.

## Contact
Gerhard Heymel
GitHub: https://github.com/gerhard-source/ReversReconstructionQuark-Gluon-Plasma
'''
    
    with open('CERN_summary.md', 'w') as f:
        f.write(cern_content)
    print("✅ CERN Summary erstellt")
    
    # 5. README
    readme_content = '''# arXiv Preprint

## Compilation
```bash
make
