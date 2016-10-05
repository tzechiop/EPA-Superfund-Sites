import os
outdir = r"C:\Users\thasegawa\Documents\68 NYC DEP Papers\05 Data\Newtown Creek\Sediment Trap Maps"
mxd = arcpy.mapping.MapDocument("CURRENT")
df_list = arcpy.mapping.ListDataFrames(mxd)
df_layer_list = [arcpy.mapping.ListLayers(df) for df in df_list]
chemical_list = ['Lead', 'Mercury', 'Copper', 'PCB-11 (ppm)', 'TPCB Ratio']
for chemical in chemical_list:
	for layer_list in df_layer_list:
		for layer in layer_list:
			if chemical in layer.name:
				layer.visible = True
	arcpy.RefreshActiveView()
	arcpy.RefreshTOC()
	outfname = 'SedTraps_{0}.pdf'.format(chemical)
	time.sleep(5)
	arcpy.mapping.ExportToPDF(mxd, os.path.join(outdir, outfname))
	for layer_list in df_layer_list:
		for layer in layer_list:
			if chemical in layer.name:
				layer.visible = False	
	arcpy.RefreshTOC()
	    