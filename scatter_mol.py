import os

import numpy as np 
import pandas as pd

from rdkit import Chem, DataStructs
from rdkit.Chem import AllChem, PandasTools, Draw

from bokeh.plotting import figure, output_notebook, show
from bokeh.models import ColumnDataSource, HoverTool, CrosshairTool, WheelZoomTool
from bokeh.models import ColorBar, ResetTool, PanTool, LinearColorMapper

import bokeh.palettes as palettes
output_notebook()
import matplotlib as mpl

def scatter_mol(df):
    """
    Makes an interactive scatter plot with  
    """

    def get_structures(mol_df):
        img_path = []
        img_dir = "imgs/" 
        
        if not os.path.exists(img_dir):  #  Checks if folder exists then creates it
            os.makedirs(img_dir)
            
        for mol in range(len(mol_df)):
            Draw.MolToFile(mol_df['mol'][mol],
                            "imgs/" + mol_df.name[mol] + ".svg",
                            imageType="svg",
                            fitImage=False,
                            size=(200, 200))
            img_path.append("imgs/" + mol_df.name[mol] + ".svg")
        mol_df["img_path"] = img_path
        return mol_df

    pca_df = get_structures(df)

    colormap = {'0': '#d9534f', '1': '#428bca'}
    colors = [colormap[x] for x in pca_df["activity"]]
    pca_df['colors'] = colors
    source = ColumnDataSource(pca_df.drop("mol", axis = 1))

    hover = HoverTool(tooltips = 
                """
                <div>
                    <img src="@img_path" width="170" height="170"></img>
                </div> 
                <div>
                    <span style="font-size: 12px; font-weight: bold;">@name</span>
                </div>
                <div>
                    <span style="font-size: 12px; font-weight: bold;">PCA:</span>
                    <span style="font-size: 12px;">@comp1, @comp2</span>
                </div>
                <div>
                    <span style="font-size: 12px; font-weight: bold;">Activity:</span>
                    <span style="font-size: 12px;">@activity</span>
                </div>

                """)

    colormap = {'0': 'red', '1': '#35B778'}
    colors = [colormap[x] for x in source.data["activity"]]
    TOOLS=[hover, CrosshairTool(), WheelZoomTool(), ResetTool(), PanTool()]
    p = figure(plot_width=800, plot_height=800,title="PCA Morgan FPS", tools=TOOLS)
    p.scatter(x='comp1',y= 'comp2', size=5, alpha = 0.9, color='colors', source=source)
    #output_file("test_mol.html")
    show(p)