

run: setup
	#podman-compose up			# podman has better support for volume export/backup etc
	docker-compose up

setup: venv

venv:
	python3 -m venv venv
	. ./activate && pip install -r requirements.txt
	#. ./activate && pip install -e src/python/nsdf-data-catalog




backup-volumes:
	# ensure backup directory
	mkdir ./backup

	# TODO: ensure containers using volumes in question are stopped
	#podman-compose down
	
	# run temporary container
	


restore-volumes:

