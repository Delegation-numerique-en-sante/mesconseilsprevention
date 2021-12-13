# Un exemple avec les données Santé.fr

## Intentions

Développer une première version d’une API permettant 
d’exposer les contenus de santé.fr dans des sites tiers.

## Principes techniques

À partir d’un fichier CSV d’export, une base de données SQLite est créée
puis injectée dans datasette afin d’explorer et de servir ces données
sous forme d’API. La partie client vient consommer ces données d’API
pour les afficher dans une page en HTML.

## Installations

Il y a deux parties distinctes :

1. Le serveur, voir le README dans le dossier dédié.
2. Le client, voir le README dans le dossier dédié.
