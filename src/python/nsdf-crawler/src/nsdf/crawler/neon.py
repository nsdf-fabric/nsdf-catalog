
import os,sys,requests,time, datetime,urllib3, requests,json,copy, psutil, json, csv, functools

# ///////////////////////////////////////////////////////////////////////////////////
from ratelimit import limits, RateLimitException, sleep_and_retry
@limits(calls=60, period=60) 
def GetNetworkResponse(url, headers={}, params={},connection_timeout=10,response_timeout=60):
	for I in range(3):
		response=requests.get(url, verify=True, timeout=(connection_timeout,response_timeout), headers=headers, params=params)
		if response.status_code == 200:
			return response.json()
		time.sleep(5)
	
	error_msg=f'GetNetworkResponse error url={url} response={response}, tried several times'
	print(error_msg)
	raise Exception(error_msg)

# ///////////////////////////////////////////////////////////////////////////////////
def GetNeonResponse(url, headers={}, params={}):
		try:
			ret=GetNetworkResponse(url, headers,params)
		except Exception as ex:
			return None # failed, do not care...
		return ret

# ///////////////////////////////////////////////////////////////////////////////////
def cint(value):
	try:
		return int(value)
	except:
		return 0


# ///////////////////////////////////////////////////////////////////////////////////
def Main():
	# https://data.neonscience.org/data-api/endpoints 
	# https://data.neonscience.org/data-products/DP3.30026.001
	with open("neon.csv", 'w') as fout:

		csv_writer = csv.writer(fout)

		io1 = psutil.net_io_counters()
		T1=time.time()
		t1=time.time()

		num_files,tot_size=0,0
		known_products=set()
		known_releases=set()

		# ///////////////////////////////////////////////////
		def print_stats(force=False):
			nonlocal t1
			if force or time.time()-t1 > 2.0:
				t1=time.time()
				io2 = psutil.net_io_counters()
				print(f"tot_size={tot_size:,} tot_size-tb={tot_size/1024**4:.2f} num_files={num_files:,} num-network-upload-bytes={io2.bytes_sent - io1.bytes_sent:,} network-download-bytes={io2.bytes_recv - io1.bytes_recv:,} sec={time.time()-T1:.2f}")
		# ///////////////////////////////////////////////////
		def append_row(row):
			nonlocal num_files,tot_size, csv_writer,t1
			num_files+=1
			tot_size+=row[3]
			csv_writer.writerow(row)

		# ///////////////////////////////////////////////////
		def visitFile(productCode,siteCode, file):
			if not productCode or not siteCode or not file: return
			name=file["name"] #"NEON.D16.ABBY.DP1.00001.001.000.020.002.2DWSD_2min.2019-08.basic.20220115T171830Z.csv",
			size=cint(file["size"]) #2346693,
			md5=str(file.get("md5",file.get("crc32",file.get("crc32c"))))
			url=file["url"] 
			append_row(["neon",f"file-{productCode}-{siteCode}",name,size,'',md5])
			print_stats()
			return size

		# ///////////////////////////////////////////////////
		def visitRelease(release):
			if not release: return
			nonlocal known_releases
    
			uuid=release["uuid"]
			if uuid in known_releases: return
			known_releases.add(uuid)
   
			# print("visitRelease",uuid)
   
			# artifacts 
			for artifact in release.get("artifacts",[]):
				append_row(["neon",f"release-{uuid}",artifact["name"],cint(artifact["size"]),"",artifact.get("md5",'')])    

			# dataProducts (==new products)
			for data_product in release.get("dataProducts",[]):
				productCode=data_product["productCode"]
				response=GetNeonResponse(f"https://data.neonscience.org/api/v0/products/{productCode}")
				if response:
					visitProduct(response.get("data",None))
			
			print_stats()
	
		# ///////////////////////////////////////////////////
		def visitSpec(productCode, spec):
			if not productCode or not spec: return
			specId=spec["specId"] # "8365",
			specNumber=spec["specNumber"] # "NEON.DOC.000780vD"
			specType=spec["specType"] # "application/pdf",
			specSize=cint(spec.get("specSize",0)) # 715529,
			specDescription=spec["specDescription"] # "NEON Algorithm Theoretical Basis Document (ATBD) – 2D Wind Speed and Direction",
			specUrl=spec["specUrl"] # "https://data.neonscience.org/api/v0/documents/NEON.DOC.000780vD"
			# catalog,bucket,name,size,last_modified,etag
			append_row(["neon",f"spec-{productCode}-{specId}",specNumber,specSize,"",""])
			print_stats()
			return specSize
    
    # ///////////////////////////////////////////////////
		def visitProduct(product):
			if not product: return
			nonlocal known_products
			productCode=product["productCode"] # DP1.00001.001
			if productCode in known_products: return
			known_products.add(productCode)
   
			num_files=0
			tot_size=0

			# spec
			specs=product.get("specs",[])
			for spec in specs if specs else []:
				tot_size+=visitSpec(productCode, spec)
				num_files+=1
   
			# releases
			releases=product.get("releases",[])
			for release in releases:
				response=GetNeonResponse(release["url"])
				if response:
					visitRelease(response.get("data",None))

			# site codes (contains files too, called 'data')
			site_codes=product.get("siteCodes",[])
			for sitecode in site_codes if site_codes else []:
				siteCode=sitecode["siteCode"]
				for data_url in sitecode["availableDataUrls"]:
					response=GetNeonResponse(data_url)
					if response and "data" in response:
							for file in response["data"].get("files",[]):
								tot_size+=visitFile(productCode, siteCode, file)
								num_files+=1

			print(f"visitProduct productCode={productCode} num-files={num_files:,} tot_size={tot_size:,}")
			print_stats()

		# curl -X 'GET' 'https://data.neonscience.org/api/v0/products' -H 'accept: application/json'
		# curl -X 'GET' 'https://data.neonscience.org/api/v0/releases -H 'accept: application/json'
		response=GetNeonResponse("https://data.neonscience.org/api/v0/products")
		if response:
			for product in response.get("data",[]):
				visitProduct(product)
		print_stats(force=True)

# ///////////////////////////////////////////////////////////////////////////////////
if __name__=="__main__":
	Main()


