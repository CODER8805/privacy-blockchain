// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract DataStorage {
    // This struct defines what a single record looks like.
    // Notice there is no plaintext data here!
    struct DataRecord {
        string cid;
        string dataHash;
        address sender;
        uint256 timestamp;
    }

    // An array to store all records sequentially
    DataRecord[] private records;

    // An event emitted every time new data is stored (useful for frontends)
    event DataStored(string cid, string dataHash, address sender, uint256 timestamp);

    // Function to store the metadata
    function storeData(string memory _cid, string memory _dataHash) public {
        records.push(DataRecord({
            cid: _cid,
            dataHash: _dataHash,
            sender: msg.sender,       // Automatically captures the caller's address
            timestamp: block.timestamp // Automatically captures the block time
        }));

        emit DataStored(_cid, _dataHash, msg.sender, block.timestamp);
    }

    // Function to retrieve a specific record by its index
    function getRecord(uint256 _index) public view returns (string memory cid, string memory dataHash, address sender, uint256 timestamp) {
        require(_index < records.length, "Record does not exist");
        DataRecord memory record = records[_index];
        return (record.cid, record.dataHash, record.sender, record.timestamp);
    }

    // Function to see how many records exist total
    function getRecordCount() public view returns (uint256) {
        return records.length;
    }
}