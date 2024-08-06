# Deploying Ansible Automation Platform 2.4 on Red Hat OpenShift

This guide provides procedures and reference information for the supported installation scenarios for the Red Hat Ansible Automation Platform operator on OpenShift Container Platform.

<details>
  <summary>Prerequisites</summary>

* [Size recommendations for your automation controller pod containers](https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.4/html-single/deploying_ansible_automation_platform_2_on_red_hat_openshift/index#size_recommendations_for_your_automation_controller_pod_containers)
* [Size recommendations for your Postgres pod](https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.4/html-single/deploying_ansible_automation_platform_2_on_red_hat_openshift/index#size_recommendations_for_your_postgres_pod)

Properly setting the resource requests and limits of our control plane (control pod) and our container group/execution plane (automation job pods) is necessary to ensure the control and execution capacity is balanced

* [Automation controller system requirements](https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.4/html/red_hat_ansible_automation_platform_installation_guide/platform-system-requirements#ref-controller-system-requirements)
  * In this section you can only refer to - Table 2.2. Execution node
* [Network ports and protocols](https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.4/html/red_hat_ansible_automation_platform_planning_guide/ref-network-ports-protocols_planning)
* [Obtaining an authorized Ansible automation controller subscription ](https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.4/html/getting_started_with_automation_controller/controller-managing-subscriptions#controller-obtaining-subscriptions)
  
</details>

<details>
  <summary>Installation</summary>

The installation of AAP 2.4 requires at least version Red Hat OpenShift 4.10. For more details, visit the [Red Hat Ansible Automation Platform Life Cycle](https://access.redhat.com/support/policy/updates/ansible-automation-platform) page.

* [Installing the Ansible Automation Platform Operator ](https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.4/html-single/deploying_ansible_automation_platform_2_on_red_hat_openshift/index#install_operator)
  * To install the operator from the operator catalog you need internet connection from your cluster to RedHat operator hub, if you dont have this connection you must download the operator images and create your own catalog to preform this installation. 
* [Installing automation controller](https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.4/html-single/deploying_ansible_automation_platform_2_on_red_hat_openshift/index#install_controller)
* [Importing a subscription](https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.4/html/getting_started_with_automation_controller/controller-managing-subscriptions#controller-importing-subscriptions)


</details>

<details>
  <summary>Automation mesh for operator-based Red Hat Ansible Automation Platform</summary>

In order to add Exection nodes you need to install receptor collection from the ansible galaxy on the node, if your node located in disconnected environment please downlaod the [receptor collection from here](https://galaxy.ansible.com/ui/repo/published/ansible/receptor/) and put it on your node.
Here you can find guide how to install Ansible collections in disconnected environment

* [How to install an Ansible Collection on a disconnected Ansible control node](https://www.redhat.com/sysadmin/install-ansible-disconnected-node)
* [Prerequisites](https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.4/html/red_hat_ansible_automation_platform_automation_mesh_for_operator-based_installations/assembly-automation-mesh-operator-aap#ref-operator-mesh-prerequisites)
* [Setting up Virtual Machines for use in an automation mesh](https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.4/html/red_hat_ansible_automation_platform_automation_mesh_for_operator-based_installations/assembly-automation-mesh-operator-aap#proc-set-up-virtual-machines) 
* [Defining automation mesh node types](https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.4/html/red_hat_ansible_automation_platform_automation_mesh_for_operator-based_installations/assembly-automation-mesh-operator-aap#proc-define-mesh-node-types)
* [Creating an instance group](https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.4/html/red_hat_ansible_automation_platform_automation_mesh_for_operator-based_installations/assembly-automation-mesh-operator-aap#controller-create-instance-group)
* [Associating instances to an instance group](https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.4/html/red_hat_ansible_automation_platform_automation_mesh_for_operator-based_installations/assembly-automation-mesh-operator-aap#controller-associate-instances-to-instance-group)


</details>

<details>
  <summary>Additional Operations</summary>

* [Setting up LDAP Authentication](https://docs.ansible.com/automation-controller/latest/html/administration/ldap_auth.html)
* [Execution Environments](https://docs.ansible.com/automation-controller/latest/html/userguide/execution_environments.html)

</details>