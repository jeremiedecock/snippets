### Écrire un prompt dans Neovim

Dans le composeur Codex CLI :

1. Appuyez sur `Ctrl+G`.
2. Rédigez le prompt dans Neovim.
3. Enregistrez et quittez avec `:wq`.
4. Le texte revient dans le composeur, où vous pouvez encore le relire avant de l’envoyer.

Codex consulte d’abord `VISUAL`, puis `EDITOR`. Une variable `VISUAL` définie ultérieurement prendra donc le dessus sur `EDITOR=nvim`.
Documentation OpenAI sur l’éditeur de prompts (https://learn.chatgpt.com/docs/cli-customization).

Pour obtenir immédiatement un confort Markdown dans Neovim :

```
:set filetype=markdown
:set wrap linebreak
:set spell
```

### Les raccourcis qui changent vraiment l’expérience

- `@` : recherche floue d’un fichier et insertion de son chemin dans le prompt.
- `↑ / ↓` : retrouve les brouillons précédents.
- `Ctrl+R` : recherche dans tout l’historique des prompts.
- `Esc Esc`, composeur vide : reprend le précédent message pour le modifier et crée une branche de la conversation.
- `Enter` pendant le travail de Codex : injecte immédiatement une précision dans le tour actif.
- `Tab` pendant le travail : place le prompt en attente pour le prochain tour.
- Une ligne commençant par `!` : exécute directement une commande locale.
- `Ctrl+O ou /copy` : copie la dernière réponse terminée.
- `/vim` : active l’édition Vim directement dans le composeur. Pour la rendre permanente : `tui.vim_mode_default = true dans config.toml`.
- `/keymap` : remappe et conserve vos raccourcis, par exemple `shift-enter`.

Ces raccourcis sont recensés dans la référence officielle des commandes Codex (https://learn.chatgpt.com/docs/developer-commands?surface=cli).

### Se rapprocher d’une interface web ou d’un IDE

- `/side` question… : ouvre une conversation latérale temporaire sans polluer le fil principal.
- `/fork` : crée une vraie branche pour essayer une autre approche.
- `/rename nom-explicite` : rend une conversation facile à retrouver.
- `/resume` ou `codex resume --last` : reprend une conversation interrompue.
- `/compact` : résume un long historique et libère de la fenêtre de contexte.
- `/new` : démarre un nouveau fil sans quitter Codex.
- `/ide` : ajoute au prochain prompt les fichiers ouverts et la sélection de l’IDE, lorsque l’intégration IDE est disponible.
- `/mention chemin` : attache explicitement un fichier ou dossier.
- Collez une image dans le composeur, ou démarrez avec `codex --image capture.png`.
- `/theme`, `/statusline` et `/title` : personnalisent respectivement les couleurs, le pied de page et le titre de l’onglet terminal.
- `/raw` ou `Alt+R` : simplifie la sélection et la copie de longues sorties.
- `codex completion bash`, `zsh` ou `fish` : ajoute l’autocomplétion shell.

Enfin, mettez les conventions répétitives dans `AGENTS.md` — `/init` peut en générer l’ébauche. Cela évite de répéter dans chaque prompt les commandes de test, règles de style et contraintes du dépôt.

Pour des prompts réutilisables ou très longs, conservez-les comme fichiers Markdown et utilisez le mode non interactif :

```
codex exec - < prompt.md
```

Le trio le plus efficace au quotidien est généralement : `Ctrl+G` pour composer dans Neovim, `@` pour fournir précisément le contexte, puis `Enter/Tab` pour piloter Codex pendant qu’il travaille.
