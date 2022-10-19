from bs4 import BeautifulSoup
import requests,json,time
from multiprocessing.pool import ThreadPool
import time
import csv,os,sys

# //////////////////////////////////////////////////////////////////////////////
# https://kiwidamien.github.io/webscraping-beyond-beautifulsoup-and-selenium.html
def GetProjecs(type, prefix="https://www.naic.edu/datacatalog/index.php/datasets/view/"):
	body=requests.get(f"https://www.naic.edu/datacatalog/index.php/search{type}").content
	soup = BeautifulSoup(body,"html.parser")
	ret=[]
	for it in soup.find_all("a",href=True):
		href=it["href"]
		if not prefix or href.startswith(prefix):
			id=href.split("/")[-1]
			ret.append({
				'id' : id,
				'type':type
			}) # last is project id

	return ret

# ////////////////////////////////
def GetFiles(proj, url="https://www.naic.edu/datacatalog/index.php/datasetsJList",chunk_length=100000):

	# Open In Chrome something like https://www.naic.edu/datacatalog/index.php/datasets/view/P2016
	# curl -d "proj=P2016&draw=1&start=0&length=100000000" -X POST https://www.naic.edu/datacatalog/index.php/datasetsJList

	"""
	Example:
	{
		'id': 'P2016', 
		'type': 'Astronomy',
		'files': [
				{'id': '2547128', 'RemoteFile': 'data20160622191550.000', 'Size': '480000000', 'FileAttributes': '', 'ReqAccess': ''}, 
				{'id': '2547129', 'RemoteFile': ...
		]
	"""

	files=[]
	t1=time.time()
	print(f"GetFiles proj={proj['id']} started")

	while True:

		out=requests.post(
			url, 
			data={
				'frmt':'',
				'proj':proj['id'],
				'draw':'1',
				'start':len(files),
				'length': chunk_length,}
		).content

		try:
			v=json.loads("[{" + out.decode("utf-8") .split("[{",maxsplit=1)[1].split("}]")[0] + "}]")
		except:
			v=[]

		if v:
			files=files+v
			sec=int(time.time()-t1)
			print(f"...got another chunk proj={proj['id']} tot={len(files)} {sec} seconds")

		if len(v)<chunk_length:
			break

	sec=int(time.time()-t1)
	print(f"GetFiles proj={proj['id']} FINISHED tot={len(files)} {sec} seconds")
	proj['files']=files


# ////////////////////////////////////////////////////////
def GetProject(id):
	for proj in projects:
		if proj['id']==id:
			return proj
	return None

# ////////////////////////////////////////////////////////
if __name__=="__main__":
  
	output_filename=sys.argv[1]
	num_threads=int(sys.argv[2])
 
	print("output_filename",output_filename)  
	print("num_threads    ",num_threads) 

	projects=GetProjecs("Astronomy") + GetProjecs("Atmospheric") + GetProjecs("Planetary") 

	print(f"num_projects",len(projects))
	p = ThreadPool(num_threads)
	p.map(GetFiles, projects)

	TOT_BYTES,NUM_FILES=0,0
	GB=1024*1024*1024
	for proj in projects:
		files= proj['files']
		num_files=len(files)
		if num_files==0: continue
		tot_bytes=0
		for file in files:
			s_size=file['Size'].split()[0] # sometimes I have spurious char at the end
			tot_bytes+=int(s_size)
		print(f"proj={proj['id']} num_files={num_files} tot_bytes={tot_bytes} tot_gb={int(tot_bytes/GB)}")
		TOT_BYTES+=tot_bytes
		NUM_FILES+=num_files
	print(f"NUM_FILES={NUM_FILES} TOT_BYTES={TOT_BYTES} TOT_GBYTES={int(TOT_BYTES/GB)}")

	rows=[]
	for proj in projects:
		for file in proj['files']:
			catalog='arecibo'
			bucket=proj['id']
			file_id=file['id'] # should I need it?
			name=file['RemoteFile']
			size=int(file['Size'].split()[0])
			last_modified=''
			etag=''
			rows.append((catalog,bucket,name,size,last_modified,etag))
  
	with open(output_filename, 'wt') as f:
		csv.writer(f).writerows(rows)
