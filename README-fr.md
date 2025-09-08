# Intégration CommVault avec Visual TOM
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE.md)&nbsp;
[![fr](https://img.shields.io/badge/lang-fr-yellow.svg)](README-fr.md)  
Ce projet permet l'intégration des opérations de sauvegarde CommVault avec avec l'ordonnanceur Visual TOM.

L'intégration fournit une solution complète pour lancer et surveiller les travaux de sauvegarde CommVault via Visual TOM, supportant les environnements Windows et Linux.

## Fonctionnalités

L'intégration supporte les opérations suivantes :
  * Lancer des travaux de sauvegarde pour des clients et des jeux de sauvegarde spécifiques
  * Surveiller le statut d'exécution des travaux en temps réel
  * Support pour les sauvegardes spécifiques aux sous-clients
  * Méthodes d'authentification multiples (ligne de commande, variables d'environnement, fichiers de configuration)
  * Intervalles de surveillance et délais d'attente configurables
  * Rapports d'exécution détaillés
  * Support multiplateforme (Windows/Linux)

## Avertissement
Aucun Support et aucune Garantie ne sont fournis par Absyss SAS pour ce projet et le matériel associé. L'utilisation des fichiers de ce projet se fait à vos propres risques.
Absyss SAS n'assume aucune responsabilité pour les dommages causés par l'utilisation de l'un des fichiers proposés ici via ce dépôt Github.
Des jours de conseil peuvent être demandés pour aider à l'implémentation.

## Prérequis

  * Visual TOM 7.1.2 ou supérieur
  * Python 3.x ou supérieur
  * Serveur CommVault avec accès API REST
  * Connectivité réseau au serveur CommVault
  * Identifiants utilisateur CommVault valides avec permissions de sauvegarde

## Installation

1. Copiez les fichiers d'intégration dans votre répertoire binaire Visual TOM (`%ABM_BIN%` sur Windows ou `${ABM_BIN}` sur Linux)
2. Installez les dépendances Python :
   ```bash
   pip install -r requirements.txt
   ```
3. Importez le modèle d'application (`VTOM_CommvaultJob.xml`) dans Visual TOM
4. Configurez l'authentification (voir section Authentification ci-dessous)

## Authentification

L'intégration supporte plusieurs méthodes d'authentification :

### Méthode 1 : Arguments de ligne de commande
```bash
python vtom-commvault_backup-jobs.py --host commvault.company.com --username admin --password secret --client "SERVER01" --backup-set "DefaultBackupSet"
```

### Méthode 2 : Variables d'environnement
```bash
export COMMVAULT_USERNAME=admin
export COMMVAULT_PASSWORD=secret
python vtom-commvault_backup-jobs.py --host commvault.company.com --client "SERVER01" --backup-set "DefaultBackupSet"
```

### Méthode 3 : Fichier de configuration
Créez un fichier `auth.conf` basé sur `auth.conf.example` :
```ini
[Authentication]
username = votre_nom_utilisateur_commvault
password = votre_mot_de_passe_commvault
```

Puis utilisez :
```bash
python vtom-commvault_backup-jobs.py --host commvault.company.com --config-file auth.conf --client "SERVER01" --backup-set "DefaultBackupSet"
```

## Guide d'utilisation

### Intégration Visual TOM

Le modèle d'application doit être importé dans Visual TOM. Le travail Visual TOM doit être exécuté depuis une machine ayant un accès réseau au serveur CommVault.

### Paramètres requis

- **Host** : Nom d'hôte ou adresse IP du serveur CommVault
- **Client** : Nom du client à sauvegarder
- **Backup Set** : Nom du jeu de sauvegarde à exécuter

### Paramètres optionnels

- **Port** : Port du serveur CommVault (par défaut : 8400)
- **Use SSL** : Activer la connexion SSL/TLS (par défaut : true)
- **Subclient** : Nom du sous-client spécifique (optionnel)
- **Username/Password** : Identifiants d'authentification
- **Config File** : Chemin vers le fichier de configuration d'authentification
- **Check Interval** : Intervalle de vérification du statut en secondes (par défaut : 30)
- **Timeout** : Temps d'attente maximum en secondes (par défaut : 3600)
- **Verbose** : Activer la journalisation détaillée

## Exemples

### Exécution Python directe

```bash
# Sauvegarde de base avec invite d'authentification
python vtom-commvault_backup-jobs.py --host commvault.company.com --client "SERVER01" --backup-set "DefaultBackupSet"

# Sauvegarde avec sous-client spécifique
python vtom-commvault_backup-jobs.py --host commvault.company.com --client "SERVER01" --backup-set "DefaultBackupSet" --subclient "Database"

# Sauvegarde avec paramètres de surveillance personnalisés
python vtom-commvault_backup-jobs.py --host commvault.company.com --client "SERVER01" --backup-set "DefaultBackupSet" --check-interval 60 --timeout 7200

# Journalisation verbeuse
python vtom-commvault_backup-jobs.py --host commvault.company.com --client "SERVER01" --backup-set "DefaultBackupSet" --verbose
```

### Exécution via queue batch Visual TOM

#### Windows
```batch
submit_queue_commvault.bat "commvault.company.com" "SERVER01" "DefaultBackupSet" "8400" "true" "" "admin" "secret" "" "30" "3600" "false"
```

#### Linux
```bash
tom_submit.commvault "commvault.company.com" "SERVER01" "DefaultBackupSet" "8400" "true" "" "admin" "secret" "" "30" "3600" "false"
```

## Codes de sortie

Le script retourne les codes de sortie suivants :
- **0** : Succès - Travail terminé avec succès
- **1** : Erreur d'authentification
- **2** : Erreur d'exécution du travail
- **3** : Erreur de délai d'attente
- **4** : Erreur de vérification du statut
- **5** : Arguments invalides
- **6** : Interruption utilisateur (Ctrl+C)

## Fichiers de configuration

### Arguments.json
Contient les définitions de paramètres pour l'intégration Visual TOM, incluant les types de paramètres, descriptions et valeurs par défaut.

### commvault_modele.xml
Modèle d'application Visual TOM qui définit le type de travail personnalisé avec tous les champs requis et leurs propriétés.

## Surveillance et rapports

L'intégration fournit des capacités de surveillance complètes :

- Surveillance du statut des travaux en temps réel
- Intervalles de vérification configurables
- Gestion automatique des délais d'attente
- Rapports d'exécution détaillés incluant :
  - ID et statut du travail
  - Heures de début et de fin
  - Durée
  - Fichiers et octets traités
  - Messages d'erreur (le cas échéant)

## Dépannage

### Problèmes courants

1. **Échecs d'authentification**
   - Vérifiez la connectivité au serveur CommVault
   - Vérifiez les identifiants nom d'utilisateur/mot de passe
   - Assurez-vous que l'utilisateur a les permissions de sauvegarde

2. **Problèmes de connexion**
   - Vérifiez le nom d'hôte/IP et le port
   - Vérifiez les paramètres SSL/TLS
   - Assurez-vous de la connectivité réseau

3. **Échecs d'exécution des travaux**
   - Vérifiez que le nom du client existe dans CommVault
   - Vérifiez la configuration du jeu de sauvegarde
   - Consultez les journaux du serveur CommVault

### Mode débogage

Activez la journalisation verbeuse pour un dépannage détaillé :
```bash
python vtom-commvault_backup-jobs.py --host commvault.company.com --client "SERVER01" --backup-set "DefaultBackupSet" --verbose
```

## Licence
Ce projet est sous licence Apache 2.0 - voir le fichier [LICENSE](LICENSE) pour plus de détails

## Code de conduite
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v2.1%20adopted-ff69b4.svg)](code-of-conduct.md)  
Absyss SAS a adopté le [Contributor Covenant](CODE_OF_CONDUCT.md) comme Code de Conduite, et nous attendons des participants au projet qu'ils s'y conforment. Veuillez lire le [texte complet](CODE_OF_CONDUCT.md) pour comprendre quelles actions seront tolérées ou non.
