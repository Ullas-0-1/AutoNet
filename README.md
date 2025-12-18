AutoNet: Self-Healing AI-Driven Network Defense System
======================================================

AutoNet is a comprehensive **DevSecOps** and **Network Function Virtualization (NFV)** platform engineered to protect microservices architectures against sophisticated application-layer threats. It implements a **Closed-Loop Automation**system that integrates real-time Anomaly Detection with automated network reconfiguration to mitigate threats without manual intervention.

Project Overview
----------------

The system simulates a production environment where a vulnerable application is subjected to continuous traffic. AutoNet operates as an intelligent perimeter defense, leveraging unsupervised machine learning to establish traffic baselines and identify deviations indicative of malicious activity.

### Key Capabilities

*   **Zero-Touch Remediation:** Automatically detects and mitigates SQL Injection, Cross-Site Scripting (XSS), and Path Traversal attacks by dynamically updating access control lists (ACLs).
    
*   **Hybrid Detection Engine:** Combines **Signature-Based Detection** (Regular Expressions) for known threat patterns with **Unsupervised Machine Learning** (Isolation Forest) for zero-day anomaly detection.
    
*   **Resilient Infrastructure:** Deployed on **Kubernetes**, utilizing liveness probes for self-healing and Horizontal Pod Autoscaling (HPA) for dynamic resource management under load.
    
*   **Data Loss Prevention (DLP):** Implements an egress proxy layer that inspects and sanitizes HTTP responses, redacting sensitive information (PII, credentials) to prevent data exfiltration.
    
    

System Architecture
-------------------

The solution is composed of five distinct containerized microservices orchestrated via Kubernetes:

1.  **Gateway Service (Nginx):**
    
    *   Functions as the primary Reverse Proxy and ingress controller.
        
    *   Enforces security policies dynamically by ingesting configuration updates from the analysis engine.
        
    *   Routes legitimate traffic to the application and suspicious traffic to the Honeypot.
        
2.  **Target Application (OWASP Juice Shop):**
    
    *   A production-grade vulnerable web application used to validate the efficacy of the defense system against successful exploitation attempts.
        
3.  **Analysis Engine:**
    
    *   The central intelligence unit responsible for log aggregation and threat detection.
        
    *   **MLOps Pipeline:** Integrates model training into the CI/CD process. An **Isolation Forest** model is trained on synthetic benign traffic during the build phase to establish a baseline for anomaly detection.
        
    *   **Justification for Isolation Forest:** While Transformer-based models (e.g., BERT) offer semantic understanding, they introduce significant computational overhead and latency unsuitable for real-time edge detection in this scope. Isolation Forest was selected for its efficiency in high-dimensional feature spaces and its ability to detect outliers without labeled attack data, ensuring low-latency inference.
        
    *   **Automation:** Triggers **Ansible** playbooks to execute remediation actions on the Gateway.
        
4.  **Traffic Simulation Engine:**
    
    *   A Python-based load generator capable of simulating legitimate user behavior alongside specific attack vectors (SQLi, XSS) to validate system responsiveness.
        
5.  **DLP Proxy:**
    
    *   A middleware service that intercepts application responses. It utilizes pattern matching to identify and redact sensitive entities before the response is transmitted to the client.
        
6.  **Observability Stack (ELK):**
    
    *   Integrates Elasticsearch, Logstash, Kibana, and Filebeat to provide real-time visualization of security metrics, traffic throughput, and attack geolocation.
        

Tech Stack
----------

*   **Orchestration:** Kubernetes (K8s), Horizontal Pod Autoscaler (HPA)
    
*   **Configuration Management:** Ansible, Ansible Vault
    
*   **CI/CD:** Jenkins
    
*   **Containerization:** Docker, Docker Compose
    
*   **Network Security:** Nginx, Python Scikit-Learn (Anomaly Detection)
    
*   **Observability:** Elasticsearch, Logstash, Kibana (ELK), Filebeat