#!/usr/bin/env python

from __future__ import print_function
import re
from optparse import OptionParser
import sys
import os
import os.path

def ShiftFreqAnalyse(ksize, seq):
	dictKmer = {}

	kmerRegExp = '(.{' + str(ksize) + '})' 
	kmerRe = re.compile(kmerRegExp)
	for k in range(ksize):
		kmers = kmerRe.findall(seq[k:])
		for kmer in kmers:
			if(kmer in dictKmer):
				dictKmer[kmer][k] += 1
			else:
				dictKmer[kmer] = [0] * ksize

	return dictKmer

def WriteKmerDict(dictKmer, outFile):
	for kmer in dictKmer:
		outFile.write("%s,%s\n" % (kmer, ','.join(map(str, dictKmer[kmer]))))

def main():

	# parse the command line options

	usage = 'usage: %prog [options] seqFile.fa KSIZE'
	parser = OptionParser(usage=usage, version='%prog 0.1.0')

	(options, args) = parser.parse_args()
	if(len(args) != 2):
		parser.print_help()
		sys.exit(0)

	seqFileName = args[0]
	ksize = int(args[1])

	if(not os.path.exists(seqFileName)):
		print('error: sequence file "', seqFileName, '"', ' doest not exist.')
		sys.exit(-1)

	dictSeq = {}
	with open(seqFileName, 'r') as seqFile :
		chrname = ''
		seq = ''
		for line in seqFile:
			if(line[0] == '>'):
				
				# save current seq for current chr

				if(chrname != ''):
					dictSeq[chrname] = seq
				
				# new chrname & seq

				chrname = line[1:].strip()
				seq = ''
				print('    loading sequence: ' + chrname)
			else:
				seq += line.strip().upper()
		
		# write the last chr

		if(chrname != ''):
			dictSeq[chrname] = seq
	seqFile.close()

	for chrname in dictSeq:
		outFile = open(chrname, 'w')
		dictKmer = ShiftFreqAnalyse(ksize, dictSeq[chrname])
		WriteKmerDict(dictKmer, outFile)

if __name__ == '__main__':
	main()