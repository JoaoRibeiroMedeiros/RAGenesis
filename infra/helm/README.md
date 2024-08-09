### Pointing to Vultr
Check if you are pointin to the right cluster
kubectl config get-contexts

### Decoding the config for github action
cat ~/.kube/config | base64 | pbcopy

### check the repo config
Go to the VUltr repo container regitry and copy .dockerconfigjson from  Docker Credentials For Kubernetespage tab

### Install Ingress
- make ingress 
or
- helm install ingress-nginx ingress-nginx/ingress-nginx --namespace ingress-nginx --create-namespace

### Install Cert-manager
- kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.12.1/cert-manager.yaml
- kubectl apply -f cert-issuer.yaml
- kubectl get certificaterequests -A

### Install the Helm Chart:
- make apidev
- make cleandev



