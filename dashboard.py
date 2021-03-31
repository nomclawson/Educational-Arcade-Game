from globals import *


class Key(Sprite):
    """
    Key image
    """
    def __init__(self, x, y):
        super().__init__(filename="images/transparent_key.png")
        self.scale = 1
        self.center_x = x
        self.center_y = y

class Dashboard:
    def __init__(self):
        self.color = arcade.color.DARK_GRAY
        self.left = 0
        self.right = RELOAD_BOX_WIDTH
        self.top = SCREEN_HEIGHT
        self.bottom = 0
        self.math = Math()
        self.question = ""
        self.answer = 0
        self.keys = [arcade.key.A, arcade.key.S, arcade.key.D, arcade.key.F]
        self.answers = {arcade.key.A : 0, arcade.key.S : 0, arcade.key.D : 0, arcade.key.F : 0}
        self.symbols = {arcade.key.A : "A", arcade.key.S : "S", arcade.key.D : "D", arcade.key.F : "F"}
        self.get_question()
        self.keysImages = SpriteList()
        key = Key(SCREEN_WIDTH //2,  SCREEN_HEIGHT // 2)
        self.keysImages.append(key)
    
    def draw(self):
        # The whole  dashbord in gray 
        arcade.draw_lrtb_rectangle_filled(self.left, self.right, self.top, self.bottom, self.color)
        # self.keysImages.draw()
        # Display the querstions and the possible answers
        arcade.draw_text(f"{self.question} = ",self.left+15, SCREEN_HEIGHT//2+70, arcade.color.DARK_BLUE, font_size=30)
        offset = 0
        for key in self.answers:
            value = self.answers[key]
            symbol = self.symbols[key]
            offset -= 30
            arcade.draw_text(f"{symbol}) {value}",self.left+30, SCREEN_HEIGHT//2 + 50 +offset, arcade.color.DARK_BLUE, font_size=24)
        
    def check_answer(self, key):
        correct = self.answers[key] == self.answer
        self.get_question()
        # print(correct)
        return correct
    
    def fake_answer(self, answer):
        # print(answer) -3 - (-3*.5), -3 + (-3*.5)
        if answer > 0:
            false_answer = randint(answer - int(answer * 0.5), answer + int(answer * .5))
        else:
            false_answer = randint(answer + int(answer * 0.5), answer - int(answer * .5))        
        while false_answer in list(self.answers.values()) or false_answer == answer:
            false_answer += randint(1,5)
        
        return false_answer
        
                
    def get_question(self):
        # get new question and answer
        self.question = self.math.question
        self.answer = self.math.answer

        # randomly choose one key to be correct answer
        correct_key = choice(self.keys)
        self.answers[correct_key] = self.answer
        for key in self.answers:
            if self.answers[key] != self.answer:
                # false_answer = randint(0,100)
                # false_answer = self.answer
                # while false_answer in self.answers.values():
                false_answer = self.fake_answer(self.answer)
                
                self.answers[key] = false_answer
                print()
        # print(self.answers)
        # print(self.question, self.answer)
    
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
        my_operators = {'+':self.add, '-':self.sub, 'x':self.mult}
        m = randint(2,10)
        n = randint(2,10)
        operator = choice(['+', '-', 'x'])
        self._question = f"{m} {operator} {n}"
        self._answer = my_operators[operator](m,n)
        
        return self._question 
    
    def add(self,a,b):
        return sum([a,b])

    def sub(self, a, b):
        return a-b

    def mult(self, a, b):
        return a*b

    # def div(self, a ,b):
    #     return a/b

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




    


