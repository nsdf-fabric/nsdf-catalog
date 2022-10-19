
import os, sys, base64, glob, subprocess, time, logging, datetime
import materials_commons.api as mcapi

# /////////////////////////////////////////////////////////////////////
class MaterialCommonsCatalog:

	# constructor
	def __init__(self,name):
		self.token=os.environ["MC_TOKEN"]
		self.name=name

	# listDatasets
	def listDatasets(self, args={}):
		client=mcapi.Client(self.token)
		datasets=client.get_all_published_datasets()
		# datasets=[dataset for dataset in datasets if len(client.get_published_dataset_files(dataset.id))>0 ]
		ret=[{
			'dataset_id':dataset.id
			} for dataset in datasets]
		print(f"MaterialCommonsCatalog::listDatasets #({len(ret)})")
		return ret

	# getDatasetKey
	def getDatasetKey(self,args):
		dataset_id=args["dataset_id"]
		return "{}/{}".format(self.name,dataset_id)

	# listCatalogObjects
	def listCatalogObjects(self,args):
		dataset_id=args["dataset_id"]
		client=mcapi.Client(self.token)
		files = client.get_published_dataset_files(dataset_id)
		ret=[]
		BYTES,COUNT=0,0
		for file in files:
			ret.append([
				self.name,
				dataset_id,
				file.name, 
				file.size, 
				None,
				file.checksum])
			BYTES+=file.size
			COUNT+=1
		print(f"MaterialCommonsCatalog::listCatalogObjects END dataset_id({dataset_id}) #({COUNT}) size({BYTES})")
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

	catalog=MaterialCommonsCatalog("mc")
	for dataset in catalog.listDatasets():
		key=catalog.getDatasetKey(dataset)
		loc=os.path.join(output_dir,catalog.getDatasetKey(dataset))
		t1=time.time()
		objects=catalog.listCatalogObjects(dataset)
		WriteCSV(loc,objects)
		print(f"dataset({dataset}) loc({loc}) #({len(objects)}) file_size({os.path.getsize(loc)}) {int(time.time()-t1)} seconds")
