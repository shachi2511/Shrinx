import re
import random

class QuizSystem:
    def __init__(self):
        self.score = 0
        self.total_questions = 0
    
    def parse_mcq_questions(self, mcq_text):
        """Parse MCQ questions from AI-generated text"""
        questions = []
        question_blocks = mcq_text.split('\n\n')
        
        for block in question_blocks:
            if 'Q' in block and 'A)' in block:
                lines = block.strip().split('\n')
                question = ""
                options = []
                correct = ""
                explanation = ""
                
                for line in lines:
                    if line.startswith('Q'):
                        question = line.split(':', 1)[1].strip() if ':' in line else line
                    elif line.startswith(('A)', 'B)', 'C)', 'D)')):
                        options.append(line.strip())
                    elif line.startswith('Correct:'):
                        correct = line.split(':', 1)[1].strip()
                    elif line.startswith('Explanation:'):
                        explanation = line.split(':', 1)[1].strip()
                
                if question and len(options) == 4 and correct:
                    questions.append({
                        'question': question,
                        'options': options,
                        'correct': correct.upper(),
                        'explanation': explanation
                    })
        
        return questions
    
    def parse_fill_blanks(self, fb_text):
        """Parse fill-in-the-blank questions"""
        questions = []
        question_blocks = fb_text.split('\n\n')
        
        for block in question_blocks:
            lines = block.strip().split('\n')
            question = ""
            answer = ""
            explanation = ""
            
            for line in lines:
                if line.startswith('Q:'):
                    question = line.split(':', 1)[1].strip()
                elif line.startswith('A:'):
                    answer = line.split(':', 1)[1].strip()
                elif line.startswith('Explanation:'):
                    explanation = line.split(':', 1)[1].strip()
            
            if question and answer:
                questions.append({
                    'question': question,
                    'answer': answer,
                    'explanation': explanation
                })
        
        return questions
    
    def parse_true_false(self, tf_text):
        """Parse true/false questions"""
        questions = []
        question_blocks = tf_text.split('\n\n')
        
        for block in question_blocks:
            lines = block.strip().split('\n')
            question = ""
            answer = ""
            explanation = ""
            
            for line in lines:
                if line.startswith('Q:'):
                    question = line.split(':', 1)[1].strip()
                elif line.startswith('A:'):
                    answer = line.split(':', 1)[1].strip()
                elif line.startswith('Explanation:'):
                    explanation = line.split(':', 1)[1].strip()
            
            if question and answer:
                questions.append({
                    'question': question,
                    'answer': answer,
                    'explanation': explanation
                })
        
        return questions
    
    def play_mcq_quiz(self, questions):
        """Play MCQ quiz"""
        if not questions:
            print("No MCQ questions available!")
            return
        
        print(f"\n🎯 Starting MCQ Quiz! ({len(questions)} questions)")
        print("=" * 50)
        
        self.score = 0
        self.total_questions = len(questions)
        
        for i, q in enumerate(questions, 1):
            print(f"\nQuestion {i}: {q['question']}")
            for option in q['options']:
                print(f"  {option}")
            
            while True:
                answer = input("\nYour answer (A/B/C/D): ").upper().strip()
                if answer in ['A', 'B', 'C', 'D']:
                    break
                print("Please enter A, B, C, or D")
            
            if answer == q['correct']:
                print("✅ Correct! Good going!")
                self.score += 1
            else:
                print(f"❌ Wrong! The correct answer is {q['correct']}")
            
            if q['explanation']:
                print(f"💡 Explanation: {q['explanation']}")
            
            input("\nPress Enter to continue...")
        
        self.show_final_score()
    
    def play_fill_blanks_quiz(self, questions):
        """Play fill-in-the-blanks quiz"""
        if not questions:
            print("No fill-in-the-blank questions available!")
            return
        
        print(f"\n📝 Starting Fill-in-the-Blanks Quiz! ({len(questions)} questions)")
        print("=" * 50)
        
        self.score = 0
        self.total_questions = len(questions)
        
        for i, q in enumerate(questions, 1):
            print(f"\nQuestion {i}: {q['question']}")
            user_answer = input("Your answer: ").strip()
            
            # Simple answer checking (case-insensitive)
            if user_answer.lower() == q['answer'].lower():
                print("✅ Correct! Good going!")
                self.score += 1
            elif self.check_partial_match(user_answer.lower(), q['answer'].lower()):
                print("🟡 Nearly there! Close enough!")
                self.score += 0.5
            else:
                print(f"❌ Wrong! The correct answer is: {q['answer']}")
            
            if q['explanation']:
                print(f"💡 Explanation: {q['explanation']}")
            
            input("\nPress Enter to continue...")
        
        self.show_final_score()
    
    def play_true_false_quiz(self, questions):
        """Play true/false quiz"""
        if not questions:
            print("No true/false questions available!")
            return
        
        print(f"\n✓❌ Starting True/False Quiz! ({len(questions)} questions)")
        print("=" * 50)
        
        self.score = 0
        self.total_questions = len(questions)
        
        for i, q in enumerate(questions, 1):
            print(f"\nQuestion {i}: {q['question']}")
            
            while True:
                answer = input("Your answer (True/False or T/F): ").strip().lower()
                if answer in ['true', 't', 'false', 'f']:
                    break
                print("Please enter True/False or T/F")
            
            # Normalize answers
            user_answer = 'true' if answer in ['true', 't'] else 'false'
            correct_answer = q['answer'].lower()
            
            if user_answer == correct_answer:
                print("✅ Correct! Good going!")
                self.score += 1
            else:
                print(f"❌ Wrong! The correct answer is: {q['answer']}")
            
            if q['explanation']:
                print(f"💡 Explanation: {q['explanation']}")
            
            input("\nPress Enter to continue...")
        
        self.show_final_score()
    
    def check_partial_match(self, user_answer, correct_answer):
        """Check if user answer is partially correct"""
        # Simple similarity check
        words_user = set(user_answer.split())
        words_correct = set(correct_answer.split())
        
        if len(words_correct) == 0:
            return False
        
        overlap = len(words_user.intersection(words_correct))
        similarity = overlap / len(words_correct)
        
        return similarity >= 0.6  # 60% similarity threshold
    
    def show_final_score(self):
        """Show final quiz score"""
        percentage = (self.score / self.total_questions) * 100
        
        print("\n" + "=" * 50)
        print("🏆 QUIZ COMPLETED!")
        print("=" * 50)
        print(f"Your Score: {self.score}/{self.total_questions} ({percentage:.1f}%)")
        
        if percentage >= 90:
            print("🌟 Excellent! You're a star!")
        elif percentage >= 80:
            print("🎉 Great job! Well done!")
        elif percentage >= 70:
            print("👏 Good work! Keep it up!")
        elif percentage >= 60:
            print("📚 Not bad! Try reviewing the material again.")
        else:
            print("💪 Keep studying! You'll get there!")
        
        print("=" * 50)