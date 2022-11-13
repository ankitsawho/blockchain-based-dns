from web3_utils import store, retrieve

store(
    "ankitsahu.me.",
    3600,
    "ns1.ankitsahu.me.",
    "admin.ankitsahu.me.",
    "{time}",
    3600,
    600,
    604800,
    86400,
    ["ns1.ankitsahu.me.", "ns2.ankitsahu.me.",
        "ns3.ankitsahu.me.", "ns4.ankitsahu.me."],
    ["185.199.109.153", "185.199.110.153", "185.199.111.153", "185.199.108.153"]
)
