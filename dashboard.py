from globals import *

TEST_QUESTIONS = [("3*12", 26),("13-5", 8), ("4*7",28),("3.5+2.5",6)]


class Dashboard:
    def __init__(self):
        self.color = arcade.color.DARK_GRAY
        self.left = 0
        self.right = RELOAD_BOX_WIDTH
        self.top = SCREEN_HEIGHT
        self.bottom = 0
        self.math = Math()
        self.question = self.math.question
        self.answer = self.math.answer
        self.keys = [arcade.key.A, arcade.key.S, arcade.key.D, arcade.key.F]

        self.answers = {arcade.key.A : 0, arcade.key.S : 0, arcade.key.D : 0, arcade.key.F : 0}
    
    def draw(self):
        arcade.draw_lrtb_rectangle_filled(self.left, self.right, self.top, self.bottom, self.color)

        arcade.draw_text(f"{self.question}={self.answer}",self.left+(self.right//2), SCREEN_HEIGHT//2, arcade.color.AIR_FORCE_BLUE)
        
    def check_answer(self, key):
        correct = self.answers[key] == self.answer
        self.get_question()
        return correct

    def get_question(self):
        self.question = self.math.question
        self.answer = self.math.answer
        correct = choice(self.keys)
        self.answers[correct] = self.answer
        for key in self.answers:
            if key != correct:
                false_answer = randint(0,100)
                self.answers[correct] = false_answer


class Math:
    def __init__(self):
        #self._question = ""
        self.answers = {arcade.key.A : "", arcade.key.S : "",\
            arcade.key.D : "", arcade.key.F : ""} 
        
    @property
    def question(self):
        """
        Getter
        Assign self.question to new question:
            Phase 1 - hard coded questions
            Phase 2 - get questions from API
        """
        my_operators = {'+':self.add, '-':self.sub, '*':self.mult, '/':self.div}
        m = randint(2,10)
        n = randint(2,10)
        operator = choice(['+', '-', '/', '*'])
        self._question = f"{m}{operator}{n}"
        self._answer = my_operators[operator](n,m)
        

        # operator = choice(['+', '-', '/', '*'])
        # a = randint(2,10)
        # b = randint(2,10)
        # solution = 0
        # if(operator == '+'):
        #     solution
        # self._question = f'{a}{operator}{b}'
        
        # i = randint(0,len(TEST_QUESTIONS)-1)
        # self._question = TEST_QUESTIONS[i][0]
        # self._answer = TEST_QUESTIONS[i][1]
        return self._question 
    
    def add(self,a,b):
        return sum([a,b])

    def sub(self, a, b):
        return a-b

    def mult(self, a, b):
        return a*b

    def div(self, a ,b):
        return a/b

    @property
    def answer(self):
        return self._answer

    

    def get_key(self, key):
        if self.answer[key] == self.answer:
            print("good job")

    def __str__(self):
        return f"{self.question} = "

# math = Math()
# print(math)
# print(math)
# print(math)




    


