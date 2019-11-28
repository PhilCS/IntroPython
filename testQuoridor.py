"""Quoridor - étape 2 - tests unitaires du module quoridor"""
import unittest
from quoridor import *


class TestInit(unittest.TestCase):
    def test_joueurs_iterable(self):
        """test joueurs itérable"""
        with self.assertRaises(QuoridorError) as err:
            Quoridor(joueurs=0)
        self.assertEqual(str(err.exception), "L'argument 'joueurs' n'est pas itérable")

    def test_nb_joueurs(self):
        """test nb joueurs"""
        with self.assertRaises(QuoridorError) as err:
            Quoridor(joueurs=[
                {"nom": "henri", "murs": 10, "pos": (5, 1)},
                {"nom": "robot", "murs": 10, "pos": (5, 9)},
                {"nom": "jason", "murs": 0, "pos": (5, 5)}
            ])
        self.assertEqual(str(err.exception), "Il doit uniquement y avoir 2 joueurs")

    def test_nb_murs_placables(self):
        """test nb murs plaçables"""
        with self.assertRaises(QuoridorError) as err:
            Quoridor(joueurs=[
                {"nom": "henri", "murs": -1, "pos": (5, 1)},
                {"nom": "robot", "murs": 10, "pos": (5, 9)}
            ])
        self.assertEqual(str(err.exception), "Le nombre de murs qu'un joueur peut placer est >10, ou négatif")

        with self.assertRaises(QuoridorError) as err:
            Quoridor(joueurs=[
                {"nom": "henri", "murs": 10, "pos": (5, 1)},
                {"nom": "robot", "murs": 11, "pos": (5, 9)}
            ])
        self.assertEqual(str(err.exception), "Le nombre de murs qu'un joueur peut placer est >10, ou négatif")

    def test_pos_joueur(self):
        """test pos joueur"""
        with self.assertRaises(QuoridorError) as err:
            Quoridor(joueurs=[
                {"nom": "henri", "murs": 10, "pos": (5, 0)},
                {"nom": "robot", "murs": 10, "pos": (5, 9)}
            ])
        self.assertEqual(str(err.exception), "La position d'un des joueurs est invalide")

        with self.assertRaises(QuoridorError) as err:
            Quoridor(joueurs=[
                {"nom": "henri", "murs": 10, "pos": (5, 1)},
                {"nom": "robot", "murs": 10, "pos": (10, 9)}
            ])
        self.assertEqual(str(err.exception), "La position d'un des joueurs est invalide")

    def test_mur_dict(self):
        """test mur dict"""
        with self.assertRaises(QuoridorError) as err:
            Quoridor(joueurs=[
                {"nom": "henri", "murs": 10, "pos": (5, 1)},
                {"nom": "robot", "murs": 10, "pos": (5, 9)}
            ], murs=0)
        self.assertEqual(str(err.exception), "L'argument 'murs' n'est pas un dictionnaire")

    def test_nb_murs_total(self):
        """test nb murs total"""
        with self.assertRaises(QuoridorError) as err:
            Quoridor(joueurs=[
                {"nom": "henri", "murs": 1, "pos": (5, 1)},
                {"nom": "robot", "murs": 0, "pos": (5, 9)}
            ], murs={
                "horizontaux": [(2, 2), (2, 3), (2, 4), (2, 5), (2, 6),
                                (2, 7), (2, 8), (2, 9), (4, 2), (4, 3)],
                "verticaux": [(2, 2), (2, 4), (2, 6), (2, 8), (4, 2),
                              (4, 4), (4, 6), (4, 8), (6, 2), (6, 4)]
            })
        self.assertEqual(str(err.exception), "Le total des murs placés et plaçables n'est pas égal à 20")

        with self.assertRaises(QuoridorError) as err:
            Quoridor(joueurs=[
                {"nom": "henri", "murs": 0, "pos": (5, 1)},
                {"nom": "robot", "murs": 0, "pos": (5, 9)}
            ], murs={
                "horizontaux": [(2, 2), (2, 3), (2, 4), (2, 5), (2, 6),
                                (2, 7), (2, 8), (2, 9), (4, 2), (4, 3)],
                "verticaux": [(2, 2), (2, 4), (2, 6), (2, 8), (4, 2),
                              (4, 4), (4, 6), (4, 8), (6, 2), (6, 4), (6, 6)]
            })
        self.assertEqual(str(err.exception), "Le total des murs placés et plaçables n'est pas égal à 20")

    def test_pos_mur_h(self):
        """test pos mur h"""
        with self.assertRaises(QuoridorError) as err:
            Quoridor(joueurs=[
                {"nom": "henri", "murs": 9, "pos": (5, 1)},
                {"nom": "robot", "murs": 10, "pos": (5, 9)}
            ], murs={
                "horizontaux": [(0, 2)],
                "verticaux": []
            })
        self.assertEqual(str(err.exception), "La position d'un des murs horizontaux est invalide")

    def test_chevauchement_murs_h(self):
        """test chevauchement murs h"""
        with self.assertRaises(QuoridorError) as err:
            Quoridor(joueurs=[
                {"nom": "henri", "murs": 9, "pos": (5, 1)},
                {"nom": "robot", "murs": 9, "pos": (5, 9)}
            ], murs={
                "horizontaux": [(2, 2), (3, 2)],
                "verticaux": []
            })
        self.assertEqual(str(err.exception), "Deux des murs horizontaux se chevauchent")

    def test_pos_mur_v(self):
        """test pos mur v"""
        with self.assertRaises(QuoridorError) as err:
            Quoridor(joueurs=[
                {"nom": "henri", "murs": 9, "pos": (5, 1)},
                {"nom": "robot", "murs": 10, "pos": (5, 9)}
            ], murs={
                "horizontaux": [],
                "verticaux": [(2, 0)]
            })
        self.assertEqual(str(err.exception), "La position d'un des murs verticaux est invalide")

    def test_chevauchement_murs_v(self):
        """test chevauchement murs v"""
        with self.assertRaises(QuoridorError) as err:
            Quoridor(joueurs=[
                {"nom": "henri", "murs": 9, "pos": (5, 1)},
                {"nom": "robot", "murs": 9, "pos": (5, 9)}
            ], murs={
                "horizontaux": [],
                "verticaux": [(2, 2), (2, 3)]
            })
        self.assertEqual(str(err.exception), "Deux des murs verticaux se chevauchent")

    def test_chevauchement_murs_hv(self):
        """test chevauchement murs hv"""
        with self.assertRaises(QuoridorError) as err:
            Quoridor(joueurs=[
                {"nom": "henri", "murs": 9, "pos": (5, 1)},
                {"nom": "robot", "murs": 9, "pos": (5, 9)}
            ], murs={
                "horizontaux": [(2, 3)],
                "verticaux": [(3, 2)]
            })
        self.assertEqual(str(err.exception), "Un des murs horizontaux et un des murs verticaux se chevauchent")

    def test_prisonnier(self):
        """test prisonnier"""
        with self.assertRaises(QuoridorError) as err:
            Quoridor(joueurs=[
                {"nom": "henri", "murs": 8, "pos": (5, 1)},
                {"nom": "robot", "murs": 8, "pos": (3, 8)}
            ], murs={
                "horizontaux": [(2, 8), (2, 9)],
                "verticaux": [(2, 8), (4, 8)]
            })
        self.assertEqual(str(err.exception), "Un des joueurs est emprisonné par des murs")

    def test_etat(self):
        """test état"""
        partie = Quoridor(joueurs=[
            {"nom": "henri", "murs": 0, "pos": (5, 1)},
            {"nom": "robot", "murs": 0, "pos": (5, 9)}
        ], murs={
            "horizontaux": [(2, 2), (2, 3), (2, 4), (2, 5), (2, 6),
                            (2, 7), (2, 8), (2, 9), (4, 2), (4, 3)],
            "verticaux": [(2, 2), (2, 4), (2, 6), (2, 8), (4, 2),
                          (4, 4), (4, 6), (4, 8), (6, 2), (6, 4)]
        })
        self.assertDictEqual(partie.etat, {
            "joueurs": [
                {"nom": "henri", "murs": 0, "pos": (5, 1)},
                {"nom": "robot", "murs": 0, "pos": (5, 9)}
            ],
            "murs": {
                "horizontaux": [(2, 2), (2, 3), (2, 4), (2, 5), (2, 6),
                                (2, 7), (2, 8), (2, 9), (4, 2), (4, 3)],
                "verticaux": [(2, 2), (2, 4), (2, 6), (2, 8), (4, 2),
                              (4, 4), (4, 6), (4, 8), (6, 2), (6, 4)]
            }
        })


class TestStr(unittest.TestCase):
    def test_str(self):
        """test str"""
        partie = Quoridor(joueurs=[
            {"nom": "henri", "murs": 0, "pos": (5, 1)},
            {"nom": "robot", "murs": 0, "pos": (5, 9)}
        ], murs={
            "horizontaux": [(2, 2), (2, 3), (2, 4), (2, 5), (2, 6),
                            (2, 7), (2, 8), (2, 9), (4, 2), (4, 3)],
            "verticaux": [(2, 2), (2, 4), (2, 6), (2, 8), (4, 2),
                          (4, 4), (4, 6), (4, 8), (6, 2), (6, 4)]
        })
        self.assertEqual(str(partie), "\n".join(("Légende: 1=henri, 2=robot",
                                                 "   -----------------------------------",
                                                 "9 | . | .   . | .   2   .   .   .   . |",
                                                 "  |   |-------|                       |",
                                                 "8 | . | .   . | .   .   .   .   .   . |",
                                                 "  |    -------                        |",
                                                 "7 | . | .   . | .   .   .   .   .   . |",
                                                 "  |   |-------|                       |",
                                                 "6 | . | .   . | .   .   .   .   .   . |",
                                                 "  |    -------                        |",
                                                 "5 | . | .   . | .   . | .   .   .   . |",
                                                 "  |   |-------|       |               |",
                                                 "4 | . | .   . | .   . | .   .   .   . |",
                                                 "  |    -------                        |",
                                                 "3 | . | .   . | .   . | .   .   .   . |",
                                                 "  |   |-------|-------|               |",
                                                 "2 | . | .   . | .   . | .   .   .   . |",
                                                 "  |    ------- -------                |",
                                                 "1 | .   .   .   .   1   .   .   .   . |",
                                                 "--|-----------------------------------",
                                                 "  | 1   2   3   4   5   6   7   8   9")))


if __name__ == "__main__":
    unittest.main()
