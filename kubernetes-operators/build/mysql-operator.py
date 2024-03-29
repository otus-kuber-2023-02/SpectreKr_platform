import kopf
import yaml
import kubernetes
import time
from jinja2 import Environment, FileSystemLoader
from yaml.loader import SafeLoader


def render_template(filename, vars_dict):
    env = Environment(loader=FileSystemLoader('./templates'))
    template = env.get_template(filename)
    yaml_manifest = template.render(vars_dict)
    json_manifest = yaml.load(yaml_manifest, Loader=SafeLoader)
    return json_manifest


def delete_success_jobs(jobname): #mysql_instance_name):
    api = kubernetes.client.BatchV1Api()
    jobs = api.list_namespaced_job('default')
    for job in jobs.items:
#        jobname = job.metadata.name
#        if (jobname == f"backup-{mysql_instance_name}-job"):
        if (job.metadata.name == jobname):
            if job.status.succeeded == 1:
                api.delete_namespaced_job(jobname,
                                          'default',
                                          propagation_policy='Background'
                                          )


def wait_until_job_end(jobname):
    api = kubernetes.client.BatchV1Api()
    job_finished = False
    jobs = api.list_namespaced_job('default')
    while (not job_finished) and \
            any(job.metadata.name == jobname for job in jobs.items):
        time.sleep(1)
        jobs = api.list_namespaced_job('default')
        for job in jobs.items:
            if job.metadata.name == jobname:
                if job.status.succeeded == 1:
                    job_finished = True


@kopf.on.create('otus.homework', 'v1', 'mysqls')
def mysql_on_create(body, spec, **kwargs):
    exists_backup = True
    name = body['metadata']['name']
    image = body['spec']['image']
    password = body['spec']['password']
    database = body['spec']['database']
    try:
        storage_size = body['spec']['storage_size']
    except KeyError:
        storage_size = "1G"

    # Генерируем JSON манифесты для деплоя
    persistent_volume = render_template('mysql-pv.yml.j2',
                                        {
                                         'name': name,
                                         'storage_size': storage_size
                                         }
                                        )
    persistent_volume_claim = render_template('mysql-pvc.yml.j2',
                                              {
                                               'name': name,
                                               'storage_size': storage_size
                                               }
                                              )
    service = render_template('mysql-service.yml.j2', {'name': name})
    deployment = render_template('mysql-deployment.yml.j2',
                                 {
                                  'name': name,
                                  'image': image,
                                  'password': password,
                                  'database': database
                                  }
                                 )
    restore_job = render_template('restore-job.yml.j2', {
                                  'name': name,
                                  'image': image,
                                  'password': password,
                                  'database': database}
                                  )

    # Определяем, что созданные ресурсы являются дочерними к управляемому CustomResource:
    kopf.append_owner_reference(persistent_volume, owner=body)
    kopf.append_owner_reference(persistent_volume_claim, owner=body)  # addopt
    kopf.append_owner_reference(service, owner=body)
    kopf.append_owner_reference(deployment, owner=body)
    kopf.append_owner_reference(restore_job, owner=body)
    # Таким образом при удалении CR удалятся все, связанные с ним pv,pvc,svc, deployments

    api = kubernetes.client.CoreV1Api()
    # Создаем mysql PV:
    try:
        api.create_persistent_volume(persistent_volume)
    except kubernetes.client.rest.ApiException:
        pass
    # Создаем mysql PVC:
    try:
        api.create_namespaced_persistent_volume_claim('default', persistent_volume_claim)
    except kubernetes.client.rest.ApiException:
        pass
    # Создаем mysql SVC:
    api.create_namespaced_service('default', service)
    # Создаем mysql Deployment:
    api = kubernetes.client.AppsV1Api()
    api.create_namespaced_deployment('default', deployment)

    # Пытаемся восстановиться из backup
    try:
        api = kubernetes.client.BatchV1Api()
        api.create_namespaced_job('default', restore_job)
    except kubernetes.client.rest.ApiException:
        pass

    # Cоздаем PVC  и PV для бэкапов:
    backup_pv = render_template('backup-pv.yml.j2', {
                                                     'name': name,
                                                     'storage_size': storage_size
                                                     })
    api = kubernetes.client.CoreV1Api()
    try:
        api.create_persistent_volume(backup_pv)
    except kubernetes.client.rest.ApiException:
        pass
    backup_pvc = render_template('backup-pvc.yml.j2', {
                                                       'name': name,
                                                       'storage_size': storage_size
                                                       })
    api = kubernetes.client.CoreV1Api()
    try:
        api.create_namespaced_persistent_volume_claim('default', backup_pvc)
        exists_backup = False
    except kubernetes.client.rest.ApiException:
        pass

    # Проверяем происходило восстановление или нет
    if exists_backup:
        return {'Message': 'mysql-instance created with restore-job'}
    else:
        return {'message': 'mysql-instance created without restore-job'}


@kopf.on.delete('otus.homework', 'v1', 'mysqls')
def delete_object_make_backup(body, **kwargs):
    name = body['metadata']['name']
    image = body['spec']['image']
    password = body['spec']['password']
    database = body['spec']['database']
    delete_success_jobs(f"backup-{name}-job") #name)
    # Cоздаем backup job:
    api = kubernetes.client.BatchV1Api()
    backup_job = render_template('backup-job.yml.j2', {
                                 'name': name,
                                 'image': image,
                                 'password': password,
                                 'database': database
                                 })
    api.create_namespaced_job('default', backup_job)
    wait_until_job_end(f"backup-{name}-job")
    delete_success_jobs(f"backup-{name}-job")
    return {'message': "mysql and its children resources deleted"}


@kopf.on.update('otus.homework', 'v1', 'mysqls', field='spec.password')
def change_password(body, **kwargs):
    name = body['metadata']['name']
    image = body['spec']['image']
    password = body['spec']['password']
    # database = body['spec']['database']
    last_pass = yaml.load(body['metadata']['annotations']['kopf.zalando.org/last-handled-configuration'], Loader=SafeLoader)['spec']['password']
    #print(password, last_pass)

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
