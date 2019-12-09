"""Quoridor - module quoridorx"""
import turtle
from quoridor import Quoridor


class QuoridorX(Quoridor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.afficher()

    def afficher(self):
        # config damier

        taille_case = 30
        marge_case = 20
        nb_rangees = 9
        xy_offset = - (taille_case * nb_rangees + marge_case * (nb_rangees - 1)) / 2 \
                    - taille_case - marge_case
        xy_incr = taille_case + marge_case
        taille_police = 18

        def pos_damier(num_case):
            return num_case * xy_incr + xy_offset

        turtle.Screen().tracer(0, 0)  # gèle fenêtre
        turtle.clear()
        turtle.penup()

        # dessin damier

        turtle.color("lightgray")
        turtle.pensize(5)
        turtle.setheading(90)

        for x in range(1, nb_rangees + 1):
            for y in range(1, nb_rangees + 1):
                turtle.setpos(pos_damier(x), pos_damier(y))
                turtle.pendown()
                turtle.begin_fill()

                for _ in range(4):
                    turtle.forward(taille_case)
                    turtle.right(90)

                turtle.end_fill()
                turtle.penup()

        # config murs

        longueur_mur = taille_case * 2.4 + marge_case
        recul_mur = taille_case * 0.2
        offset_mur = marge_case / 2

        turtle.color("black")

        # dessin murs h

        turtle.setheading(0)

        for mur_h in self.etat.get("murs")["horizontaux"]:
            turtle.setpos(pos_damier(mur_h[0]) - recul_mur, pos_damier(mur_h[1]) - offset_mur)
            turtle.pendown()
            turtle.forward(longueur_mur)
            turtle.penup()

        # dessin murs v

        turtle.setheading(90)

        for mur_v in self.etat.get("murs")["verticaux"]:
            turtle.setpos(pos_damier(mur_v[0]) - offset_mur, pos_damier(mur_v[1]) - recul_mur)
            turtle.pendown()
            turtle.forward(longueur_mur)
            turtle.penup()

        # config pions

        offset_pion = taille_case / 2
        taille_pion = 30

        # dessin pions

        turtle.color("white")

        for i, joueur in enumerate(self.etat["joueurs"]):
            turtle.setpos(pos_damier(joueur["pos"][0]) + offset_pion,
                          pos_damier(joueur["pos"][1]) + offset_pion)
            turtle.dot(taille_pion, "forestgreen" if i == 0 else "firebrick")
            turtle.setpos(pos_damier(joueur["pos"][0]) + offset_pion,
                          pos_damier(joueur["pos"][1]))
            turtle.write(str(i+1), font=("", taille_police), align="center")

        # dessin nombres

        turtle.color("black")

        for i in range(1, nb_rangees+1):
            turtle.setpos(pos_damier(i) + offset_pion, pos_damier(0) + offset_pion)  # hor
            turtle.write(str(i), font=("", taille_police), align="center")
            turtle.setpos(pos_damier(0) + taille_case, pos_damier(i))  # ver
            turtle.write(str(i), font=("", taille_police), align="center")

        # dessin légende

        id_joueurs = [f'{i+1}={joueur["nom"]}' for i, joueur in enumerate(self.etat["joueurs"])]
        turtle.setpos(pos_damier(1), pos_damier(10) - marge_case/2)
        turtle.write("Légende: " + ", ".join(id_joueurs), font=("", 14))

        # plaçage des pions

        for i, joueur in enumerate(self.etat["joueurs"]):
            id_joueur = str(i + 1)
            id_joueurs.append(f'{id_joueur}={joueur["nom"]}')

        # affichage

        turtle.hideturtle()
        turtle.title("QuoridorX")
        turtle.update()  # dégèle fenêtre


# test
if __name__ == "__main__":
    QuoridorX(joueurs=[
        {"nom": "henri", "murs": 0, "pos": (5, 1)},
        {"nom": "robot", "murs": 0, "pos": (5, 9)}
    ], murs={
        "horizontaux": [(2, 2), (2, 3), (2, 4), (2, 5), (2, 6),
                        (2, 7), (2, 8), (2, 9), (4, 2), (4, 3)],
        "verticaux": [(2, 2), (2, 4), (2, 6), (2, 8), (4, 2),
                      (4, 4), (4, 6), (4, 8), (6, 2), (6, 4)]
    })
    turtle.mainloop()
