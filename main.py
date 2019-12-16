'''Module principal'''
from argparse import ArgumentParser
from quoridor import Quoridor, QuoridorError
from quoridorx import QuoridorX
from api import débuter_partie, jouer_coup


def analyser_commande():
    '''Traitement des arguments passés dans l'invité de commandes'''
    parser = ArgumentParser(description='Jeu Quoridor - phase 3')
    
    #Positional arguments
    parser.add_argument('idul', metavar='IDUL', help='IDUL du joueur', type=str)

    #Optional arguments
    parser.add_argument('-a','--automatique', action='store_true', help="Activer le mode automatique")
    parser.add_argument('-x','--graphique', action='store_true', help="Activer le mode graphique")
    return parser.parse_args()

