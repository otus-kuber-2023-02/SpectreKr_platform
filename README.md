# SpectreKr_platform
SpectreKr Platform repository

DZ #1
1. Создан Dockerfile запускающий nginx от непривелигированного пользователя, слушающий 8000 порт и использующий каталог /app как рабочую дирикторию
2. Создан манифест web-pod.yaml для запуска пода основанного на контейнере созданом с помощью dockerfile
3. Создан манифест frontend-pod.yaml запуска frontend'a Hipster Shop, с помощью командной строки kubectl run frontend --image spectrekr/otus:frontend --restart=Never --dry-run -o yaml > frontend-pod.yaml
4. Сохдан манифест frontend-pod-healthy.yaml исправляющий ошибки и запускающий frontend pod
