# numberlinkSolver

## Instructions

### Cell Resolution

Requirements : pygame

Pour lancer une résolution via cette méthode, se placer dans le dossier cellResolution puis éxécuter le fichier numberlinkMain :
```
cd cellResolution
python numberlinkMain.py
```

Si `created_with_grid` vaut `True`, une fenêtre s'ouvre pour sélectionner les pairs qui constituent les bouts des chemins. Pour changer les paramètres, changer la taille dans `size`, et `hexa_grid` à `True` (resp. `False`) pour avoir une grille hexagonale (resp. rectangulaire).

Si `created_with_grid` vaut `False`, la grille considérée est celle dans la variable `game`. Dans le fichier `game_storage.py`, il y a plusieurs grilles pour les différents scénarios possibles. Il est possible d'en rajouter en respectant le formatage suivant : un dictionnaire avec :
- `game` (obligatoire) : la grille sous forme de liste de string. Pour des cases inaccessibles, mettre des `"#"`. 
- `bridges` (optionel, `[]` par défaut) : positions des ponts sous forme de liste de coordonées.
- `hexa` (optionel, `False` par défaut) : booléen qui indique si la grille est hexagonale.
- `shiftFirstLine` (optionel, `False` par défaut) : booléen qui indique si les lignes d'indices paires (dont la première) doivent un peu décalés en arrière par rapport aux lignes d'indices impaires.