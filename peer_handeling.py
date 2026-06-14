import announce
import socket
from announce import info_hash, peer_id
import handeling_peer_message as hpm

handshake=(bytes([19])+b'BitTorrent protocol'+b'\x00'*8+info_hash+peer_id.encode())# this step is must predefined shit for the connection
client=None
client_connected=None

for ip,port in announce.peers:
    try:
        client =socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client.settimeout(5)
        client.connect((ip,port))
        client.send(handshake)
        return_handshake=client.recv(68)

        # checking if the returned thing is validate
        if len(return_handshake)<68:
            raise ValueError("incomplete handshake")
        if return_handshake[1:20] !=b"BitTorrent protocol":
            raise ValueError("not the protocol we are looking for ")

        print('client connected succesfully')
        client_connected=client
        print(return_handshake)
        break
    except Exception as e:
        print(f"couldn't connected to {ip} at {port} - {e}")
        client.close()

# if none of the peer connect
if client_connected  is None:
    print("no peer connected")
    exit()
#_________________________________________________________________________________

NUM_PEICES=announce.num_pieces

# reciving the message sent from the  peer
message_id, payload=hpm.recv_any_message_from_peer(client_connected)

peer_pieces=[]
if message_id==5:# its a bit field message and we neee to do further
    peer_piece=hpm.bitfield_parser(payload,NUM_PEICES)
    # above variable have the list of Trues and false
    print(f"recived a boolean value of peices that a {client_connected}")
    for piece in peer_piece:
        print(piece)
# since we have the bitfield of a peer and the boolean values o fparticular peices
#now to send our bit field
my_peices=set()
client_connected.send(hpm.build_bitfield(my_peices,NUM_PEICES))

# now sending the message we are intrested in downloading a peice
hpm.send_intrested(client_connected)

# now its peer's turn to sendn the message weather he is intrested in us or not  by  sending choke or
#unchoke

while True:
    msg_id, _ = hpm.recv_any_message_from_peer(client_connected)
    if msg_id == 1:  # peer chose to unchoke us
        print("wow he unchoked us")
        # we will send which peice we want
        hpm.send_block_req(client_connected, begin=0, piece_index=0)
        # we will recive the message from the peer but we don't know what it is
        # it so we passed it in to bifuracte
        msg_id_of_recived_data, load = hpm.recv_any_message_from_peer(client_connected)
        if msg_id_of_recived_data == 7:  # this means the it send the piece we need so we can further process the payload
            index, begin_offset, actual_data = hpm.parser_peice(load)
            print(
                f'got peice {index} which begins at the offset {begin_offset} and the length of the rest of the data{len(actual_data)}')
            with open(f"peice_{index} begins_{begin_offset}.bin", 'wb') as f:
                f.write(actual_data)
                print("done writing stuff")
        break
    else:
        print("he didn't choked us ")

