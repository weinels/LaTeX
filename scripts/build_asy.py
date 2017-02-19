import pathlib
import hashlib
import sys
import subprocess
import multiprocessing
import os
import re

def natural_sort_key(s, _nsre=re.compile('([0-9]+)')):
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(_nsre, s)] 

BLOCKSIZE = 65536

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

def write_hashes(path, files):
	with open(path, 'w') as f:
		for fn, h in files.items():
			f.write("{file}\t{hash}\n".format(file=fn, hash=h))

def run_asy(path):
	output = subprocess.run(['asy', '-q', path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf-8")
	if output.stdout != "":
		return "{0}:\n{1}".format(pathlib.Path(path).name, output.stdout)

	return ""
			
if __name__ == "__main__":
	p = pathlib.Path(".")

	hash_file = "asy.hashes"
	
	files = {}

	# loop over all asymptote files in the directory
	for fp in p.glob("*.asy"):
		# hash the file
		h = hashlib.md5()
		with fp.open('br') as f:
			while True:
				buffer = f.read(BLOCKSIZE)

				if len(buffer) == 0:
					break
					
				h.update(buffer)

		# add file to dict
		hash = h.hexdigest()
		files[str(fp.resolve())] = hash

	# if there were not asymptote files, then exit
	if len(files) == 0:
		print("No Asymptote files found.")
		sys.exit(0)

	# load the previous hashes
	old_hashes = load_hashes(hash_file)

	# to track changed and unchaged files
	new = []

	# Not the most efficent way, but the output is nicer to read
	keys = list(files.keys())
	keys.sort(key=natural_sort_key)
	
	for f in keys:
		fn = pathlib.Path(f).name
		h = files[f]
#		print("{0} :: {1}".format(fn,h))
		# seperate the files into changed and unchanged
		if f in old_hashes:
#			print("{0} ?? {1}".format(h,old_hashes[fn]))
			if h == old_hashes[f]:
				print("Unchanged: {0}".format(fn))
			else:
				print("  Changed: {0}".format(fn))
				new.append(f)
		else:
			print("      New: {0}".format(fn))
			new.append(f)

	# process the changed files
	output = []

	if len(new) == 1:
		print("Processing 1 file... ", end='', flush=True)
	else:
		print("Processing {0} files... ".format(len(new)), end='', flush=True)

	if len(new) <= 1 or os.cpu_count() == 1:
		# with only one item, no need to build a worker pool
		for f in new:
			output.append(run_asy(f))

	else:

		print("Using {0} subprocesses... ".format(os.cpu_count()), end='', flush=True)
		# create the pool
		with multiprocessing.Pool(os.cpu_count()) as pool:

			# set the pool to work on the changed files
			output = pool.map(run_asy, new)

	print("Done.")

	must_exit = False
	for r in output:
		if len(r) > 0:
			print(r)
			must_exit = True

	if must_exit:
		sys.exit(1)
	else:
		write_hashes(hash_file, files)
