import os,sys,requests,time, datetime,urllib3
import zenodopy
from pprint import pprint
import json, csv
from ratelimit import limits, RateLimitException, sleep_and_retry

# this is an hard limit imposed by the Zenodo Search API that is using ElasticCache
ZENODO_MAX_RECORDS=10000

# I can use the guest account, it has some limitation bgut will be fine to get public records
zeno = zenodopy.Client()


# /////////////////////////////////////////////////////////////
@sleep_and_retry
@limits(calls=30, period=60) 
def GetJSONResponse(url):
	ret=requests.get(url, verify=True, timeout=(10,60))
	if ret.status_code!=200:
		raise Exception(f"Cannot get response for url={url} got {ret.status_code} {ret.reason}")
	return ret

# /////////////////////////////////////////////////////////////
def GetZenodoRecords(a,b):
	# create the url with the condition on publication_date
	d1=datetime.date.fromordinal(a)
	d2=datetime.date.fromordinal(b)
	m=f"{d1.year}-{d1.month:02d}-{d1.day:02d}"
	M=f"{d2.year}-{d2.month:02d}-{d2.day:02d}"
	url=requests.Request('GET','https://zenodo.org/api/records', params={
		'q': '(publication_date: ["%s" TO "%s"})' % (m,M), # first date is included, second data is excluded
		'sort': 'publication_date',
		'status': 'published', 
		'size' : ZENODO_MAX_RECORDS,
		'page' : '1'
		}).prepare().url

	
	# try several times...
	t1=time.time()
	#print(f"starting requests d1={d1} d2={d2} delta={b-a} ...")
	for retry in range(3):
		try:
			response=GetJSONResponse(url).json()
			break
		except Exception as ex:
			# too many retries
			if retry==2: 
				raise

	total=response['hits']['total']
	print(f"Got response d1={d1} d2={d2} delta={b-a} in {time.time()-t1:.2f} seconds #records={total}")

	# am I getting all hits?
	if  total<ZENODO_MAX_RECORDS:
		return response['hits']['hits']

	# failed, need to try with lower delta
	delta=b-a
	if delta==1:
		raise Exception(f"Cannot do much, got #records={total} with delta={delta}")

	delta=max(1,delta//2)
	print(f"Got Too many records, reducing delta={delta}")
	ret=[]
	for d in range(a,b,delta):
		ret.extend(GetZenodoRecords(d,min(d+delta,b)))
	return ret


# /////////////////////////////////////////////////////
if __name__=="__main__":

	action=sys.argv[1]

   # /////////////////////////////////////////////////////
	if action=="json":
		RECORDS=[]
		long_ago=datetime.date(2010, 1, 1).toordinal() #  I am loosing some Zenodo records but with wrong date
		today=datetime.datetime.today().toordinal()

		import psutil
		io1 = psutil.net_io_counters()
		T1=time.time()

		# choose the delta in a way that you don't get more than 10K records for a request
		delta=5

		for A in range(long_ago,today,delta):
			B=min(today,A+delta)
			try:
				RECORDS.extend(GetZenodoRecords(A,B))
			except Exception as ex:
				print(f"ERROR A={A} B={B} exception={ex}")

		io2 = psutil.net_io_counters()
		print(f"num-network-upload-bytes={io2.bytes_sent - io1.bytes_sent:,} network-download-bytes={io2.bytes_recv - io1.bytes_recv:,} sec={time.time()-T1:.2f}")	

		with open("zenodo.json", 'w') as fp:
			json.dump(RECORDS, fp)
	
		print("ALl done")
		sys.exit(0)
   
   # /////////////////////////////////////////////////////
	if action=="csv":

		with open("zenodo.json", 'r') as fin:
			RECORDS=json.load(fin)

		with open("zenodo.csv","w")  as fout:
			writer=csv.writer(fout)
			num_files,tot_size=0,0
			for record in RECORDS:
				for f in record.get('files',[]):

					def Encode(value):
						return str(value).replace(","," ").replace("'"," ").replace('"'," ").replace("  "," ")
					
					writer.writerow([
						"zenodo.org",                  # catalog
						record.get("conceptdoi","na"), # bucket
						Encode(f.get("key","")),       # filename
						f.get("size",0),               # size
						record.get("created",""),      # creation time and/or modification time
						f.get("checksum","")           # checksum
					])   
					num_files+=1
					tot_size+=f.get("size",0)
			print("num_files",num_files,"tot_size",tot_size)
		sys.exit(0)