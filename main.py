'''Module principal'''
from argparse import ArgumentParser
from quoridor import Quoridor, QuoridorError
from quoridorx import QuoridorX
from api import débuter_partie, jouer_coup, lister_parties
from time import sleep


def analyser_commande():
    '''Traitement des arguments passés dans l'invité de commandes'''
    parser = ArgumentParser(description='Jeu Quoridor - phase 3')

    # Positional arguments
    parser.add_argument('idul', metavar='IDUL',
                        help='IDUL du joueur', type=str)

    # Optional arguments
    parser.add_argument('-a', '--automatique',
                        action='store_true', help="Activer le mode automatique")
    parser.add_argument('-x', '--graphique', action='store_true',
                        help="Activer le mode graphique")
    return parser.parse_args()


def lancer_jeu(args):
    print('\n' + '-'*50 + '\n' + ' '*19 + 'Jeu Quoridor\n' + '-'*50 + '\n')
    print(args)
    boucle_jeu(args)


def boucle_auto(graphique=False):
   pass


def boucle_jeu(args):
    en_jeu = True

    try:
        id_partie, etat = débuter_partie(args.idul)
        print(
            'Une partie a été entamée avec le serveur de jeu.',
            f'ID de la partie: {id_partie}',
            f'Automatique = {args.automatique}',
            f'Graphique = {args.graphique}'
        )
    except RuntimeError as err:
        print(
            'Une erreur est survenue lors du lancement de la partie.',
            f"Le message suivant a été communiqué par le serveur: {str(err)}"
        )

    if args.graphique:
        game = QuoridorX((args.idul, 'robot'), etat['murs'])
    else:
        game = Quoridor((args.idul, 'robot'), etat['murs'])

    

    while en_jeu:

        try:
            print("Coup de l'adversaire: ")
            game.afficher()

            if args.automatique:
                print("Calcul du meilleur coup...")
                pos, type_coup = game.jouer_coup(1)
                game.afficher()
                sleep(2)
                etat = jouer_coup(id_partie, type_coup, pos)

            else:
                type_coup = input(
                    'Veuillez entrer le type de coup que vous vouelz jouer (D, MH ou MV): '
                )
                assert type_coup in ('D', 'MH', 'MV'), 'Le type de coup entré est invalide'

                pos_coup_str = input(
                    '''Veuillez entrer la position sous la forme "x, y": '''
                )

                pos_coup = pos_coup_str.split(sep=',')
                pos_coup = (int(pos_coup[0]), int(pos_coup[1]))

                if type_coup == 'D':
                    game.déplacer_jeton(1, pos_coup)
                else:
                    if type_coup == 'MH':
                        game.placer_mur(1, pos_coup, 'horizontal')
                    else:
                        game.placer_mur(1, pos_coup, 'vertical')

                etat = jouer_coup(id_partie, type_coup, pos_coup)
                game.afficher()
                sleep(2)
            
            if args.graphique:
                game = QuoridorX((etat['joueurs'][0], etat['joueurs'][1]), etat['murs'])
            else:
                game = Quoridor((etat['joueurs'][0], etat['joueurs'][1]), etat['murs'])

                
        except AssertionError as err:
            print(err)

        except RuntimeError as err:
            print(err)
        
        except StopIteration as gagnant:
            print(str(gagnant) + ' a gagné la partie!')

        except KeyboardInterrupt:
            print("\nPartie annulée par l'utilisateur")

        except IndexError:
            print('Le format entré est invalide')


        





if __name__ == "__main__":
    args = analyser_commande()
    lancer_jeu(args)
    
