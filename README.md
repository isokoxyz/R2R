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
