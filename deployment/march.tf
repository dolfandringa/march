resource "kubernetes_deployment" "march-backend" {
  metadata {
    name = "march-backend"
    labels = {
      app = "march-backend"
    }
  }
  spec {
    progress_deadline_seconds = 600
    replicas                  = 2
    revision_history_limit    = 10
    selector {
      match_labels = {
        app = "march-backend"
      }
    }
    strategy {
      rolling_update {
        max_surge       = "25%"
        max_unavailable = "25%"
      }
      type = "RollingUpdate"
    }
    template {
      metadata {
        labels = {
          app = "march-backend"
        }
      }
      spec {
        dns_policy                       = "ClusterFirst"
        restart_policy                   = "Always"
        termination_grace_period_seconds = 30
        container {
          image             = "march-backend:latest"
          image_pull_policy = "Never"
          liveness_probe {
            failure_threshold = 3
            http_get {
              http_header {
                name  = "Connection"
                value = "close"
              }
              path   = "/"
              port   = 8000
              scheme = "HTTP"
            }
          }
          name = "march-frontend"
          port {
            container_port = 8000
          }
        }
      }
    }
  }
}
resource "kubernetes_deployment" "march-frontend" {
  metadata {
    name = "march-frontend"
    labels = {
      app = "march-frontend"
    }
  }
  spec {
    progress_deadline_seconds = 600
    replicas                  = 2
    revision_history_limit    = 10
    selector {
      match_labels = {
        app = "march-frontend"
      }
    }
    strategy {
      rolling_update {
        max_surge       = "25%"
        max_unavailable = "25%"
      }
      type = "RollingUpdate"
    }
    template {
      metadata {
        labels = {
          app = "march-frontend"
        }
      }
      spec {
        dns_policy                       = "ClusterFirst"
        restart_policy                   = "Always"
        termination_grace_period_seconds = 30
        container {
          image             = "march-frontend:latest"
          image_pull_policy = "Never"
          liveness_probe {
            failure_threshold = 3
            http_get {
              http_header {
                name  = "Connection"
                value = "close"
              }
              path   = "/"
              port   = 80
              scheme = "HTTP"
            }
          }
          name = "march-frontend"
          port {
            container_port = 80
          }
        }
      }
    }
  }
}
resource "kubernetes_service" "march-frontend" {
  metadata {
    name = "march-frontend"
    labels = {
      app = "march-frontend"
    }
  }
  spec {
    selector = {
      app = kubernetes_deployment.march-frontend.spec.0.template.0.metadata.0.labels.app
    }
    type = "NodePort"
    port {
      node_port   = 30201
      port        = 80
      target_port = 80
    }
  }
}
resource "kubernetes_service" "march-backend" {
  metadata {
    name = "march-backend"
    labels = {
      app = "march-backend"
    }
  }
  spec {
    selector = {
      app = kubernetes_deployment.march-backend.spec.0.template.0.metadata.0.labels.app
    }
    type = "NodePort"
    port {
      node_port   = 30211
      port        = 8000
      target_port = 8000
    }
  }
}
resource "kubernetes_ingress_v1" "march-ingress" {
  metadata {
    name = "march-ingress"
    annotations = {
      "nginx.ingress.kubernetes.io/rewrite-target" = "/"
    }
  }
  spec {
    rule {
      host = "march.dolf.lan"
      http {
        path {
          path      = "/api"
          path_type = "Prefix"
          backend {
            service {
              name = "march-backend"
              port {
                number = "8000"
              }
            }
          }
        }
        path {
          path      = "/"
          path_type = "Prefix"
          backend {
            service {
              name = "march-frontend"
              port {
                number = "80"
              }
            }
          }
        }
      }
    }
  }
}
