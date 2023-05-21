# SpectreKr_platform
SpectreKr Platform repository

DZ #1
1. Создан Dockerfile запускающий nginx от непривелигированного пользователя, слушающий 8000 порт и использующий каталог /app как рабочую дирикторию
2. Создан манифест web-pod.yaml для запуска пода основанного на контейнере созданом с помощью dockerfile
3. Создан манифест frontend-pod.yaml запуска frontend'a Hipster Shop, с помощью командной строки kubectl run frontend --image spectrekr/otus:frontend --restart=Never --dry-run -o yaml > frontend-pod.yaml
4. Сохдан манифест frontend-pod-healthy.yaml исправляющий ошибки и запускающий frontend pod

DZ #2
1. Создан манифест frontend-replicaset.yaml для frontend пода, который запускает 3 экземпляра.
2. Создан манифест paymentservice-replicaset.yaml для paymentservice пода, который запускает 3 экземпляра.
3. Создан манифест paymentservice-deployment.yaml который разворачивает 3 экземпляра пода paymentservice контролируемые deployment.
4. Создан манифест paymentservice-deployment-bg.yaml реализующий обновление подов paymentservice способом blue-green.
5. Создан манифест paymentservice-deployment-reverse.yaml реализующий обновление подов paymentservice способом Reverse Rolling Update.
6. Создан манифест frontend-deployment.yaml запускающий под frontend кнтролируемый deployment и реализует readinessprobe.
7. Создан манифест node-exporter-daemonset.yaml запускающий под node-exporter на всех нодах класстера, так же добавлен tolerations для запуска на мастер ноде.

DZ #3
1. Настройка readinessProbe и livenessProbe в pod`ах.
2. Реализовали стратегии обнавлений.
3. Создан манифест web-svc-cip.yaml в котором реализуется service настроенный на clusterIP.
4. minikube был перенастроен на работу IPVS.
5. Произведен деплой лоадбалансера MetalLB.
6. Создан манифест web-svc-lb.yaml в котором реализуется работа service через лоадбалансер.
7. Созданы манифесты в каталоге coredns настраивающие доступ к coredns из вне кластера через лоадбалансер.
8. Создан манифест web-svc-headless.yaml убирающий внутренний адрес у service для последующей настройки доступа через ingress.
9. Создан манифест web-ingress.yaml открывающий доступ к поду через ingress.
10. В каталоге dashboard создан манифест открывающий доступ к kubernets dashboard через ingress.
11. В каталоге canary созданы манифесты создающие 2 тестовых web пода, 2 сервиса для доступа к ним и 2 ingress сущности реализующие канареечный доступ к подам.

DZ #4
1. Создан манифест minio-statefulset.yaml осуществляющий деплой S3 хранилища minio.
2. Создан манифест minio-headless-service.yaml предоставляющий доступ к панели администрирования minio.
3. Создан манифест minio-secrets.yaml который создает secret для хранения creds от панели администрирования minio.
4. Создан манифест minio-secrets-statefulset.yaml осуществляющий деплой S3 хранилища использующий secret для получения чувствительных данных.

DZ #5
1. Создан манифест 01-sa-bob создающий service account bob и подключающий права администратора кластера.
2. Создан манифест 02-sa-dave создающий service account dave который не имеет доступа к кластеру.
3. Создан манифест 01-ns создающий namespace prometheus.
4. Создан манифест 02-sa создающий service account carol в namespace prometheus.
5. Создан манифест 03-role создающий cluster role с правами просмотра подов во всем кластере.
6. Создан манифест 04-rolebinding подключающий выше описанную роль к service account carol.
7. Создан манифест 01-ns создающий namespace dev.
8. Создан манифест 02-sa-jane создающий service account jane в namespace dev.
9. Создан манифест 03-role-jane создающий role с правами администратора в nmespace dev.
10. Создан манифест 04-rolebinding-jane подключающий выше описанную роль к service account jane.
11. Создан манифест 05-sa-ken создающий service account ken в namespace dev.
12. Создан манифест 06-role-ken создающий role с правами просмотра в nmespace dev.
13. Создан манифест 07-rolebinding-ken подключающий выше описанную роль к service account ken.

DZ #6
1. Научились работать с helm, добавлять репозитории, устанавливать чарты из репозитория или локального файла.
2. Установили ingress-nginx и cert-manager.
3. Поставили кастомизированный chartmuseum.
4. Научились загружать helm chart в chartmuseum, деплоить chart из него.
5. Установили кастомизированный harbor.
6. Создали helmfile для установки ingress-nginx, cert-manager, harbor совместно.
7. Создали свой чарт для деплоя hipster-shop.
8. Вынесли frontend в отдельный чарт. И добавили его в зависимости к основному чарту.
9. Добавили redis в зависимости к чарту, чтоб деплой redis проходил из свежего чарта, выкаченного из репозитория.
10. Научились работать с helm-secrets, необходимого для хранения чувствительной информации в values.
11. Вынес paymentservice в отдельный деплой с использование kubecfg.
12. Вынес emailservice в отдельный деплой с использованием qbec.
13. Вынес adservice в отдельный деплой с использованием kustomize, настроил деплой в 2 окружения hipster-shop и hipster-shop-prod.

DZ #7
1. Создали CRD и CR для развертывания mysql
2. Создали mysql-operator выполняющий резервное копирование и восстановление БД
3. Создали манифесты деплоя для mysql-operator
4. Провели тестирование:
```bash
kubectl get jobs
backup-mysql-instance-job    1/1           5s         6m23s
restore-mysql-instance-job   1/1           43s        3m7s
```
```bash
kubectl exec -it $MYSQLPOD -- mysql -potuspassword -e "select * from test;" otus-database
mysql: [Warning] Using a password on the command line interface can be insecure.
+----+-------------+
| id | name        |
+----+-------------+
|  1 | some data   |
|  2 | some data-2 |
|  3 | some data   |
|  4 | some data-2 |
+----+-------------+
```
5. Добавление в описание объекта поля status с описанием создания инстанса.
В описание схемы обязательно добавить параметр:
x-kubernetes-preserve-unknown-fields: true
Далее дорабатываем код нашего оператора, чтоб заполнял наше поле, вводим переменную состояния exists_backup. По умолчанию она равна True что подразумевает существование бэкапа, далее на этапе создания PVC для бекапа, в случае успешного создания, переменная принимает значение False, что означает отсутствие бекапа:
```python
if exists_backup:
        return {'Message': 'mysql-instance created with restore-job'}
    else:
        return {'message': 'mysql-instance created without restore-job'}
```
Данный код проверяет состояние переменной отвечающей за наличие резервной копией и выставляет статус.
```bash
Spec:
  Database:     otus-database
  Image:        arm64v8/mysql
  Password:     otuspassword
  usless_data:  useless info
Status:
  mysql_on_create:
    Message:  mysql-instance created without restore-job
Events:
  Type    Reason   Age   From  Message
```
6. Реализовал смену пароля пользователя при обновлении инстанса.
Для этого добавил ашблон job change-pass.yml.j2 который запускает под и производит смену пароля пользователя.
Код в операторе который отслеживает обновление поля spec.password и запускает job. Перед запуском job оператор определяет текущий пароль и предыдущий и передает их в под.
```python
@kopf.on.update('otus.homework', 'v1', 'mysqls', field='spec.password')
def change_password(body, **kwargs):
    name = body['metadata']['name']
    image = body['spec']['image']
    password = body['spec']['password']
    last_pass = yaml.load(body['metadata']['annotations']['kopf.zalando.org/last-handled-configuration'], Loader=SafeLoader)['spec']['password']

    change_pass_job = render_template('change-pass.yml.j2', {
                                      'name': name,
                                      'image': image,
                                      'password': password,
                                      'last_pass': last_pass}
                                      )
    api = kubernetes.client.BatchV1Api()
    api.create_namespaced_job('default', change_pass_job)
    wait_until_job_end(f"change-pass-{name}-job")
    delete_success_jobs(f"change-pass-{name}-job")
    return {'Message': 'mysql-instance password changed'}
```