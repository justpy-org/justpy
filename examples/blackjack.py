# This is the "black jack" example for justpy
# see https://github.com/justpy-org/justpy/blob/master/examples/blackjack.py

# Simplified blackjack game using https://deckofcardsapi.com/ API
# Not all rules are implemented

import justpy as jp
import asyncio

card_size = 0.5
card_width = int(226 * card_size)
card_height = int(card_width * 314 / 226)
button_classes = """
inline-flex items-center px-6 py-6 border border-gray-700 text-2xl leading-6 font-bold rounded-md text-gray-700 
bg-white hover:text-gray-500 focus:outline-none focus:border-blue-300 focus:shadow-outline-blue active:text-gray-800 
active:bg-gray-50 transition ease-in-out duration-150
"""
div_classes = "items-center px-6 py-6 border border-gray-700 text-3xl leading-6 font-bold rounded-md text-gray-700; bg-white "


class Card(jp.Img):
    """
    Card component: an extended image with predefined width and height and a transition
    """

    def __init__(self, **kwargs):
        """
        constructor
        """
        super().__init__(**kwargs)
        self.width = card_width
        self.height = card_height
        self.set_class("ml-2")

        self.transition = {
            "load": "transition origin-left ease-out duration-1000",
            "load_start": "transform scale-x-0",
            "load_end": "transform scale-x-100",
            "enter": "transition origin-left ease-out duration-1000",
            "enter_start": "transform scale-x-0",
            "enter_end": "transform scale-x-100",
        }


async def create_deck():
    """
    get a new deck
    """
    deck = await jp.get("https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1")
    return deck["deck_id"]


async def deal(deck_id, count=1):
    """
    deal
    """
    try:
        cards = await jp.get(
            f"https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count={count}"
        )
    except:
        print("error in deal")
    return cards


def hand_value(hand):
    """
    calculate the hand value
    """
    value = 0
    aces = 0
    for card in hand:
        if card.value == "ACE":
            aces += 1
            value += 1
        else:
            try:
                value += int(card.value)
            except:
                value += 10
    if aces and value < 12:
        value += 10
    return value


async def hit(self, msg):
    """
    react on hit button
    """
    wp = msg.page
    card_dict = jp.Dict(await deal(wp.deck_id))
    card = card_dict.cards[0]
    wp.player_hand.append(card)
    wp.player_div.add(Card(src=card.image))
    player_hand_value = hand_value(wp.player_hand)
    if player_hand_value < 22:
        wp.hand_value_div.text = f"Hand value: {player_hand_value}"
    else:
        wp.hand_value_div.text = f"YOU HAVE BUSTED, Hand value: {player_hand_value}"
        dealer_hand_value = hand_value(wp.dealer_hand)
        result_div = jp.Div(classes=div_classes, a=wp.outer_div)
        result_div.text = f"YOU LOST, Your hand: {player_hand_value}, Dealer's hand: {dealer_hand_value}"
        for btn in [wp.stand_btn, wp.hit_btn]:
            btn.disabled = True
            btn.set_classes("cursor-not-allowed bg-gray-200 opacity-50")
        wp.play_again_btn.remove_class("hidden")


async def stand(self, msg):
    """
    react on stand button
    """
    wp = msg.page
    # Show dealer card
    wp.card_back.set_class("hidden")
    wp.down_card.remove_class("hidden")
    for btn in [wp.stand_btn, wp.hit_btn]:
        btn.disabled = True
        btn.set_classes("cursor-not-allowed bg-gray-200 opacity-50")
    await wp.update()
    await asyncio.sleep(1.1)

    while True:
        dealer_hand_value = hand_value(wp.dealer_hand)
        if dealer_hand_value > 16:
            break
        card_dict = jp.Dict(await deal(wp.deck_id))
        card = card_dict.cards[0]
        wp.dealer_hand.append(card)
        wp.dealer_div.add(Card(src=card.image))
        await wp.update()
        await asyncio.sleep(1.1)
    player_hand_value = hand_value(wp.player_hand)
    result_div = jp.Div(classes=div_classes, a=wp.outer_div)
    if (dealer_hand_value > 21) or (dealer_hand_value < player_hand_value):
        result_div.text = f"YOU WON, Your hand: {player_hand_value}, Dealer's hand: {dealer_hand_value}"
    elif dealer_hand_value > player_hand_value:
        result_div.text = f"YOU LOST, Your hand: {player_hand_value}, Dealer's hand: {dealer_hand_value}"
    else:
        result_div.text = f"IT IS A DRAW, Your hand: {player_hand_value}, Dealer's hand: {dealer_hand_value}"

    wp.play_again_btn.remove_class("hidden")


async def play_again(self, msg):
    """
    react on play again button
    """
    wp = msg.page
    await wp.reload()


async def blackjack():
    """
    the async web page to serve
    """
    wp = jp.WebPage()
    wp.outer_div = jp.Div(
        classes="container mx-auto px-4 sm:px-6 lg:px-8 space-y-5", a=wp
    )
    wp.deck_id = await create_deck()
    # Deal initial four cards
    cards = jp.Dict(await deal(wp.deck_id, 4))
    wp.player_hand = [cards.cards[0], cards.cards[2]]
    wp.dealer_hand = [cards.cards[1], cards.cards[3]]
    jp.Div(
        text="Blackjack Demo",
        a=wp.outer_div,
        classes="m-2 p-4 text-3xl font-bold leading-7 text-gray-900  sm:leading-9 sm:truncate",
    )
    wp.dealer_div = jp.Div(classes="flex flex-wrap m-2", a=wp.outer_div)
    # Image of back of card
    wp.card_back = Card(
        src="https://raw.githubusercontent.com/elimintz/elimintz.github.io/master/card_back.png",
        a=wp.dealer_div,
    )
    wp.down_card = Card(src=wp.dealer_hand[0].image, a=wp.dealer_div, classes="hidden")
    Card(src=wp.dealer_hand[1].image, a=wp.dealer_div, style="transition-delay: 1000ms")
    wp.player_div = jp.Div(classes="flex flex-wrap m-2", a=wp.outer_div)
    for card in wp.player_hand:
        Card(src=card.image, a=wp.player_div, style="transition-delay: 2000ms")
    button_div = jp.Div(classes="flex m-2 space-x-6", a=wp.outer_div)
    wp.stand_btn = jp.Button(
        text="Stand", a=button_div, classes=button_classes, click=stand
    )
    wp.hit_btn = jp.Button(text="Hit", a=button_div, classes=button_classes, click=hit)
    wp.play_again_btn = jp.Button(
        text="Play Again", a=button_div, classes=button_classes, click=play_again
    )
    wp.play_again_btn.set_class("hidden")
    wp.hand_value_div = jp.Div(
        text=f"Hand value: {hand_value(wp.player_hand)}",
        a=wp.outer_div,
        classes="text-2xl",
    )
    return wp


from examples.basedemo import Demo

Demo("blackjack demo", blackjack)
