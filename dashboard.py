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
    
    def draw(self):
        arcade.draw_lrtb_rectangle_filled(self.left, self.right, self.top, self.bottom, self.color)

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
        i = randint(0,len(TEST_QUESTIONS)-1)
        self._question = TEST_QUESTIONS[i][0]
        self._answer = TEST_QUESTIONS[i][1]
        return self._question 
    
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




    


