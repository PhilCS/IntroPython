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
        pass

    def déplacer_jeton(self, joueur, position):
        """
        Pour le joueur spécifié, déplacer son jeton à la position spécifiée.

        :param joueur: un entier spécifiant le numéro du joueur (1 ou 2).
        :param position: le tuple (x, y) de la position du jeton (1<=x<=9 et 1<=y<=9).
        :raises QuoridorError: si le numéro du joueur est autre que 1 ou 2.
        :raises QuoridorError: si la position est invalide (en dehors du damier).
        :raises QuoridorError: si la position est invalide pour l'état actuel du jeu.
        """
        pass

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
        pass

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
