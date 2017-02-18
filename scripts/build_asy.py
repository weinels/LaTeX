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
				item = line.strip().split(' ')

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
			f.write("{file} {hash}\n".format(file=fn, hash=h))

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
	old = []
	new = []

	for fn, h in files.items():
		# seperate the files into changed and unchanged
		if fn in old_hashes:
			if h == old_hashes[fn]:
				old.append(fn)
			else:
				new.append(fn)
		else:
			new.append(fn)

	# sort lists
	old.sort(key=natural_sort_key)
	new.sort(key=natural_sort_key)
			
	# list the unchanged files
	if len(old) > 0:
		print("Unchanged:")
		for fn in old:
			print(pathlib.Path(fn).name)

	# process the changed files
	if len(new) > 0:
		print("Processing... ", end='', flush=False)

		if len(new) == 1:
			# with only one item, no need to build a worker pool
			run_asy(new[0])

		else:
			# create the pool
			with multiprocessing.Pool(os.cpu_count()) as pool:

				# set the pool to work on the changed files
				res = pool.map(run_asy, new)

		print("Done.")

		must_exit = False
		for r in res:
			if len(r) > 0:
				print(r)
				must_exit = True

		if must_exit:
			sys.exit(1)
		else:
			write_hashes(hash_file, files)
