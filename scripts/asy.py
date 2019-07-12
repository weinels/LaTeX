import pathlib
import hashlib
import subprocess
import multiprocessing
import os
import re
import sys

# key for performing a natural sort
def natural_sort_key(s, _nsre=re.compile('([0-9]+)')):
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(_nsre, s)] 

# exception to handle asymptote errors
class AsyError(Exception):
	def __init__(self, path="", stdout="", stderr=""):
		self.path = path
		self.file = pathlib.Path(path).name
		self.stdout = stdout
		self.stderr = stderr
	    	    
BLOCKSIZE = 65536

# build a hash for every file in the passed path
def load_hashes(path):
	hashes = {}
	try:
		with open(path, 'r') as f:
			for line in f:
				# split the line
				item = line.strip().split('\t')
				# only add the file to the dict if the corresponding pdf is still there
				p = pathlib.Path(item[0][:-4] + "_0.pdf")
				if p.exists():
					hashes[item[0]] = item[1]
	except FileNotFoundError:
		return {}

	return hashes

# write out the hashes
def write_hashes(path, files):
	with open(path, 'w') as f:
		for fn, h in files.items():
			f.write("{file}\t{hash}\n".format(file=fn, hash=h))

# run asy on a given file
def run_asy(path):
	output = subprocess.run(['asy', '-q', str(path)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf-8")

	# since asy doesn't respect return codes for stderr, we have to assume that any output means an error.
	if len(output.stdout) > 0:
		raise AsyError(str(path), output.stdout)
		
	return [path, output.stdout]

# run asy on all valid files in path, will return the number of files processed
def process(files_path, hashes_path, verbose=True):
	p = pathlib.Path(files_path)
	
	files = {}

	# loop over all asymptote files in the directory
	for fp in p.glob("*.asy"):
		# hash the file
		h = hashlib.md5()

		# read the file in as binary
		with fp.open('br') as f:
			while True:
				buffer = f.read(BLOCKSIZE)

				if len(buffer) == 0:
					break
					
				h.update(buffer)

		# add hash to dict
		hash = h.hexdigest()
		files[str(fp.resolve())] = hash

	# if there were not asymptote files, then exit
	if len(files) == 0:
		return 0

	# load the previous hashes
	old_hashes = load_hashes(hashes_path)

	# to track changed and unchaged files
	new = []

	# Not the most efficent way, but the output is nicer to read
	keys = list(files.keys())
	keys.sort(key=natural_sort_key)
	
	for f in keys:
		fn = pathlib.Path(f).name
		h = files[f]
		# seperate the files into changed and unchanged
		if f in old_hashes:
			if h == old_hashes[f]:
				if verbose:
					print("Unchanged: {0}".format(fn))
			else:
				if verbose:
					print("  Changed: {0}".format(fn))
				new.append(f)
		else:
			if verbose:
				print("      New: {0}".format(fn))
			new.append(f)

	# process the changed files
	output = []

	if verbose:
		if len(new) == 1:
			print("Processing 1 file... ", end='', flush=True)
		else:
			print("Processing {0} files... ".format(len(new)), end='', flush=True)

	if len(new) <= 1 or os.cpu_count() == 1:
		# with only one item, no need to build a worker pool
		for f in new:
			output.append(run_asy(f))

	else:
		if verbose:
			print("Using {0} subprocesses... ".format(os.cpu_count()), end='', flush=True)
			
		# create the pool
		with multiprocessing.Pool(os.cpu_count()) as pool:

			# set the pool to work on the changed files
			output = pool.map(run_asy, new)

	if verbose:
		print("Done.")
	
	# update the hash file
	write_hashes(hashes_path, files)

	return len(new)

# if this file is ran, then it will just process all .asy files in the current directory
if __name__ == "__main__":
	try:
		process(".", "asy.hashes")
		sys.exit(0)
	except AsyError as e:
		if "Cannot write to texput.log" not in e.stdout:
			print("\nError in {0}:\n{1}".format(e.file, e.stdout))
			sys.exit(1)
