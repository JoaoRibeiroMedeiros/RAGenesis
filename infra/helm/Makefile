# Makefile for Helm deployments

CHART_PATH_API = ./api
RELEASE_NAME = ragenesis-api
NAMESPACE=ragenesis

.PHONY: all apidev apiqa apiprod

all: apidev apiqa apiprod ingress

ingress:
	helm install ingress-nginx ingress-nginx/ingress-nginx --namespace ingress-nginx --create-namespace

apidev:
	helm upgrade --install $(RELEASE_NAME)-dev $(CHART_PATH_API) -f $(CHART_PATH_API)/values-dev.yaml --namespace $(NAMESPACE)-dev --create-namespace

apiqa:
	helm upgrade --install $(RELEASE_NAME)-qa $(CHART_PATH_API) -f $(CHART_PATH_API)/values-qa.yaml --namespace $(NAMESPACE)-qa --create-namespace

apiprod:
	helm upgrade --install $(RELEASE_NAME)-prod $(CHART_PATH_API) -f $(CHART_PATH_API)/values-prod.yaml --namespace $(NAMESPACE)-prod --create-namespace

cleandev:
	 kubectl delete namespace <namespace …>

cleanqa:
	helm uninstall $(RELEASE_NAME)-qa

cleanprod:
	helm uninstall $(RELEASE_NAME)-prod

clean: clean-dev clean-qa clean-prod
