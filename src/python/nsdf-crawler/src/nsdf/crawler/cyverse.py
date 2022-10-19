import os,sys,requests,time, datetime,urllib3, requests,json,copy, psutil, json, csv, functools

__token,__last_token=None,None


# ///////////////////////////////////////////////////////////////////////////////////
def cint(value):
	try:
		return int(value)
	except:
		return 0

# /////////////////////////////////////////////////////////////////////////////////// 
def GetToken():
	# renew token every X minutes
	global __token, __last_token
	if __last_token is None or (__last_token-time.time())>20*60:
		username = os.environ["CYVERSE_USERNAME"]
		password = os.environ["CYVERSE_PASSWORD"]
		__token = requests.get("https://de.cyverse.org/terrain/token", auth=(username, password)).json()['access_token']
		print("Got new token")
		__last_token=time.time()
	return __token
 

# ///////////////////////////////////////////////////////////////////////////////////
def GetResponse(url=None, headers=None, params=None):
	connection_timeout=10
	response_timeout=60
	response=requests.get(url, verify=True, timeout=(connection_timeout,response_timeout), headers=headers, params=params)
	if response.status_code == 200:
		response=response.json()
		return response
	else:
		raise Exception(f'GetNetworkResponse error url={url} response={response}, tried several times')  


# ///////////////////////////////////////////////////////////////////////////////////
def Traverse(csv_writer, folder, rec):
	
	# skipping JSON code
	if "/json/" in folder:
		print(f"Skipping folder=[{folder}] since it is JSON")
		return

	# permission denied
	if "magnoliagrandiFLORA/images/specimens" in folder:
		print(f"Skipping folder=[{folder}] since it I don't have access")
		return

	try:
		response = GetResponse(
			url="https://de.cyverse.org/terrain/filesystem/paged-directory", 
			headers={"Authorization": "Bearer " + GetToken(), 'Accept': '`application/json'},
			params={'path': folder, 'entity-type':'any',  'limit':'9999999999999999', 'sort-col':'NAME', 'sort-dir':'ASC'},
		)
	except Exception as ex:
		print("ERROR",ex)
		return

	# files
	files=[file for file in response.get('files',[]) if 'path' in file and 'file-size' in file]
	for file in files:
		# catalog,bucket,name,size,last_modified,etag	
		size=cint(file['file-size'])
		row=["cyverse",os.path.dirname(file['path']),os.path.basename(file['path']),size,file.get('date-modified',''),'']
		csv_writer.writerow(row)

	# recursive
	sub_folders=[it for it in response.get('folders',[]) if 'path' in it]
	for sub in sub_folders:
		Traverse(csv_writer, sub['path'],rec+1)

# ///////////////////////////////////////////////////////////////////////////////////
if __name__=="__main__":
	root_dir="/iplant/home/shared"
	print("root_dir",root_dir)
	with open('cyverse.csv', 'w') as fout:
		csv_writer = csv.writer(fout)
		Traverse(csv_writer,root_dir ,0)