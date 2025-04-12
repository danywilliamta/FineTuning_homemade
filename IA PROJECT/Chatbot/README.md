Ce chatbot à pour but de permettre à l’utilisateur d’effectuer d’intéragir avec l’ERP Carooline via des instruction textuelle. Exemple “Crée moi un devis pour le client A avec 3 produits A,B,C”.

Il serait intégrés en tant que copilot dans la fenetre de l’utilisateur.

Architecture Implémentation Technique

Open Diagramme vierge (1).png
Diagramme vierge (1).png


🔹 Architecture et Fonctionnement de l'Application

L'interface utilisateur (IHM) est construite à l'aide d'un template XML, avec une dynamisation assurée par un script JavaScript. Ce script gère l'animation de la fenêtre et orchestre l'interaction entre l'utilisateur et le chatbot via des appels JSON-RPC.

1️⃣ Interaction Utilisateur & Traitement du Message

L'utilisateur envoie un message via l'IHM.

Le script JS effectue un appel JSON-RPC vers une route définie dans un contrôleur HTTP.

Cette route transmet le message à l'API Flask, qui contient la définition de l'agent conversationnel et du LLM pré-entraîné qui l'alimente.

L’agent analyse la requête et décide, de manière autonome, de l'action à effectuer.

2️⃣ Utilisation des Outils & Interaction avec Odoo

L'agent dispose d'outils sous forme de fonctions qui effectuent des actions spécifiques.

Chaque outil correspond à un appel HTTP vers une route d'Odoo, laquelle exécute une action ORM (ex. : création de devis, consultation du stock).

Une fois l’action effectuée, la réponse est renvoyée à l’API Flask pour finalement être renvoyé en json via la route appelé au départ. Le message du bot est transmise à l’utilisateur via JSON-RPC.

3️⃣ Gestion de la Mémoire Conversationnelle

Une mémoire conversationnelle a été implémentée à l’aide de Redis.

L’historique de la conversation est stocké en associant session_id à l’ID utilisateur.

Cela permet de préserver le contexte et d'améliorer l’expérience utilisateur.

4️⃣ Infrastructure et Déploiement

L’ensemble des services (Odoo, PostgreSQL, Flask, Redis) est déployé sur un même réseau Docker. Cette architecture facilite la communication entre les conteneurs.