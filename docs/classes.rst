Classes
=======

This section documents the main classes and their APIs in the Release Engineer Agent.

Core Classes
------------

.. automodule:: release_engineer_agent
   :members:
   :undoc-members:
   :show-inheritance:

DeploymentEngine
----------------

.. autoclass:: release_engineer_agent.deployment.DeploymentEngine
   :members:
   :undoc-members:
   :show-inheritance:

   The DeploymentEngine class handles the core deployment logic.

   **Example**::

      from release_engineer_agent.deployment import DeploymentEngine
      
      engine = DeploymentEngine(config)
      result = engine.deploy(manifest, environment='production')

ValidationService
-----------------

.. autoclass:: release_engineer_agent.validation.ValidationService
   :members:
   :undoc-members:
   :show-inheritance:

   The ValidationService performs pre and post-deployment validations.

   **Example**::

      from release_engineer_agent.validation import ValidationService
      
      validator = ValidationService()
      is_valid = validator.validate(deployment)

RecoveryManager
---------------

.. autoclass:: release_engineer_agent.recovery.RecoveryManager
   :members:
   :undoc-members:
   :show-inheritance:

   The RecoveryManager handles rollback and recovery procedures.

   **Example**::

      from release_engineer_agent.recovery import RecoveryManager
      
      manager = RecoveryManager()
      manager.rollback(deployment_id)

AIDecisionEngine
----------------

.. autoclass:: release_engineer_agent.ai.AIDecisionEngine
   :members:
   :undoc-members:
   :show-inheritance:

   The AIDecisionEngine provides AI-powered decision making.

   **Example**::

      from release_engineer_agent.ai import AIDecisionEngine
      
      ai_engine = AIDecisionEngine()
      decision = ai_engine.recommend_strategy(deployment_context)

ConfigurationManager
--------------------

.. autoclass:: release_engineer_agent.config.ConfigurationManager
   :members:
   :undoc-members:
   :show-inheritance:

   The ConfigurationManager handles environment-specific configurations.

   **Example**::

      from release_engineer_agent.config import ConfigurationManager
      
      config_manager = ConfigurationManager()
      config = config_manager.get_environment_config('production')

Data Models
-----------

Deployment
~~~~~~~~~~

.. autoclass:: release_engineer_agent.models.Deployment
   :members:
   :undoc-members:
   :show-inheritance:

DeploymentStatus
~~~~~~~~~~~~~~~~

.. autoclass:: release_engineer_agent.models.DeploymentStatus
   :members:
   :undoc-members:
   :show-inheritance:

Environment
~~~~~~~~~~~

.. autoclass:: release_engineer_agent.models.Environment
   :members:
   :undoc-members:
   :show-inheritance:

