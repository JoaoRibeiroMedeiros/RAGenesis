# Makefile for Helm deployments

CHART_PATH_API = ./gendoc-api
RELEASE_NAME = gendoc-api

.PHONY: all apidev apiqa apiprod

all: apidev apiqa apiprod

apidev:
	helm upgrade --install $(RELEASE_NAME)-dev $(CHART_PATH_API) -f $(CHART_PATH_API)/values-dev.yaml --namespace gendoc-dev --create-namespace

apiqa:
	helm upgrade --install $(RELEASE_NAME)-qa $(CHART_PATH_API) -f $(CHART_PATH_API)/values-qa.yaml --namespace gendoc-dev --create-namespace

apiprod:
	helm upgrade --install $(RELEASE_NAME)-prod $(CHART_PATH_API) -f $(CHART_PATH_API)/values-prod.yaml --namespace gendoc-dev --create-namespace

clean-dev:
	helm uninstall gendoc-api-dev

clean-qa:
	helm uninstall gendoc-api-qa

clean-prod:
	helm uninstall gendoc-api-prod

clean: clean-dev clean-qa clean-prod
