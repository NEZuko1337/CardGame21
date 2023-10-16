from links_to_photos import *

def img_for_card(card_number: int):
    match card_number:
        case 2:
            return link_to_2
        case 3:
            return link_to_3
        case 4:
            return link_to_4
        case 5:
            return link_to_5
        case 6:
            return link_to_6
        case 7:
            return link_to_7
        case 8:
            return link_to_8
        case 9:
            return link_to_9
        case 10:
            return link_to_10
        case 11:
            return link_to_11
        case _:
            return None

