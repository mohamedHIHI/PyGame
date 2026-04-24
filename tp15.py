import pygame
import random
import sys

# Initialisation
pygame.init()

# ========== Configuration ==========
LARGEUR = 800
HAUTEUR = 600

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
ROUGE = (255, 0, 0)
BLEU = (0, 0, 255)
VERT = (0, 255, 0)
JAUNE = (255, 255, 0)
ORANGE = (255, 165, 0)
ROSE = (255, 192, 203)

# Fenêtre
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Space Shooter - Mode 2 Joueurs")


# ========== Classe du Joueur 1 (Bleu) ==========
class Joueur1:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.largeur = 40
        self.hauteur = 40
        self.vitesse = 7
        self.score = 0
        self.vies = 3

    def creer_vaisseau(self):
        surface = pygame.Surface((self.largeur, self.hauteur), pygame.SRCALPHA)
        # Vaisseau triangulaire bleu
        points = [
            (self.largeur // 2, 0),
            (self.largeur, self.hauteur),
            (self.largeur // 2, self.hauteur - 10),
            (0, self.hauteur)
        ]
        pygame.draw.polygon(surface, BLEU, points)
        pygame.draw.polygon(surface, BLANC, points, 2)
        return surface

    def deplacer(self, gauche=False, droite=False, haut=False, bas=False):
        if gauche and self.x > 0:
            self.x -= self.vitesse
        if droite and self.x < LARGEUR // 2 - self.largeur:
            self.x += self.vitesse
        if haut and self.y > HAUTEUR // 2:
            self.y -= self.vitesse
        if bas and self.y < HAUTEUR - self.hauteur:
            self.y += self.vitesse

    def dessiner(self, fenetre):
        pygame.draw.polygon(fenetre, BLEU, [
            (self.x + self.largeur // 2, self.y),
            (self.x + self.largeur, self.y + self.hauteur),
            (self.x + self.largeur // 2, self.y + self.hauteur - 10),
            (self.x, self.y + self.hauteur)
        ])
        pygame.draw.polygon(fenetre, BLANC, [
            (self.x + self.largeur // 2, self.y),
            (self.x + self.largeur, self.y + self.hauteur),
            (self.x + self.largeur // 2, self.y + self.hauteur - 5),
            (self.x, self.y + self.hauteur)
        ], 2)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.largeur, self.hauteur)


# ========== Classe du Joueur 2 (Orange) ==========
class Joueur2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.largeur = 40
        self.hauteur = 40
        self.vitesse = 7
        self.score = 0
        self.vies = 3

    def creer_vaisseau(self):
        surface = pygame.Surface((self.largeur, self.hauteur), pygame.SRCALPHA)
        points = [
            (self.largeur // 2, 0),
            (self.largeur, self.hauteur),
            (self.largeur // 2, self.hauteur - 10),
            (0, self.hauteur)
        ]
        pygame.draw.polygon(surface, ORANGE, points)
        pygame.draw.polygon(surface, BLANC, points, 2)
        return surface

    def deplacer(self, gauche=False, droite=False, haut=False, bas=False):
        if gauche and self.x > LARGEUR // 2:
            self.x -= self.vitesse
        if droite and self.x < LARGEUR - self.largeur:
            self.x += self.vitesse
        if haut and self.y > HAUTEUR // 2:
            self.y -= self.vitesse
        if bas and self.y < HAUTEUR - self.hauteur:
            self.y += self.vitesse

    def dessiner(self, fenetre):
        pygame.draw.polygon(fenetre, ORANGE, [
            (self.x + self.largeur // 2, self.y),
            (self.x + self.largeur, self.y + self.hauteur),
            (self.x + self.largeur // 2, self.y + self.hauteur - 10),
            (self.x, self.y + self.hauteur)
        ])
        pygame.draw.polygon(fenetre, BLANC, [
            (self.x + self.largeur // 2, self.y),
            (self.x + self.largeur, self.y + self.hauteur),
            (self.x + self.largeur // 2, self.y + self.hauteur - 5),
            (self.x, self.y + self.hauteur)
        ], 2)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.largeur, self.hauteur)


# ========== Classe des projectiles ==========
class Projectile:
    def __init__(self, x, y, joueur_id):
        self.x = x
        self.y = y
        self.largeur = 5
        self.hauteur = 10
        self.vitesse = 10
        self.joueur_id = joueur_id  # 1 ou 2

    def deplacer(self):
        self.y -= self.vitesse

    def dessiner(self, fenetre):
        couleur = BLEU if self.joueur_id == 1 else ORANGE
        pygame.draw.rect(fenetre, couleur, (self.x, self.y, self.largeur, self.hauteur))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.largeur, self.hauteur)


# ========== Classe des ennemis ==========
class Ennemi:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.largeur = 35
        self.hauteur = 35
        self.vitesse = 3
        self.type = random.choice(['normal', 'rapide', 'resistant'])

        if self.type == 'rapide':
            self.vitesse = 5
            self.vies = 1
            self.couleur = JAUNE
        elif self.type == 'resistant':
            self.vitesse = 2
            self.vies = 3
            self.couleur = ROUGE
        else:
            self.vitesse = 3
            self.vies = 1
            self.couleur = (128, 0, 128)  # Violet

    def deplacer(self):
        self.y += self.vitesse

    def dessiner(self, fenetre):
        pygame.draw.rect(fenetre, self.couleur, (self.x, self.y, self.largeur, self.hauteur))
        pygame.draw.rect(fenetre, BLANC, (self.x, self.y, self.largeur, self.hauteur), 2)

        # Afficher les vies pour les ennemis résistants
        if self.type == 'resistant':
            font = pygame.font.Font(None, 20)
            texte = font.render(str(self.vies), True, BLANC)
            fenetre.blit(texte, (self.x + 12, self.y + 10))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.largeur, self.hauteur)


# ========== Fonction principale ==========
def jeu_2_joueurs():
    # Initialisation
    joueur1 = Joueur1(LARGEUR // 4 - 20, HAUTEUR - 80)
    joueur2 = Joueur2(3 * LARGEUR // 4 - 20, HAUTEUR - 80)

    projectiles1 = []
    projectiles2 = []
    ennemis = []

    clock = pygame.time.Clock()
    police = pygame.font.Font(None, 36)
    petite_police = pygame.font.Font(None, 24)

    temps_dernier_ennemi = pygame.time.get_ticks()
    intervalle_ennemi = 800

    jeu_termine = False
    running = True
    victoire = None

    # Fond étoilé
    fond = pygame.Surface((LARGEUR, HAUTEUR))
    fond.fill(NOIR)
    etoiles = [(random.randint(0, LARGEUR), random.randint(0, HAUTEUR)) for _ in range(150)]

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return

            # Tir Joueur 1 (Touche ESPACE)
            if event.type == pygame.KEYDOWN and not jeu_termine:
                if event.key == pygame.K_SPACE:
                    projectile = Projectile(
                        joueur1.x + joueur1.largeur // 2 - 2.5,
                        joueur1.y,
                        1
                    )
                    projectiles1.append(projectile)

                # Tir Joueur 2 (Touche ENTER)
                if event.key == pygame.K_RETURN:
                    projectile = Projectile(
                        joueur2.x + joueur2.largeur // 2 - 2.5,
                        joueur2.y,
                        2
                    )
                    projectiles2.append(projectile)

        if jeu_termine:
            # Afficher écran de fin
            fenetre.fill(NOIR)

            if victoire == 1:
                texte = police.render(f"JOUEUR 1 GAGNE! Score: {joueur1.score}", True, BLEU)
            elif victoire == 2:
                texte = police.render(f"JOUEUR 2 GAGNE! Score: {joueur2.score}", True, ORANGE)
            else:
                texte = police.render("PARTIE TERMINEE", True, ROUGE)

            texte_rect = texte.get_rect(center=(LARGEUR // 2, HAUTEUR // 2 - 50))
            fenetre.blit(texte, texte_rect)

            replay = petite_police.render("Appuyez sur R pour rejouer ou ECHAP pour quitter", True, VERT)
            replay_rect = replay.get_rect(center=(LARGEUR // 2, HAUTEUR // 2 + 50))
            fenetre.blit(replay, replay_rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return jeu_2_joueurs()
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                        pygame.quit()
                        return
            continue

        # Déplacement Joueur 1 (Q, D, Z, S)
        touches = pygame.key.get_pressed()
        joueur1.deplacer(
            gauche=touches[pygame.K_q],
            droite=touches[pygame.K_d],
            haut=touches[pygame.K_z],
            bas=touches[pygame.K_s]
        )

        # Déplacement Joueur 2 (Flèches)
        joueur2.deplacer(
            gauche=touches[pygame.K_LEFT],
            droite=touches[pygame.K_RIGHT],
            haut=touches[pygame.K_UP],
            bas=touches[pygame.K_DOWN]
        )

        # Mise à jour projectiles Joueur 1
        for projectile in projectiles1[:]:
            projectile.deplacer()
            if projectile.y < 0:
                projectiles1.remove(projectile)

        # Mise à jour projectiles Joueur 2
        for projectile in projectiles2[:]:
            projectile.deplacer()
            if projectile.y < 0:
                projectiles2.remove(projectile)

        # Génération ennemis
        temps_actuel = pygame.time.get_ticks()
        if temps_actuel - temps_dernier_ennemi > intervalle_ennemi:
            x_ennemi = random.randint(0, LARGEUR - 35)
            ennemi = Ennemi(x_ennemi, -35)
            ennemis.append(ennemi)
            temps_dernier_ennemi = temps_actuel

        # Mise à jour ennemis
        for ennemi in ennemis[:]:
            ennemi.deplacer()
            if ennemi.y > HAUTEUR:
                ennemis.remove(ennemi)

        # Collisions projectiles Joueur 1
        for projectile in projectiles1[:]:
            for ennemi in ennemis[:]:
                if projectile.get_rect().colliderect(ennemi.get_rect()):
                    if projectile in projectiles1:
                        projectiles1.remove(projectile)
                    ennemi.vies -= 1
                    if ennemi.vies <= 0:
                        if ennemi in ennemis:
                            ennemis.remove(ennemi)
                        joueur1.score += 10

        # Collisions projectiles Joueur 2
        for projectile in projectiles2[:]:
            for ennemi in ennemis[:]:
                if projectile.get_rect().colliderect(ennemi.get_rect()):
                    if projectile in projectiles2:
                        projectiles2.remove(projectile)
                    ennemi.vies -= 1
                    if ennemi.vies <= 0:
                        if ennemi in ennemis:
                            ennemis.remove(ennemi)
                        joueur2.score += 10

        # Collision joueurs avec ennemis
        for ennemi in ennemis[:]:
            if joueur1.get_rect().colliderect(ennemi.get_rect()):
                joueur1.vies -= 1
                ennemis.remove(ennemi)
                if joueur1.vies <= 0:
                    jeu_termine = True
                    victoire = 2

            if joueur2.get_rect().colliderect(ennemi.get_rect()):
                joueur2.vies -= 1
                ennemis.remove(ennemi)
                if joueur2.vies <= 0:
                    jeu_termine = True
                    victoire = 1

        # Vérifier si un ennemi atteint le bas
        for ennemi in ennemis:
            if ennemi.y + ennemi.hauteur >= HAUTEUR:
                jeu_termine = True
                victoire = None

        # ========== Dessin ==========
        # Fond
        fenetre.fill(NOIR)
        for x, y in etoiles:
            pygame.draw.circle(fenetre, BLANC, (x, y), 1)

        # Ligne de séparation
        pygame.draw.line(fenetre, BLANC, (LARGEUR // 2, 0), (LARGEUR // 2, HAUTEUR), 2)

        # Afficher zone des joueurs
        zone1 = police.render("JOUEUR 1", True, BLEU)
        zone2 = police.render("JOUEUR 2", True, ORANGE)
        fenetre.blit(zone1, (10, 10))
        fenetre.blit(zone2, (LARGEUR - 110, 10))

        # Dessiner joueurs
        joueur1.dessiner(fenetre)
        joueur2.dessiner(fenetre)

        # Dessiner projectiles
        for projectile in projectiles1:
            projectile.dessiner(fenetre)
        for projectile in projectiles2:
            projectile.dessiner(fenetre)

        # Dessiner ennemis
        for ennemi in ennemis:
            ennemi.dessiner(fenetre)

        # Afficher scores et vies
        texte_score1 = police.render(f"Score: {joueur1.score}  Vies: {joueur1.vies}", True, BLEU)
        texte_score2 = police.render(f"Score: {joueur2.score}  Vies: {joueur2.vies}", True, ORANGE)
        fenetre.blit(texte_score1, (10, 50))
        fenetre.blit(texte_score2, (LARGEUR - 220, 50))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


# ========== Menu principal ==========
def menu():
    fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
    pygame.display.set_caption("Space Shooter - Menu")
    police = pygame.font.Font(None, 48)
    petite_police = pygame.font.Font(None, 36)

    while True:
        fenetre.fill(NOIR)

        titre = police.render("SPACE SHOOTER", True, BLANC)
        titre_rect = titre.get_rect(center=(LARGEUR // 2, HAUTEUR // 2 - 100))
        fenetre.blit(titre, titre_rect)

        option1 = petite_police.render("1. Mode 1 Joueur", True, BLEU)
        option2 = petite_police.render("2. Mode 2 Joueurs", True, ORANGE)
        option3 = petite_police.render("3. Quitter", True, ROUGE)

        option1_rect = option1.get_rect(center=(LARGEUR // 2, HAUTEUR // 2))
        option2_rect = option2.get_rect(center=(LARGEUR // 2, HAUTEUR // 2 + 50))
        option3_rect = option3.get_rect(center=(LARGEUR // 2, HAUTEUR // 2 + 100))

        fenetre.blit(option1, option1_rect)
        fenetre.blit(option2, option2_rect)
        fenetre.blit(option3, option3_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    jeu_1_joueur()
                elif event.key == pygame.K_2:
                    jeu_2_joueurs()
                elif event.key == pygame.K_3:
                    pygame.quit()
                    return


# Version simplifiée 1 joueur (appel depuis le menu)
def jeu_1_joueur():
    # Implémentation du mode 1 joueur (version précédente)
    pass


if __name__ == "__main__":
    menu()