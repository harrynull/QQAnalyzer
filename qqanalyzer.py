import os
import sys
import re
import time

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
	def __init__(self, file_content):
		# define some constants, use the array index
		GROUP_NAME_LINE=5
		START_LINE=8

		# init
		name_re=re.compile(r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (.*)\((.*?)\)\n")
		name_email=re.compile(r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (.*)\<(.*?)\>\n")

		# get the group name in the 5th line
		self.name=(lambda line:line[line.index(":")+1:])(file_content[GROUP_NAME_LINE])

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
		print("\rDone"+" "*32)

	def getMessages(self):
		return self.msgs;

data = open(sys.argv[1],encoding="utf-8")
msgs = messages(data.readlines())
data.close()

# to analyze the relationship between the numbers of messages and days
def analyze_all(msgs, min_unit):
	time_start=int(msgs.msgs[0].time//min_unit)
	stat={}
	for m in msgs.getMessages():
		key=int(m.time//min_unit-time_start)
		try:
			stat[key]=stat[key]+1
		except KeyError:
			stat[key]=1
	return stat

# to analyze the relationship between the numbers of messages and each day of weeks
def analyze_week(msgs):
	CHECK_INV=60*60*24 # a day
	stat={}
	for m in msgs.getMessages():
		key=int(m.time//CHECK_INV%7)
		try:
			stat[key]=stat[key]+1
		except KeyError:
			stat[key]=1
	return stat

# to analyze the numbers of members' messages
def analyze_user(msgs):
	stat={}
	for msg in msgs.getMessages():
		try:
			stat[msg.qq]=stat[msg.qq]+1
		except KeyError:
			stat[msg.qq]=1
	return stat

def print_plain(out,dic):
	for (key, value) in stat.items():
		out.write("%d,%s\n"%(key,value))

def print_uv(out,dic,msgs):
	for (k,v) in dic.items():
		output.write("%d,%s,%s\n"%(v,msgs.user_qq_name[k],k))

def print_uv_sorted(out,dic,msgs):
	for (k,v) in ((k, dic[k]) for k in sorted(dic, key=dic.get, reverse=True)):
		output.write("%d,%s,%s\n"%(v,msgs.user_qq_name[k],k))

output=open("res.csv","w",encoding="utf-8")
print_uv_sorted(output,analyze_user(msgs),msgs)
output.close()
