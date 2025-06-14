import itertools


def make_combination(list, number_of_comb):
    return itertools.combinations(list, number_of_comb)


def make_deck():
    deck = []
    for i in itertools.combinations(itertools.chain(suits, ranks), 2):
        if (i[0] in suits and i[1] not in suits) or (i[0] in ranks and i[1] not in ranks):
            deck.append(i[0] + i[1])
    return deck
if __name__ =="__main__":

    suits = ['♥', '♠', '♦', '♣']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

    deck = make_deck()
    for i in make_combination(deck,5):
        print(i)