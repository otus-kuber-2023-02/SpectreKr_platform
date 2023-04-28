local env = {
  name: std.extVar('qbec.io/env'),
  namespace: std.extVar('qbec.io/defaultNs'),
};
local p = import '../params.libsonnet';
local params = p.components.emailservice;

[
  {
  "apiVersion": "apps/v1",
  "kind": "Deployment",
  "metadata": {
    "name": params.name
  },
  "spec": {
    "replicas": params.replicas,
    "selector": {
      "matchLabels": {
        "app": params.name
      }
    },
    "template": {
      "metadata": {
        "labels": {
          "app": params.name
        }
      },
      "spec": {
        "serviceAccountName": "default",
        "terminationGracePeriodSeconds": 5,
        "securityContext": {
            "fsGroup": 1000,
            "runAsGroup": 1000,
            "runAsNonRoot": true,
            "runAsUser": 1000,
        },
        "containers": [
          {
            "name": "server",
            "securityContext": {
                "allowPrivilegeEscalation": false,
                "capabilities": {
                    "drop" :[
                        "all"
                    ],
                },
                "privileged": false,
                "readOnlyRootFilesystem": true,
            },
            "image": params.image,
            "ports": [
              {
                "containerPort": params.containterPort
              }
            ],
            "readinessProbe": {
              "periodSeconds": 5,
              "exec": {
                "command": [
                  "/bin/grpc_health_probe",
                  "-addr=:8080"
                ]
              }
            },
            "livenessProbe": {
              "periodSeconds": 5,
              "exec": {
                "command": [
                  "/bin/grpc_health_probe",
                  "-addr=:8080"
                ]
              }
            },
            "env": [
              {
                "name": "PORT",
                "value": "8080"
              },
              {
                "name": "DISABLE_PROFILER",
                "value": "1"
              }
            ],
            "resources": {
              "requests": {
                "cpu": params.cpu_requests,
                "memory": params.memory_requests
              },
              "limits": {
                "cpu": params.cpu_limits,
                "memory": params.memory_limits
              }
            }
          }
        ]
      }
    }
  }
},

{
  "apiVersion": "v1",
  "kind": "Service",
  "metadata": {
    "name": params.name
  },
  "spec": {
    "type": "ClusterIP",
    "selector": {
      "app": params.name
    },
    "ports": [
      {
        "name": "grpc",
        "port": params.servicePort,
        "targetPort": params.containterPort
      }
    ]
  }
}
]