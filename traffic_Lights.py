import turtle

turtle.setup(400,500)
wn = turtle.Screen()
wn.title('Tess Traffic Controller')
wn.bgcolor('lightgreen')
tess = turtle.Turtle()

def model():
    tess.pensize(3)
    tess.color('black','darkgrey')
    tess.begin_fill()
    tess.forward(80)
    tess.left(90)
    tess.forward(200)
    tess.circle(40,180)
    tess.forward(200)
    tess.left(90)
    tess.end_fill()

model()

tess.penup()

tess.forward(40)
tess.left(90)
tess.forward(50)
tess.shape('circle')
tess.shapesize(3)
tess.fillcolor('green')

state = 0

def advanced_state():
    global state
    if state == 0:
        tess.forward(70)
        tess.fillcolor('orange')
        state = 1
    elif state == 1:
        tess.forward(70)
        tess.fillcolor('red')
        state = 2
    else:
        tess.back(140)
        tess.fillcolor('green')
        state = 0

wn.onkey(advanced_state, 'space')

wn.listen()
wn.mainloop()
