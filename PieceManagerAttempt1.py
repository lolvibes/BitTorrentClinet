import asyncio
from announce import num_pieces
from handeling_PeerConnection_with_Asyncio import reader_peer,writer_peer
from handeling_peer_message import recv_any_message_from_peer, build_bitfield, bitfield_parser
class PieceManagerAttempt1:
    set_of_our_piece=set()
    NUM_PIECES=num_pieces
    READER=reader_peer
    WRITER=writer_peer
    lock=asyncio.Lock()
async def checking_for_message_id_and_taking_action(reader):
    async  with PieceManagerAttempt1.lock:  # locking cuz bitfield is key common route

        message_id, payload=await asyncio.wait_for(recv_any_message_from_peer(reader),timeout=5)
        if message_id==5:
            peer_bitfield=await generating_peer_bitfield(payload)
            await sending_bitfield(PieceManagerAttempt1.WRITER)
            return peer_bitfield

async def generating_peer_bitfield(payload):
    peer_bitfield = bitfield_parser(payload, PieceManagerAttempt1.NUM_PIECES)
    return peer_bitfield

async def sending_bitfield(writer):
    #lets build our bitfield
    writer.write(build_bitfield(PieceManagerAttempt1.set_of_our_piece, PieceManagerAttempt1.NUM_PIECES))
    writer.drain()

