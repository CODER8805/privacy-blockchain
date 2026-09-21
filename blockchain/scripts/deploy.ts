import { network } from "hardhat";

async function main() {
    // Connect to the local Hardhat network
    const { ethers } = await network.connect();
    
    console.log("Deploying DataStorage...");

    // Get the compiled contract
    const DataStorage = await ethers.getContractFactory("DataStorage");

    // Deploy the contract to the network
    const dataStorage = await DataStorage.deploy();

    // Wait for the deployment transaction to be confirmed
    await dataStorage.waitForDeployment();

    // Get the address where the contract was deployed
    const address = await dataStorage.getAddress();

    console.log("=========================================");
    console.log("DataStorage deployed to:", address);
    console.log("=========================================");
}

main().catch((error) => {
    console.error(error);
    process.exitCode = 1;
});