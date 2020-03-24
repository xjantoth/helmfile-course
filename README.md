
# Content
  - [Creating a helm chart with 2 child helm chart helm v3](#creating-a-helm-chart-with-2-child-helm-chart-helm-v3)
  - [Check you helmchart repositories](#check-you-helmchart-repositories)
  - [List content of your main-helmchart](#list-content-of-your-main-helmchart)
  - [Helm v3 dependency update](#helm-v3-dependency-update)
  - [Check the content of charts/ folder in main-helmchart/](#check-the-content-of-charts/-folder-in-main-helmchart/)
  - [Check what is going to be installed](#check-what-is-going-to-be-installed)

#### Creating a helm chart with 2 child helm chart helm v3

```bash
helm3 create main-helmchart
```

Edit this file `main-helmchart/Chart.yaml` and append following line at the very end 

```bash
cat <<'EOF' >> main-helmchart/Chart.yaml

dependencies:
- name: nginx-ingress
  version: "1.34.2"
  repository: "https://kubernetes-charts.storage.googleapis.com"
  tags:
    - nginx-ingress
    - front-end
  condition: nginx-ingress.enabled, global.nginx-ingress.enabled

- name: memcached
  version: "3.2.3"
  repository: "https://kubernetes-charts.storage.googleapis.com"
  tags:
    - memcached
    - cache
  condition: memcached.enabled, global.memcached.enabled

EOF

cat <<'EOF' >> main-helmchart/values.yaml

nginx-ingress:
  enabled: false

memcached:
  enabled: false

EOF
```

#### Check you helmchart repositories
```bash
helm3 repo list
NAME      	URL                                               
stable    	https://kubernetes-charts.storage.googleapis.com  
hc-v3-repo	https://xjantoth.github.io/microservice/hc-v3-repo
```

#### List content of your main-helmchart
```bash
tree -L 2  main-helmchart/
main-helmchart/
├── charts
├── Chart.yaml
├── templates
│   ├── deployment.yaml
│   ├── _helpers.tpl
│   ├── ingress.yaml
│   ├── NOTES.txt
│   ├── serviceaccount.yaml
│   ├── service.yaml
│   └── tests
└── values.yaml

3 directories, 8 files
```

#### Helm v3 dependency update

```bash
cd main-helmchart && helm3 dependency update
Hang tight while we grab the latest from your chart repositories...
...Successfully got an update from the "hc-v3-repo" chart repository
...Successfully got an update from the "stable" chart repository
Update Complete. ⎈Happy Helming!⎈
Saving 2 charts
Downloading nginx-ingress from repo https://kubernetes-charts.storage.googleapis.com
Downloading memcached from repo https://kubernetes-charts.storage.googleapis.com
Deleting outdated charts

```

#### Check the content of charts/ folder in main-helmchart/

Please **notice** two new files within `charts/` folder: 

* _charts/memcached-3.2.3.tgz_
* _charts/nginx-ingress-1.34.2.tgz_

```bash
tree -L 2  .
.
├── Chart.lock
├── charts
│   ├── memcached-3.2.3.tgz
│   └── nginx-ingress-1.34.2.tgz
├── Chart.yaml
├── templates
│   ├── deployment.yaml
│   ├── _helpers.tpl
│   ├── ingress.yaml
│   ├── NOTES.txt
│   ├── serviceaccount.yaml
│   ├── service.yaml
│   └── tests
└── values.yaml

3 directories, 11 files
```


#### Check what is going to be installed

There is no `memcached` nor `nginx-ingress` controller to be installed because it has been 
disabled within `main-helmchart/values.yaml` at the very end of this file.

```bash
tail main-helmchart/values.yaml 

...
nginx-ingress:
  enabled: false

memcached:
  enabled: false
...
```

```bash
helm3 template  name-of-my-deployment .

---
# Source: main-helmchart/templates/serviceaccount.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: name-of-my-deployment-main-helmchart
  labels:
    helm.sh/chart: main-helmchart-0.1.0
    app.kubernetes.io/name: main-helmchart
    app.kubernetes.io/instance: name-of-my-deployment
    app.kubernetes.io/version: "1.16.0"
    app.kubernetes.io/managed-by: Helm
---
# Source: main-helmchart/templates/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: name-of-my-deployment-main-helmchart
  labels:
    helm.sh/chart: main-helmchart-0.1.0
    app.kubernetes.io/name: main-helmchart
    app.kubernetes.io/instance: name-of-my-deployment
    app.kubernetes.io/version: "1.16.0"
    app.kubernetes.io/managed-by: Helm
spec:
  type: ClusterIP
  ports:
    - port: 80
      targetPort: http
      protocol: TCP
      name: http
  selector:
    app.kubernetes.io/name: main-helmchart
    app.kubernetes.io/instance: name-of-my-deployment
---
# Source: main-helmchart/templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: name-of-my-deployment-main-helmchart
  labels:
    helm.sh/chart: main-helmchart-0.1.0
    app.kubernetes.io/name: main-helmchart
    app.kubernetes.io/instance: name-of-my-deployment
    app.kubernetes.io/version: "1.16.0"
    app.kubernetes.io/managed-by: Helm
spec:
  replicas: 1
  selector:
    matchLabels:
      app.kubernetes.io/name: main-helmchart
      app.kubernetes.io/instance: name-of-my-deployment
  template:
    metadata:
      labels:
        app.kubernetes.io/name: main-helmchart
        app.kubernetes.io/instance: name-of-my-deployment
    spec:
      serviceAccountName: name-of-my-deployment-main-helmchart
      securityContext:
        {}
      containers:
        - name: main-helmchart
          securityContext:
            {}
          image: "nginx:1.16.0"
          imagePullPolicy: IfNotPresent
          ports:
            - name: http
              containerPort: 80
              protocol: TCP
          livenessProbe:
            httpGet:
              path: /
              port: http
          readinessProbe:
            httpGet:
              path: /
              port: http
          resources:
            {}
---
# Source: main-helmchart/templates/tests/test-connection.yaml
apiVersion: v1
kind: Pod
metadata:
  name: "name-of-my-deployment-main-helmchart-test-connection"
  labels:
    helm.sh/chart: main-helmchart-0.1.0
    app.kubernetes.io/name: main-helmchart
    app.kubernetes.io/instance: name-of-my-deployment
    app.kubernetes.io/version: "1.16.0"
    app.kubernetes.io/managed-by: Helm
  annotations:
    "helm.sh/hook": test-success
spec:
  containers:
    - name: wget
      image: busybox
      command: ['wget']
      args: ['name-of-my-deployment-main-helmchart:80']
  restartPolicy: Never


```

Link to reference https://gist.github.com/fvcproductions/1bfc2d4aecb01a834b46