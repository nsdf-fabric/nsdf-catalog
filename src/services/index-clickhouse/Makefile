


run: docker-run


debug:
	docker exec -it $(shell docker ps -aqf "name=nsdf_catalog_index") bash



docker-run: docker-build
	docker-compose up

podman-run: podman-build
	# https://hub.docker.com/r/yandex/clickhouse-server
	# Container exposes 8123 port for HTTP interface and 9000 port for native client.
	podman run -p 


docker-build:
	docker build -t nsdf_catalog_index .

podman-build:
	podman build -f ./Dockerfile

