# SteamBundleBot 🚀🃏

SteamBundleBot est un script d'automatisation Python conçu pour scanner le magasin Steam à la recherche de **Bundles** ou de jeux en promotion et déterminer leur **rentabilité nette** en fonction de la valeur de revente de leurs *Steam Trading Cards* sur le marché communautaire.

## Fonctionnalités Principales

- 🔍 **Scraping de Bundles Steam** : Récupère les packs et les offres disponibles directement sur le store Steam.
- 📉 **Calcul de Rentabilité** : Interroge le Steam Community Market pour estimer la valeur moyenne des cartes. Déduit la taxe Steam (15%) pour vous indiquer le profit réel.
- 🛡️ **Filtrage Intelligent** : Exclut automatiquement de l'analyse les jeux que vous possédez déjà sur votre compte afin de ne pas fausser le calcul (API Steam).
- 💾 **Base de Données Locale** : Utilise SQLite pour mémoriser les bundles déjà scannés et les offres rentables.
- ⏰ **Automatisation** : Script planifié pour tourner automatiquement tous les jours à 21h00.
- 📩 **Notification Discord** : Envoie un *Rich Embed* via un Webhook Discord avec le détail et les profits générés par les offres trouvées.

## Prérequis

- **Python 3.10+**
- Un compte Steam avec accès à l'API publique (une clé Web API).
- Un serveur/salon Discord (pour les notifications Webhook).

## Installation

1. **Cloner le dépôt** :
   ```bash
   git clone https://github.com/Nathan-Camredon/SteamBundleBot.git
   cd SteamBundleBot
   ```

2. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

3. **Configuration de l'Environnement** :
   Copiez le fichier d'exemple et remplissez-le avec vos informations :
   ```bash
   cp .env.example .env
   ```
   **Contenu du `.env`** :
   - `STEAM_API_KEY` : Clé générée sur la page Steam API.
   - `STEAM_ID` : Votre SteamID64 public.
   - `DISCORD_WEBHOOK_URL` : L'URL de votre Webhook Discord (Créé dans les intégrations d'un salon Discord).

## Utilisation

Démarrez simplement le script principal. Il s'exécutera une première fois à l'initialisation, puis se mettra en attente pour son exécution quotidienne planifiée.

```bash
python main.py
```

*Note : L'algorithme intègre des mécanismes de `time.sleep()` pour scrupuleusement respecter les quotas d'appels de l'API Steam et vous éviter un blocage d'IP. Ne réduisez pas ces limites au risque de vous faire bannir de l'API Market.*

## Architecture

Le projet respecte les principes SOLID. Les dossiers sont structurés ainsi :
- `src/` : Coeur métier (logique d'extraction, calculs, modèles `Game` & `Bundle`).
- `src/utils/` : Connecteurs externes (Notifier Discord).
- `data/` : Dossier contenant la base SQLite générée automatiquement.
- `.agents/` : Mémoire et architecture IA pour l'aide au développement futur.

## Contribution

Toutes les modifications doivent suivre le workflow Git suivant :
1. Création d'une branche `feat/...` ou `fix/...` depuis la branche `preprod`.
2. Fusion de la fonctionnalité validée sur `preprod`.
3. Validation finale de `preprod` pour une mise en production sur `main`.
