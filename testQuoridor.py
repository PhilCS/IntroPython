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
        self.assertEqual(str(err.exception), "Le nombre de murs qu'un joueur peut placer est >10, négatif, ou invalide")

        with self.assertRaises(QuoridorError) as err:
            Quoridor(joueurs=[
                {"nom": "henri", "murs": 10, "pos": (5, 1)},
                {"nom": "robot", "murs": 11, "pos": (5, 9)}
            ])
        self.assertEqual(str(err.exception), "Le nombre de murs qu'un joueur peut placer est >10, négatif, ou invalide")

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


class TestDeplacerJeton(unittest.TestCase):
    def test_num_joueur(self):
        """test num joueur"""
        partie = Quoridor(joueurs=[
            {"nom": "henri", "murs": 10, "pos": (5, 1)},
            {"nom": "robot", "murs": 10, "pos": (5, 9)}
        ])
        with self.assertRaises(QuoridorError) as err:
            partie.déplacer_jeton(3, (5, 2))
        self.assertEqual(str(err.exception), "Le numéro du joueur est invalide")

    def test_pos_joueur_dehors(self):
        """test pos joueur dehors"""
        partie = Quoridor(joueurs=[
            {"nom": "henri", "murs": 10, "pos": (5, 1)},
            {"nom": "robot", "murs": 10, "pos": (5, 9)}
        ])
        with self.assertRaises(QuoridorError) as err:
            partie.déplacer_jeton(1, (0, 0))
        self.assertEqual(str(err.exception), "La position est invalide (en dehors du damier)")

    def test_pos_joueur_saut(self):
        """test pos joueur saut"""
        partie = Quoridor(joueurs=[
            {"nom": "henri", "murs": 10, "pos": (5, 1)},
            {"nom": "robot", "murs": 10, "pos": (5, 9)}
        ])
        with self.assertRaises(QuoridorError) as err:
            partie.déplacer_jeton(1, (5, 3))
        self.assertEqual(str(err.exception), "La position est invalide pour l'état actuel du jeu")

    def test_pos_joueur_mur(self):
        """test pos joueur mur"""
        partie = Quoridor(joueurs=[
            {"nom": "henri", "murs": 9, "pos": (5, 1)},
            {"nom": "robot", "murs": 10, "pos": (5, 9)}
        ], murs={
            "horizontaux": [(5, 2)],
            "verticaux": []
        })
        with self.assertRaises(QuoridorError) as err:
            partie.déplacer_jeton(1, (5, 2))
        self.assertEqual(str(err.exception), "La position est invalide pour l'état actuel du jeu")

    def test_pos_joueur_sautemouton(self):
        """test pos joueur sautemouton"""
        partie = Quoridor(joueurs=[
            {"nom": "henri", "murs": 10, "pos": (5, 4)},
            {"nom": "robot", "murs": 10, "pos": (5, 5)}
        ])
        partie.déplacer_jeton(1, (5, 6))


class TestPlacerMur(unittest.TestCase):
    def test_num_joueur(self):
        """test num joueur"""
        partie = Quoridor(joueurs=[
            {"nom": "henri", "murs": 10, "pos": (5, 1)},
            {"nom": "robot", "murs": 10, "pos": (5, 9)}
        ])
        with self.assertRaises(QuoridorError) as err:
            partie.placer_mur(3, (5, 5), "horizontal")
        self.assertEqual(str(err.exception), "Le numéro du joueur est invalide")

    def test_orientation(self):
        """test orientation"""
        partie = Quoridor(joueurs=[
            {"nom": "henri", "murs": 10, "pos": (5, 1)},
            {"nom": "robot", "murs": 10, "pos": (5, 9)}
        ])
        with self.assertRaises(QuoridorError) as err:
            partie.placer_mur(1, (5, 5), "diagonal")
        self.assertEqual(str(err.exception), "L'orientation du mur est invalide")

    def test_pos_mur_h(self):
        """test pos mur h"""
        partie = Quoridor(joueurs=[
            {"nom": "henri", "murs": 10, "pos": (5, 1)},
            {"nom": "robot", "murs": 10, "pos": (5, 9)}
        ])
        with self.assertRaises(QuoridorError) as err:
            partie.placer_mur(1, (0, 2), "horizontal")
        self.assertEqual(str(err.exception), "La position de ce mur horizontal est invalide")

    def test_chevauchement_murs_h(self):
        """test chevauchement murs h"""
        partie = Quoridor(joueurs=[
            {"nom": "henri", "murs": 9, "pos": (5, 1)},
            {"nom": "robot", "murs": 10, "pos": (5, 9)}
        ], murs={
            "horizontaux": [(2, 2)],
            "verticaux": []
        })
        with self.assertRaises(QuoridorError) as err:
            partie.placer_mur(1, (3, 2), "horizontal")
        self.assertEqual(str(err.exception), "Deux des murs horizontaux se chevauchent")

    def test_pos_mur_v(self):
        """test pos mur v"""
        partie = Quoridor(joueurs=[
            {"nom": "henri", "murs": 10, "pos": (5, 1)},
            {"nom": "robot", "murs": 10, "pos": (5, 9)}
        ])
        with self.assertRaises(QuoridorError) as err:
            partie.placer_mur(1, (2, 0), "vertical")
        self.assertEqual(str(err.exception), "La position de ce mur vertical est invalide")

    def test_chevauchement_murs_v(self):
        """test chevauchement murs v"""
        partie = Quoridor(joueurs=[
            {"nom": "henri", "murs": 9, "pos": (5, 1)},
            {"nom": "robot", "murs": 10, "pos": (5, 9)}
        ], murs={
            "horizontaux": [],
            "verticaux": [(2, 2)]
        })
        with self.assertRaises(QuoridorError) as err:
            partie.placer_mur(1, (2, 3), "vertical")
        self.assertEqual(str(err.exception), "Deux des murs verticaux se chevauchent")

    def test_chevauchement_murs_hv(self):
        """test chevauchement murs hv"""
        partie = Quoridor(joueurs=[
            {"nom": "henri", "murs": 9, "pos": (5, 1)},
            {"nom": "robot", "murs": 10, "pos": (5, 9)}
        ], murs={
            "horizontaux": [(2, 3)],
            "verticaux": []
        })
        with self.assertRaises(QuoridorError) as err:
            partie.placer_mur(1, (3, 2), "vertical")
        self.assertEqual(str(err.exception), "Un des murs horizontaux et un des murs verticaux se chevauchent")

    def test_prisonnier(self):
        """test prisonnier"""
        partie = Quoridor(joueurs=[
            {"nom": "henri", "murs": 8, "pos": (5, 1)},
            {"nom": "robot", "murs": 9, "pos": (3, 8)}
        ], murs={
            "horizontaux": [(2, 8), (2, 9)],
            "verticaux": [(2, 8)]
        })
        with self.assertRaises(QuoridorError) as err:
            partie.placer_mur(1, (4, 8), "vertical")
        self.assertEqual(str(err.exception), "Un des joueurs serait emprisonné par ce mur")


class TestPartieTerminee(unittest.TestCase):
    def test_partie_terminee(self):
        """test partie terminee"""
        partie = Quoridor(joueurs=[
            {"nom": "henri", "murs": 10, "pos": (1, 9)},
            {"nom": "robot", "murs": 10, "pos": (5, 9)}
        ])
        self.assertEqual(partie.partie_terminée(), "henri")


if __name__ == "__main__":
    unittest.main()
