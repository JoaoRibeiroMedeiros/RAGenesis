### Install Ingress
- helm install ingress-nginx ingress-nginx/ingress-nginx --namespace ingress-nginx --create-namespace

### Install Cert-manager
- kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.12.1/cert-manager.yaml
- kubectl apply -f cert-issuer.yaml
- kubectl get certificaterequests -A

### Install Prometheus Stack
- helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
- helm repo update
- helm install prometheus prometheus-community/prometheus --namespace monitoring --create-namespace
- helm uninstall prometheus prometheus-community/prometheus --namespace monitoring

#### fix default storage / pvc issue (min 40GB)
- kubectl delete pvc prometheus-server -n monitoring
- helm upgrade prometheus prometheus-community/prometheus -f values.yml -monitoring
- kubectl expose service prometheus-server --type=NodePort --target-port=9090 --name=prometheus-server-ext -n monitoring

- helm uninstall prometheus prometheus-community/prometheus --namespace monitoring

- helm repo add grafana https://grafana.github.io/helm-charts 
- helm repo update

### Install the Helm Chart:
- helm upgrade --install gendocapi ./gendoc-api -f ./gendoc-api/values-dev.yaml --namespace gendoc-dev --create-namespace
- helm uninstall gendocapi ./gendoc-api/ --namespace gendoc-prod

### Upgrade the Helm Chart:
- helm upgrade gendoc-api ./gendoc-api --namespace gendoc-prod

### Decoding the config for github action
cat ~/.kube/config | base64 | pbcopy


