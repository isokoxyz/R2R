# Ready2Render (R2R)

This is an oracle application built for the purposes of demonstrating upgradable NFTs on the Kadena Blockchain. 

## Kadcars
The initial proof of concept use case is with Kadcars NFTs whereby the Kadcars Video Game allows users to apply upgrades to their Kadcars by attaching sticker NFTs to the 3D model of their vehicles.
This process is comprised of two components; on-chain locking/unlocking and ownership verification, as well as the 3D asset manipulation via Blender that combines the NFT assets together

Below is a breakdown of how these upgrades are performed by R2R:
* Execute exec transaction that is the first step of the upgrade defpact which does the following
  * Verifies the user initiating the upgrade process is the true owner of both; the target and attachment NFTs
  * Creates a blueprint of the upgrade details and adds it to the blueprints table with a status of "started"
  * Locks the target NFT via the royalty policy of the marmalade v2 standard
* Verify the first step of the upgrade defpact is completed
* Fetch Kadcar data from the blockchain
* Fetch upgrade sticker NFT data from the blockchain
* Download the Kadcar GLTF file from IPFS
* Load the Kadcar into Blender
* Load upgrade sticker asset into blender
* Apply the sticker to the Appropriate target UV Map (specified in sticker metadata) on the Kadcar as an image texture shader node
* Export the upgraded Kadcar model
* Render the upgraded Kadcar model
* Update the metadata of the Kadcar to contain a list of "attachments" which will include the sticker that was just attached
* Upload the upgraded metadata and render to Digital Ocean
* Execute the Cont transaction to complete the last step of the upgrade defpact
  * Unlock the target NFT (Kadcar) via the royalty policy of the marmalade v2 standard
  * Update the blueprint of this upgrade to reflect a status of "completed"
  * Retrieve the blueprint of the successful upgrade and return it
  * Complete the defpact last step

## How this would be hosted
This application is intended to be a server-side application since it includes hardware intensive operations to perform 3D asset manipulation.

Below are the requirements to use this in a production environment:
* NVIDIA RTX GPU
  * This is to get reliable rendering and blender operation performance
  * RTX 3080 was used in testing
* Linux or UNIX OS
  * This is to enable the execution of pact transactions with the subprocess python module as this application uses the kad_py library to execute pact transactions
* Install and set up [pact](https://github.com/kadena-io/pact)
  * This application executes transactions on Kadena blockchain
  * Set up your Kadena keyset; a public and private key pair are needed for pact transactions. See [kad_py](https://github.com/isokoxyz/kad_py)
* Digital Ocean setup
  * R2R currently expects to download assets from cloud storage; Digital Ocean support is included as that is where Kadcars assets and metadata are stored. However, it can support any other cloud storage with some modification to the code.
  * If using Digital ocean, API key is needed in a .env file for these operations to be successful
* Set up your environment file paths
  * A .env file is required as the application expects to download and upload assets from and to Digital Ocean so you need to specify the local paths on the host machine where these asets are made accessible
