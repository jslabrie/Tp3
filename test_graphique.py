import turtle


état_actuel = {
    "joueurs": [
        {"nom": "idul", "murs": 7, "pos": [2, 3]}, 
        {"nom": "automate", "murs": 3, "pos": [8, 6]}
    ], 
    "murs": {
        "horizontaux": [[5, 4], [2, 6], [3, 8], [5, 8], [7, 8]], 
        "verticaux": [[6, 2], [4, 4], [2, 6], [7, 5], [7, 7]]
    }
}



# Initialisation du graphique
écran = turtle.Screen()
écran.setup(width=600, height=600)
écran.bgcolor('white')
écran.title('Jeu Quoridor')

pen = turtle.Turtle()
pen.speed(0)
pen.pu()
pen.setx(-250)
pen.sety(-250)
pen.pd()

# Création graphique

# Contour
pen.color('black', 'yellow')
pen.width(4)
pen.begin_fill()
for i in range(2):
    pen.forward(500)
    pen.left(90)
    pen.forward(500)
    pen.left(90)
pen.end_fill()

pen.color('black', 'gray')
pen.begin_fill()
pen.forward(500)
pen.left(90)
pen.forward(50)
pen.left(90)
pen.forward(450)
pen.right(90)
pen.forward(450)
pen.left(90)
pen.forward(50)
pen.left(90)
pen.forward(500)
pen.end_fill()
pen.pd()


# Colonnes
pen.setx(-250)
pen.sety(-250)
pen.left(90)
pen.width(2)
for i in range(5):
    pen.pu()
    pen.forward(50)
    pen.left(90)
    pen.pd()
    pen.forward(500)
    pen.left(-90)
    pen.pu()
    pen.forward(50)
    pen.left(-90)
    pen.pd()
    pen.forward(500)
    pen.left(90)

# Lignes
for i in range(5):
    pen.left(90)
    pen.pu()
    pen.forward(50)
    pen.left(90)
    pen.pd()
    pen.forward(500)
    pen.right(90)
    pen.pu()  
    pen.forward(50)
    pen.right(90)
    pen.pd()
    pen.forward(500)

# Chiffres lignes
pen.setx(-250)
pen.sety(-250)
pen.pu()
pen.left(90)
pen.forward(10)
pen.right(90)
pen.forward(42)
for i in range(9):
    pen.forward(25)
    pen.write(i+1, font=('Time', 30, 'normal'))
    pen.forward(25)


# Chriffres colonne
pen.setx(-250)
pen.sety(-250)
pen.forward(17)
pen.left(90)
pen.forward(37)
for i in range(9):
    pen.forward(25)
    pen.write(i+1, font=('Time', 30, 'normal'))
    pen.forward(25)

# Placer joueurs
pen.setx(-200)
pen.sety(-200)
pen.right(90)

position_joueur = état_actuel['joueurs'][0]['pos']
pen.forward(25)
pen.forward(50 * (position_joueur[0]-1))
pen.left(90)
pen.forward(25)
pen.forward(50 * (position_joueur[1]-1))
pen.pd()
pen.dot(40, 'green')
pen.pu()
pen.backward(13)
pen.left(90)
pen.forward(5)
pen.pd()
pen.write('1', font=('Time', 20, 'normal'))
pen.pu()

pen.setx(-200)
pen.sety(-200)
pen.right(180)

position_joueur = état_actuel['joueurs'][1]['pos']
pen.forward(25)
pen.forward(50 * (position_joueur[0]-1))
pen.left(90)
pen.forward(25)
pen.forward(50 * (position_joueur[1]-1))
pen.pd()
pen.dot(40, 'turquoise')
pen.pu()
pen.backward(13)
pen.left(90)
pen.forward(5)
pen.write('2', font=('Time', 20, 'normal'))
pen.pu()

# Placer murs
pen.color('red')
pen.width(6)
pen.setx(-200)
pen.sety(-200)
pen.right(90)

position_murs = état_actuel['murs']['horizontaux']
for x in position_murs:
    pen.forward(50 * (x[1]-1))
    pen.right(90)
    pen.forward(50 * (x[0]-1))
    pen.pd()
    pen.forward(25)
    pen.forward(75)
    pen.pu()
    pen.setx(-200)
    pen.sety(-200)
    pen.left(90)


pen.right(90)
position_murs = état_actuel['murs']['verticaux']
for y in position_murs:
    pen.forward(50 * (y[0]-1))
    pen.left(90)
    pen.forward(50 * (y[1]-1))
    pen.pd()
    pen.forward(25)
    pen.forward(75)
    pen.pu()
    pen.setx(-200)
    pen.sety(-200)
    pen.right(90)
    





turtle.done()
