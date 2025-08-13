#!/usr/bin/env python3
import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sellhub.settings')
django.setup()

from django.contrib.auth.models import User
from forum.models import Post

def create_forum_data():
    print("Création des posts de forum...")
    
    # Récupérer l'utilisateur de test
    user = User.objects.get(username='testuser')
    
    # Supprimer les anciens posts
    Post.objects.filter(author=user).delete()
    print("Anciens posts supprimés")
    
    # Créer des posts de test
    posts = [
        {
            'title': 'Conseils pour acheter sa première maison',
            'content': '''Bonjour à tous ! Je suis nouveau dans l'immobilier et j'aimerais avoir vos conseils pour acheter ma première maison. 

Quels sont les points importants à vérifier avant d'acheter ? 
- L'état de la toiture
- Les installations électriques
- La plomberie
- Les documents légaux

Avez-vous des expériences à partager ? Merci d'avance !'''
        },
        {
            'title': 'Quartiers recommandés à Douala',
            'content': '''Salut la communauté ! Je cherche à m'installer à Douala et j'aimerais connaître les meilleurs quartiers pour une famille.

Je recherche :
- Un quartier calme et sécurisé
- Proche des écoles
- Accès facile aux transports
- Prix raisonnables

Quels sont vos quartiers préférés et pourquoi ?'''
        },
        {
            'title': 'Investissement locatif : bon plan ?',
            'content': '''Bonjour ! Je réfléchis à investir dans l'immobilier locatif. 

Questions :
1. Quels sont les rendements moyens à Douala ?
2. Quels types de biens sont les plus demandés ?
3. Quelles sont les charges à prévoir ?
4. Conseils pour bien gérer ses locataires ?

Merci pour vos retours d'expérience !'''
        },
        {
            'title': 'Rénovation : par où commencer ?',
            'content': '''J'ai acheté une maison qui nécessite des travaux. Je ne sais pas par où commencer !

Priorités selon vous :
- Électricité et plomberie en premier ?
- Isolation et toiture ?
- Décoration et finitions ?

Avez-vous des recommandations d'artisans sérieux ?'''
        },
        {
            'title': 'Prêt immobilier : conseils pratiques',
            'content': '''Bonjour ! Je vais bientôt demander un prêt immobilier et j'aimerais vos conseils.

Questions :
- Quels documents préparer ?
- Quelle banque recommandez-vous ?
- Taux d'intérêt actuels ?
- Durée de prêt optimale ?

Merci pour votre aide !'''
        }
    ]
    
    for i, post_data in enumerate(posts):
        post = Post.objects.create(
            title=post_data['title'],
            content=post_data['content'],
            author=user
        )
        print(f"Post créé: {post.title}")
    
    print(f"\n✅ {len(posts)} posts créés avec succès !")
    print("🌐 Accédez au forum: http://127.0.0.1:8000/forum/")

if __name__ == '__main__':
    create_forum_data()

