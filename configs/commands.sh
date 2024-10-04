kubectl apply -f deployment.yaml


kubectl apply -f service.yaml

kubectl get pods
kubectl get service

kubectl logs pods -c container_name -- command

#this would launch interactive logs
kubectl logs   -f pod_name

kubectl exec -it pod_name -- /bin/bash

kubectl delete  deployment deployment_name
kubectl delete service service_name
