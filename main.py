'''Module principal'''
from argparse import ArgumentParser
import api


def analyser_commande():
    '''Traitement des arguments passés dans l'invité de commandes'''
    parser = ArgumentParser(description='Jeu Quoridor - phase 3')
    
    #Positional arguments
    parser.add_argument('idul', metavar='idul', help='IDUL du joueur', type=str)

    #Optional arguments
    parser.add_argument('-a','--automatique', action='store_true', help="Activer le mode automatique")
    parser.add_argument('-x','--graphique', action='store_true', help="Activer le mode graphique")
    return parser.parse_args()

if __name__ == "__main__":
    print(analyser_commande())

