# OpenShift Container Platform installation

This guide provides all the necessary information to install RedHat OpenShift IPI on vSphere in a restricted network. Before following this guide, ensure you have a valid RedHat account with the required subscriptions.

<details>
  <summary>Architecture and information about Openshift installtion</summary>

* [Installation process details](https://docs.openshift.com/container-platform/4.15/architecture/architecture-installation.html#installation-process_architecture-installation)
* [VMware vSphere infrastructure requirements](https://docs.openshift.com/container-platform/4.8/installing/installing_vsphere/installing-vsphere-installer-provisioned.html#installation-vsphere-infrastructure_installing-vsphere-installer-provisioned)
* [vCenter requirements](https://docs.openshift.com/container-platform/4.8/installing/installing_vsphere/installing-vsphere-installer-provisioned.html#installation-vsphere-installer-infra-requirements_installing-vsphere-installer-provisioned)
* [Requirements for a cluster with user-provisioned infrastructure](https://docs.openshift.com/container-platform/4.15/installing/installing_platform_agnostic/installing-platform-agnostic.html#installation-requirements-user-infra_installing-platform-agnostic)
* [Minimum resource requirements for cluster installation](https://docs.openshift.com/container-platform/4.15/installing/installing_platform_agnostic/installing-platform-agnostic.html#installation-minimum-resource-requirements_installing-platform-agnostic)
* [Networking requirements for user-provisioned infrastructure](https://docs.openshift.com/container-platform/4.15/installing/installing_platform_agnostic/installing-platform-agnostic.html#installation-network-user-infra_installing-platform-agnostic)
* [User-provisioned DNS requirements](https://docs.openshift.com/container-platform/4.15/installing/installing_platform_agnostic/installing-platform-agnostic.html#installation-dns-user-infra_installing-platform-agnostic)
    * *When you use IPI you need only DNS name resolution for <mark>The Kubernetes API</mark> and <mark>The OpenShift Container Platform application wildcard</mark>*
</details>

<details>
  <summary>Preparing the OpenShift infrastructure</summary>

These steps should be performed on a bastion machine, which will provide the necessary infrastructure for the OpenShift installation.

* [Validating DNS resolution for user-provisioned infrastructure](https://docs.openshift.com/container-platform/4.15/installing/installing_platform_agnostic/installing-platform-agnostic.html#installation-user-provisioned-validating-dns_installing-platform-agnostic)
* [Installing the OpenShift CLI by downloading the binary](https://docs.openshift.com/container-platform/4.15/installing/installing_vsphere/ipi/ipi-vsphere-preparing-to-install.html#cli-installing-cli_ipi-vsphere-preparing-to-install)
* [Generating a key pair for cluster node SSH access](https://docs.openshift.com/container-platform/4.15/installing/installing_vsphere/ipi/ipi-vsphere-preparing-to-install.html#ssh-agent-using_ipi-vsphere-preparing-to-install)
* [Adding vCenter root CA certificates to your system trust](https://docs.openshift.com/container-platform/4.15/installing/installing_vsphere/ipi/ipi-vsphere-preparing-to-install.html#installation-adding-vcenter-root-certificates_ipi-vsphere-preparing-to-install)

If you don't have a registry to host the installation images, follow the steps to install Minimal Quay on your bastion machine and use it as a registry for your installation. In a restricted network environment, you must create one Quay registry in an environment with an internet connection to pull the images and another inside your restricted network (which could be your bastion server).

* [Red Hat minimal Quay registry](https://github.com/shu5hu/matrix/blob/main/openshift/openshift-restricted-upi-vsphere-cheet-sheet.md#Red-Hat-minimal-Quay-registry)
    * *If you wnat to use server certificate that signed by your organization CA, please create this certificate before you start this proccess, this certificat must contain alt name*
* [Configuring credentials that allow images to be mirrored](https://docs.openshift.com/container-platform/4.15/installing/disconnected_install/installing-mirroring-installation-images.html#installation-adding-registry-pull-secret_installing-mirroring-installation-images)
* [Mirroring the OpenShift Container Platform image repository](https://docs.openshift.com/container-platform/4.15/installing/disconnected_install/installing-mirroring-installation-images.html#installation-mirror-repository_installing-mirroring-installation-images)
  * [Pull OpenShift installation images](https://github.com/shu5hu/matrix/blob/main/openshift/openshift-restricted-upi-vsphere-cheet-sheet.md#pull-openshift-installation-images)
  * [Push images to the local registry](https://github.com/shu5hu/matrix/blob/main/openshift/openshift-restricted-upi-vsphere-cheet-sheet.md#Push-images-to-the-local-registry)
</details>

<details>
  <summary>Installation process</summary>

* [Creating the installation configuration file](https://docs.openshift.com/container-platform/4.15/installing/installing_vsphere/ipi/installing-restricted-networks-installer-provisioned-vsphere.html#installation-initializing_installing-restricted-networks-installer-provisioned-vsphere)
    * [Sample install-config.yaml file for an installer-provisioned VMware vSphere cluster](https://docs.openshift.com/container-platform/4.15/installing/installing_vsphere/ipi/installing-restricted-networks-installer-provisioned-vsphere.html#installation-installer-provisioned-vsphere-config-yaml_installing-restricted-networks-installer-provisioned-vsphere)
    * *Optional* [Configuring the cluster-wide proxy during installation](https://docs.openshift.com/container-platform/4.15/installing/installing_vsphere/ipi/installing-restricted-networks-installer-provisioned-vsphere.html#installation-configure-proxy_installing-restricted-networks-installer-provisioned-vsphere)
* [Deploying the cluster](https://docs.openshift.com/container-platform/4.15/installing/installing_vsphere/ipi/installing-restricted-networks-installer-provisioned-vsphere.html#installation-launching-installer_installing-restricted-networks-installer-provisioned-vsphere)
* [Logging in to the cluster by using the CLI](https://docs.openshift.com/container-platform/4.15/installing/installing_vsphere/ipi/installing-restricted-networks-installer-provisioned-vsphere.html#cli-logging-in-kubeadmin_installing-restricted-networks-installer-provisioned-vsphere)
* [Disabling the default OperatorHub catalog sources](https://docs.openshift.com/container-platform/4.15/installing/installing_vsphere/ipi/installing-restricted-networks-installer-provisioned-vsphere.html#olm-restricted-networks-operatorhub_installing-restricted-networks-installer-provisioned-vsphere)
* *Optional* [Configuring an external load balancer](https://docs.openshift.com/container-platform/4.15/installing/installing_vsphere/ipi/installing-restricted-networks-installer-provisioned-vsphere.html#nw-osp-configuring-external-load-balancer_installing-restricted-networks-installer-provisioned-vsphere)
</details>