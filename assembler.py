from collections import defaultdict
from random import randrange
import re
import sys
import pdb
opcode = defaultdict(dict)
newopcode = defaultdict(dict)

macrodict = defaultdict(dict)
code=[]
labels=[]
unmacrocode=[]
symboltable = defaultdict(dict)
mnemonics = defaultdict(dict)
loop = defaultdict(dict)

unmacrocode2=[]
macrodict2 = defaultdict(dict)
code2=[]
labels2=[]
symboltable2 = defaultdict(dict)
loop2 = defaultdict(dict)
mnemonics2 = defaultdict(dict)
externtable = []

def makeopcode(ddict,codefile):

	f = open(codefile,'r')
	for line in f:
		split=[]
		split = line.split(' ')
		##print split
		ddict[split[0]]['length']=split[-1].rstrip('\n')
		ddict[split[0]]['code']=split[-2]
		if len(split)==3:
			#this is 0 operand instructions
			ddict[split[0]]['operands']='null' 
		if len(split)==4:
			try:
				ddict[split[0]]['operands']='one'
				ddict[split[0]]['op1'].append(split[1])
			except:
				ddict[split[0]]['op1']=list()
				ddict[split[0]]['op1'].append(split[1])
		if len(split)==5:
			ddict[split[0]]['operands']='two'
			try:
				if split[1] not in ddict[split[0]]['op1']:
					ddict[split[0]]['op1'].append(split[1])
			except:
				ddict[split[0]]['op1']=list()
				ddict[split[0]]['op1'].append(split[1])
			try:
				if split[2] not in ddict[split[0]]['op2']:
					ddict[split[0]]['op2'].append(split[2])
			except:
				ddict[split[0]]['op2']=list()
				ddict[split[0]]['op2'].append(split[2])	
		if len(split)==6:
			ddict[split[0]]['operands']='three'
			try:
				if split[1] not in ddict[split[0]]['op1']:
					ddict[split[0]]['op1'].append(split[1])
			except:
				ddict[split[0]]['op1']=list()
				ddict[split[0]]['op1'].append(split[1])
			try:
				if split[2] not in ddict[split[0]]['op2']:
					ddict[split[0]]['op2'].append(split[2])
			except:
				ddict[split[0]]['op2']=list()
				ddict[split[0]]['op2'].append(split[2])	
			try:
				if split[3] not in ddict[split[0]]['op3']:
					ddict[split[0]]['op3'].append(split[3])
			except:
				ddict[split[0]]['op3']=list()
				ddict[split[0]]['op3'].append(split[3])	

def makenewopcode(newdict,codefile):
	f = open(codefile,'r')
	for line in f:
		split=[]
		split = line.split(' ')
		##print split
		newdict[split[0]]['length']=split[-1].rstrip('\n')
		newdict[split[0]]['code']=split[-2]
		if len(split)==3:
			#this is 0 operand instructions
			newdict[split[0]]['operands']='null' 
		if len(split)==4:
			try:
				newdict[split[0]]['operands']='one'
				newdict[split[0]]['op1'].append(split[1])
			except:
				newdict[split[0]]['op1']=list()
				newdict[split[0]]['op1'].append(split[1])
		if len(split)==5:
			newdict[split[0]]['operands']='two'
			try:
				if split[1] not in newdict[split[0]]['op1']:
					newdict[split[0]]['op1'].append(split[1])
			except:
				newdict[split[0]]['op1']=list()
				newdict[split[0]]['op1'].append(split[1])
			try:
				if split[2] not in newdict[split[0]]['op2']:
					newdict[split[0]]['op2'].append(split[2])
			except:
				newdict[split[0]]['op2']=list()
				newdict[split[0]]['op2'].append(split[2])
		if len(split)==6:
			newdict[split[0]]['operands']='three'
			try:
				if plit[1] not in newddict[split[0]]['op1']:
					newdict[split[0]]['op1'].append(split[1])
			except:
				newdict[split[0]]['op1']=list()
				newdict[split[0]]['op1'].append(split[1])
			try:
				if plit[2] not in newddict[split[0]]['op2']:
					newdict[split[0]]['op2'].append(split[2])
			except:
				newdict[split[0]]['op2']=list()
				newdict[split[0]]['op2'].append(split[2])	
			try:
				if plit[3] not in newddict[split[0]]['op3']:
					newdict[split[0]]['op3'].append(split[3])
			except:
				newdict[split[0]]['op3']=list()
				newdict[split[0]]['op3'].append(split[3])	


def writeline(arg):
	h.write(arg+'\n')

def loopwrite(*arg):
	for i in range(0,len(arg)):
		#print "in for loop"
		writeline(arg[i])

def get_code_labels(a,b,c):
	g = open(a,'r')
	for line in g:
		b.append(line.rstrip('\n'))
		m_obj = re.search(r"(\S*)(:)", line)
		if m_obj:
			c.append(m_obj.group(1))
	g.close()

def get_unmacrocode(list,a):
	g = open(a,'r')
	for line in g:
		list.append(line.rstrip('\n'))
	g.close()

def replace(*arg):
	#print "replacing"

	if len(arg)==1:
		#line,opcode
		if arg[0] == 'CCF':
			loopwrite('STC','CMC')
	if len(arg) == 2:
		if arg[0] == 'DOUBLE':
			loopwrite('LDA '+arg[1],'LXI H,'+arg[1],'MOV B,M','ADD B','STA '+arg[1])
		if arg[0] == 'NOT':
			loopwrite('PUSH PSW','LDA '+arg[1],'CMA','STA '+arg[1],'POP PSW')

	if len(arg) == 3:
		if arg[0]== 'SWAPM':
			loopwrite('PUSH H','PUSH B','PUSH PSW','LXI H,'+arg[1],'MOV B,M','LXI H,'+arg[2],'MOV C,M','MOV A,B','MOV B,C', 'MOV C,A','MOV L,B','SHLD '+arg[1],'MOV L,C','SHLD '+arg[2],'POP PSW','POP B','POP H')
		if arg[0]== 'SWAP':
			loopwrite('PUSH PSW','MOV A,'+arg[1],'MOV '+arg[1]+','+arg[2],'MOV '+arg[2]+',A','POP PSW')
		if arg[0] == 'MOVM':
			loopwrite('PUSH B','LXI H,'+arg[1],'MOV B,M','LXI H,'+arg[2],'MOV C,M','MOV M,B','LXI H,'+arg[1],'MOV M,C','POP B')
		if arg[0] == 'MUL':
			loopwrite('PUSH PSW','PUSH D','PUSH H','MVI D,00','MVI A,00','LXI H,'+arg[1],'MOV B,M','LXI H,'+arg[2],'MOV C,M','LOOP: ADD B','JNC NEXT','INR D','NEXT: DCR C','JNZ LOOP','MOV C,A','MOV B,D','POP H','POP D','POP PSW')
		if arg[0] == 'COMP':
			loopwrite('PUSH PSW','MOV A,'+arg[1],'CMP '+arg[2],'POP PSW')
	if len(arg) == 4:
		if arg[0]== 'RAND':
			#print arg
			loopwrite('MVI '+arg[1]+','+str(randrange(int(arg[2]),int(arg[3]))))


def convert(theunmacrocode,opcodedict,newopcodedict):
	c=0
	#print "converting"
	for line in theunmacrocode:
		iserror = True
		c += 1
		if line is not '':
			
			if line[0] == ';':
				writeline(line)
				continue
			####################
			if line.split()[0] == 'EXTERN':
				writeline(line)
			labOp = re.match( r'\s*(\S+): +(\S*)$',line, re.I)
			op = re.match(r'\s*(\S+)$',line,re.I)
			#print line,labOp,op

			if labOp:
				i=1
				onlyop = labOp
			if op:
				i=0
				onlyop = op

			if labOp or op:
				#print newopcodedict['RAND']
				if onlyop.group(i+1) in opcodedict:
					if opcodedict[onlyop.group(i+1)]['operands']=='null':
						writeline(line)
						continue
				#print line,newopcodedict[onlyop.group(i+1)]
				if onlyop.group(i+1) in newopcodedict:
					#print "new opcode dict"
					#print onlyop.group(i+1)
					if newopcodedict[onlyop.group(i+1)]['operands']=='null':
						if i==1:
							h.write(onlyop.group(1)+': ')
						replace(onlyop.group(i+1))
				
			#############################################################
			
			labOpOp1 = re.match( r'\s*(\S+): +(\S*) (\S*)$',line, re.I)
			opOp1 = re.match(r'\s*(\S+) +(\S+)$',line,re.I)
			if labOpOp1:
				i=1
				#print i
				oneop = labOpOp1
			if opOp1:
				i=0
				oneop = opOp1

			iserror = True

			if labOpOp1 or opOp1:
				##print oneop.group()
				if oneop.group(i+1) in opcodedict:
					#print oneop.group(i+2)
					if opcodedict[oneop.group(i+1)]['operands']=='one':
						if opcodedict[oneop.group(i+1)]['op1']==['Data']:
							iserror = False
						if opcodedict[oneop.group(i+1)]['op1']==['Address']:
							iserror = False
						#print labels,opcode[oneop.group(i+1)]['op1']
						if opcodedict[oneop.group(i+1)]['op1']==['Label']:
							iserror = False
								#print "yes"
						if oneop.group(i+2) in opcodedict[oneop.group(i+1)]['op1']:
							iserror = False

				if not iserror:
					#print line
					writeline(line)


				iserror = True
				if oneop.group(i+1) in newopcodedict and newopcodedict[oneop.group(i+1)]['operands']=='one':
					if newopcodedict[oneop.group(i+1)]['op1']==['Data']:
						iserror = False
					if newopcodedict[oneop.group(i+1)]['op1']==['Address']:
						iserror = False
					if newopcodedict[oneop.group(i+1)]['op1']==['Label']:
						iserror = False
					if oneop.group(i+2) in newopcodedict[oneop.group(i+1)]['op1']:
						iserror = False
				if not iserror:
					if i==1:
						h.write(oneop.group(1)+': ')
					replace(oneop.group(i+1),oneop.group(i+2))

					
	############0############################

			labOpOp1Op2 = re.match( r'\s*(\S+): +(\S*) (.*),(.*)',line, re.I)
			opOp1Op2 = re.match(r'\s*(\S+) +(\S+),+(\S+)$',line,re.I)
			iserror = True
			#print line,labOpOp1Op2,opOp1Op2
			if labOpOp1Op2:
				i=1
				twoop = labOpOp1Op2
			if opOp1Op2:
				i=0
				twoop = opOp1Op2
			#label opcodedict op1 op2
			if labOpOp1Op2 or opOp1Op2:
				#iserror = True
				if twoop.group(i+1) in opcodedict and opcodedict[twoop.group(i+1)]['operands']=='two':
					if opcodedict[twoop.group(i+1)]['op1']==['Data']:
						iserror = False
					if opcodedict[twoop.group(i+1)]['op1']==['Address']:
						iserror = False
					if opcodedict[twoop.group(i+1)]['op1']==['Label']:
						iserror = False
					if twoop.group(i+2) in opcodedict[twoop.group(i+1)]['op1']:
						iserror = False

					if opcodedict[twoop.group(i+1)]['op2']==['Data']:
						iserror = False
					if opcodedict[twoop.group(i+1)]['op2']==['Address']:
						iserror = False
					if opcodedict[twoop.group(i+1)]['op2']==['Label']:
						iserror = False
					if twoop.group(i+3) in opcodedict[twoop.group(i+1)]['op2']:
						iserror = False

				

				if not iserror:
					writeline(line)

				iserror = True

				if twoop.group(i+1) in newopcodedict and newopcodedict[twoop.group(i+1)]['operands']=='two':
					#print twoop.group()
					if newopcodedict[twoop.group(i+1)]['op1']==['Data']:
						iserror = False
					if newopcodedict[twoop.group(i+1)]['op1']==['Address']:
						iserror = False
					if newopcodedict[twoop.group(i+1)]['op1']==['Label']:
						iserror = False

					if twoop.group(i+2) in newopcodedict[twoop.group(i+1)]['op1']:
						iserror = False
					else:
						if twoop.group(i+1) == 'SWAP':
							#print twoop.group(i+2) 
							if twoop.group(i+2) not in ['B','C','D','E','H','L','M']:
								err = open('err','w')
								err.write('Error on line '+str(c)+'\n')
								err.close()
							if twoop.group(i+3) not in ['B','C','D','E','H','L','M']:
								err = open('err','w')
								err.write('Error on line '+str(c)+'\n')
								err.close()	
						if twoop.group(i+1) == 'COMP':
							if twoop.group(i+2) not in ['A','B','C','D','E','H','L','M']:
								err = open('err','a')
								err.write('Error on line '+str(c)+'\n')
								err.close()	





					if newopcodedict[twoop.group(i+1)]['op2']==['Data']:
						iserror = False
					if newopcodedict[twoop.group(i+1)]['op2']==['Address']:
						iserror = False
					if newopcodedict[twoop.group(i+1)]['op2']==['Label']:
						iserror = False
					if twoop.group(i+3) in newopcodedict[twoop.group(i+1)]['op2']:
						iserror = False
					
					if not iserror:
						if i == 1:
							h.write(twoop.group(1)+': ')
						replace(twoop.group(i+1),twoop.group(i+2),twoop.group(i+3))

					if iserror:
						print "Error in line "+str(c)
				
			####################################################
			labOpOp1Op2Op3 = re.match( r'\s*(\S+): +(\S*) (.*),(.*),(.*)$',line, re.I)
			opOp1Op2Op3 = re.match(r'\s*(\S+) +(\S+),+(\S+),+(\S+)$',line,re.I)
			#print line,labOpOp1Op2Op3,opOp1Op2Op3
			iserror = True
			if labOpOp1Op2Op3:
				i=1
				#print i
				threeop = labOpOp1Op2Op3
			if opOp1Op2:
				i=0
				threeop = opOp1Op2Op3
			#label opcodedict op1 op2 op3

			if labOpOp1Op2Op3 or opOp1Op2Op3:
				#iserror = True
				if threeop.group(i+1) in newopcodedict and newopcodedict[threeop.group(i+1)]['operands']=='three':
					if newopcodedict[threeop.group(i+1)]['op1']==['Data']:
						iserror = False
					if newopcodedict[threeop.group(i+1)]['op1']==['Address']:
						iserror = False
					if newopcodedict[threeop.group(i+1)]['op1']==['Label']:
						iserror = False
					if threeop.group(i+2) in newopcodedict[threeop.group(i+1)]['op1']:
						iserror = False

					if newopcodedict[threeop.group(i+1)]['op2']==['Data']:
						iserror = False
					if newopcodedict[threeop.group(i+1)]['op2']==['Address']:
						iserror = False
					if newopcodedict[threeop.group(i+1)]['op2']==['Label']:
						iserror = False
					if threeop.group(i+3) in newopcodedict[threeop.group(i+1)]['op2']:
						iserror = False


					if newopcodedict[threeop.group(i+1)]['op3']==['Data']:
						iserror = False
					if newopcodedict[threeop.group(i+1)]['op3']==['Address']:
						iserror = False
					if newopcodedict[threeop.group(i+1)]['op3']==['Label']:
						if threeop.group(i+4) in labels:
							iserror = False
					if threeop.group(i+4) in newopcodedict[threeop.group(i+1)]['op3']:
						iserror = False

					if not iserror:
						if i == 1:
							h.write(threeop.group(1)+': ')
						replace(threeop.group(i+1),threeop.group(i+2),threeop.group(i+3),threeop.group(i+4))
					if iserror:
						print "Error in line "+str(c)
				
	
def macro(thecode,themacrodict,loopdict):
	check = 0
	for line in thecode:
		# print line,check
		if line == 'MACRO':
			check = 1
			continue
		if line == 'LSTART':
			check = 5
			continue
		if check == 1:
			split = line.split()
			name = split[0]
			resplit = split[1].split(',')
			themacrodict[split[0]]['op'] = list()
			for word in resplit:
				themacrodict[split[0]]['op'].append(word)
			check = 2
			continue

		if check == 5:
			split = line.split()
			name = split[0]
			resplit = ['im1','im2','im3']
			themacrodict[split[0]]['op'] = list()
			for word in resplit:
				themacrodict[split[0]]['op'].append(word)
			
			themacrodict[name]['expansion'] = list()
			themacrodict[name]['expansion'].append('PUSH PSW')
			themacrodict[name]['expansion'].append('MVI A,im1')
			themacrodict[name]['expansion'].append('LIPO: NOP')

			check = 6
			continue

		if check == 2:
			if line!='MEND':
				try:
					themacrodict[name]['expansion'].append(line)
				except:	
					themacrodict[name]['expansion'] = list()
					themacrodict[name]['expansion'].append(line)
			
		#if check == 6:
		#	if line !='LEND':
		#		themacrodict[name]['expansion'].append(line)
		#	continue

		if line == 'MEND':
			check = 0
		if line == 'LEND':
			check = 0
			themacrodict[name]['expansion'].append('ADI im2')
			themacrodict[name]['expansion'].append('CPI im3')
			themacrodict[name]['expansion'].append('JC LIPO')
			themacrodict[name]['expansion'].append('POP PSW')

def expandmacro(a,b,themacrodict):
	print themacrodict
	c = 0
	define = False
	codefile = open(a,'r')
	expanded = open(b,'w')
	flag =2
	for line in codefile:
		if line is not '':
			if line == 'MACRO\n':
				flag = 1
				continue

			if line == 'LSTART\n':
				flag = 5
				continue

			if line == 'MEND\n':
				flag = 2
				continue
				
			if line == 'LEND\n':
				i = 3
				#print macrodict[name]
				while i<len(themacrodict[name]['expansion']): 
						lin = themacrodict[name]['expansion'][i]
						index = 0
						for ch in themacrodict[name]['op']:
							if ch in lin:
								lin = lin.replace(ch,actualops[index])
							index += 1
						expanded.write(lin+'\n')
						i += 1
				continue				
			
			if flag == 1:
				continue
			if flag == 5:
				loopstart = line
				if len(line.split())>1:
					name = line.split()[0]
					actualops = line.split()[1].split(',')
					#print actualops
					#print name
					#print "dict"
					#print themacrodict[name]
					i = 0
					while i<3: 
						lin = themacrodict[name]['expansion'][i]
						index = 0
						for ch in themacrodict[name]['op']:
							if ch in lin:
								lin = lin.replace(ch,actualops[index])
							index += 1
						expanded.write(lin+'\n')
						i += 1
					#pdb.set_trace()
					flag = 6
					continue

			#if flag ==6:
			#	expanded.write(line)
			labOp = re.match( r'\s*(\S+): +(\S*) +(\S*)$',line, re.I)
			op = re.match(r'\s*(\S+) +(\S*)$',line,re.I)
			##print line,labOp,op

			if labOp:
				s = labOp
				i = 1
			if op:
				i = 0
				s = op
				
			if op or labOp:
				
				if s.group(i+1) in themacrodict:
					##print s.group(i+1)
					##print s.group(i+2).split(',')
					#print "in macro if"
					#print s.group()
					length = len(themacrodict[s.group(i+1)]['expansion'])
					count = 0
					##print themacrodict[s.group(i+1)]['expansion']
					
					actualops = s.group(i+2).split(',')
					##print themacrodict[s.group(i+1)]['op']
					##print themacrodict[s.group(i+1)]['expansion']
					# in this above i need to replace the op's by those in split line
					index = 0
					for lin in themacrodict[s.group(i+1)]['expansion']:
						index = 0
						for ch in themacrodict[s.group(i+1)]['op']:
							if ch in lin:
								lin = lin.replace(ch,actualops[index])
							index += 1
						expanded.write(lin+'\n')
					
				else:
					expanded.write(line)
			else:
				expanded.write(line)
	codefile.close()
	expanded.close()


def pass1(a,symtab,opcodedict,mnemonicsdict,adrs):

		fo=open(a,'r')

		i=0
		lc=adrs
		j=0

		for line in fo:
			m_obj = re.search(r"(\S*)(:)", line)
			a_obj = re.search(r"(\S*)(\s*)(\S*)", line)
			
			if m_obj:
				symtab[m_obj.group(1)]['lc'] = lc
				i=i+1

			if a_obj:
				for line in opcodedict:
					if line == a_obj.group(1) or line == a_obj.group(3):
						#print line,mnemonicsdict
						mnemonicsdict[line]['address'] = lc
						mnemonicsdict[line]['opcode'] = opcodedict[line]['code']

						lc = lc + int(opcodedict[line]['length']) 
						j=j+1
		
				if a_obj.group(1) == "EXTERN"  :
					externtable.append(a_obj.group(3))		
		fo.close()
		#print mnemonicsdict

def merge():
	writer = open(str(sys.argv[1])+str(sys.argv[2])+'_merged.asm','w')
	with open(str(sys.argv[1])+'_pass2.asm') as f:
	    content = f.readlines()
	with open(str(sys.argv[2])+'_pass2.asm') as f:
	    content2 = f.readlines()
	for item in content:
		writer.write(item)
	for item in content2:
		if item !='HLT\n':
			writer.write(item)
		if item == 'HLT\n':
			writer.write('RET\n')

def pass2(a,b,symtab,adrs):
	new = open(a,'r')
	fileContent = new.readlines()
	new.close()
	final = open(b,'w')
	#print symtab
	for i in range(0,len(fileContent)):

		for x in symtab:
				if re.search("\\b"+x+":"+"\s",fileContent[i]):
					#fileContent[i] = re.sub("\\b"+x+":",str(symboltable[x]['lc']),fileContent[i])
					fileContent[i] = re.sub("\\b"+x+":"+"\s","",fileContent[i])
				if re.search("\\b"+x+"\\b",fileContent[i]):
					fileContent[i] = re.sub("\\b"+x+"\\b",str(symtab[x]['lc']),fileContent[i])
					
	for x in fileContent:
		#print x
		final.write(x)

trial = open('err','w')
trial.close()

makeopcode(opcode,'opcode')
makenewopcode(newopcode,'newopcode')
#print "new"
#print newopcode['RAND']
get_code_labels(str(sys.argv[1]),code,labels)
macro(code,macrodict,loop)
#print mnemonics
expandmacro(str(sys.argv[1]),str(sys.argv[1])+'_macroexpanded.asm',macrodict)
get_unmacrocode(unmacrocode,str(sys.argv[1])+'_macroexpanded.asm')

h = open(str(sys.argv[1])+'_prepass.asm','w')
convert(unmacrocode,opcode,newopcode)
h.close()

#print len(sys.argv)

if len(sys.argv) == 3:
	y1=0
	y2=0

if len(sys.argv) == 4:
	y1 = int(sys.argv[3])
	y2 = 0

if len(sys.argv) == 5:
	y1 = int(sys.argv[3])
	y2 = int(sys.argv[4])

pass1(str(sys.argv[1])+'_prepass.asm',symboltable,opcode,mnemonics,y1)
print symboltable
pass2(str(sys.argv[1])+'_prepass.asm',str(sys.argv[1])+'_pass2.asm',symboltable,y1)

if sys.argv[2] != 'NONE' and sys.argv[2] != 'none':

	get_code_labels(str(sys.argv[2]),code2,labels2)
	macro(code2,macrodict2,loop2)

	expandmacro(str(sys.argv[2]),str(sys.argv[2])+'_macroexpanded.asm',macrodict2)
	get_unmacrocode(unmacrocode2,str(sys.argv[2])+'_macroexpanded.asm')

	h = open(str(sys.argv[2])+'_prepass.asm','w')
	convert(unmacrocode2,opcode,newopcode)
	h.close()

	pass1(str(sys.argv[2])+'_prepass.asm',symboltable2,opcode,mnemonics2,y2)
	pass2(str(sys.argv[2])+'_prepass.asm',str(sys.argv[2])+'_pass2.asm',symboltable2,y2)

	for line in symboltable2:
		if len(sys.argv) < 5:
			symboltable2[line]['lc'] = symboltable2[line]['lc'] + mnemonics['HLT']['address']

	pass2(str(sys.argv[2])+'_prepass.asm',str(sys.argv[2])+'_pass2.asm',symboltable2,y2)
	merge()

	merged = open(str(sys.argv[1])+str(sys.argv[2])+'_merged.asm','r')
	fileContent = merged.readlines()
	merged.close()
	final = open(str(sys.argv[1])+str(sys.argv[2])+'_output.asm','w')
	#print symtab
	for i in range(0,len(fileContent)):

		if re.search("EXTERN"+"\s"+"\S*",fileContent[i]):
			fileContent[i] = re.sub("EXTERN"+"\s"+"\S*","",fileContent[i])
				
		for x in externtable:
			if re.search("\\b"+x+"\\b",fileContent[i]):
				fileContent[i] = re.sub("\\b"+x+"\\b",str(symboltable2[x]['lc']),fileContent[i])

	for x in fileContent:
		final.write(x)

