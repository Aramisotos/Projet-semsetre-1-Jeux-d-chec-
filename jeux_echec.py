import fltk


def case_vers_pixel(case):
    """
    Fonction.

    fonction recevant les coordonnées d"une case du plateau sous la
    forme d"un couple d"entiers (ligne, colonne) et renvoyant les
    coordonnées du pixel se trouvant au centre de cette case. Ce calcul
    prend en compte la taille de chaque case, donnée par la variable
    globale taille_case.
    """
    i, j = case
    return (i - 1.5) * taille_case, (j - 1.5) * taille_case


def clic_case():
    """
    Fonction recevant les coordonnées d'un clic et renvoie la case séléctionné.

    sous forme d'un couple d'entier (ligne, colonne)
    """
    y, x = fltk.attend_clic_gauche()
    return int((x)/taille_case)+2, int((y)/taille_case)+2



def cree_plateau():
    """
    Fonction qui crée le quadrillage du plateau

    """
    for i in range(8):
        for j in range(8):
            if i % 2 == 0 and j % 2 == 0:
                fltk.rectangle((j+1) * taille_case, i * taille_case, (j+2) * taille_case, (i+1)*taille_case, remplissage="brown")
            elif j % 2 == 0:
                fltk.rectangle(j*taille_case, i*taille_case, (j+1)*taille_case, (i+1)*taille_case, remplissage="brown")
    fltk.rectangle(8*taille_case, 0, 12*taille_case, 12*taille_case, remplissage="brown")
    fltk.rectangle(8*taille_case, 7*taille_case, 12*taille_case, 8*taille_case, remplissage="red")
    fltk.texte(9*taille_case, 7.5*taille_case, "Quitter", couleur="white", ancrage="center", taille=25)


def charge_image(tableau):
    """
    Fonction qui affiche les pièces sur le plateau.

    """
    for y in range(10):
        for x in range(10):
            if tab[y][x] != 0 and tab[y][x] != -2:
                a, b = case_vers_pixel((x, y))
                fltk.image(a, b, str(tab[y][x])+".png", tag="piece")


def choix_piece(ev, tab, Tour):
    """
    Vérifie que le joueur ait bien séclectionne une de ses pièces.

    """
    while ev[1] > 9:
        ev = clic_case()
    while (tab[ev[0]][ev[1]] < 2 and Tour == 1) or (tab[ev[0]][ev[1]] > -2 and Tour == -1):
        ev = clic_case()
    fltk.efface("rectangle")
    fltk.rectangle((ev[1]-2) * taille_case, (ev[0]-2)*taille_case, (ev[1]-1)*taille_case, (ev[0]-1)*taille_case, epaisseur=5, tag="rectangle")
    fltk.mise_a_jour()
    return ev


def menu_debut(choix):
    """
    Permet de dessiner le menu du debut qui permet de choisir entre le mode facile.

    moyen et difficile.
    :param: choix int
    :return: int
    >>> 288 <= menu_debut(choix) <= 512 and 100<= menu_debut(choix) <= 150
    1
    >>> 288 <= menu_debut(choix) <= 512 and 200<= menu_debut(choix) <= 250
    2
    >>> 288 <= menu_debut(choix) <= 512 and 288 <= menu_debut(choix) <= 350
    3
    """
    fltk.cree_fenetre(800, 400)
    fltk.texte(250, 40, "le jeux unique d'echec", couleur="black")
    fltk.rectangle(290, 100, 510, 150, epaisseur=4, remplissage="black")
    fltk.texte(350, 105, "Jouer", couleur='green')
    fltk.rectangle(290, 200, 510, 250, epaisseur=4, remplissage="black")
    fltk.texte(340, 205, "quitter", couleur="red")
    while True:
        ev = fltk.donne_ev()
        tev = fltk.type_ev(ev)
        if tev == 'Quitte':
            break
        if tev == "ClicGauche":
            if fltk.abscisse(ev) >= 288 and fltk.abscisse(ev) <= 510 and fltk.ordonnee(ev) >= 100 and fltk.ordonnee(ev) <= 150:
                choix = True
                return choix
                break
            if fltk.abscisse(ev) >= 288 and fltk.abscisse(ev) <= 510 and fltk.ordonnee(ev) >= 200 and fltk.ordonnee(ev) <= 250:
                choix = False
                return choix
                break
        else:
            fltk.mise_a_jour()


def pion(tab, Tour, ev):
    """
    Realise le deplacement de la piéce.

    parametre : pion
    parametre : plateau : list de list , represente le plateau de jeux
    return la position du pion

    >>>>>> def pion(tab,-1, ev)
    [(7, 2), (6, 2)]
    >>>>>> def pion(tab,+1,ev)
    [(7, 3), (6, 3)]
    >>>>>> def pion(tab,Tour,ev)
    [(4, 2), (5, 2)]
    >>>>>> def pion(tab,Tour,ev)
    [(6, 8)]

    """
    deplacemnt = []
    danger = [(ev[0]-Tour, ev[1]-1), (ev[0]-Tour, ev[1]+1)]
    if tab[ev[0]-Tour][ev[1]] == 0:
        deplacemnt.append((ev[0]-Tour, ev[1]))
        if tab[ev[0]-Tour-Tour][ev[1]] == 0 and ((ev[0] == 8 and Tour == 1) or (ev[0] == 3 and Tour == -1)):
            deplacemnt.append((ev[0]-Tour-Tour, ev[1]))
    if (tab[ev[0]-Tour][ev[1]+1] < -2 and Tour == 1) or (tab[ev[0]-Tour][ev[1]+1] > 2 and Tour == -1):
        deplacemnt.append((ev[0]-Tour, ev[1]+1))
    if (tab[ev[0]-Tour][ev[1]-1] < -2 and Tour == 1) or (tab[ev[0]-Tour][ev[1]-1] > 2 and Tour == -1):
        deplacemnt.append((ev[0]-Tour, ev[1]-1))
    return deplacemnt, danger


def fou(tab, Tour, ev):
    """
    Prend en comte l'affichage.

    et le deplacemnt de la piéce
    parametre :fou
    return la position des fous
    >>>>>>def fou(tab, Tour, ev)
    [(3, 8), (4, 9)]
    >>>>>>def fou(tab, Tour, ev)
    [(3, 8), (2, 7), (5, 8), (6, 7), (7, 6), (8, 5)]
    """
    deplacemnt = []
    for i in [(1, 1), (-1, -1), (1, -1), (-1, 1)]:
        case_sup = 1
        while tab[ev[0]+case_sup*i[0]][ev[1]+case_sup*i[1]] == 0:
            deplacemnt.append((ev[0]+case_sup*i[0], ev[1]+case_sup*i[1]))
            case_sup += 1
        if (tab[ev[0]+case_sup*i[0]][ev[1]+case_sup*i[1]] > 2 and Tour == -1) or (tab[ev[0]+case_sup*i[0]][ev[1]+case_sup*i[1]] < -2 and Tour == 1):
            deplacemnt.append((ev[0]+case_sup*i[0], ev[1]+case_sup*i[1]))  # manger piece
    return deplacemnt


def tour(tab, Tour, ev):
    """
    Prend en comte l'affichage.

    et le deplacemnt de la piéce
    parametre: tour
    return la position des tours

    >>>>> def (tour)
    [(4, 8), (4, 9), (4, 6), (4, 5), (4, 4), (4, 3), (4, 2), (5, 7), (6, 7),
     (7, 7), (8, 7)]
    >>>>> def (tour)
    [(0, -2]
    """
    deplacemnt = []
    for i in [(0, 1), (0, -1), (-1, 0), (1, 0)]:
        case_sup = 1
        while tab[ev[0]+case_sup*i[0]][ev[1]+case_sup*i[1]] == 0:
            deplacemnt.append((ev[0]+case_sup*i[0], ev[1]+case_sup*i[1]))
            case_sup += 1
        if (tab[ev[0]+case_sup*i[0]][ev[1]+case_sup*i[1]] > 2 and Tour == -1) or (tab[ev[0]+case_sup*i[0]][ev[1]+case_sup*i[1]] < -2 and Tour == 1):
            deplacemnt.append((ev[0]+case_sup*i[0], ev[1]+case_sup*i[1]))
    return deplacemnt


def reine(tab, Tour, ev):
    """
    Prend en compte le deplacemnt de la piéce
    parametre: tour
    return la position des tours

    >>>>> def (tour)
    [(4, 8), (4, 9), (4, 6), (4, 5), (4, 4), (4, 3), (4, 2), (5, 7), (6, 7),
     (7, 7), (8, 7)]
    >>>>> def (tour)
    [(0, -2]
    """
    deplacemnt = tour(tab, Tour, ev) + fou(tab, Tour, ev)
    return deplacemnt


def cavalier(tab, Tour, ev):
    """
    Prend en compte le deplacemnt de la piéce
    parametre tab,Tour,ev
    return la position des cavaliers
    >>>>> def cavalier(cav)
    [(9, 8), (5, 8), (5, 6), (6, 5), (6, 9)]
    >>>>> def cavalier (cav)
    [(4, 9), (4, 7)]
    """
    deplacemnt = []
    for i in [(2, 1), (2, -1), (-2, 1), (-2, -1), (-1, -2), (-1, 2), (1, 2), (1, -2)]:
        if (tab[ev[0]+i[0]][ev[1]+i[1]] > 2 and Tour == -1) or(tab[ev[0]+i[0]][ev[1]+i[1]] < -2 and Tour == 1) or (tab[ev[0]+i[0]][ev[1]+i[1]] == 0):
            deplacemnt.append((ev[0]+i[0], ev[1]+i[1]))
    return deplacemnt


def roi(tab, Tour, ev):
    """
    Prend le deplacemnt de la piéce
    parametre: roi
    return la posotion des roi
    >>>def roi (tab, Tour, ev)
    [(8, 5), (8, 6)]
    >>>def roi (tab, Tour, ev)
    [(5, 8), (3, 6), (5, 6), (3, 8), (4, 8), (4, 6), (3, 7), (5, 7)]
    """
    deplacemnt = []
    for i in [(1, 1), (-1, -1), (1, -1), (-1, 1), (0, 1), (0, -1), (-1, 0),
              (1, 0)]:
        if (tab[ev[0] + i[0]][ev[1] + i[1]] > 2 and Tour == -1) or (tab[ev[0] + i[0]][ev[1] + i[1]] < -2 and Tour == 1) or (tab[ev[0] + i[0]][ev[1] + i[1]] == 0):
            deplacemnt.append((ev[0]+i[0], ev[1]+i[1]))
    return deplacemnt


def selection_piece(Tour, pos, tab):
    """
    Détermine la pièce sélectionné.

    """
    # saisie controle
    if tab[pos[0]][pos[1]] == 3*Tour:
        return pion(tab, Tour, pos)[0]
    elif tab[pos[0]][pos[1]] == 4*Tour:
        return fou(tab, Tour, pos)
    elif tab[pos[0]][pos[1]] == 5*Tour:
        return tour(tab, Tour, pos)
    elif tab[pos[0]][pos[1]] == 6*Tour:
        return reine(tab, Tour, pos)
    elif tab[pos[0]][pos[1]] == 7*Tour:
        return cavalier(tab, Tour, pos)
    elif tab[pos[0]][pos[1]] == 8*Tour:
        return roi(tab, Tour, pos)
    else:
        return []


def affiche_deplacement(pos, tab, Tour, RoiBlanc, RoiNoir):
    """
    Affichage des deplacments des pieces.

    retourne les valeurs des fontions de deplacement des pieces en
    les affichants
    """
    mouvement = []
    deplacemnt = selection_piece(Tour, pos, tab)
    a, b = pos
    for i in deplacemnt:
        case_sup = tab[i[0]][i[1]]
        case_sup2 = tab[a][b]
        tab[i[0]][i[1]] = tab[a][b]
        tab[a][b] = 0
        if (a, b) == RoiBlanc:
            if echec((i[0], i[1]), RoiNoir, Tour, roi_echec(tab, Tour)) == False:
                mouvement.append(i)
        elif (a, b) == RoiNoir:
            if echec(RoiBlanc, (i[0], i[1]), Tour, roi_echec(tab, Tour)) == False:
                mouvement.append(i)
        else:
            if echec(RoiBlanc, RoiNoir, Tour, roi_echec(tab, Tour)) == False:
                mouvement.append(i)
        tab[a][b] = case_sup2
        tab[i[0]][i[1]] = case_sup
    for i in mouvement:
        x, y = case_vers_pixel(i)
        if Tour == 1:
            fltk.cercle(y, x, 20, remplissage="white", tag="cercle")
        if Tour == -1:
            fltk.cercle(y, x, 20, remplissage="black", tag="cercle")
    return mouvement


def roi_echec(tab, Tour):
    """
    Affiche les positions du roi en echec.

    """
    x = []
    for p in range(2, 10):
        for q in range(2, 10):
            if Tour == 1:
                if tab[p][q] == -3:
                    x += pion(tab, -Tour, (p, q))[1]
                elif tab[p][q] < -2:
                    x += selection_piece(-Tour, (p, q), tab)
            else:
                if tab[p][q] == 3:
                    x += pion(tab, -Tour, (p, q))[1]
                elif tab[p][q] > 2:
                    x += selection_piece(-Tour, (p, q), tab)
    return x


def echec_et_mat(tab, Tour):
    '''
    Fonction permettant de retourner True ou False.

    '''
    x = []
    for p in range(2, 10):
        for q in range(2, 10):
            if Tour == 1 and tab[p][q] > 2:
                x += affiche_deplacement((p, q), tab, Tour, RoiBlanc, RoiNoir)
            elif tab[p][q] < -2:
                x += affiche_deplacement((p, q), tab, Tour, RoiBlanc, RoiNoir)
    fltk.efface("danger")
    fltk.efface("cercle")
    fltk.mise_a_jour()
    return bool(x == [])


def echec(RoiBlanc, RoiNoir, Tour, danger):
    """
    Remarque les situation d'echec et entoure le Roi du joueur en echec

    renvoie des booléens True ou False
    """
    if Tour == 1 and (RoiBlanc in danger):
        y, x = case_vers_pixel(RoiBlanc)
        fltk.cercle(x, y, 20, remplissage="red", tag="danger")
        return bool(RoiBlanc in danger)
    elif Tour == -1 and (RoiNoir in danger):
        y, x = case_vers_pixel(RoiNoir)
        fltk.cercle(x, y, 20, remplissage="red", tag="danger")
        return bool(RoiNoir in danger)
    else:
        return False


def tableau_valeur():
    '''
    Tableau contenant les pieces,les cases vides et les limites du jeux.

    renvoie le tab ainsi que les tours des joueur.

    '''
    tab = [[-2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2],
           [-2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2],
           [-2, -2, -5, -7, -4, -6, -8, -7, -4, -5, -2, -2],
           [-2, -2, -3, -3, -3, -3, -3, -3, -3, -3, -2, -2],
           [-2, -2, 0, 0, 0, 0, 0, 0, 0, 0, -2, -2],
           [-2, -2, 0, 0, 0, 0, 0, 0, 0, 0, -2, -2],
           [-2, -2, 0, 0, 0, 0, 0, 0, 0, 0, -2, -2],
           [-2, -2, 0, 0, 0, 0, 0, 0, 0, 0, -2, -2],
           [-2, -2, 3, 3, 3, 3, 3, 3, 3, 3, -2, -2],
           [-2, -2, 5, 7, 4, 6, 8, 7, 4, 5, -2, -2],
           [-2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2],
           [-2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2]]
    Tour = 1
    RoiBlanc = (9, 6)
    RoiNoir = (2, 6)
    return tab, Tour, RoiBlanc, RoiNoir


def rejouer_quitter():
    """
    Permet de dessiner le menu de fin pour condition de rejouer et quitter.

    :return: bool
    >>> 69 <= rejour_quitter() <= 320 and 200<= rejour_quitter() <= 250
    True
    >>> 69 <= rejour_quitter() <= 320 and 300<= rejour_quitter() <= 350
    False
    """
    fltk.ferme_fenetre()
    fltk.cree_fenetre(400, 400)
    fltk.rectangle(320, 200, 100, 250, epaisseur=4, remplissage="black")
    fltk.texte(150, 210, "rejouer", couleur="white")
    fltk.rectangle(320, 300, 100, 350, epaisseur=4, remplissage="red")
    fltk.texte(150, 310, "quitter", couleur="white")
    while True:
        ev = fltk.donne_ev()
        tev = fltk.type_ev(ev)
        if tev == 'Quitte':
            choix2 = False
            choix1 = False
            return choix2, choix1
        if tev == "ClicGauche":
            if fltk.abscisse(ev) >= 69 and fltk.abscisse(ev) <= 320 and fltk.ordonnee(ev) >= 200 and fltk.ordonnee(ev) <= 250:
                choix2 = True
                choix1 = True
                return choix2, choix1
            if fltk.abscisse(ev) >= 69 and fltk.abscisse(ev) <= 320 and fltk.ordonnee(ev) >= 300 and fltk.ordonnee(ev) <= 350:
                choix2 = False
                choix1 = False
                return choix2, choix1
        else:
            fltk.mise_a_jour()


if __name__ == "__main__":
    choix1 = True
    jouer = True
    joueur1 = str(input("Joueur 1:"))
    joueur2 = str(input("Joueur 2:"))
    choix1 = menu_debut(choix1)

    fltk.ferme_fenetre()
    while jouer == choix1:
        tab, Tour, RoiBlanc, RoiNoir = tableau_valeur()
        taille_case = 100
        fltk.cree_fenetre(13 * taille_case, 8*taille_case)
        cree_plateau()
        choix2 = True
        while jouer == choix2:
            if Tour == 1:
                fltk.texte(10*taille_case, taille_case, 'Au tour de '+joueur1, couleur="white", ancrage="center", taille=30, tag="score")
            if Tour == -1:
                fltk.texte(10*taille_case, taille_case, 'Au tour de '+joueur2, couleur="black", ancrage="center", taille=30, tag="score")
            compt = 1
            charge_image(tab)
            ev = clic_case()
            a, b = ev
            danger = roi_echec(tab, Tour)  #Pour savoir si le roi est en echec
            echec(RoiBlanc, RoiNoir, Tour, danger)
            if echec(RoiBlanc, RoiNoir, Tour, danger) == True and echec_et_mat(tab, Tour) == False:
                fltk.texte(10*taille_case, 3*taille_case, 'ECHEC', couleur="red", ancrage="center", taille=30, tag="echec")
            if echec(RoiBlanc, RoiNoir, Tour, danger) == True:
                if echec_et_mat(tab, Tour) == True:
                    fltk.efface("score")
                    if Tour == -1:
                        fltk.texte(10*taille_case, 4*taille_case, joueur1+' gagne', couleur="black", ancrage="center", taille=30, tag="resultat")
                    if Tour == 1:
                        fltk.texte(10*taille_case, 4*taille_case, joueur2 + ' gagne', couleur="black", ancrage="center", taille=30, tag="resultat")
                    fltk.attend_clic_gauche()
                    break
            if ev[1] > 9 and ev[0] > 8:
                choix2, choix1 = rejouer_quitter()
                if choix2 == True:
                    break
            else:
                while compt == 1:
                    ev = choix_piece(ev, tab, Tour)
                    a, b = ev  # position initiale de la piece
                    deplacemnt = affiche_deplacement(ev, tab, Tour, RoiBlanc, RoiNoir)
                    ev = clic_case()
                    if ev in deplacemnt: # pour transformer le pion en dame
                        if tab[a][b] == 3 and ev[0] == 2:
                            tab[ev[0]][ev[1]] = 6
                        elif tab[a][b] == -3 and ev[0] == 9:
                            tab[ev[0]][ev[1]] = -6
                        else:
                            tab[ev[0]][ev[1]] = tab[a][b]
                        if tab[a][b] == 8:
                            RoiBlanc = (ev[0], ev[1])  # position changer du Roi
                        elif tab[a][b] == -8:
                            RoiNoir = (ev[0], ev[1])  # position changer du Roi
                        tab[a][b] = 0
                        compt = 0
                    fltk.efface("cercle")
                    fltk.efface("score")
                    fltk.efface('danger')
                    fltk.efface('echec')
                    fltk.mise_a_jour()
                Tour = -Tour
            fltk.efface("piece")
        fltk.mise_a_jour()
        fltk.ferme_fenetre()
