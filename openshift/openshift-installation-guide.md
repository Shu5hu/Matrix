# OpenShift Container Platform version 4.12 installation

This guide provides all the necessary information to install RedHat OpenShift UPI on vSphere in a restricted network. Before following this guide, ensure you have a valid RedHat account with the required subscriptions.

<details>
  <summary>Architecture and information about Openshift installtion</summary>

* [Installation process details](https://docs.openshift.com/container-platform/4.12/architecture/architecture-installation.html#installation-process_architecture-installation)
* [VMware vSphere infrastructure requirements](https://docs.openshift.com/container-platform/4.12/installing/installing_vsphere/installing-restricted-networks-vsphere.html#installation-vsphere-infrastructure_installing-restricted-networks-vsphere)
* [VMware vSphere CSI Driver Operator requirements](https://docs.openshift.com/container-platform/4.12/installing/installing_vsphere/installing-restricted-networks-vsphere.html#vsphere-csi-driver-reqs_installing-restricted-networks-vsphere)
* [vCenter requirements](https://docs.openshift.com/container-platform/4.12/installing/installing_vsphere/installing-restricted-networks-vsphere.html#installation-vsphere-installer-infra-requirements_installing-restricted-networks-vsphere)
* [Required machines for cluster installation](https://docs.openshift.com/container-platform/4.12/installing/installing_vsphere/installing-restricted-networks-vsphere.html#installation-vsphere-installer-infra-requirements_installing-restricted-networks-vsphere)
* [Minimum resource requirements for cluster installation](https://docs.openshift.com/container-platform/4.12/installing/installing_vsphere/installing-restricted-networks-vsphere.html#installation-minimum-resource-requirements_installing-restricted-networks-vsphere)
* [Networking requirements for user-provisioned infrastructure](https://docs.openshift.com/container-platform/4.12/installing/installing_vsphere/installing-restricted-networks-vsphere.html#installation-network-user-infra_installing-restricted-networks-vsphere)
* [User-provisioned DNS requirements](https://docs.openshift.com/container-platform/4.12/installing/installing_vsphere/installing-restricted-networks-vsphere.html#installation-dns-user-infra_installing-restricted-networks-vsphere)
* [Load balancing requirements for user-provisioned infrastructure](https://docs.openshift.com/container-platform/4.12/installing/installing_vsphere/installing-restricted-networks-vsphere.html#installation-load-balancing-user-infra_installing-restricted-networks-vsphere)

</details>

<details>
  <summary>About installations in restricted networks</summary>

* [Internet access for OpenShift Container Platform](https://docs.openshift.com/container-platform/4.12/installing/installing_vsphere/installing-restricted-networks-vsphere.html#cluster-entitlements_installing-restricted-networks-vsphere)
* [Mirroring the OpenShift Container Platform image repository](https://docs.openshift.com/container-platform/4.12/installing/disconnected_install/installing-mirroring-installation-images.html#installation-about-mirror-registry_installing-mirroring-installation-images)
* [Configuring credentials that allow images to be mirrored](https://docs.openshift.com/container-platform/4.12/installing/disconnected_install/installing-mirroring-installation-images.html#installation-adding-registry-pull-secret_installing-mirroring-installation-images)
* [Mirroring the OpenShift Container Platform image repository](https://docs.openshift.com/container-platform/4.12/installing/disconnected_install/installing-mirroring-installation-images.html#installation-mirror-repository_installing-mirroring-installation-images)
  * [Pull OpenShift installation images](https://github.com/shu5hu/matrix/blob/main/openshift/openshift-restricted-upi-vsphere-cheet-sheet.md#pull-openshift-installation-images)
* [Creating the RHCOS image for restricted network installations](https://docs.openshift.com/container-platform/4.15/installing/installing_vsphere/ipi/installing-restricted-networks-installer-provisioned-vsphere.html#installation-creating-image-restricted_installing-restricted-networks-installer-provisioned-vsphere)
  * *The latest RHCOS OVA for version 4.12 available [here](https://mirror.openshift.com/pub/openshift-v4/dependencies/rhcos/4.12/latest/)*
* [Obtaining the installation program](https://docs.openshift.com/container-platform/4.15/installing/installing_vsphere/ipi/ipi-vsphere-preparing-to-install.html#installation-obtaining-installer_ipi-vsphere-preparing-to-install)
* [Obtaining the OpenShift CLI by downloading the binary](https://docs.openshift.com/container-platform/4.15/installing/installing_vsphere/ipi/ipi-vsphere-preparing-to-install.html#cli-installing-cli_ipi-vsphere-preparing-to-install)

</details>

<details>
  <summary>Preparing the OpenShift infrastructure</summary>

These steps should be performed on a bastion machine, which will provide the necessary infrastructure for the OpenShift installation.
<br>

If you don't have a registry to host the installation images, follow the steps to install Minimal Quay on your bastion machine and use it as a registry for your installation. In a restricted network environment, you must pull first the images to the connected machine, than bring them over to your restricted network and push them to your local registry
* [Red Hat minimal Quay registry](https://github.com/shu5hu/matrix/blob/main/openshift/openshift-restricted-upi-vsphere-cheet-sheet.md#Red-Hat-minimal-Quay-registry)
    * *If you wnat to use server certificate that signed by your organization CA, please create this certificate before you start this proccess, this certificat must contain alt name*
* [Push images to the local registry](https://github.com/shu5hu/matrix/blob/main/openshift/openshift-restricted-upi-vsphere-cheet-sheet.md#Push-images-to-the-local-registry)
* [Load balancing requirements for user-provisioned infrastructure](https://docs.openshift.com/container-platform/4.12/installing/installing_vsphere/installing-restricted-networks-vsphere.html#installation-load-balancing-user-infra_installing-restricted-networks-vsphere)
* [Validating DNS resolution for user-provisioned infrastructure](https://docs.openshift.com/container-platform/4.12/installing/installing_vsphere/installing-restricted-networks-vsphere.html#installation-user-provisioned-validating-dns_installing-restricted-networks-vsphere)
  * *Optional* [Install Helm Binary](https://helm.sh/docs/intro/install/)
* [Generating a key pair for cluster node SSH access](https://docs.openshift.com/container-platform/4.12/installing/installing_vsphere/installing-restricted-networks-vsphere.html#ssh-agent-using_installing-restricted-networks-vsphere)
* [install the installation program](https://docs.openshift.com/container-platform/4.15/installing/installing_vsphere/ipi/ipi-vsphere-preparing-to-install.html#installation-obtaining-installer_ipi-vsphere-preparing-to-install)
* [install the OpenShift CLI by downloading the binary](https://docs.openshift.com/container-platform/4.15/installing/installing_vsphere/ipi/ipi-vsphere-preparing-to-install.html#cli-installing-cli_ipi-vsphere-preparing-to-install)
* [Adding vCenter root CA certificates to your system trust](https://docs.openshift.com/container-platform/4.15/installing/installing_vsphere/ipi/ipi-vsphere-preparing-to-install.html#installation-adding-vcenter-root-certificates_ipi-vsphere-preparing-to-install)

</details>

<details>
  <summary>Installation process</summary>

* [Manually creating the installation configuration file](https://docs.openshift.com/container-platform/4.12/installing/installing_vsphere/installing-restricted-networks-vsphere.html#installation-initializing-manual_installing-restricted-networks-vsphere)
    * [Sample install-config.yaml file for an installer-provisioned VMware vSphere cluster](https://docs.openshift.com/container-platform/4.12/installing/installing_vsphere/installing-restricted-networks-vsphere.html#installation-vsphere-config-yaml_installing-restricted-networks-vsphere)
    * *Optional* [Configuring the cluster-wide proxy during installation](https://docs.openshift.com/container-platform/4.12/installing/installing_vsphere/installing-restricted-networks-vsphere.html#installation-configure-proxy_installing-restricted-networks-vsphere)
* [Creating the Kubernetes manifest and Ignition config files](https://docs.openshift.com/container-platform/4.12/installing/installing_vsphere/installing-restricted-networks-vsphere.html#installation-user-infra-generate-k8s-manifest-ignition_installing-restricted-networks-vsphere)
* [Configuring chrony time service](https://docs.openshift.com/container-platform/4.12/installing/installing_vsphere/installing-restricted-networks-vsphere.html#installation-special-config-chrony_installing-restricted-networks-vsphere)
* [Extracting the infrastructure name](https://docs.openshift.com/container-platform/4.12/installing/installing_vsphere/installing-restricted-networks-vsphere.html#installation-extracting-infraid_installing-restricted-networks-vsphere)
* [Installing RHCOS and starting the OpenShift Container Platform bootstrap process](https://docs.openshift.com/container-platform/4.12/installing/installing_vsphere/installing-restricted-networks-vsphere.html#installation-vsphere-machines_installing-restricted-networks-vsphere)
* [Adding more compute machines to a cluster in vSphere](https://docs.openshift.com/container-platform/4.12/installing/installing_vsphere/installing-restricted-networks-vsphere.html#machine-vsphere-machines_installing-restricted-networks-vsphere)
* [Waiting for the bootstrap process to complete](https://docs.openshift.com/container-platform/4.12/installing/installing_vsphere/installing-restricted-networks-vsphere.html#installation-installing-bare-metal_installing-restricted-networks-vsphere)
* [Logging in to the cluster by using the CLI](https://docs.openshift.com/container-platform/4.12/installing/installing_vsphere/installing-restricted-networks-vsphere.html#cli-logging-in-kubeadmin_installing-restricted-networks-vsphere)
* [Approving the certificate signing requests for your machines](https://docs.openshift.com/container-platform/4.12/installing/installing_vsphere/installing-restricted-networks-vsphere.html#installation-approve-csrs_installing-restricted-networks-vsphere)
* [Disabling the default OperatorHub catalog sources](https://docs.openshift.com/container-platform/4.12/installing/installing_vsphere/installing-restricted-networks-vsphere.html#olm-restricted-networks-operatorhub_installing-restricted-networks-vsphere)
* [Completing installation on user-provisioned infrastructure](https://docs.openshift.com/container-platform/4.12/installing/installing_vsphere/installing-restricted-networks-vsphere.html#installation-complete-user-infra_installing-restricted-networks-vsphere)

</details>