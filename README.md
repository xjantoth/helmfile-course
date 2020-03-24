
- [Creating a helm chart with 2 child helm chart helm v3](#creating-a-helm-chart-with-2-child-helm-chart-helm-v3)
- [Helm v3 dependency update](#helm-v3-dependency-update)

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
- name: memcached
  version: "3.2.3"
  repository: "https://kubernetes-charts.storage.googleapis.com"

EOF
```

#### Helm v3 dependency update

```bash
cd main-helmchart && helm3 dependency update
```




Link to reference https://gist.github.com/fvcproductions/1bfc2d4aecb01a834b46