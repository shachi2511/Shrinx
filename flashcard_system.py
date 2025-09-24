import random

class FlashcardSystem:
    def __init__(self):
        self.current_card = 0
        self.cards = []
    
    def parse_flashcards(self, flashcard_text):
        """Parse flashcards from AI-generated text"""
        cards = []
        card_blocks = flashcard_text.split('---')
        
        for block in card_blocks:
            lines = block.strip().split('\n')
            question = ""
            answer = ""
            
            for line in lines:
                if line.startswith('Q:'):
                    question = line.split(':', 1)[1].strip()
                elif line.startswith('A:'):
                    answer = line.split(':', 1)[1].strip()
            
            if question and answer:
                cards.append({
                    'question': question,
                    'answer': answer
                })
        
        return cards
    
    def study_flashcards(self, cards):
        """Interactive flashcard study session"""
        if not cards:
            print("No flashcards available!")
            return
        
        self.cards = cards
        print(f"\n🃏 Starting Flashcard Study Session!")
        print(f"Total cards: {len(cards)}")
        print("Commands: 'n' = next, 'p' = previous, 'r' = random, 's' = shuffle, 'q' = quit")
        print("=" * 60)
        
        self.current_card = 0
        shuffled = False
        
        while True:
            self.show_flashcard(self.current_card)
            
            command = input("\nPress Enter to reveal answer, or enter command: ").strip().lower()
            
            if command == '':
                # Show answer
                print(f"\n💡 Answer: {self.cards[self.current_card]['answer']}")
                
                while True:
                    next_action = input("\nHow did you do? (e)asy, (h)ard, (n)ext, (p)rev, (q)uit: ").lower()
                    if next_action in ['e', 'easy']:
                        print("Great! 🌟")
                        self.next_card()
                        break
                    elif next_action in ['h', 'hard']:
                        print("No worries, keep practicing! 💪")
                        self.next_card()
                        break
                    elif next_action in ['n', 'next']:
                        self.next_card()
                        break
                    elif next_action in ['p', 'prev']:
                        self.prev_card()
                        break
                    elif next_action in ['q', 'quit']:
                        return
                    else:
                        print("Please enter e, h, n, p, or q")
            
            elif command in ['n', 'next']:
                self.next_card()
            elif command in ['p', 'prev', 'previous']:
                self.prev_card()
            elif command in ['r', 'random']:
                self.current_card = random.randint(0, len(self.cards) - 1)
            elif command in ['s', 'shuffle']:
                random.shuffle(self.cards)
                self.current_card = 0
                print("🔀 Cards shuffled!")
                shuffled = True
            elif command in ['q', 'quit']:
                break
            else:
                print("Unknown command. Use 'n', 'p', 'r', 's', or 'q'")
        
        print("\n📚 Study session completed! Great work!")
    
    def show_flashcard(self, index):
        """Display current flashcard"""
        print("\n" + "=" * 60)
        print(f"Card {index + 1} of {len(self.cards)}")
        print("=" * 60)
        print(f"❓ Question: {self.cards[index]['question']}")
        print("=" * 60)
    
    def next_card(self):
        """Move to next card"""
        self.current_card = (self.current_card + 1) % len(self.cards)
    
    def prev_card(self):
        """Move to previous card"""
        self.current_card = (self.current_card - 1) % len(self.cards)