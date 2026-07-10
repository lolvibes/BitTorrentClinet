
import announce
import socket
from announce import info_hash, peer_id, result
import handeling_peer_message as hpm
from handeling_peer_message import BLOCK_SIZE
# hanshake
handshake=(bytes([19])+b'BitTorrent protocol'+b'\x00'*8+info_hash+peer_id.encode())# this step is must predefined shit for the connection
# client=None
# client_connected=None
# #we will conect wit the peers in the list trough looping over it
# for ip,port in announce.peers:
#     try:
#         client =socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#         client.settimeout(5)
#         print("connecting....")
#         client.connect((ip,port))
#         print("connected and sending handshake")
#         client.send(handshake)
#         print("handshake sent waiting for respond")
#         return_handshake=client.recv(68)
#         # checking if the returned thing is validate
#         if len(return_handshake)<68:
#             return_handshake = client.recv(68)
#             print(f"got {len(return_handshake)} bytes: {return_handshake}")
#             raise ValueError("incomplete handshake")
#         if return_handshake[1:20] !=b"BitTorrent protocol":
#             raise ValueError("not the protocol we are looking for ")
#         print('client connected succesfully')
#         client_connected=client
#         print(return_handshake)
#         break
#     except Exception as e:
#         print(f"couldn't connected to {ip} at {port} - {e}")
#         client.close()
#
# # if none of the peer connect
# if client_connected  is None:
#     print("no peer connected")
#     exit()
# # in above section we just tried to connect to one client sucessfully  and do the handshake
# #_________________________________________________________________________________
# # now the bitfield ewxchange begins
# NUM_PEICES=announce.num_pieces
# # reciving the message sent from the  peer
# message_id, payload=hpm.recv_any_message_from_peer(client_connected)
#
# peer_pieces=[]
# if message_id==5:# its a bit field message and we neee to do further
#     peer_piece=hpm.bitfield_parser(payload,NUM_PEICES)
#     # above variable have the list of Trues and false
#     print(f"recived a boolean value of peices that a {client_connected}")
#     for piece in peer_piece:
#         print(piece)
# # since we have the bitfield of a peer and the boolean values o fparticular peices
# #now to send our bit field
# my_peices=set()
# client_connected.send(hpm.build_bitfield(my_peices,NUM_PEICES))
# # now sending the message we are intrested in downloading a peice
# hpm.send_intrested(client_connected)
#
# # now its peer's turn to send the message weather he is intrested in us or not  by  sending choke or
# #unchoke
#
# num_pieces_in_torrent=announce.num_pieces # this gives the total in the torrent
# # now here we are trying to get all the blocks in a particular piece
# piece_index = 0  # startign from the intial block for now
# piece_length = announce.result[b'info'][b'piece length']  # getting the size of particular piece
# block_numbers = piece_length // BLOCK_SIZE  # to calculate the total number of blocks in the piece
#
# #____________________________________________________________________________________________________
# already_unchoked=False
# while not already_unchoked:
#     msg_id, _ = hpm.recv_any_message_from_peer(client_connected)
#     if msg_id == 1:  # peer chose to unchoke us
#         print("wow he unchoked us")
#         already_unchoked=True
#         break
#     elif msg_id ==0:
#         print("peer chocked us, waiting...")
#     elif msg_id ==4:
#         continue
#     elif msg_id is None:
#         continue
# #can't get any blocks /pieces from the peer untilll is unchokes and keep away the irrelvant messages
# #_________________________________________________________
# #downloading the piefces
# all_pieces={} # storing all the pieces
# for piece_index in range(num_pieces_in_torrent):
#     blocks={}
#     print(f"downloading peice {piece_index}")
#     for block_num in range(block_numbers):  # looping through our no. of blocks per piece
#         begin = block_num * BLOCK_SIZE  # calculating from where the block should begin
#         hpm.send_block_req(client_connected, begin=begin, piece_index=piece_index)  # sending the req to block
#         while True:
#             msg_id_of_recived_data, load = hpm.recv_any_message_from_peer(client_connected)
#             if msg_id_of_recived_data == 7:  # this means the it send the piece we need so we can further process the payload
#                 index, begin_offset, actual_data = hpm.parser_peice(load)
#                 blocks[begin_offset]=actual_data #stroing the block in the dict with the offset for later stiching
#                 print(f'got peice {index} which begins at the offset {begin_offset} and the length of the rest of the data {len(actual_data)}')
#                 # with open(f"peice_{index} begins_{begin_offset}.bin", 'wb') as f:
#                 #     f.write(actual_data)
#                 #     print("done writing stuff")
#                 break
#             elif msg_id_of_recived_data==1:
#                 hpm.send_block_req(client_connected,begin=begin,piece_index=piece_index)
#             elif msg_id_of_recived_data==4:
#                 continue
#             else:
#                 print(f"unexpected the peice with message id 7 but got{msg_id_of_recived_data}")
#     full_piece=b""
#     for offset in sorted(blocks.keys()):
#         full_piece+=blocks[offset]
#         print(f"assembled full piece {len(full_piece)} bytes")
#     all_pieces[piece_index]=full_piece
# with open("downloaded_test_file.bin","wb") as f:
#     for i in range(num_pieces_in_torrent):
#         f.write(all_pieces[i])
# print("file downloaded succefully")