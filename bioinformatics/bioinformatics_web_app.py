####################
# Import libraries
####################

import pickle
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image
from rdkit import Chem
from rdkit.Chem import Descriptors


######################
# Custom function
######################

# Calculate molecular descriptors
def AromaticProportion(m):
    aromatic_atoms = [m.GetAtomWithIdx(i).GetIsAromatic() for i in range(m.GetNumAtoms())]
    aa_count = []
    for i in aromatic_atoms:
        if i == True:
            aa_count.append(1)
    AromaticAtom = sum(aa_count)
    HeavyAtom = Descriptors.HeavyAtomCount(m)
    AR = AromaticAtom / HeavyAtom
    return AR


def generate(smiles, verbose=False):
    moldata = []
    for elem in smiles:
        mol = Chem.MolFromSmiles(elem)
        moldata.append(mol)

    baseData = np.arange(1, 1)
    i = 0
    for mol in moldata:

        desc_MolLogP = Descriptors.MolLogP(mol)
        desc_MolWt = Descriptors.MolWt(mol)
        desc_NumRotatableBonds = Descriptors.NumRotatableBonds(mol)
        desc_AromaticProportion = AromaticProportion(mol)

        row = np.array([desc_MolLogP,
                        desc_MolWt,
                        desc_NumRotatableBonds,
                        desc_AromaticProportion])

        if (i == 0):
            baseData = row
        else:
            baseData = np.vstack([baseData, row])
        i = i + 1

    columnNames = ["MolLogP", "MolWt", "NumRotatableBonds", "AromaticProportion"]
    descriptors = pd.DataFrame(data=baseData, columns=columnNames)

    return descriptors


######################
# Page Title
######################

path_logo_jpg = Path("bioinformatics_web_app") / "solubility-logo.jpg"
image = Image.open(path_logo_jpg)
st.image(image, use_column_width=True)

st.write("""
# Molecular Solubility Prediction App
This app predicts the **Solubility (LogS)** values of molecules!
Data obtained from the John S. Delaney. [ESOL:  Estimating Aqueous Solubility Directly from Molecular Structure](https://pubs.acs.org/doi/10.1021/ci034243x). ***J. Chem. Inf. Comput. Sci.*** 2004, 44, 3, 1000-1005.
***
""")

######################
# Input molecules (Side Panel)
######################

st.sidebar.header("User Input Features")

# Read SMILES input
SMILES_input = "NCCCC\nCCC\nCN"

SMILES = st.sidebar.text_area("SMILES input", SMILES_input)
SMILES = SMILES.split("\n")
SMILES.insert(0, "C")

# Calculate molecular descriptors
st.header("Computed molecular descriptors")
X = generate(SMILES)[1:]
st.dataframe(X)

######################
# Pre-built model
######################

# Load prediction model
path_model_pkl = Path("bioinformatics_web_app") / "solubility_model.pkl"
with open(path_model_pkl, "rb") as fp:
    model = pickle.load(fp)

# Make predictions
pred = model.predict(X)

st.header("Predicted LogS values")
pred
