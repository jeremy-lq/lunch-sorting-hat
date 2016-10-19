#!/usr/bin/env python
import logging
import os
import random

from slackclient import SlackClient

log = logging.getLogger(__name__)


def main():
    slack_token = os.environ['SLACK_TOKEN']
#    bot_user = os.environ['BOT_USER']
    lunch_room = os.environ.get('LUNCH_CHAN', 'randomlunch')
    target_grp_size = os.environ.get('LUNCH_SIZE', 4)

    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

    client = SlackClient(slack_token)

    all_channels = client.api_call('channels.list')
    lunch_cid = None
    for channel in all_channels['channels']:
        if channel['name'] == lunch_room:
            lunch_cid = channel['id']
    lunch_info = client.api_call('channels.info', channel=lunch_cid)
    members = lunch_info['channel']['members']

    for group in make_groups(members, target_grp_size):
        user_strs = ['<@%s>' % uid for uid in group]
        text = "Hey %s, y'all are lunch friends!" % ', '.join(user_strs)
        print text
        client.api_call('chat.postMessage', channel=lunch_cid, text=text)


# TODO: actually do something with target_grp_size. right now it's assumed to be 4
def make_groups(lst, target_grp_size):
    random.shuffle(lst)
    group_sizes = get_sizes(len(lst))
    groups = []
    pointer = 0
    for size in group_sizes:
        groups.append(lst[pointer:pointer+size])
        pointer += size
    return groups


def get_sizes(num):
    sizes = []
    while num > 0:
        sizes.append(bite_off_chunk(num))
        num -= sizes[-1]
    return sizes


def bite_off_chunk(num):
    if num <= 5:
        return num
    elif num == 6:
        return 3
    else:
        return 4


if __name__ == '__main__':
    main()
