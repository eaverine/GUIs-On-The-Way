import turtle

turtle.setup(400,500)
wn = turtle.Screen()
wn.title('Mouse_Control')
wn.bgcolor('lightgreen')

tess = turtle.Turtle()
tess.color('purple')
tess.pensize(3)
tess.shape('circle')

def h1(x,y):
    tess.goto(x,y)

wn.onclick(h1)
wn.mainloop()
