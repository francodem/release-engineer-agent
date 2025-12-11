System Design
==============

This section describes the architecture and internal design of the **AlertsInjestor** component 
of the Release Engineer Agent. This module is responsible for ingesting, validating, and 
persisting alert data originating from Prometheus Alertmanager.

Architecture Overview
---------------------

The AlertsInjestor follows a clean, modular, SOLID-oriented architecture. It acts as the 
entry point for all alert events received through Alertmanager's webhook mechanism.

.. figure:: _static/alerts-injestor-diagram.png
   :alt: Alerts Injestor Architecture Diagram
   :align: center

   High-level architecture of the AlertsInjestor component

Core Responsibilities
---------------------

**Webhook Receiver**
   Exposes an HTTP endpoint that receives alert batches from Prometheus Alertmanager. 
   The receiver deserializes the payload and dispatches each alert for parallel processing.

**Alert Sanitizer**
   Normalizes raw alert data by extracting essential fields such as alert name, severity, 
   deployment name, namespace, and timestamps.

**Alert Validator**
   Validates incoming alerts against the Kubernetes cluster to ensure the referenced 
   resources (e.g., Deployments, Namespaces) actually exist. Invalid alerts are tagged and 
   persisted accordingly.

**Alert Enricher**
   Queries the Kubernetes API to enrich alerts with live cluster metadata such as 
   replica counts, available replicas, image versions, and rollout information.

**Alert Repository**
   Persists processed alerts into the agent's internal storage system (`alerts-db`). 
   Enables historical analysis, correlation, and downstream AI-driven decision-making.

**Kubernetes Client Abstraction**
   A clean interface for interacting with Kubernetes. The AlertsInjestor relies on 
   abstracted operations (e.g., `DeploymentExists`, `GetDeploymentInfo`) rather than 
   concrete implementations, ensuring portability and testability.

Class Design (UML)
------------------

The following UML diagram illustrates how the AlertsInjestor components interact, 
including the interfaces for sanitizer, validator, enricher, and repository, as well 
as the Kubernetes client abstraction.

.. figure:: _static/images/rea-alertsinjestor-uml-diagram.png
   :alt: AlertsInjestor UML Diagram
   :align: center

   AlertsInjestor class design and interfaces

Data Flow
---------

1. **Alert Reception**: Alertmanager sends a POST request to the injestor’s webhook endpoint.
2. **Batch Extraction**: The payload is parsed and each raw alert is extracted.
3. **Parallel Processing**: Each alert is processed concurrently through a well-defined pipeline.
4. **Sanitization**: RawAlert → SanitizedAlert transformation.
5. **Validation**: Kubernetes resource validation (namespace, deployment, etc.).
6. **Enrichment**: Cluster metadata added to produce an EnrichedAlert.
7. **Persistence**: A ProcessedAlert is written to the `alerts-db` for further analysis.
8. **Acknowledgement**: The webhook responds immediately to Alertmanager to prevent retries.

Technology Stack
----------------

* **Language**: Go
* **Framework**: Standard Library (`net/http`), optional `gorilla/mux`
* **Kubernetes Client**: `client-go` (typed client or dynamic)
* **Concurrency Model**: Goroutines and worker pools for O(n) parallel alert processing
* **Storage**: Pluggable repository implementation (`alerts-db`, SQL/NoSQL)
* **Serialization**: `encoding/json`

Deployment Architecture
-----------------------

The AlertsInjestor can be deployed in multiple configurations:

* **Standalone Kubernetes Service**  
  Runs independently inside the cluster and receives Alertmanager webhooks.

* **Sidecar Within the Release Engineer Agent**  
  Injected alongside other components to tightly couple alerting with decision systems.

* **External Service**  
  Hosted outside the cluster with secure access to the Kubernetes API.

Security Considerations
-----------------------

* Webhook endpoint must enforce TLS/SSL for all inbound communication.
* Kubernetes API credentials follow least-privilege RBAC principles.
* All secrets are encrypted both at rest and in transit.
* Input validation is performed on all alert payloads received from Alertmanager.
* Parallel workers are isolated to prevent shared-state vulnerabilities.

