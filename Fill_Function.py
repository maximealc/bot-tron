#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 13:16:01 2020

@author: maxime


Read It : Ce programme permet de simuler la fonction de scoring du bot qui est la fonction fill().
Pour ce faire, on modélise la map comme une matrice de zéros de taille n x m, on peut la laisser vierge
ou y simuler des tracés en faisant quelques modifications à la matrice comme ci dessous, puis on lance la fonction fill() en précisant les coordonnées
de la tête de mon bot et la précision attendue.
La précision est le nombre maximum qui peut être attribué à une cellule. La réduire permet de réduire drastiquement le nombre de calculs,
mais aussi la précision du score.
Le problème étant que l'augmenter semble aussi réduire la précision, puisque si elle est trop élevée 
(i.e inutile, environ > 150 ),le score ne semble pas différer selon les coups joués.
"""

import matplotlib.pyplot as plt
import numpy as np


#import timeit


hauteur, largeur = 20, 30
map_test = np.zeros((hauteur,largeur))

''' C'est ici que je fais les modifications sur la matrice pour simuler des situations différentes, par exemple
fais tourner l'algo une fois, puis rajoute un # avant la commande map_test[9][0] = 0 pour l'annuler, j'ai ainsi simulé
l'effet du mouvement de mon bot de (1, 9) vers (0, 9) sur l'influence de l'adversaire qui diminue drastiquement.'''
map_test[0][15:30] = [1 for i in range(15)]
map_test[1][0:15] = [1 for i in range(15)]
'''for i in range(10):
    map_test[10+i][28] = 1
map_test[8][29] = 1'''

plt.matshow(map_test, cmap=plt.cm.Blues)
#map_test[28][10:19] = [1 for i in range(9)]



def fill(grid, col_start, row_start, precision):
    influence = np.zeros((hauteur, largeur))
    stack = [(col_start, row_start)]
    visited = set()
    param = 0

    while stack:
        if param == precision: break
        col, row, stack = stack[0][0], stack[0][1], stack[1:]
        if (col, row) not in visited:
            param +=0.25
            #print(len(stack))
            if grid[row][col] != 1:
                influence[row, col] = round(param)
                if col > 0:
                    stack.append((col - 1, row))
                if col < (largeur - 1):
                    stack.append((col + 1, row))
                if row > 0:
                    stack.append((col, row - 1))
                if row < (hauteur - 1):
                    stack.append((col, row + 1))
            visited.add((col, row))
    print(influence)
    print(influence.sum())
    return influence

''' La ligne ci dessous permet de visualiser la matrice influence avec les nuances de bleu. 
Il faut que tu cliques sur l'onglet Plot au dessus de la console. Tu peux modifier 4, 4 par les coordonnées de
la tête de mon bot que tu veux, et 90 par une autre sensibilité. '''

plt.matshow(fill(map_test, 14, 0, 70), cmap=plt.cm.Blues)
plt.matshow(fill(map_test, 15, 5, 70), cmap=plt.cm.Blues)

"""
print(timeit.timeit(setup = my_setup,
                    stmt = my_code,
                    number = 1000))
"""



""" NOUVEAU SCORING :
    def scoring(self, coord):
        global trajet
        precision = 80
        scores = []
        if tour == 0:
            for item in coord:
                 scores.append(fill(map_game, hauteur, largeur, item[1], item[0], precision))
            return scores
        adv = trajet[1][-1]
        for item in coord:
            score = fill(map_game, hauteur, largeur, item[1], item[0], precision)
            map_game[item[1]][item[0]] = 1
            score_adv = fill(map_game, hauteur, largeur, adv[1], adv[0], precision)
            map_game[item[1]][item[0]] = 0
            scores.append(score-score_adv)
        return scores
        """