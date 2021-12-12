import json
from os import path



slovar = {-10:'A',-4:'B',-3:'C',-2:'D',-1:'E',1:'F',2:'G',3:'H',4:'I',5:'J',
		  6:'K',7:'L',8:'M',9:'F',10:'G',11:'H',12:'I',13:'J',14:'K',15:'L',
		  16:'M',17:'N',18:'O',19:'P',20:'Q',21:'R',22:'S',23:'T',24:'U',25:'N',
		  26:'O',27:'P',28:'Q',29:'V',30:'W',31:'X',32:'Y'}

slovar2 = {
	'A': ('H', (640, 0, 160, 160)),
	'B': ('N', (480, 0, 160, 160)),'C': ('N', (320, 0, 160, 160)),'D': ('N', (0, 0, 160, 160)),
	'E': ('N', (160, 0, 160, 160)),'F': ('W', (160, 480, 160, 160)),'G': ('W', (640, 480, 160, 160)),
	'H': ('W', (160, 0, 160, 160)),'I': ('W', (640, 0, 160, 160)),'J': ('W', (320, 480, 160, 160)),
	'K': ('W', (480, 480, 160, 160)),'L': ('W', (320, 0, 160, 160)),'M': ('W', (480, 0, 160, 160)),
	'N': ('W', (160, 320, 160, 160)),'O': ('W', (640, 320, 160, 160)),'P': ('W', (160, 160, 160, 160)),
	'Q': ('W', (640, 160, 160, 160)),'R': ('W', (640, 640, 160, 160)),'S': ('W', (480, 640, 160, 160)),
	'T': ('W', (320, 640, 160, 160)),'U': ('W', (160, 640, 160, 160)),'V': ('W', (320, 320, 160, 160)),
	'W': ('W', (480, 320, 160, 160)),'X': ('W', (320, 160, 160, 160)),'Y': ('W', (480, 160, 160, 160))
}

def redo_chunk(chunk_name):
	"""file->file"""
	with open(path.join('resources', 'chunks', chunk_name + '_refactored.txt'), 'w') as f:
		dump = open(path.join('resources', 'chunks', chunk_name), 'r').readlines()
		for y, line in enumerate(dump):
			for x, sym in enumerate(line.strip()):
				if sym == '.':
					ID = -1
					if dump[y][x-1] != '.': ID-= 1
					if dump[y][x+1] != '.': ID-= 2
				elif sym == 'H':
					ID = -10
				elif sym == 'W':
					ID = 1
					if y!=0 and dump[y-1][x] == '#': ID+= 1
					if x!=len(line)-1 and dump[y][x+1] == '#': ID+= 2
					if y!=len(dump)-1 and dump[y+1][x] == '#': ID+= 4
					if y!=len(dump)-1 and dump[y+1][x-1] == '#': ID+= 8
					if x!=0 and dump[y][x-1] == '#': ID+= 16
				Letter = slovar[ID]
				f.write(Letter)
			f.write('\n')

if __name__ == '__main__':
	chunk_name = input()
	redo_chunk(chunk_name)
