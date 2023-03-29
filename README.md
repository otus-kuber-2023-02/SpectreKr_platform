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