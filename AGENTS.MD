# AGENTS.MD — Guide pour les contributions IA / automatisées (Overlay Streamer)

Ce dépôt concerne un **overlay de streamer** affichant les **kills** et **deaths** du streamer.
L’overlay est **piloté par un backend** et un **bot Discord**.

Technos :
- **React** (front overlay)
- **FastAPI** (backend)
- Bot **Discord** (intégration/contrôle)

---

## Règle d’or : PLAN AVANT TOUT (obligatoire)
Avant **toute** écriture, modification ou génération de code, configuration ou documentation, un **plan explicite** doit être produit.

### Format obligatoire du plan
Le plan doit être fourni en Markdown sous forme de checklist :

- [ ] **Objectif (1 phrase)** : …
- [ ] **Hypothèses** :
  - …
- [ ] **Périmètre** :
  - Inclus : …
  - Exclu : …
- [ ] **Approche (étapes ordonnées)** :
  1. …
  2. …
  3. …
- [ ] **Risques & atténuations** :
  - Risque : … → Atténuation : …
- [ ] **Validation** :
  - Commandes : `…`
  - Scénarios : …

> Aucune implémentation ne doit commencer tant que le plan n’est pas rédigé.  
> En cas d’ambiguïté, formuler des hypothèses raisonnables et les expliciter.

---

## Toujours challenger les demandes (obligatoire)
L’agent doit **systématiquement challenger** toute demande avant de l’exécuter :
- Vérifier si le besoin est **réel** ou si une solution plus simple existe.
- Détecter le risque de sur-ingénierie (abstractions, refactors hors scope, complexité inutile).
- Confirmer l’alignement avec l’objectif produit : **un overlay fiable, lisible, réactif**.
- Si une demande augmente la complexité sans gain clair, proposer un **MVP** ou refuser.

Règle : **simplicité d’abord**.

---

## Familiarisation obligatoire avec le projet
Avant toute modification :
- Lire la structure du projet (front, backend, bot) et les fichiers clés.
- Comprendre le flux bout-en-bout : **commande Discord → backend → overlay**.
- Identifier où sont gérés : l’état (kills/deaths), la persistance éventuelle, et le temps réel.

> ❌ Il est interdit de modifier du code sans comprendre son rôle fonctionnel.  
> ❌ Aucun refactoring opportuniste hors périmètre.

---

## Principes de contribution
- Toujours commencer par l’**option la plus simple viable (MVP)**.
- Changements **petits, ciblés et réversibles**.
- Une PR = un objectif clair.
- N’ajouter aucune dépendance sans justification explicite.

---

## Frontend (React) — Overlay
Objectifs non négociables :
- Lisibilité immédiate (stream = contexte rapide).
- Zéro friction (démarrage simple, config minimale).
- Performance stable (pas de re-render inutile, pas d’animations lourdes non nécessaires).

Règles :
- Éviter le state management complexe si non indispensable.
- Garder les composants simples, orientés affichage.
- Toute logique non-UI doit rester hors composants quand possible.

---

## Backend (FastAPI)
Objectifs non négociables :
- API simple et stable pour piloter l’overlay.
- Validation des entrées (éviter valeurs incohérentes ou abus).
- Robustesse : gestion claire des erreurs, logs utiles mais non sensibles.

Règles :
- Privilégier des endpoints explicites et minimalistes.
- Ne pas complexifier avec des patterns lourds tant que le besoin ne le justifie pas.

---

## Bot Discord
Objectifs non négociables :
- Commandes claires, feedback utilisateur immédiat.
- Pas de comportements surprenants (permissions, spam, rate limits).

Règles :
- Minimiser le nombre de commandes.
- Valider et normaliser les entrées avant envoi au backend.
- Anticiper les limitations (rate limit, erreurs réseau) avec une gestion simple et lisible.

---

## Commentaires (OBLIGATOIREMENT en français)
Tous les commentaires doivent être **en français**, clairs et utiles.

Règles :
- Commenter le **pourquoi**, pas le **quoi**.
- Éviter les commentaires redondants.
- Ton neutre, professionnel, factuel.
- Les TODO doivent être justifiés et temporaires.

---

## Sécurité & données
- Jamais de secrets, tokens, clés dans le dépôt.
- Ne pas exposer d’infos sensibles (tokens Discord, URLs privées, identifiants).
- Toute entrée externe est considérée non fiable (Discord, HTTP).

---

## Definition of Done (DoD) — Qualité minimale attendue
> Objectif : livrer rapidement sans dégrader la stabilité ni la lisibilité.

### 1) Plan présent et correct (obligatoire)
- [ ] Le **plan** est présent dans la PR ou le premier commentaire.
- [ ] Le plan reflète le **périmètre réel** (pas de promesses non livrées).
- [ ] La validation est décrite (commandes + scénarios).

### 2) Familiarisation (obligatoire)
- [ ] Le flux impacté est identifié (Discord → backend → overlay).
- [ ] Aucun changement hors périmètre.

### 3) Qualité & maintenabilité (obligatoire)
- [ ] Changements minimaux, lisibles, cohérents avec l’existant.
- [ ] Pas d’abstraction prématurée.
- [ ] Pas de dépendance ajoutée sans justification.
- [ ] Commentaires en français, utiles.

### 4) Validation manuelle (obligatoire)
- [ ] Vérification du comportement de bout-en-bout (commande Discord → overlay mis à jour).
- [ ] Vérification d’au moins un cas limite (ex : valeurs invalides, commande répétée, backend indisponible).

### 5) Tests (désactivés)
- [ ] Aucun test requis. Ne pas en ajouter dans le cadre de ce projet.

---

## Ce qui est interdit
- Ajouter des couches/patterns non justifiés (complexité gratuite).
- Refactorer du code non lié au besoin.
- Introduire de nouvelles librairies sans accord explicite.
- Mettre des exemples de code ou des snippets dans ce document.
