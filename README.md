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