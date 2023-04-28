{
  components: {
    emailservice: {
      name: 'emailservice',
      image: 'gcr.io/google-samples/microservices-demo/emailservice:v0.5.0',
      replicas: 1,
      containterPort: 8080,
      servicePort: 500,
      cpu_requests: "100m",
      memory_requests: "64Mi",
      cpu_limits: "500m",
      memory_limits: "512Mi",
    },
  },
}