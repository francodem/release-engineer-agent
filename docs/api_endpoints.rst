API Endpoints
=============

This section documents the RESTful API endpoints provided by the Release Engineer Agent.

Base URL
--------

All API endpoints are relative to the base URL::

   https://api.example.com/v1

Authentication
--------------

All API requests require authentication using Bearer tokens::

   Authorization: Bearer <your-token>

Deployments
-----------

Create Deployment
~~~~~~~~~~~~~~~~~

Create a new deployment.

**Endpoint**: ``POST /deployments``

**Request Body**:

.. code-block:: json

   {
     "manifest": "...",
     "environment": "production",
     "strategy": "rolling",
     "timeout": 300
   }

**Response**: ``201 Created``

.. code-block:: json

   {
     "id": "deployment-123",
     "status": "pending",
     "created_at": "2025-01-01T00:00:00Z"
   }

Get Deployment
~~~~~~~~~~~~~~

Retrieve deployment details by ID.

**Endpoint**: ``GET /deployments/{deployment_id}``

**Response**: ``200 OK``

.. code-block:: json

   {
     "id": "deployment-123",
     "status": "success",
     "environment": "production",
     "created_at": "2025-01-01T00:00:00Z",
     "completed_at": "2025-01-01T00:05:00Z"
   }

List Deployments
~~~~~~~~~~~~~~~~

List all deployments with optional filtering.

**Endpoint**: ``GET /deployments``

**Query Parameters**:

* ``environment`` (optional): Filter by environment
* ``status`` (optional): Filter by status
* ``limit`` (optional): Maximum number of results (default: 50)
* ``offset`` (optional): Pagination offset

**Response**: ``200 OK``

.. code-block:: json

   {
     "deployments": [
       {
         "id": "deployment-123",
         "status": "success",
         "environment": "production"
       }
     ],
     "total": 100,
     "limit": 50,
     "offset": 0
   }

Rollback Deployment
~~~~~~~~~~~~~~~~~~

Rollback a deployment to a previous version.

**Endpoint**: ``POST /deployments/{deployment_id}/rollback``

**Request Body**:

.. code-block:: json

   {
     "target_version": "v1.2.3"
   }

**Response**: ``200 OK``

.. code-block:: json

   {
     "id": "deployment-124",
     "status": "pending",
     "rollback_from": "deployment-123"
   }

Validations
-----------

Run Validation
~~~~~~~~~~~~~~

Run validation checks for a deployment.

**Endpoint**: ``POST /validations``

**Request Body**:

.. code-block:: json

   {
     "deployment_id": "deployment-123",
     "validation_type": "health_check"
   }

**Response**: ``200 OK``

.. code-block:: json

   {
     "id": "validation-456",
     "status": "passed",
     "checks": [
       {
         "name": "health_check",
         "status": "passed",
         "message": "All pods are healthy"
       }
     ]
   }

Get Validation Results
~~~~~~~~~~~~~~~~~~~~~~

Get validation results for a deployment.

**Endpoint**: ``GET /validations/{validation_id}``

**Response**: ``200 OK``

.. code-block:: json

   {
     "id": "validation-456",
     "deployment_id": "deployment-123",
     "status": "passed",
     "checks": [...],
     "created_at": "2025-01-01T00:00:00Z"
   }

Environments
------------

List Environments
~~~~~~~~~~~~~~~~~

List all available environments.

**Endpoint**: ``GET /environments``

**Response**: ``200 OK``

.. code-block:: json

   {
     "environments": [
       {
         "id": "production",
         "name": "Production",
         "cluster": "prod-cluster",
         "namespace": "default"
       }
     ]
   }

Get Environment Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Get configuration for a specific environment.

**Endpoint**: ``GET /environments/{environment_id}/config``

**Response**: ``200 OK``

.. code-block:: json

   {
     "environment_id": "production",
     "config": {
       "replicas": 3,
       "resources": {...}
     }
   }

Health Check
------------

Check API health status.

**Endpoint**: ``GET /health``

**Response**: ``200 OK``

.. code-block:: json

   {
     "status": "healthy",
     "version": "0.1.0",
     "timestamp": "2025-01-01T00:00:00Z"
   }

Error Responses
---------------

All endpoints may return the following error responses:

**400 Bad Request**

.. code-block:: json

   {
     "error": "Invalid request",
     "message": "Missing required field: manifest"
   }

**401 Unauthorized**

.. code-block:: json

   {
     "error": "Unauthorized",
     "message": "Invalid or missing authentication token"
   }

**404 Not Found**

.. code-block:: json

   {
     "error": "Not Found",
     "message": "Deployment not found"
   }

**500 Internal Server Error**

.. code-block:: json

   {
     "error": "Internal Server Error",
     "message": "An unexpected error occurred"
   }

