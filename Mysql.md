# MySQL installation with Persisten Volumes included

thanks for commands. At first let me recapitulate whether I got this commands right.


1) As far as I can see you cloned project with all helmcharts (stable, incubator, ...) correct     
this step is not necessary in your case because      
you are mixing two concepts:     

   * you run: `helm serach mysql` (incorrect for helm v2 and helm v3 as well)     

        
   * **correct** for `helm v2`:
     ```bash
     helm search stable/mysql -l | head 
     NAME            	CHART VERSION	APP VERSION	DESCRIPTION                                                 
     stable/mysql    	1.6.2        	5.7.28     	Fast, reliable, scalable, and easy to use open-source rel...
     ```
  

   * **correct** for `helm v3`:

     ```bash
     helm3 search repo stable/mysql -l | head 
     NAME            	CHART VERSION	APP VERSION	DESCRIPTION                                       
     stable/mysql    	1.6.2        	5.7.28     	Fast, reliable, scalable, and easy to use open-..
     ```
2) then you `cat charts/stable/mysql/values.yaml` and if I did understand it the thight way there is only change in size of Peristent Volume

   ```bash
   <   size: 8Gi
   ---
   >   size: 1Gi
   ```

3) When it comes to MySQL installation itself via **helm v2** and **helm v3**


   * Helm v2 **templating** showcase:
```bash
# template svc.yaml file first
helm template -x templates/svc.yaml \
--name mysql \
--set persistence.enabled=true \
--set persistence.size=1Gi \
charts/stable/mysql

# deployment.yaml file
helm template -x templates/deployment.yaml \
--name mysql \
--set persistence.enabled=true \
--set persistence.size=1Gi \
charts/stable/mysql 
```

   * Helm v2 **installation**:
```bash
helm install \
--name mysql \
--set persistence.enabled=true \ 
--set persistence.size=1Gi \
stable/mysql 


kubectl get pods,svc
NAME                         READY   STATUS    RESTARTS   AGE
pod/mysql-7df48fd996-pxvnz   1/1     Running   0          91s

NAME                 TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
service/kubernetes   ClusterIP   100.64.0.1      <none>        443/TCP    15m
service/mysql        ClusterIP   100.66.49.169   <none>        3306/TCP   91s

```


4. To get **into MySQL**

```bash
To get your root password run:

    MYSQL_ROOT_PASSWORD=$(kubectl get secret --namespace default mysql -o jsonpath="{.data.mysql-root-password}" | base64 --decode; echo)

To connect to your database:

1. Run an Ubuntu pod that you can use as a client:

    kubectl run -i --tty ubuntu --image=ubuntu:16.04 --restart=Never -- bash -il

2. Install the mysql client:

    $ apt-get update && apt-get install mysql-client -y

3. Connect using the mysql cli, then provide your password:
    $ mysql -h mysql -p

To connect to your database directly from outside the K8s cluster:
    MYSQL_HOST=127.0.0.1
    MYSQL_PORT=3306

    # Execute the following command to route the connection:
    kubectl port-forward svc/mysql 3306

    mysql -h ${MYSQL_HOST} -P${MYSQL_PORT} -u root -p${MYSQL_ROOT_PASSWORD}
```


I **followed** above **instructions**: 
```bash
root@ubuntu:/# mysql -h mysql -p
Enter password: 
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 59
Server version: 5.7.28 MySQL Community Server (GPL)

Copyright (c) 2000, 2020, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> 
mysql> 
mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
4 rows in set (0.00 sec)

mysql> 
```

As you can see MySQL **is now** using **Persitent Volume** and **Persitent Volume Claim**
```bash
kubectl get pv,pvc
NAME                                                        CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM           STORAGECLASS   REASON   AGE
persistentvolume/pvc-47207990-70b8-11ea-889a-023e882b55d0   1Gi        RWO            Delete           Bound    default/mysql   gp2                     6m42s

NAME                          STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
persistentvolumeclaim/mysql   Bound    pvc-47207990-70b8-11ea-889a-023e882b55d0   1Gi        RWO            gp2            7m2s
```
