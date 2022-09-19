class Card
    def initialize(rankVal, suit)
        @rankVal = rankVal
        @suit = suit
        return nil
    end

    def toString
        return @rankVal + " " + @suit
    end
end

class Deck < Card
    NUM_CARDS = 54

    def initialize

        suits = ["s", "h", "d", "c"]
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]  
        count = 0  
        @cards = Array.new(NUM_CARDS)
        for i in suits
            for j in ranks
                @cards[count] = Card.new(j, i)
                count += 1
            end
        @cards[NUM_CARDS - 2] = Card.new("Jk", "l")
        @cards[NUM_CARDS - 1] = Card.new("Jk", "b")
        end
    end

    def deal(n)
        if(n <= 0)
            puts("Unacceptable amount of cards.")
        elsif(n > 54)
            n = 54
        end

        for i in 0 ... n
            card = @cards[i].toString
            puts(card)
        end
    end

    def shuffle
        @cards.shuffle!
    end
end

numCards = ARGV[0]
myDeck = Deck.new()
myDeck.shuffle()
myDeck.deal(numCards.to_i)
    


        
