import asyncio
import logging

from announce import peers, num_pieces, result, left
from peer_handeling import handshake as h
from PieceManager import PieceManager
from handeling_PeerConnection_with_Asyncio import PeerConnection

logging.basicConfig(filename="peerdata.log", level=logging.INFO)

PIECE_LENGTH = result[b'info'][b'piece length']
TOTAL_LENGTH = left  # already computed in announce.py


async def try_connecting_with_peer(peer, handshake, piece_manager):
    peer_ip, peer_port = peer
    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(peer_ip, peer_port), timeout=5
        )
    except (asyncio.TimeoutError, OSError) as e:
        logging.info(f"could not connect to {peer}: {e}")
        return None

    conn = PeerConnection(reader, writer, piece_manager)

    try:
        await conn.do_handhsake(handshake, peer)
        await conn.exchange_bitfields()
        await conn.send_interested()
    except (asyncio.TimeoutError, ConnectionError, ValueError) as e:
        logging.info(f"handshake/setup failed for {peer}: {e}")
        writer.close()
        return None

    return conn


async def run_peer(peer, handshake, piece_manager):
    conn = await try_connecting_with_peer(peer, handshake, piece_manager)
    if conn is None:
        return
    await conn.download_loop()

async def main():
    piece_manager = PieceManager(
        num_pieces=num_pieces,
        piece_length=PIECE_LENGTH,
        total_file_length=TOTAL_LENGTH,
    )

    handshake = h

    tasks = [run_peer(peer, handshake, piece_manager) for peer in peers]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    for peer, result in zip(peers, results):
        if isinstance(result, Exception):
            import traceback
            print(f"peer {peer} failed: {type(result).__name__}: {result}")
            traceback.print_exception(type(result), result, result.__traceback__)

    print(f"done. pieces collected: {len(piece_manager.my_piece)}/{num_pieces}")
    piece_manager.close()


if __name__ == "__main__":
    asyncio.run(main())