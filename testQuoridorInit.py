"""Quoridor - étape 2 - tests unitaires du constructeur de Quoridor"""
import unittest
from quoridor import *


class TestQuoridorInit(unittest.TestCase):
    def test_joueurs_iterable(self):
        with self.assertRaises(QuoridorError) as err:
            Quoridor(joueurs=0)
        self.assertEqual(str(err.exception), "L'argument 'joueurs' n'est pas itérable")

    def test_trop_joueurs(self):
        with self.assertRaises(QuoridorError) as err:
            Quoridor(joueurs=[
                {"nom": "nom1", "murs": 10, "pos": (5, 1)},
                {"nom": "nom2", "murs": 10, "pos": (5, 9)},
                {"nom": "nom3", "murs": 10, "pos": (5, 9)}
            ])
        self.assertEqual(str(err.exception), "L'itérable de joueurs en contient plus de deux")

    def test_nb_murs_placables(self):
        with self.assertRaises(QuoridorError) as err:
            Quoridor(joueurs=[
                {"nom": "nom1", "murs": -1, "pos": (5, 1)},
                {"nom": "nom2", "murs": 10, "pos": (5, 9)}
            ])
        self.assertEqual(str(err.exception), "Le nombre de murs qu'un joueur peut placer est >10, ou négatif")

        with self.assertRaises(QuoridorError) as err:
            Quoridor(joueurs=[
                {"nom": "nom1", "murs": 10, "pos": (5, 1)},
                {"nom": "nom2", "murs": 11, "pos": (5, 9)}
            ])
        self.assertEqual(str(err.exception), "Le nombre de murs qu'un joueur peut placer est >10, ou négatif")

    def test_pos_joueur(self):
        with self.assertRaises(QuoridorError) as err:
            Quoridor(joueurs=[
                {"nom": "nom1", "murs": 10, "pos": (5, 0)},
                {"nom": "nom2", "murs": 10, "pos": (5, 9)}
            ])
        self.assertEqual(str(err.exception), "La position d'un des joueurs est invalide")

        with self.assertRaises(QuoridorError) as err:
            Quoridor(joueurs=[
                {"nom": "nom1", "murs": 10, "pos": (5, 1)},
                {"nom": "nom2", "murs": 10, "pos": (10, 9)}
            ])
        self.assertEqual(str(err.exception), "La position d'un des joueurs est invalide")

    def test_mur_dict(self):
        with self.assertRaises(QuoridorError) as err:
            Quoridor(joueurs=[
                {"nom": "nom1", "murs": 10, "pos": (5, 1)},
                {"nom": "nom2", "murs": 10, "pos": (5, 9)}
            ], murs=0)
        self.assertEqual(str(err.exception), "L'argument 'murs' n'est pas un dictionnaire")

    def test_nb_murs_total(self):
        with self.assertRaises(QuoridorError) as err:
            Quoridor(joueurs=[
                {"nom": "nom1", "murs": 1, "pos": (5, 1)},
                {"nom": "nom2", "murs": 0, "pos": (5, 9)}
            ], murs={
                "horizontaux": [(2, 2), (2, 3), (2, 4), (2, 5), (2, 6),
                                (2, 7), (2, 8), (2, 9), (4, 2), (4, 3)],
                "verticaux":   [(3, 2), (3, 4), (3, 6), (3, 8), (5, 2),
                                (5, 4), (5, 6), (5, 8), (6, 2), (6, 4)]
            })
        self.assertEqual(str(err.exception), "Le total des murs placés et plaçables n'est pas égal à 20")

        with self.assertRaises(QuoridorError) as err:
            Quoridor(joueurs=[
                {"nom": "nom1", "murs": 0, "pos": (5, 1)},
                {"nom": "nom2", "murs": 0, "pos": (5, 9)}
            ], murs={
                "horizontaux": [(2, 2), (2, 3), (2, 4), (2, 5), (2, 6),
                                (2, 7), (2, 8), (2, 9), (4, 2), (4, 3), (4, 4)],
                "verticaux":   [(3, 2), (3, 4), (3, 6), (3, 8), (5, 2),
                                (5, 4), (5, 6), (5, 8), (6, 2), (6, 4)]
            })
        self.assertEqual(str(err.exception), "Le total des murs placés et plaçables n'est pas égal à 20")

    def test_pos_mur(self):
        with self.assertRaises(QuoridorError) as err:
            Quoridor(joueurs=[
                {"nom": "nom1", "murs": 0, "pos": (5, 1)},
                {"nom": "nom2", "murs": 0, "pos": (5, 9)}
            ], murs={
                "horizontaux": [(0, 2), (2, 3), (2, 4), (2, 5), (2, 6),
                                (2, 7), (2, 8), (2, 9), (4, 2), (4, 3)],
                "verticaux":   [(3, 2), (3, 4), (3, 6), (3, 8), (5, 2),
                                (5, 4), (5, 6), (5, 8), (6, 2), (6, 4)]
            })
        self.assertEqual(str(err.exception), "La position d'un des murs est invalide")

    def test_etat(self):
        partie = Quoridor(joueurs=[
            {"nom": "nom1", "murs": 0, "pos": (5, 1)},
            {"nom": "nom2", "murs": 0, "pos": (5, 9)}
        ], murs={
            "horizontaux": [(2, 2), (2, 3), (2, 4), (2, 5), (2, 6),
                            (2, 7), (2, 8), (2, 9), (4, 2), (4, 3)],
            "verticaux":   [(3, 2), (3, 4), (3, 6), (3, 8), (5, 2),
                            (5, 4), (5, 6), (5, 8), (6, 2), (6, 4)]
        })
        self.assertDictEqual(partie.etat, {
            "joueurs": [
                {"nom": "nom1", "murs": 0, "pos": (5, 1)},
                {"nom": "nom2", "murs": 0, "pos": (5, 9)}
            ],
            "murs": {
                "horizontaux": [(2, 2), (2, 3), (2, 4), (2, 5), (2, 6),
                                (2, 7), (2, 8), (2, 9), (4, 2), (4, 3)],
                "verticaux":   [(3, 2), (3, 4), (3, 6), (3, 8), (5, 2),
                                (5, 4), (5, 6), (5, 8), (6, 2), (6, 4)]
            }
        })


if __name__ == "__main__":
    unittest.main()
