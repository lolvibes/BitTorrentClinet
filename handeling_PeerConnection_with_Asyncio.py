import asyncio
import logging
from fileinput import filename

from peer_handeling import handshake as h
# import threading
from announce import peers
logging.basicConfig(filename="peerdata.log",level=logging.INFO)

async def try_connecting_with_peer(peer,handshake):
    peer_ip,peer_port=peer
    try:
        reader,writer=await asyncio.wait_for(asyncio.open_connection(peer_ip,peer_port),timeout=5)
        writer.write(handshake)
        await writer.drain()# .drain do is give ur param handshake to the operating system to handel


        received_handshake_from_peer=await asyncio.wait_for(reader.readexactly(68), timeout=5)
        #checking validity of handshake we recived from peer
        if len(received_handshake_from_peer)<68:
            raise ValueError("incomplete handshake")
        if received_handshake_from_peer[1:20] !=b'BitTorrent protocol':
            raise ValueError("not the right protocol")
        logging.info(f"peer connected : {peer_ip} {peer_port}")
        return reader,writer
    except Exception as e:
        print(f"can't connected with {peer_ip} {peer_port} -{e}  ")#handeling timeout exception
    return None,None
#____________________________________________________________________________________________________________________________
# tried creating one thread per peer to handel it all its functionality but not scalable architecture alternates are better
# def starting_thread(peer,handshake):
#     asyncio.run(try_connecting_with_peer(peer,handshake))
#
# for peer in peers:
#     thread=threading.Thread(target=starting_thread,args=(peer,handshake))
#     thread.start()
#_______________________________________________________________________________________________________________________________
async def connect_to_peers():
    handshake=h
    task=[try_connecting_with_peer(peer,handshake) for peer in peers]
    result =await asyncio.gather(*task)
    connected_peers=[r for r in result if r is not (None,None)]
    logging.info(len(connected_peers))
    return connected_peers

asyncio.run(connect_to_peers())

