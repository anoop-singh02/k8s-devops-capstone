# Local development loop. Requires: docker, kind, kubectl.
CLUSTER := capstone

.PHONY: test build kind-up deploy-local logs kind-down

test:
	cd app/api && pytest -v

build:
	docker build -t capstone-api:dev app/api
	docker build -t capstone-frontend:dev app/frontend

kind-up:
	kind create cluster --config kind/cluster.yaml

deploy-local: build
	kind load docker-image capstone-api:dev capstone-frontend:dev --name $(CLUSTER)
	kubectl apply -k k8s/overlays/local
	kubectl -n capstone rollout status deployment/api --timeout=120s
	kubectl -n capstone rollout status deployment/frontend --timeout=120s
	@echo "App is up: http://localhost:8080"

logs:
	kubectl -n capstone logs -l app=api --tail=50 -f

kind-down:
	kind delete cluster --name $(CLUSTER)
