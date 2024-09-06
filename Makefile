



build:
	@echo "Building dockers"
	docker build -t ttl.sh/imageserver:latest -f services/imageserver/dockerfiles/Dockerfile --target=production services/imageserver
	docker push ttl.sh/imageserver:latest
	docker build -t ttl.sh/processingserver:latest -f services/processingserver/dockerfiles/Dockerfile --target=production services/processingserver
	docker push ttl.sh/processingserver:latest

run_compose:
	@echo "Running docker-compose"
	docker-compose down && docker-compose -f docker-compose.yml up

test_status:
	@echo "Running tests"
	curl -X GET http://localhost:8080/v0/status
	curl -X GET http://localhost:8081/v0/status

helm_update:
	@echo "Update deps"
	helm repo add bitnami https://charts.bitnami.com/bitnami
	helm dependencies update chart

helm_deploy:
	@echo "Deploying helm"
	helm upgrade --install my-release chart

helm_uninstall:
	@echo "Uninstall helm chart"
	helm uninstall my-release