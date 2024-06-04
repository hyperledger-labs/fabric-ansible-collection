# Fabproxy Removal

This is a support project for removing Fabproxy from migrated instances from IBM Blockchain Platform Software as a Service.The customer who are migrated from SaaS to HLF Support instance still using fabproxy. This section will help to remove the fabproxy from migrated instances. We are using ansible script for remove fabproxy from the HLF Support instances. its has following section.


- Migrate the All CA address.
- Update associated nodes.
- Migrate the self hosted and imported Peer address.
- Migrate the orderering node address.
- Update anchor peer in the channel.


## Prerequisites

This script is executed using the Hyperledger Fabric Ansible collection. Therefore, the customer needs to set up their environment so that the script may run.  Kindly click the link below to set up the prerequisites needed to run this ansible script.

- [Fabric Ansible Collction Pre-requisite](https://labs.hyperledger.org/fabric-ansible-collection/installation.html#requirements)

Alternative way of executing  this script is using docker image. It's easier to exec into a running ansible docker image with the command below, then change to the playbooks directory, then run the playbooks.

```
docker run -it --rm -u $(id -u) -v "local fully qualified path to fabproxy removal playbooks":/playbooks ghcr.io/hyperledger-labs/fabric-ansible:sha-c9330b9 bash

```

E.g:

```
docker run -it --rm -u $(id -u) -v ./examples/fabproxy-removal:/playbooks ghcr.io/hyperledger-labs/fabric-ansible:sha-c9330b9 bash
```

Once the pre-requisite configured in the execution environement. Customer need to checkout the `fabric-ansible-collection`  and navigate to the `examples/fabproxy-removal` directory. This directory contains the execution playbook.  The Customer HLF console and the components shoud be in following version.

| **Component name** | **Version** |
| ------- | ------- |
| Peer  | 2.5.7-20240507 |
| Orderer  | 2.5.7-20240507 |
| CA  | 1.5.10-20240507 |
| Console  | 1.0.9-20240507	 |


The customer should carry out the script under the supervision of an IBM HLF SRE team member. If the client is confident  in the Ansible script's execution process they can execute the script therself. They must gather logs and communicate them via support tickets in the event that there are failures in the sequential execution flow. It is necessary to complete each step in order.
{: important}

## Step 1: Download Hyperledger Fabric Binaries.

Excute the following shell script from the playbook directory.  it will download the all the fabroc binaries.

***Note:***
If docker images are being used, this step can be omitted.
```
./setup.sh
```

## Step 2: Download Identies from the HLF Support Console.

To export data in bulk, navigate to the Settings tab in the left hand navigation. You will see a section called Bulk data management followed by two buttons. The Export button will open a panel on the right, where you have several options of what to export.

- By default, the Identities box in the export panel is left deselected. Download the peer, CA, and orderer identities by selecting the identities box.

- Under the `fabproxy-removal `directory, create a `wallet` directory and add all of the identification files to it.

## Step 3: Editing the variable files.

 Variable files are used to store variables that are used across multiple Ansible playbooks. Each organization has their own variable file, and you must edit these files to specify the connection details for the instance for that organization.The playbook repository has two ansible variable files such as` chanels.yml` and `common-vars.yml`.

 This is how the `console.yml` definition appears. It has the System channel name and the Application channel name by default. if the client's orderer node with system channel. Since `testchainid` is the default system channel name, they don't need to modify it. The customer must alter the name of the appropriate application channel. They have entered each name individually if they have more than one application channel name. If the customer has the orderer node without system channel, they don't need mention the system channel name `testchainid`.


 ```
 channel_names:
   - testchainid
   - channel1

 ```
An alternate method for determining the channel list. Please execute the below command to find the list of channel associated with the network and update channel variable files.

```
kubectl exec -it [Ordrer Node Name] -c orderer -n [Namespace] -- ls /ordererdata/ledger/ibporderer/chains | xargs printf ' - %s \n'
```



This is how the `common-vars.yml` definition appears. Edit the variable file.

- Determine the URL of your instance’s console.

- Determine the API key and secret you use to access your console. You can also use a username and password instead of an API key and secret.

- Set `api_endpoint` to the URL of your console.

- Set `api_authtype` to basic.

- Set `api_key` to your API key or username.

- Set `api_secret` to your API secret or password.

- Set `ordering_service_name`. its the name of your orderering service.

- Set `ordering_service_node_name`. its the name of your orderering service node name. If you have multiple Orderering Service node. The execution mode will one by one. Each time change respective  orderering service node name and execute script.

- Set `ordering_service_admin_identity` the OS identity name.

- Set `ordering_service_msp_id` th OS MSP name. We can get the name from Orderering Service MSP definition.

  ```
  api_endpoint: <Console URL>
  api_authtype: basic
  api_key: <Console UserName>
  api_secret: <Console Password>
  preferred_url_os: "os"
  preferred_url_legacy: "legacy"
  ordering_service_name: <Orderering Service Name>
  ordering_service_node_name: <Orderering Service Node Name>
  ordering_service_admin_identity: <Orderering Service Admin Identity>
  ordering_service_msp_id: <Orderering Service MSP Name>
  dry_run: false
  wait_timeout: 600

  ```

## Step 4: Migrate the All CA address.

 1. This script will renew the CA TLS certificates.

 2. Execute the following script. if we want to see the logs trace. We can add `-vvv` as a suffix in the end of the command

  ```
  ansible-playbook 01-migrate-all-ca-addresses.yml
  ```
 3. Once the script executed.  Check the CA pods are restarted. If its restarted navigate to the console and click the CA node. In the CA `info and usage` page the `Operations url` and `API url`  port has been changed into `443`.

***Note:***

After migrating all CA addresses. Before proceeding to the next step. If the customer has multi-console setup/using imported CA, then export all of the CAs and replace the imported CAs in all consoles.

## Step 5: Update Associated Nodes.

 1. The steps associate nodes the respective to the CA nodes.

 2. Execute the following command.

   ```
   ansible-playbook 02-update-associated-nodes.yml
  ```
 3. Once the script executed.  Check the respective nodes to the CA are restarted. For example Peer and Orderer nodes getting restarted.

## Step 6: Migrate the self hosted and imported Peer address.

 1. The steps migrate Peer and imported Orderer node address and also Re-enroll the peer TLS certificates.

 2. Execute the following command.

   ```
   ansible-playbook 03-migrate-peer-and-imported-addresses.yml
  ```
 3. Once the aforementioned command has been executed, confirm that the respective peer nodes are restarting. If its restarted navigate to the console and click the Peer node. In the Peer `info and usage` page the `Operations url` and `API url`  port has been changed into `443`.

 ## Step 7: Migrate the orderering node address.



  1. The steps migrate renew the Orderer TLS certificate and migrate the Orderer address.

  2. Verify that everything is configured appropriately by reviewing your variable configuration files before running the script. If a customer uses the RAFT ordering service, we must update the name of the ordering service node in the `common-vars.yml` file after each execution.

 3. We require each execution to Verify that the election process is proceeding as planned and that the RAFT leader is being replaced by looking through the Orderer logs. The script needs to be applied for the subsequent ordering service if everything is operating as it should.

 4. Execute the following command.

   ```
   ansible-playbook 04-migrate-ordering-node-addresses.yml
  ```
 5. Once the aforementioned command has been executed, confirm that the respective Orderer nodes are restarting. If its restarted navigate to the console and click the Orderer node. In the Orderer `info and usage` page the `Operations url` and `API url`  port has been changed into `443`.


***Note:***

In the `common-vars.yml`, set the `dry-run` variable to true for the first run. This will ensure all channels are reachable and all actions can be completeted with making changes to the channels.
!important

## Step 8: Update anchor peer in the channel.

 1. The steps migrate the anchor peer address in the application channel config.

 2. Execute the following command.

   ```
   ansible-playbook 05-update_anchor_peers.yml
  ```
 3. Once the above steps executed check the application channel config. The peer address are migrated.

# Verify the HLF Instance of the Post execution

**Step 1:** Verify that the ports for the HLF components(Peer/CA/Orderer) have been updated to 1.

**Step 2:** Scale down the fabproxy deployments in `ibpinfra` namespace  using the below command.

```
kubectl scale deployment --replicas=0 proxy-fabproxy -n ibpinfra
```

**Step 3:** Once the fabproxy pods are scale down to zero. Check the console all the compoents are in green state.

**Step 4:**  Complete the transaction and verify that the console is operating as it did previously.

**Step 4:**  If eveything working as expected. User can remove `ibpinfra` namespace.
