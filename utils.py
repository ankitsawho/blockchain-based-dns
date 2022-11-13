from web3_utils import retrieve


def get_zone_data(data):
    res = retrieve(domain=data)
    return res


def get_flags(flags):
    # Byte 1
    byte1 = bytes(flags[:1])
    QR = '1'
    OPCODE = ''
    for bit in range(1, 5):
        OPCODE += str(ord(byte1) & (1 << bit))

    AA = '1'
    TC = '0'
    RD = '0'

    # Byte 2
    byte2 = bytes(flags[1:2])
    RA = '0'
    Z = '000'
    RCODE = '0000'

    return int(QR+OPCODE+AA+TC+RD, 2).to_bytes(1, byteorder='big')+int(RA+Z+RCODE, 2).to_bytes(1, byteorder='big')


def get_domain(data):
    state = 0
    expected_length = 0
    domain = ''
    parts = []
    x = 0
    y = 0
    for byte in data:
        if state == 1:
            if byte != 0:
                domain += chr(byte)
            x += 1
            if x == expected_length:
                parts.append(domain)
                domain = ''
                state = 0
                x = 0
            if byte == 0:
                parts.append(domain)
                break
        else:
            state = 1
            expected_length = byte
        y += 1
    qtype = data[y:y+2]
    return (parts, qtype)


def get_zone(domain):
    global zonedata
    zone_name = '.'.join(domain)
    return get_zone_data(zone_name)


def get_recs(data):
    domain, questiontype = get_domain(data)
    qt = ''
    if questiontype == b'\x00\x01':
        qt = 'a'
    zone = get_zone(domain)
    return (zone[qt], qt, domain)


def build_question(domainname, rectype):
    qbytes = b''
    for part in domainname:
        length = len(part)
        qbytes += bytes([length])
        for char in part:
            qbytes += ord(char).to_bytes(1, byteorder='big')
    if rectype == 'a':
        qbytes += (1).to_bytes(2, byteorder='big')
    qbytes += (1).to_bytes(2, byteorder='big')
    return qbytes


def rec_to_bytes(domainname, rectype, recttl, recval):
    rbytes = b'\xc0\x0c'
    if rectype == 'a':
        rbytes = rbytes + bytes([0]) + bytes([1])
    rbytes = rbytes + bytes([0]) + bytes([1])
    rbytes += int(recttl).to_bytes(4, byteorder='big')
    if rectype == 'a':
        rbytes = rbytes + bytes([0]) + bytes([4])
        for part in recval.split('.'):
            rbytes += bytes([int(part)])
    return rbytes


def build_response(data):
    getrec = get_recs(data[12:])
    # Transaction ID
    TransactionID = data[:2]
    # Get the flags
    Flags = get_flags(data[2:4])
    # Question Count
    QDCOUNT = b'\x00\x01'
    # Answer Count
    ANCOUNT = len(getrec[0]).to_bytes(2, byteorder='big')
    # Nameserver Count
    NSCOUNT = (0).to_bytes(2, byteorder='big')
    # Additonal Count
    ARCOUNT = (0).to_bytes(2, byteorder='big')
    dnsheader = TransactionID+Flags+QDCOUNT+ANCOUNT+NSCOUNT+ARCOUNT
    # Create DNS body
    dnsbody = b''
    # Get answer for query
    records, rectype, domainname = getrec
    dnsquestion = build_question(domainname, rectype)
    for record in records:
        dnsbody += rec_to_bytes(domainname, rectype,
                                record["ttl"], record["value"])
    return dnsheader + dnsquestion + dnsbody
