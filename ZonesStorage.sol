// SPDX-License-Identifier: MIT
pragma solidity >=0.6.0 <0.9.0;

contract ZonesStorage {
    struct Zone {
        uint256 ttl;
        string mname;
        string rname;
        string serial;
        uint256 refresh;
        uint256 retry;
        uint256 expire;
        uint256 minimum;
        string[] host;
        string[] addr;
    }

    mapping(string => Zone) public zones;

    function retrieve(string memory _origin) public view returns (Zone memory) {
        return zones[_origin];
    }

    function addZone(
        string memory _origin,
        uint256 _ttl,
        string memory _mname,
        string memory _rname,
        string memory _serial,
        uint256 _refresh,
        uint256 _retry,
        uint256 _expire,
        uint256 _minimum,
        string[] memory _host,
        string[] memory _addr
    ) public {
        zones[_origin] = Zone(
            _ttl,
            _mname,
            _rname,
            _serial,
            _refresh,
            _retry,
            _expire,
            _minimum,
            _host,
            _addr
        );
    }
}
