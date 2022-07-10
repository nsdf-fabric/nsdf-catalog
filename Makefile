.PHONY: dependencies




run: setup
	#podman-compose up			# podman has better support for volume export/backup etc
	docker-compose up


setup: venv dependencies

venv:
	python3 -m venv venv

dependencies:
	# ensure submodule dependencies
	git submodule init
	git submodule update
	ls ./dependencies

	# python dependencies
	. ./activate && pip install -r requirements.txt

	# install bundled/submodule python dependencies
	. ./activate && cd ./dependencies/nsdf-software-stack && pip install -e .


secret:
	openssl rand -hex 32



reset_db:
	sudo rm -rf data/rest_endpoint_db_data/
	mkdir -p data/rest_endpoint_db_data


backup-volumes:
	# ensure backup directory
	mkdir ./backup

	# TODO: ensure containers using volumes in question are stopped
	#podman-compose down
	
	# run temporary container


restore-volumes:
	# still decide on podman vs docker
	@echo "Not implemented"






distclean:
	docker-compose rm
	rm -rf venv
