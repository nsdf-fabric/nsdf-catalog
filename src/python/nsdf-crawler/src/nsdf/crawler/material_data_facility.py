# see https://mdf-forge.readthedocs.io/en/master/examples/Example_Statistics-MDF_Datasets.html

import os, sys, base64, glob, subprocess, time, logging, datetime
import time
from mdf_forge.forge import Forge

# /////////////////////////////////////////////////////
class MaterialDataFacility:

	# constructor
	def __init__(self,name):
		self.name=name
		self.mdf = Forge(anonymous=True)
		# self.mdf.show_fields()

	# listDatasets
	def listDatasets(self, args={}):
		ret=[{
			"source_id"  :dataset['mdf']["source_id"],
			"source_name":dataset['mdf']["source_name"]
			} for id, dataset in enumerate(self.mdf.search("mdf.resource_type:dataset", advanced=True))]
		print(f"MaterialDataFacility::listDatasets #({len(ret)})")
		return ret

	# getDatasetKey
	def getDatasetKey(self,args):
		return "{}/{}".format(self.name,args["source_id"])

	# listCatalogObjects
	def listCatalogObjects(self,args):
		t1=time.time()
		source_id=args["source_id"]
		source_name=args["source_name"]
		records=self.mdf.aggregate_sources([source_name])
		ret=[]
		tot_size,tot_files=0,0
		for record in records:
			files=record.get("files",[])
			"""
			Example of a file (it is a dictionary)
			{
				'data_type': 'Hierarchical Data Format (version 5) data',
				'filename': 'series_step_19.hdf5',
				'globus': 'globus://e38ee745-6d04-11e5-ba46-22000b92c6ec/MDF/mdf_connect/prod/data/mdr_item_1427_v1/Med '
								'Mn with holes_20 Ton binder_1mm step_new paint_argus/Med Mn with '
								'holes_20 Ton binder_1mm step_new paint_argus/series_step_19.hdf5',
				'length': 12306584,
				'mime_type': 'application/x-hdf',
				'sha512': '0ed601bf9e98d7f2d3fa0cb939c88a6a73de4a2211cb7687eb976fba7c6e07274f865e0ead4172f18836956ebafe030b3303bbbb695d2f0fd5b29255edd942dc',
				'url': 	'https://e38ee745-6d04-11e5-ba46-22000b92c6ec.e.globus.org/MDF/mdf_connect/prod/data/mdr_item_1427_v1/Med '
							'Mn with holes_20 Ton binder_1mm step_new paint_argus/Med Mn with '
							'holes_20 Ton binder_1mm step_new paint_argus/series_step_19.hdf5'}]
			"""
			for file in files:
				ret.append([
					self.name, # catalog name
					source_id, # dataset id
					file['filename'], 
					int(file['length']), 
					None, # last modified
					file['sha512']
				])
				tot_size+=int(file['length'])
				tot_files+=1
		sec=time.time()-t1
		print(f"MaterialDataFacility::listCatalogObjects END source_id({source_id}) tot_files({tot_files}) tot_size({HumanSize(tot_size)}) {sec} seconds")
		return ret


# /////////////////////////////////////////////////////////////////////////////
def WriteCSV(filename,rows):
	import csv
	try:
		os.makedirs(os.path.dirname(filename),exist_ok=True)
	except:
		pass
	with open(filename, 'wt') as f:
		csv.writer(f).writerows(rows)

# ////////////////////////////////////////////////////////////////////////
if __name__=="__main__":

	output_dir=sys.argv[1]
	print("output_dir",output_dir)

	catalog=MaterialDataFacility("mdf")
	for dataset in catalog.listDatasets():
		key=catalog.getDatasetKey(dataset)
		loc=os.path.join(output_dir,catalog.getDatasetKey(dataset))
		t1=time.time()
		objects=catalog.listCatalogObjects(dataset)
		WriteCSV(loc,objects)
		print(f"ListCatalogObjectsToCsvTask dataset({dataset}) loc({loc}) #({len(objects)}) file_size({os.path.getsize(loc)}) {int(time.time()-t1)} seconds")