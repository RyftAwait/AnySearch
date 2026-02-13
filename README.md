# 🔎 AnySearch

**AnySearch** est un bot Discord polyvalent et modulaire développé en Python. Il regroupe des outils avancés pour la recherche d'informations (OSINT), la gestion de serveurs Minecraft (Bedrock), l'obfuscation de code et l'administration de serveurs.

## ✨ Fonctionnalités Principales

Le bot est structuré autour de plusieurs modules (`cogs`) pour une performance optimale :

### 🕵️ Recherche & OSINT
- **Lookup** : Recherche d'informations via bases de données (Ip Adresse).
- **Search** : Moteur de recherche intégré. (database)
- **HideMyIP** : Outils liés à la confidentialité pour les utilisateurs.
- **Last** : Historique des connexions/activités a un serveur. (MC:BE)

### 🎮 Minecraft (MCBE)
- **Query** : Interrogation de serveurs Minecraft Bedrock pour récupérer le statut.
- **Enchant** : Ecrire en Table d'enchantement.
- **Database** : Gestion de bases de données locales pour serveurs MCBE.

### 🛡️ Sécurité & Développement
- **Obfuscate** : Outil pour obfusquer un message.
- **Backup** : Système de Backup Liste discord.
- **Whitelist** : Gestion stricte des utilisateurs autorisés.

### ⚙️ Administration & Utilitaire
- **TempRole** : Gestion des rôles temporaires.
- **Invites** : Suivi des invitations.
- **Vouch & Credits** : Système de réputation sociale.
- **Ping** : Affichage de la latence.

---

## 📋 Prérequis

- **Python 3.11+**
- Un **Bot Token** Discord (via le [Developer Portal](https://discord.com/developers/applications))
- Les dépendances listées dans `requirements.txt`

---

## 🚀 Installation

1. **Cloner le dépôt**
   ```bash
   git clone [https://github.com/RyftAwait/AnySearch.git](https://github.com/RyftAwait/AnySearch.git)
   cd AnySearch
