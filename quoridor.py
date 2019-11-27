"""Quoridor - étape 2 - module quoridor"""
from copy import deepcopy
from graphe import construire_graphe


class QuoridorError(Exception):
    pass


class Quoridor:
    def __init__(self, joueurs, murs=None):
        """
        Initialiser une partie de Quoridor avec les joueurs et les murs spécifiés,
        en s'assurant de faire une copie profonde de tout ce qui a besoin d'être copié.

        :param joueurs: un itérable de deux joueurs dont le premier est toujours celui qui
        débute la partie. Un joueur est soit une chaîne de caractères soit un dictionnaire.
        Dans le cas d'une chaîne, il s'agit du nom du joueur. Selon le rang du joueur dans
        l'itérable, sa position est soit (5,1) soit (5,9), et chaque joueur peut initialement
        placer 10 murs. Dans le cas où l'argument est un dictionnaire, celui-ci doit contenir
        une clé 'nom' identifiant le joueur, une clé 'murs' spécifiant le nombre de murs qu'il
        peut encore placer, et une clé 'pos' qui spécifie sa position (x, y) actuelle.

        :param murs: un dictionnaire contenant une clé 'horizontaux' associée à la liste des
        positions (x, y) des murs horizontaux, et une clé 'verticaux' associée à la liste des
        positions (x, y) des murs verticaux. Par défaut, il n'y a aucun mur placé sur le jeu.

        :raises QuoridorError: si l'argument 'joueurs' n'est pas itérable.
        :raises QuoridorError: si l'itérable de joueurs en contient plus de deux.
        :raises QuoridorError: si le nombre de murs qu'un joueur peut placer est >10, ou négatif.
        :raises QuoridorError: si la position d'un joueur est invalide.
        :raises QuoridorError: si l'argument 'murs' n'est pas un dictionnaire lorsque présent.
        :raises QuoridorError: si le total des murs placés et plaçables n'est pas égal à 20.
        :raises QuoridorError: si la position d'un mur est invalide.
        """
        try:
            iter(joueurs)
        except TypeError:
            raise QuoridorError("L'argument 'joueurs' n'est pas itérable")

        if len(joueurs) > 2:
            raise QuoridorError("L'itérable de joueurs en contient plus de deux")

        nb_murs = 0
        self.etat = {"joueurs": [], "murs": None}

        for i, joueur in enumerate(joueurs):
            if isinstance(joueur, dict):
                if not 0 <= joueur["murs"] <= 10:
                    raise QuoridorError("Le nombre de murs qu'un joueur peut placer est >10, ou négatif")

                if len(joueur["pos"]) != 2 or any(not 1 <= x <= 9 for x in joueur["pos"]):
                    raise QuoridorError("La position d'un des joueurs est invalide")

                nb_murs += joueur["murs"]
                self.etat["joueurs"].append(deepcopy(joueur))
            else:
                self.etat["joueurs"].append({"nom": joueur, "murs": 10, "pos": [5, 1 if i == 0 else 9]})

        if murs is not None:
            if not isinstance(murs, dict):
                raise QuoridorError("L'argument 'murs' n'est pas un dictionnaire")

            murs_h, murs_v = murs["horizontaux"], murs["verticaux"]

            for i, mur_h in enumerate(murs_h):
                if not (1 <= mur_h[0] <= 8 and 2 <= mur_h[1] <= 9):
                    raise QuoridorError("La position d'un des murs horizontaux est invalide")

                if any(mur_h[1] == mur_h2[1] and mur_h[0] - 1 <= mur_h2[0] <= mur_h[0] + 1
                       for j, mur_h2 in enumerate(murs_h) if i != j):
                    raise QuoridorError("Deux des murs horizontaux se chevauchent")

            for i, mur_v in enumerate(murs_v):
                if not (2 <= mur_v[0] <= 9 and 1 <= mur_v[1] <= 8):
                    raise QuoridorError("La position d'un des murs verticaux est invalide")

                if any(mur_v[0] == mur_v2[0] and mur_v[1] - 1 <= mur_v2[1] <= mur_v[1] + 1
                       for j, mur_v2 in enumerate(murs_v) if i != j):
                    raise QuoridorError("Deux des murs verticaux se chevauchent")

                if any(mur_h == (mur_v[0] - 1, mur_v[1] + 1) for mur_h in murs_h):
                    raise QuoridorError("Un des murs horizontaux et un des murs verticaux se chevauchent")

            nb_murs += len(murs_h) + len(murs_v)

        if nb_murs != 20:
            raise QuoridorError("Le total des murs placés et plaçables n'est pas égal à 20")

        self.etat["murs"] = {"horizontaux": [], "verticaux": []} if murs is None else deepcopy(murs)

    def __str__(self):
        """
        Produire la représentation en art ascii correspondant à l'état actuel de la partie.
        Cette représentation est la même que celle du TP précédent.

        :returns: la chaîne de caractères de la représentation.
        """
        patron_carres = (" ", ".", " ", " ", " ", ".", " ", " ", " ", ".", " ", " ", " ", ".", " ", " ",
                         " ", ".", " ", " ", " ", ".", " ", " ", " ", ".", " ", " ", " ", ".", " ", " ",
                         " ", ".", " ")
        patron_murs = [" "] * 35
        plateau = []

        # génération du plateau vierge
        for i in range(17):
            if i % 2:
                plateau.append([*patron_murs])  # shallow copy du patron
            else:
                plateau.append([*patron_carres])

        id_joueurs = []

        # plaçage des pions
        for i, joueur in enumerate(self.etat["joueurs"]):
            id_joueur = str(i + 1)
            id_joueurs.append(f'{id_joueur}={joueur["nom"]}')
            ligne = -2 * joueur["pos"][1] + 1
            colonne = 4 * joueur["pos"][0] - 3
            plateau[ligne][colonne] = id_joueur

        patron_mur_h = ("-", "-", "-", "-", "-", "-", "-")

        # plaçage des murs horizontaux
        for mur_h in self.etat["murs"]["horizontaux"]:
            ligne = -2 * mur_h[1] + 2
            colonne = 4 * mur_h[0] - 4
            plateau[ligne][colonne: colonne + len(patron_mur_h)] = patron_mur_h

        # plaçage des murs verticaux
        for mur_v in self.etat["murs"]["verticaux"]:
            ligne = -2 * mur_v[1] + 1
            colonne = 4 * mur_v[0] - 5
            for i in range(ligne, ligne - 3, -1):
                plateau[i][colonne] = "|"

        # ajout des numéros de ligne
        for i, ligne in enumerate(plateau):
            num_ligne = " " if i % 2 else 9 - (i + 1) // 2
            ligne = "".join(ligne)
            plateau[i] = f'{num_ligne} |{ligne}|'

        # concaténation des morceaux du plateau
        return "".join(("Légende: ", ", ".join(id_joueurs), "\n",
                        "   -----------------------------------\n",
                        "\n".join(plateau), "\n",
                        "--|-----------------------------------\n",
                        "  | 1   2   3   4   5   6   7   8   9",))

    def déplacer_jeton(self, joueur, position):
        """
        Pour le joueur spécifié, déplacer son jeton à la position spécifiée.

        :param joueur: un entier spécifiant le numéro du joueur (1 ou 2).
        :param position: le tuple (x, y) de la position du jeton (1<=x<=9 et 1<=y<=9).
        :raises QuoridorError: si le numéro du joueur est autre que 1 ou 2.
        :raises QuoridorError: si la position est invalide (en dehors du damier).
        :raises QuoridorError: si la position est invalide pour l'état actuel du jeu.
        """
        adversaire = self.etat["joueurs"][0]["pos"]
        pos = self.etat["joueurs"][joueur - 1]["pos"]# joueur -1 = joueur actuel
        if joueur == 1:
            adversaire = self.etat["joueurs"][1]["pos"]
        if (adversaire[0] == position[0]) and (adversaire[1] == position[1]) or (pos[0] == position[0]) and (pos[1] == position[1]):
            raise QuoridorError("la position est invalide pour l'état actuel du jeu.")#test si c'est la position du joueur actuel ou de l'adversaire
        if not ((1 <= position[0] <= 9) and (1 <= position[1] <= 9)):
            raise QuoridorError("La position est invalide (en dehors du damier).")
        if position in self.etat["murs"]["verticaux"] or position in self.etat["murs"]["horizontaux"]:
            raise QuoridorError("La position est invalide pour l'état actuel du jeu.")
        if joueur != 1 and joueur != 2:
            raise QuoridorError("Le numéro du joueur est autre que 1 ou 2.")
        if not((abs(position[0] - pos[0]) == 1 and position[1] == pos[1]) or #si on bouge x il faut que y reste le meme , si on bouge x, y doit rester le meme
            (abs(position[1] - pos[1]) == 1 and position[0] == pos[0])): # si difference des x = 1 ca veut dire qu'on a fait juste un pas, y = 0
            if (abs(position[0] - adversaire[0]) == 1) and (abs(pos[0] - adversaire[0]) == 1) and (position[1] == adversaire[1]) and (adversaire[1] == pos[1]): #verifie si jouer 1 et 2 on des x différent de 1 et meme y
                self.etat["joueurs"][joueur - 1 ]["pos"] = position
            else:
                if (abs(position[1] - adversaire[1]) == 1) and (abs(pos[1] - adversaire[1]) == 1) and (position[0] == adversaire[0]) and (adversaire[0] == pos[0]): #verifie si jouer 1 et 2 on des x différent de 1 et meme y
                    self.etat["joueurs"][joueur - 1 ]["pos"] = position
                else:
                    raise QuoridorError("La position est invalide pour l'état actuel du jeu.")
        else:
            self.etat["joueurs"][joueur - 1 ]["pos"] = position





    def état_partie(self):
        """
        Produire l'état actuel de la partie.

        :returns: une copie de l'état actuel du jeu sous la forme d'un dictionnaire:
        {
            'joueurs': [
                {'nom': nom1, 'murs': n1, 'pos': (x1, y1)},
                {'nom': nom2, 'murs': n2, 'pos': (x2, y2)},
            ],
            'murs': {
                'horizontaux': [...],
                'verticaux': [...],
            }
        }

        où la clé 'nom' d'un joueur est associée à son nom, la clé 'murs' est associée
        au nombre de murs qu'il peut encore placer sur ce damier, et la clé 'pos' est
        associée à sa position sur le damier. Une position est représentée par un tuple
        de deux coordonnées x et y, où 1<=x<=9 et 1<=y<=9.

        Les murs actuellement placés sur le damier sont énumérés dans deux listes de
        positions (x, y). Les murs ont toujours une longueur de 2 cases et leur position
        est relative à leur coin inférieur gauche. Par convention, un mur horizontal se
        situe entre les lignes y-1 et y, et bloque les colonnes x et x+1. De même, un
        mur vertical se situe entre les colonnes x-1 et x, et bloque les lignes y et y+1.
        """
        pass

    def jouer_coup(self, joueur):
        """
        Pour le joueur spécifié, jouer automatiquement son meilleur coup pour l'état actuel
        de la partie. Ce coup est soit le déplacement de son jeton, soit le placement d'un
        mur horizontal ou vertical.

        :param joueur: un entier spécifiant le numéro du joueur (1 ou 2).
        :raises QuoridorError: si le numéro du joueur est autre que 1 ou 2.
        :raises QuoridorError: si la partie est déjà terminée.
        """
        pass

    def partie_terminée(self):
        """
        Déterminer si la partie est terminée.

        :returns: le nom du gagnant si la partie est terminée; False autrement.
        """
        robot = self.etat["joueurs"][1]["pos"]
        joueur = self.etat["joueurs"][0]["pos"]# joueur -1 = joueur actuel

        if joueur[1] == 9:
            return self.etat["joueurs"][0]["nom"]
        else:
            if robot[1] == 1:
                return self.etat["joueurs"][1]["nom"]
            else:
                return False

    def placer_mur(self, joueur, position, orientation):
        """
        Pour le joueur spécifié, placer un mur à la position spécifiée.

        :param joueur: le numéro du joueur (1 ou 2).
        :param position: le tuple (x, y) de la position du mur.
        :param orientation: l'orientation du mur ('horizontal' ou 'vertical').
        :raises QuoridorError: si le numéro du joueur est autre que 1 ou 2.
        :raises QuoridorError: si un mur occupe déjà cette position.
        :raises QuoridorError: si la position est invalide pour cette orientation.
        :raises QuoridorError: si le joueur a déjà placé tous ses murs.
        """
        pass

if __name__=="__main__":

    jeu = Quoridor(["dapep19", "robot"])
    print(jeu)

