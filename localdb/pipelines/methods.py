

import localdb.leveldb.utils as leveldb

import logging
import rapidjson

logger = logging.getLogger(__name__)


class Methods:

    @staticmethod
    def deal_block(block):
        """Write the block obj to leveldb

        Args:
            block(bytes) —— json string of bigchain block obj

        Returns:

        """

        conn_header = leveldb.LocalDBPool().conn['header']
        conn_bigchain = leveldb.LocalDBPool().conn['bigchain']
        block = bytes(block).decode()
        block_json_str = block
        block = rapidjson.loads(block)
        # logger.info('block deal ing...' + str(block))
        block_id = block['id']
        # logger.info('block_id is : ' + str(block_json_str))
        block_num = leveldb.get(conn_header, 'block_num')
        block_num = int(block_num)
        block_num = block_num + 1
        leveldb.insert(conn_bigchain, block_id, block_json_str,sync=False)
        leveldb.update(conn_header, 'current_block_id', block_id,sync=False)
        leveldb.update(conn_header, 'block_num', block_num,sync=False)
        Methods.get_base_info(conn_header,conn_bigchain)

    @staticmethod
    def deal_vote(vote):
        """Write the block obj to leveldb

        Args:
            vote(bytes) —— json string of bigchain vote obj

        Returns:

        """

        conn_votes = leveldb.LocalDBPool().conn['votes']
        vote = bytes(vote).decode()
        vote_json_str = vote
        vote = rapidjson.loads(vote)
        # logger.info('vote deal ing... ' + str(vote_json_str))
        previous_block = vote['vote']['previous_block']
        node_pubkey = vote['node_pubkey']
        vote_key = previous_block + '-' + node_pubkey
        # logger.info('vote_key:\n' + str(vote_key))
        leveldb.insert(conn_votes, vote_key, vote_json_str,sync=False)
        # Methods.get_votes_for_block(conn_votes,previous_block)


    @staticmethod
    def get_base_info(conn_header,conn_bigchain):
        current_bid = leveldb.get(conn_header,'current_block_id')
        logger.info('block_num: ' + str(leveldb.get(conn_header,'block_num')) + ',\ncurrent_block_id ' +
                    current_bid)
        # logger.info('current_block: ' + str(leveldb.get(conn_bigchain,current_bid)))


    @staticmethod
    def get_votes_for_block(conn_votes, block_id):
        votess = leveldb.get_prefix(conn_votes, block_id + '-')
        logger.info(str(block_id) + ' votes :\n' + str(votess))