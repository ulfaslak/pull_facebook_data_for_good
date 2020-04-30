CREDS := ~/.creds/fb.json # credentials
DATASETS := datasets.csv #Target datasets
OUTDIR := ~/somewhere_meaningful #output directory

pull:	
	python pull.py ${CREDS} ${DATASETS} ${OUTDIR}