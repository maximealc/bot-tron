#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 16:41:32 2020

@author: Maxime
"""

import numpy as np
#import matplotlib.pyplot as plt
#import time

hauteur, largeur = 20, 30
map_game = np.zeros((hauteur, largeur))
tour = 0
iterateur = 0
perdu = False

#colfixe = input('col')
#rowfixe = input('row')

deplacements = {
            'RIGHT' : [1, 0],
            'LEFT' : [-1, 0],
            'UP' : [0, -1],
            'DOWN' : [0, 1]

        }
# col_size = hauteur = 20

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
            if grid[row][col] == 0:
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
    return influence.sum()

def a_perdu(n, col):
    if col == -1: 
        deja_perdu[n] = True
        return True
    return False

class Bot:
    
    def __init__(self, col, row, n):
        self.col = col
        self.row = row
        self.n = n
        self.trajet = []
    
    def __repr__(self):
        return f'Coordonnées du bot : ({self.col},{self.row})'
    
    
    # Fonction qui vérifie que les coordonnées choisies ne font pas perdre le bot
    
    def nouveau_tour(self):
        map_game[self.row][self.col] = n + 1
        self.trajet.append([self.col, self.row])
    
    def verif(coordonnees):
        global iterateur
        iterateur += 1
        col, row = coordonnees[0], coordonnees[1]
        
        # On verifie qu'on est bien dans les limites de la matrice
        if not ((0 <= col < largeur) and (0 <= row < hauteur)): return False
        
        # Si on est bien dans les limites, on vérifie qu'on fonce pas sur quelqu'un 
        if map_game[row][col] != 0: return False
        
        #Sinon, ces coordonnées sont possibles, on continue
        return True
    
    def se_deplace(self):
        global deplacements
        c = []
        for value in deplacements.values():
            c.append([a + b for a, b in zip([self.col, self.row], value)])
        return c
    
    def scoring(self, coord):
        precision = 90
        scores_1, scores_2, scores_3 = [], [], []
        score_final = []
        score_inf = []
        coord_adv = []

        if tour > 1: 
            coord_adv = Adversaire.se_deplace()
            coord_adv.remove(Adversaire.trajet[tour-1])
        #print(f'Coord_adv : {coord_adv}')
            coord_adv = [item for item in coord_adv if Bot.verif(item)]
        if coord_adv:
            
            # TECHNIQUES CUMULEES
            for item in coord:
                #TECHNIQUE 1
                scores_1.append(fill(map_game, item[0], item[1], precision))
                
                #TECHNIQUE 3
                score_3 = 0
                map_game[item[1]][item[0]] += 1
                for poss in coord_adv:
                    score_3 += fill(map_game, poss[0], poss[1], precision)
                map_game[item[1]][item[0]] -= 1
                scores_3.append(score_3)
                
                #TECHNIQUE 2
                score_inf = []
                for poss in coord_adv:
                    map_game[poss[1]][poss[0]] += 1
                    score_inf.append(fill(map_game, item[0], item[1], precision))
                    map_game[poss[1]][poss[0]] -= 1
                #print(f'Score_inf : {score_inf}')
                scores_2.append(min(score_inf))
           # print(f'Scores Classiques : {scores_1}')
            
            W = [1, 1, 1]
            
            score_final = [(W[0] * a) + (W[1] * b) +( W[2] * c) for a, b, c in zip(scores_1, scores_2, scores_3)]
                
            return score_final
        else:
            for item in coord:
                     score_final.append(fill(map_game, item[0], item[1], precision))
            return score_final
    
    def strategie(self, p):
        global perdu
        global colfixe, rowfixe
        coord = self.se_deplace()
        if tour != 0: coord.remove(self.trajet[tour-1])
        coord_finales = [item for item in coord if Bot.verif(item)]
        
        #SI UNE SEULE POSSIBILITE, PAS BESOIN DE SCORER
        if len(coord_finales) == 1:
            proposition = [key for key, value in deplacements.items() if value == [coord_finales[0][0] - self.col, coord_finales[0][1]-self.row]]
            print(proposition[0])
            return proposition
        
        #SI AUCUNE POSSIBILITE, ON A PERDU
        if not coord_finales:
            print('ECHEC')
            perdu = True
            return perdu
        scores = self.scoring(coord_finales)
        # Dans l'ordre : UP DOWN LEFT RIGHT
        coord_finales = [coord_finales[i] for i in range(len(scores)) if scores[i] == max(scores)]
        proposition = [key for key, value in deplacements.items() if value == [coord_finales[0][0] - self.col, coord_finales[0][1]-self.row]]
        
        print(proposition[0])

#temps =[]

while not perdu:
    n, p = [int(a) for a in input().split()]
    
    # INITIALISATIONS
    if tour == 0:
        LaMachine = Bot(0, 0, p)
        Adversaire = Bot(1, 1, 1-p)
        deja_perdu = [False for i in range(n)]
        
    for i in range(n):
        col0, row0, col1, row1 = [int(j) for j in input().split()]
        
        if not deja_perdu[i]:
            if a_perdu(i, col1):
                #CORRIGER : POUR CHAQUE JOUEUR
                for item in trajet[i]:
                    map_game[item[1]][item[0]] = 0
            else:
                if i == p:
                    LaMachine.col = col1
                    LaMachine.row = row1
                    LaMachine.nouveau_tour()
                else:
                    Adversaire.col = col1
                    Adversaire.row = row1
                    Adversaire.nouveau_tour()

    LaMachine.strategie(p)
    tour += 1
    #print(iterateur)
    #plt.matshow(map_game, cmap=plt.cm.Blues)
    #print(map_game)