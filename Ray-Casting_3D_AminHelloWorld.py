    # -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pygame
import json
import math

 

class Grille():
    def __init__(self,grille_import='file.txt',coords_joueur=None,vitesse_joueur=None,surf_x=600,surf_y=600,grille_x=10,grille_y=10,render_distance=8):
        '''
        Parametres
        ----------
        grille_import : String, optional
            Remplir avec le nom du fichier dont on veut importer la grille.
            Par defaut on importe la grille dans le fichier 'file.txt' inclus avec le script.
        coords_joueur : Tableau de 2 valeurs, optional
            La position de depart du joueur. 
            Par defaut elle correspond au centre de l'ecran
        vitesse_joueur : Int/Float, optional
            La vitesse a laquelle le joueur bouge. 
            Par defaut elle correspond a surf_x/1000.
        surf_x : Int, optional
            La longeur d'une des écrans. 
            Par defaut elle correspond a 600.
        surf_y : 
            La largeur des des écrans. 
            Par defaut elle correspond a 600.
        grille_x : Int, optional
            La longeur en carrés de la grille.
            Par defaut elle correspond a 10.
        grille_y : Int, optional.
            La largeur en carrés de la grille.
            Par defaut elle correspond a 10.
        render_distance : Int, optional
            La distance maximale en carrés de la grille sur laquelle des carrés vont s'afficher sur le deuxieme écran. 
            Par defaut elle correspond a 8.

        Definit les parametres de la classe, et permet de les changer facilement.
        -------
        '''
        
        self.run=True
        self.stylo=0
        
        self.grille_import=grille_import
        
        self.surf_x,self.surf_y=surf_x,surf_y
        self.surf=pygame.display.set_mode((self.surf_x*2,self.surf_y))
        self.creerGrille(grille_x,grille_y)
        
        
        self.cote_min = min(self.surf_x, self.surf_y)
        self.cote_max = max(grille_x, grille_y)
        
        self.long_segment = self.cote_min / (1.2 * self.cote_max) #Calcule la longeur d'un segment d'un carreau de la grille
        
        x = self.surf_x / 2 - self.grille_x * self.long_segment / 2
        y = self.surf_y / 2 - self.grille_y * self.long_segment / 2
        self.depart_grille = (x, y)     #Calcule les coordonnées x et y a partir desquelles la grille sera dessinée pour permettre de la centrer sur l'ecran
        
        self.taille_joueur = self.long_segment/6    #Calcule la taille du joueur
        
        
        self.angle_joueur=3*math.pi/2   #Calcule l'angle que le joueur vise au debut du script
        
        self.dx=math.cos(self.angle_joueur) 
        self.dy=math.sin(self.angle_joueur)     #Calcule le sinus et los cosinus de l'angle du joueur
        
        
        
        if vitesse_joueur is None:
            self.vitesse_joueur= self.surf_x/1000
        else:
            self.vitesse_joueur=vitesse_joueur
            
        
        if not coords_joueur:
            self.coords_joueur= [self.surf_x/2-(self.taille_joueur/2-1),self.surf_y/2-(self.taille_joueur/2-1)]
        else:
            self.coords_joueur=coords_joueur
        
        self.render_distance=render_distance

        
        self.pos=None

   
    def sauvegarderCarte(self, name='file.txt'):
        '''
        Parametres
        ----------
        name : Str, optional
            Nom du fichier sur lequel on veut sauvegarder la grille cree. 
            Par defaut il correspond a 'file.txt'.

        Sauvegarde le tableau self.carte sur un fichier json dont le nom est name.
        -------
        None.

        '''
        with open("file.txt", "w") as output:
            json.dump(self.carte,output)
              
            
    def importerCarte(self):
        '''
        -------
        Copie le tableau dans le fichier json de nom self.grille_import sur la variable self.carte.
        -------
        '''
        with open(self.grille_import, "r") as output:
            self.carte=json.load(output)       
        
    
    def creerGrille(self,grille_x,grille_y):
        '''
        Parametres
        ----------
        grille_x : Int
            Longeur de la grille que l'on souhaite creer.
        grille_y : InterruptedError(args)
            Largeur de la grille que l'on souhaite creer.

        Cree un double tableau qui correspond a une grille de longeur grille_x et de largeur grille_y.
        Ce double tableau est sauvegardé sur la variable self.carte.
        -------

        '''
        if self.grille_import:
            self.importerCarte()
            print(self.carte)
            self.grille_y=len(self.carte)
            self.grille_x=len(self.carte[0])
        
        else:
            carte=[]
            for i in range (grille_x):
                cartetemp=[]
                for y in range (grille_y):
                    cartetemp.append(0)
                carte.append(cartetemp)
            self.carte=carte
            self.grille_x,self.grille_y=grille_x,grille_y

    def verifierCoords(self,coords):
        '''
        Parametres
        ----------
        coords : Tableau de 2 valeurs.
            Coordonnées dans la surface pygame.

        Retour
        -------
        coords_grille : Tableau de 2 valeurs.
            Coordonnées de la grille correspondant aux coordonnées données en parametre.
        '''
        coords_grille=[None,None]
        if coords[0]>self.depart_grille[0] and coords[0]<self.depart_grille[0]+self.long_segment*self.grille_x:
            if coords[1]>self.depart_grille[1] and coords[1]<self.depart_grille[1]+self.long_segment*self.grille_y: #Si on clique en dehors la grille le programme s'execute pas.
                for i in range(2):
                    counter=0
                    while coords_grille[i] is None:
                        counter+=1
                        if coords[i]<self.depart_grille[i]+self.long_segment*counter:
                            coords_grille[i]=counter-1
        return coords_grille   

    def mettre_jour_carte(self):
        '''
        Fonction qui prend les coordonnées du click du joueur et si il clique sur la grille change les proprietés de la case.
        On peut ajouter des carrés ou en enlever pour creer des environnements sans devoir changer manuellement le double tableau.
        '''
        coords_grille=self.verifierCoords(self.pos)
        # print(coords_grille)
        if not None in coords_grille:
            self.carte[coords_grille[0]][coords_grille[1]]=self.stylo

    def mettreJourJoueur(self,direction):
        '''
        Parametres
        ----------
        direction : Tableau
            Contient les etats de toutes le clés du clavier.
            Nottamment les clés w,s,a et d utilisés pour le mouvement du joueur.

        Selon la touche du clavier appuyée fait le joueur bouger.
        (A tenir en compte que les clés peuvent varier selon le format du clavier)
        W --> Le joueur avance.
        A --> Le joueur tourne a gauche.
        S --> Le joueur recule.
        D --> Le joueur tourne a droite.
        -------
        '''
        if direction[pygame.K_w]:
            self.coords_joueur[0]+=self.dx*self.vitesse_joueur
            self.coords_joueur[1]+=self.dy*self.vitesse_joueur
        elif direction [pygame.K_s]:
            self.coords_joueur[0]-=self.dx*self.vitesse_joueur
            self.coords_joueur[1]-=self.dy*self.vitesse_joueur
        
        if direction[pygame.K_a]:
            self.angle_joueur=(self.angle_joueur-0.01)%(2*math.pi)
            self.dx=math.cos(self.angle_joueur)
            self.dy=math.sin(self.angle_joueur)
            
        elif direction[pygame.K_d]:
            self.angle_joueur=(self.angle_joueur+0.01       )%(2*math.pi)
            self.dx=math.cos(self.angle_joueur)
            self.dy=math.sin(self.angle_joueur)
            

    def raycast(self,angle):
        '''
        Parametres
        ----------
        angle : Float
            Angle dont on veut creer un rayon qui detecte ou est le mur le plus proche dans cette direction.

        Calcule les coordonées du mur plus proche dans la trajectoire de l'angle et dessine une ligne pour le visualiser
        
        Retour
        -------
        (h/v)x,(h/v)y : Tableau
            Coordonnées du mur plus proche.
        distance(H/V) : Int
            La distance entre le joueur et le point de contact.
        Angle : l'angle du raycast.
        0.7 si le mur touché est en horizontal et 0.9 si le mur touché est en vertical.
        '''
        
        # POUR CALCULER LE MUR EN HORIZONTAL LE PLUS PROCHE 
        profondeur=0     #Profondeur sur laquelle on verifie s'il y a des murs
        aTan=-1/math.tan(angle)     #Definit l'inverse de la tangente de l'angle
        distanceH=100000
        hx=0
        hy=0
        
        if angle==0 or angle==math.pi:      #Si l'angle est parallele a l'axe des abscisses(regarde directement a droite ou gauche)
            raycast_x=self.coords_joueur[0] #On ne calcule pas de raycast puisque auncun mur en horizontal est dans la trajectoire du joueur
            raycast_y=self.coords_joueur[1]
            profondeur=self.render_distance
            
        elif angle>math.pi:      #Si l'angle regarde vers en haut
            raycast_y=int(self.coords_joueur[1]/self.long_segment)*self.long_segment-0.1    #Calcule la coordonée y de la ligne de la grille plus proche au joueur
            raycast_x=(self.coords_joueur[1]-raycast_y)*aTan+self.coords_joueur[0]      #Calcule la coordonnée x correspondante a la coordonée y calculée precedemment
            y_offset=-self.long_segment     #Calcule l'espace vertical qu'il y a entre chaque ligne horizontale de la grille
            x_offset=-y_offset*aTan     #Calcule l'espace horizontal correspondant au y_offset
            
        else:      #Si l'angle regarde vers en bas
            raycast_y=int(self.coords_joueur[1]/self.long_segment)*self.long_segment+self.long_segment      #Calcule la coordonée y de la ligne de la grille plus proche au joueur
            raycast_x=(self.coords_joueur[1]-raycast_y)*aTan+self.coords_joueur[0]      #Calcule la coordonnée x correspondante a la coordonée y calculée precedemment
            y_offset=self.long_segment      #Calcule l'espace vertical qu'il y a entre chaque ligne horizontale de la grille
            x_offset=-y_offset*aTan     #Calcule l'espace horizontal correspondant au y_offset
            
        
        while profondeur<self.render_distance:      #Pendant qu'on ne depasse pas la profondeur maximale
            coords_tab=self.verifierCoords((raycast_x,raycast_y))       #On verifie s'il y a un mur sur les coordonées du raycast
            if not None in coords_tab and self.carte[coords_tab[0]][coords_tab[1]]:          
                hx=raycast_x
                hy=raycast_y
                distanceH=calcDistEntreDeuxPoints((hx,hy),self.coords_joueur)
                profondeur=8 
            else:       #S'il y en a pas nous ajoutons les offset aux 
                raycast_x+=x_offset
                raycast_y+=y_offset
                profondeur+=1




    
        #POUR CALCULER LE MUR EN VERTICAL LE PLUS PROCHE DANS LA TRAJECTOIRE DE L'ANGLE (Rayon BLEU)
        profondeur=0     #Profondeur sur laquelle on verifie s'il y a des murs
        nTan=-math.tan(angle)     #Definit l'opposé de la tangente de l'angle
        distanceV=100000
        vx=0
        vy=0
        
        if angle==math.pi/2 or angle==3*math.pi/2:      #Si l'angle est parallele a l'axe des ordonnées(regarde directement en haut ou en bas)
            raycast_x=self.coords_joueur[0] #On ne calcule pas de raycast puisque auncun mur en vertical est dans la trajectoire du joueur
            raycast_y=self.coords_joueur[1]
            profondeur=self.render_distance
            
        elif 3*math.pi/2>angle>math.pi/2:      #Si l'angle regarde a gauche
            raycast_x=int(self.coords_joueur[0]/self.long_segment)*self.long_segment-0.1    #Calcule la coordonée x de la ligne de la grille plus proche au joueur
            raycast_y=(self.coords_joueur[0]-raycast_x)*nTan+self.coords_joueur[1]      #Calcule la coordonnée y correspondante a la coordonée x calculée precedemment
            x_offset=-self.long_segment     #Calcule l'espace vertical qu'il y a entre chaque ligne horizontale de la grille
            y_offset=-x_offset*nTan     #Calcule l'espace horizontal correspondant au y_offset
            
        else:      #Si l'angle regarde vers en bas
            raycast_x=int(self.coords_joueur[0]/self.long_segment)*self.long_segment+self.long_segment      #Calcule la coordonée x de la ligne de la grille plus proche au joueur
            raycast_y=(self.coords_joueur[0]-raycast_x)*nTan+self.coords_joueur[1]      #Calcule la coordonnée y correspondante a la coordonée x calculée precedemment
            x_offset=self.long_segment      #Calcule l'espace horizontal qu'il y a entre chaque ligne horizontale de la grille
            y_offset=-x_offset*nTan     #Calcule l'espace vertical correspondant au x_offset
            
        
        while profondeur<self.render_distance:      #Pendant qu'on ne depasse pas la profondeur maximale
            coords_tab=self.verifierCoords((raycast_x,raycast_y))       #On verifie s'il y a un mur sur les coordonées du raycast
            if not None in coords_tab and self.carte[coords_tab[0]][coords_tab[1]]:           
                vx=raycast_x
                vy=raycast_y
                distanceV=calcDistEntreDeuxPoints((vx,vy),self.coords_joueur)        
                profondeur=8 
            else:       #S'il y en a pas nous ajoutons les offset aux 
                raycast_x+=x_offset
                raycast_y+=y_offset
                profondeur+=1

        if distanceH<distanceV:
            pygame.draw.line(self.surf,(0,0,255),
                                 (self.coords_joueur[0]+(self.taille_joueur/2-1),self.coords_joueur[1]+(self.taille_joueur/2-1)),
                                  (hx,hy))
            return (hx,hy,distanceH,angle,0.7)
        else:
            pygame.draw.line(self.surf,(0,0,255),
                                 (self.coords_joueur[0]+(self.taille_joueur/2-1),self.coords_joueur[1]+(self.taille_joueur/2-1)),
                                  (vx,vy))#Dessine un rayon pour visualiser le raycast        
            return (vx,vy,distanceV,angle,0.9)
        
    def castRaycasts(self):
        '''
        Fonction qui cree 60 raycast depuis 30 degrés a gauche du joueur jusqu'a 30 degrés a droite du joueur
        
        Retour
        -------
        raycasts : Tableau
            Liste des coordonnées, la distance entre le joueur et le point de contact, l'angle, et la direction du mur touché de chaque raycast.

        '''
        raycasts=[]
        angle_degre=0.0174533 #Un angle en degré en radiants
        angle=self.angle_joueur-(30*angle_degre)
        for i in range(60):
            raycasts.append(self.raycast(angle))
            angle+=angle_degre
        return raycasts


    def afficherGrille(self):
        '''
        Dessine la grille sur la surface pygame (gauche de l'ecran)

        '''
        couleurs=[(255,255,255),(0,255,0),(0,0,255)]
        
        for rangee in range(self.grille_x):
            for case in range(self.grille_y):
                if self.carte[rangee][case] :
                    pygame.draw.rect(self.surf,couleurs[1],
                                     ((self.depart_grille[0]+1+rangee*self.long_segment,self.depart_grille[1]+1+case*self.long_segment),
                                     (self.long_segment,self.long_segment))
                                     )
    
        for i in range (self.grille_x+1):
            pygame.draw.line(self.surf,couleurs[0],
                             (self.depart_grille[0]+self.long_segment*(i) ,self.depart_grille[1]),
                             (self.depart_grille[0]+self.long_segment*(i) ,self.depart_grille[1] + self.long_segment*self.grille_y))
            
            
        for i in range (self.grille_y+1):
            pygame.draw.line(self.surf,couleurs[0],
                             (self.depart_grille[0] ,self.depart_grille[1]+self.long_segment*(i)),
                             (self.depart_grille[0] + self.long_segment*self.grille_x ,self.depart_grille[1]+self.long_segment*(i)))
            
    def afficherJoueur(self):
        pygame.draw.rect(self.surf, (255,0,0),
                 ((self.coords_joueur[0],self.coords_joueur[1]),
                 (self.taille_joueur,self.taille_joueur))
                 )
    
    def Afficher3D(self):
        '''
        Affiche l'environnement avec un effet 3d grace aux informations proportionnés par les raycast (droite de l'ecran)
        '''
        rangee=0
        epaisseur=int(self.surf_x/60)
        for rayon in self.fov:
            delta_angle=(self.angle_joueur-rayon[3])
            a=rayon[2]*math.cos(delta_angle)


            hauteur_ligne=(self.surf_y*self.long_segment)/a
            line_offset=(self.surf_y/2)-(hauteur_ligne/2)
            if hauteur_ligne>self.surf_y:
                hauteur_ligne=self.surf_y
            
            pygame.draw.line(self.surf,(0,0,255*rayon[4]),
                              (self.surf_x+(epaisseur*rangee),line_offset),
                              (self.surf_x+(epaisseur*rangee),line_offset+hauteur_ligne),
                              epaisseur
                              )           
            rangee+=1


                    

    def runCarte(self):
        '''
        Fonction principale qui tourne en boucle et fait marcher la simulation.
        '''
        while self.run:
            for event in pygame.event.get():
                
                if event.type==pygame.QUIT:
                    self.run=False
        
                if event.type == pygame.MOUSEBUTTONDOWN :
                    self.stylo=(self.stylo+1)%2
                
                if pygame.mouse.get_pressed() == (1,0,0) :
                    self.pos = pygame.mouse.get_pos() 
                    self.mettre_jour_carte()
                
            keydown=pygame.key.get_pressed()
            self.mettreJourJoueur(keydown)
                    
            self.surf.fill((0,0,0))
            self.afficherGrille()
            self.fov=self.castRaycasts() #Les infos du raycast sont stockées dans la variable self.fov
            self.Afficher3D()
            self.afficherJoueur()
            
            pygame.display.flip()        
        pygame.quit()


def calcDistEntreDeuxPoints(point1,point2):
        '''
        Parametres
        ----------
        point1 : Tuple/Tableau
            Coordonnées d'un point.
        point2 : Tuple/Tableau
            Coordonnées d'un autre point.

        Retourne la distance entre ces deux points grace au theoreme de pythagore
        -------
        '''
        return math.sqrt(((point1[0]-point2[0])**2)+((point1[1]-point2[1])**2))

if __name__=="__main__":
    gril=Grille()
    gril.runCarte()