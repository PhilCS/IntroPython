"""Quoridor - module main"""
import argparse


def analyser_commande():
    """Traite les options passées en ligne de commande."""
    parser = argparse.ArgumentParser(description="Jeu Quoridor")

    parser.add_argument("-l", "--lister", action="store_true",
                        help="Lister les identifiants des 20 dernières parties")

    parser.add_argument("-a", dest="console_auto", action="store_true",
                        help="Jouer en mode automatique contre le serveur")

    parser.add_argument("-x", dest="gui_manuel", action="store_true",
                        help="Jouer en mode manuel contre le serveur avec affichage graphique")

    parser.add_argument("-ax", dest="gui_auto", action="store_true",
                        help="Jouer en mode automatique contre le serveur avec affichage graphique")

    parser.add_argument("idul", help="IDUL du joueur")

    return parser.parse_args()
