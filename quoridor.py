"""Quoridor - étape 2 - module quoridor"""
from copy import deepcopy
from graphe import *


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

        if len(joueurs) != 2:
            raise QuoridorError("Il doit uniquement y avoir 2 joueurs")

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

            graphe = construire_graphe(
                [joueur["pos"] for joueur in self.etat["joueurs"]],
                murs["horizontaux"],
                murs["verticaux"]
            )

            for pos_joueur, dest_joueur in ((self.etat["joueurs"][0]["pos"], "B1"),
                                            (self.etat["joueurs"][1]["pos"], "B2")):
                if not nx.has_path(graphe, pos_joueur, dest_joueur):
                    raise QuoridorError("Un des joueurs est emprisonné par des murs")

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
        patron_carres = list(" | .   .   .   .   .   .   .   .   . |")
        patron_murs = list("  |                                   |")
        plateau = []

        # génération du plateau vierge
        num_ligne = 9
        for i in range(17):
            if i % 2:
                plateau.append([*patron_murs])  # shallow copy du patron
            else:
                plateau.append([str(num_ligne)] + patron_carres)
                num_ligne -= 1

        id_joueurs = []

        # plaçage des pions
        for i, joueur in enumerate(self.etat["joueurs"]):
            id_joueur = str(i + 1)
            id_joueurs.append(f'{id_joueur}={joueur["nom"]}')
            ligne = -2 * joueur["pos"][1] + 1
            colonne = 4 * joueur["pos"][0]
            plateau[ligne][colonne] = id_joueur

        patron_mur_h = list("-------")

        # plaçage des murs horizontaux
        for mur_h in self.etat.get("murs")["horizontaux"]:
            ligne = -2 * mur_h[1] + 2
            colonne = 4 * mur_h[0] - 1
            plateau[ligne][colonne: colonne + len(patron_mur_h)] = patron_mur_h

        # plaçage des murs verticaux
        for mur_v in self.etat.get("murs")["verticaux"]:
            ligne = -2 * mur_v[1] + 1
            colonne = 4 * mur_v[0] - 2
            for i in range(ligne, ligne - 3, -1):
                plateau[i][colonne] = "|"

        # concaténation des morceaux du plateau
        return "\n".join(["Légende: " + ", ".join(id_joueurs),
                          "   -----------------------------------",
                          *["".join(ligne) for ligne in plateau],
                          "--|-----------------------------------",
                          "  | 1   2   3   4   5   6   7   8   9"])

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
        if position in self.etat.get("murs")["verticaux"] or position in self.etat.get("murs")["horizontaux"]:
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
        est relative à leur coin supérieur gauche lorsque horizontal et inférieur droit
        lorsque vertical.
        Par convention, un mur horizontal sensitue entre les lignes y-1 et y, et bloque
        les colonnes x et x+1. De même, un mur vertical se situe entre les colonnes x-1
        et x, et bloque les lignes y et y+1.
        """
        return deepcopy(self.etat)

    def jouer_coup(self, joueur):
        """
        Pour le joueur spécifié, jouer automatiquement son meilleur coup pour l'état actuel
        de la partie. Ce coup est soit le déplacement de son jeton, soit le placement d'un
        mur horizontal ou vertical.

        :param joueur: un entier spécifiant le numéro du joueur (1 ou 2).
        :raises QuoridorError: si le numéro du joueur est autre que 1 ou 2.
        :raises QuoridorError: si la partie est déjà terminée.
        """
        if self.partie_terminée():
            raise QuoridorError("La partie est déjà terminée")

        if joueur != 1 and joueur != 2:
            raise QuoridorError("Le numéro du joueur est autre que 1 ou 2")

        joueur = int(joueur)
        adversaire = 1 if joueur == 2 else 2

        pos_joueur = self.etat.get("joueurs")[joueur-1]["pos"]
        pos_adversaire = self.etat.get("joueurs")[adversaire-1]["pos"]

        graphe = construire_graphe(
            [pos_joueur, pos_adversaire],
            self.etat.get("murs")["horizontaux"],
            self.etat.get("murs")["verticaux"]
        )

        chemin_joueur = nx.shortest_path(graphe, pos_joueur, f'B{joueur}')
        chemin_adversaire = nx.shortest_path(graphe, pos_adversaire, f'B{adversaire}')
        deplacer_joueur = False

        if len(chemin_joueur) <= len(chemin_adversaire):
            deplacer_joueur = True
        else:
            coups_adversaire = list(graphe.successors(pos_adversaire))
            if len(coups_adversaire) > 1:
                prochaine_pos_adversaire = chemin_adversaire[1]
                diff_x = prochaine_pos_adversaire[0] - pos_adversaire[0]
                diff_y = prochaine_pos_adversaire[1] - pos_adversaire[1]

                if diff_x != 0:  # tentative plaçage mur vertical
                    mur_v = [prochaine_pos_adversaire[0] - min(diff_x, 0), prochaine_pos_adversaire[1] - min(diff_y, 0)]
                    try:
                        self.placer_mur(joueur, tuple(mur_v), "vertical")
                    except QuoridorError:
                        mur_v[1] -= 1  # tentative plaçage mur vertical plus bas
                        try:
                            self.placer_mur(joueur, tuple(mur_v), "vertical")
                        except QuoridorError:
                            deplacer_joueur = True

                else:  # tentative plaçage mur horizontal
                    mur_h = [prochaine_pos_adversaire[0] - min(diff_x, 0), prochaine_pos_adversaire[1] - min(diff_y, 0)]
                    try:
                        self.placer_mur(joueur, tuple(mur_h), "horizontal")
                    except QuoridorError:
                        mur_h[0] -= 1  # tentative plaçage mur horizontal plus à gauche
                        try:
                            self.placer_mur(joueur, tuple(mur_h), "horizontal")
                        except QuoridorError:
                            deplacer_joueur = True

        if deplacer_joueur:
            self.déplacer_jeton(joueur, chemin_joueur[1])

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
        #joueur invalide
        if not joueur == 1 and not joueur == 2:
            raise QuoridorError("numéro de joueur invalide")

        #aucun mur restant
        if self.etat.get('joueurs')[joueur-1].get('murs') == 0:
            raise QuoridorError("aucun mur restant")

        #position invalide
        if orientation == 'horizontal' and ((position[0] < 1 or position[0] > 8) or (position[1] < 2 or position[1] > 9)):
            raise QuoridorError("le mur horizontal ne peut être placé là")
        if orientation == 'vertical' and ((position[0] < 2 or position[0] > 9) or (position[1] < 1 or position[1] > 8)):
            raise QuoridorError("le mur vertical ne peut être placé là")

        #déjà mur à cette position
        if orientation == 'horizontal':
            for i in self.etat.get('murs').get('horizontaux'):
                if (i[0] == position[0] or i[0] == position[0] - 1 or i[0] == position[0] + 1) and i[1] == position[1]:
                    raise QuoridorError("un mur occupe déjà cette position")
            for j in self.etat.get('murs').get('verticaux'):
                if j[0] == position[0] + 1 and j[1] == position[1] - 1:
                    raise QuoridorError("un mur occupe déjà cette position")
        if orientation == 'vertical':
            for i in self.etat.get('murs').get('verticaux'):
                if i[0] == position[0] and (i[1] == position[1] or i[1] == position[1] - 1 or i[1] == position[1] + 1):
                    raise QuoridorError("un mur occupe déjà cette position")
            for j in self.etat.get('murs').get('horizontaux'):
                if j[0] == position[0] - 1 and j[1] == position[1] + 1:
                    raise QuoridorError("un mur occupe déjà cette position")

        #aucune erreur
        if orientation == 'horizontal':
            self.etat.get('murs').get('horizontaux').append(position)
        if orientation == 'vertical':
            self.etat.get('murs').get('verticaux').append(position)


if __name__ == "__main__":
    jeu = Quoridor(["dapep19", "robot"])
    print(jeu)
