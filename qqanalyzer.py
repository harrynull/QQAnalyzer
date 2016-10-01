import os
import sys
import re

class message:
	time=""
	name=""
	qq=""
	content=[]
	def __init__(self):
		self.time=""
		self.name=""
		self.qq=""
		self.content=[]

class messages:
	name=""
	msgs=[]
	def __init__(self, file_content):
		# define some constants, use the array index
		GROUP_NAME_LINE=5
		START_LINE=8

		# init
		name_re=re.compile(r"(.*? .*?) (.*)\((.*?)\)")

		# get the group name in the 5th line
		self.name=(lambda line:line[line.index(":")+1:])(file_content[GROUP_NAME_LINE])

		for line in file_content[8:]:
			res=name_re.findall(line)
			if res:
				# remove the blank element and add to the array
				try: msg.content=msg.content[:-1]; self.msgs.append(msg);
				except NameError: pass

				# create the next message
				msg=message()
				msg.time, msg.name, msg.qq=list(res[0])
			else:
				# add to char content array
				msg.content.append(line.replace("\n",""))

		return

data = open(sys.argv[1],encoding="utf-8")
msg = messages(data.readlines())
for msg in msg.msgs:
	print("%s %s %s\n%s\n"%(msg.time,msg.name,msg.qq,msg.content))
data.close()
