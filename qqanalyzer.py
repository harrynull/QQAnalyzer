import os
import re
import time
import pickle
import argparse

class message:
	time=""
	name=""
	qq=""
	content=[]
	def __init__(self):
		self.time,self.name,self.qq,self.content=("","","",[])

class messages:
	name=""
	msgs=[]
	user_qq_name={}
	def __init__(self, file_content, buffer,buffer2, buffer_valid):
		# define some constants, use the array index
		GROUP_NAME_LINE=5
		START_LINE=8

		# init
		name_re=re.compile(r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (.*)\((.*?)\)\n")
		name_email=re.compile(r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (.*)\<(.*?)\>\n")

		# get the group name in the 5th line
		self.name=(lambda line:line[line.index(":")+1:-1])(file_content[GROUP_NAME_LINE])

		print("Start analyze " + self.name + "...")
		
		if buffer_valid:
			self.msgs=pickle.loads(buffer.read())
			self.user_qq_name=pickle.loads(buffer2.read())
		else:
			# start read messages
			prog_all=len(file_content)
			prog_now=START_LINE
			just_now=False # just after a new message, for optimizing
			time_analyze=0

			for line in file_content[8:]:
				prog_now=prog_now+1
				res=[]
				if not just_now: res=name_re.findall(line)
				if not res and not just_now: res=name_email.findall(line)

				if res:
					# check the time first
					time_analyze_this=time.mktime(time.strptime(res[0][0], "%Y-%m-%d %H:%M:%S"))
					if time_analyze_this<time_analyze: continue
					time_analyze=time_analyze_this

					# remove the blank element and add to the array
					try: msg.content=msg.content[:-1]; self.msgs.append(msg);
					except NameError: pass

					# create the next message
					msg=message()
					msg.time, msg.name, msg.qq=res[0]
					msg.name=msg.name.replace("\u202e","").replace("\u202d","")
					msg.time=time_analyze_this;

					# add/update the qq-name dict
					self.user_qq_name[msg.qq]=msg.name

					just_now=True
				else:
					# add to char content array
					msg.content.append(line.replace("\n",""))
					just_now=False

				if prog_now%10==0: print("\rProgress: %f%%(%d/%d)"%(prog_now/prog_all*100.0,prog_now,prog_all),end="")
			
			# write to buffer
			buffer.write(pickle.dumps(self.msgs))
			buffer2.write(pickle.dumps(self.user_qq_name))
			
		print("\rDone"+" "*32)

	def getMessages(self):
		return self.msgs;
		
parser = argparse.ArgumentParser(description='Analyze QQ groups\' messages')
parser.add_argument("input", help="the input file: QQ exported *.txt message file")
parser.add_argument("-cache_input", help="the cache file", default="")
parser.add_argument('--bom', dest='use_bom', action='store_true', help='use bom in the output file')
parser.add_argument('--no-bom', dest='use_bom', action='store_false', help='do not use bom in the output file')
parser.add_argument('--no-cache', dest='use_cache', action='store_false', help='ignore the cache file (if any)')
parser.add_argument("mode", help="mode you want to use",choices =("user","all","week"), default="")
parser.add_argument("-qq", help="only analyze specific qq, only available in \"all\“ and \"week\" mode", default="")
parser.add_argument("-min_unit", help="the min unit in the \"all\" mode, the default value is 1 week, the unit is second", default=60*60*24*7, type=int)
parser.set_defaults(use_bom=True,use_cache=True)
args = parser.parse_args()

file_name,cache_name=args.input,args.cache_input
if cache_name=="": cache_name=file_name
cache_extension=".cache"

buffer_valid = os.path.exists(cache_name+".cache");
data = open(file_name,encoding="utf-8")
buffer = open(cache_name+cache_extension,"rb" if buffer_valid else "wb")
buffer2 = open(cache_name+".2"+cache_extension,"rb" if buffer_valid else "wb")

msgs = messages(data.readlines(), buffer,buffer2, buffer_valid and args.use_cache)
data.close()
buffer.close()
# to analyze the relationship between the numbers of messages and days
def analyze_all(msgs, min_unit, qq):
	time_start=int(msgs.msgs[0].time//min_unit)
	stat={}
	for m in msgs.getMessages():
		if m.qq != qq and qq!="": continue
		key=int(m.time//min_unit-time_start)
		stat[key]=stat.get(key, 0)+1
	return stat

# to analyze the relationship between the numbers of messages and each day of weeks
def analyze_week(msgs, qq):
	CHECK_INV=60*60*24 # a day
	stat={}
	for m in msgs.getMessages():
		if m.qq != qq and qq!="": continue
		key=int(m.time//CHECK_INV%7)
		stat[key]=stat.get(key, 0)+1
	return stat

# to analyze the numbers of members' messages
def analyze_user(msgs):
	stat={}
	for msg in msgs.getMessages():
		stat[msg.qq]=stat.get(msg.qq, 0)+1
	return stat

def print_plain(out,dic):
	for (key, value) in dic.items():
		out.write("%d,%s\n"%(key,value))

def print_uv(out,dic,msgs):
	for (k,v) in dic.items():
		output.write("%d,%s,%s\n"%(v,msgs.user_qq_name[k],k))

def print_uv_sorted(out,dic,msgs):
	for (k,v) in ((k, dic[k]) for k in sorted(dic, key=dic.get, reverse=True)):
		output.write("%d,%s,%s\n"%(v,msgs.user_qq_name[k],k))
		


output=open(file_name+".csv","w",encoding="utf_8_sig" if args.use_bom else "utf8")

modes={
"user": lambda:print_uv_sorted(output,analyze_user(msgs),msgs),
"all": lambda:print_plain(output,analyze_all(msgs,args.min_unit,args.qq)),
"week": lambda:print_plain(output,analyze_week(msgs,args.qq))
}

modes[args.mode]()

output.close()
