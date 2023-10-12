#!/usr/bin/env python3

# To run this demo, type in a terminal: gradio demo_genai.py

import gradio as gr
import random
import time

WHISPER_OUTPUT = """On va y aller, dans l'ordre du jour, je crois qu'on a mis les OBS en premier.
C'est Nicolas qui commence du coup ?
Tout à fait.
Allez.
Bonjour à tous, vous voyez mon écran ?
Oui.
Ok, super.
Eh bien, moi, je vais vous présenter deux nouveautés dans design.
Le premier, vous l'avez présenté avec Loïc, il y a quelque temps déjà, la première
version du comparateur, qui permettait de comparer plusieurs résultats dans design.
Cependant, avec la version 1 du comparateur, il y avait un certain nombre de sections qui
avaient été mises de côté et donc qui n'étaient pas comparées, à savoir les commentaires,
les warnings, tous les graphiques, que ce soit les courbes, les camemberts et enfin
les tableaux, que ce soit classique ou les tableaux année par année.
Dans la deuxième version du comparateur que je vous présente aujourd'hui, tous ces éléments
sont maintenant comparables, sans exception.
Je compare par exemple ces trois résultats, vous pouvez voir que toutes les sections plus
graphiques présentent maintenant N boutons, N étant le nombre de résultats qu'on compare,
et vous pouvez choisir d'afficher tous les éléments graphiques pour la comparaison.
Je vais autoriser Maurice pour vous montrer des choses un peu plus graphiques.
On a maintenant par exemple tous les graphes qui vont être affichés sous forme de cartes,
pareil pour les tableaux, etc.
D'ailleurs les tableaux ont été refaits également, le design des tableaux a été refait.
Voilà, donc ça nous permet une comparaison plus détaillée.
Je ne sais pas si vous avez déjà des questions là-dessus.
Non, ça a l'air bien.
J'ai une remarque, c'est super, c'est vraiment top, je pense que ça rend l'utilisation du design
beaucoup plus facile, parce qu'on sait que par expérience on fait pas mal de calculs,
donc c'est vachement bien de pouvoir comparer un résultat avec un résultat qu'on a fait un peu
avant, plusieurs jours, voire plusieurs semaines avant, on ne se souvient pas forcément des détails.
Et du coup ça m'amène à une question, c'est est-ce qu'on a prévu de mettre en évidence
les sections qui comportent des différences entre les résultats.
Parce que tu vois tu pourrais avoir, au début tu nous as montré un affichage où les résultats
détaillés étaient en fait masqués et il fallait cliquer dessus pour les ouvrir,
mais on pourrait imaginer d'avoir un truc en rouge ou un sigle différent pour dire là
dans cette section là il y a une différence, ou au contraire, s'il n'y a pas de sigle, il n'y a pas de différence,
donc c'est même pas la peine de les regarder la section puisqu'il n'y a pas d'élément différent entre les résultats.
Je comprends bien, ça c'est peut-être Loïc qui va répondre à cette question,
j'ai bien compris ta question mais je ne sais pas si c'est prévu.
Oui, du coup je vais répondre, en effet on essaie de faire le comparateur au fur et à mesure de façon agile,
et du coup dans la roadmap on a intégré deux points qui sont développés dans les sprints suivants,
la mise en avant des différences dans les tableaux comme tu le proposes Philippe et on l'avait mis dans la roadmap,
et également d'avoir des graphiques tout en haut du comparateur qui viendront comparer des grandeurs
très importantes comme des puissances ou des longueurs de bts qui seraient accessibles
directement en haut du comparateur pour gagner du temps lorsqu'on fait une comparaison.
C'est bien intégré dans la roadmap. Super, merci Loïc.
Merci, le deuxième point que je voulais aborder aujourd'hui avec vous c'était
l'amélioration de la section des tables de copes dans la page performance de design toujours.
Jusqu'alors on n'avait pas de nomenclature obligatoire pour ces fichiers,
et aujourd'hui on va intégrer systématiquement les tables de copes
des packs qui sont installées sur les showprix bas carbone, et elles vont être de plus en plus
nombreuses, et du coup on voulait des listes déroulantes plus pratiques, plus lisibles aussi,
et des nomenclatures pour tous les fichiers avec une certaine nomenclature à respecter.
Donc c'est ce qu'on a fait aujourd'hui. Ces nouvelles listes déroulantes sont
triées par fabricant. Il y a eu aussi du tri dans les fichiers de packs. Ce tri a été fait sur les
bases de données et la migration a été effectuée sur tous les projets en prod.
Aujourd'hui j'ai créé deux petits fichiers. Si un fichier de pack ne respecte pas la nomenclature,
le nom ici, on va avoir une petite pop-up qui va nous dire que le nom du fichier n'est pas
valide, avec ici une modal qui va expliquer pourquoi un fichier n'est pas valide et comment
faire pour qu'il soit valide. Cette pop-up on la retrouve également ici, c'est la même.
Et si un fichier est bon, au contraire, on va avoir une petite pop-up pour dire que l'importation
a été réussie. Et enfin, ce qu'on peut faire, c'est qu'on peut télécharger maintenant
les fichiers de table de copes. Voilà ce qu'on ne pouvait pas faire avant. L'affichage des
tables de copes a été légèrement modifié pour que ça soit un peu plus user-friendly.
Et donc ça c'est valable pour les packs Geo comme les packs Aero. Voilà, c'est tout pour moi.
Est-ce que vous avez des questions ?
Pareil. Super. J'avais une question. Quand tu importes une table de copes, est-ce qu'elle
est valable pour toi et ou ton projet uniquement ? Ou est-ce qu'elle est valable pour tout le monde
désormais, quel que soit le projet, quel que soit l'utilisateur qui se connecte ?
Non, elle est valable pour tout le monde, quel que soit le projet, quel que soit l'utilisateur.
Ça, pour le coup, ça peut représenter un risque parce que si jamais on importe un fichier pour
faire un test, ce qui est peut-être le cas d'ailleurs là, copier, test, si on fait un test
et tu vois on n'a pas véridé le fichier et qu'il y a des erreurs dans le fichier, derrière on prend
le risque qu'il y ait un autre utilisateur qui utilise ça et du coup il y ait un résultat qui
soit orienté pour.
Ok, je peux répondre, du coup pour ça Philippe, on s'est mis d'accord aussi avec les Ops pour avoir
un process quand on intègre une nouvelle table de copes dans le design, on a créé une base de données
des tables de copes dans lequel on va aller rentrer toutes nos données pour un modèle précis. Dans
cette base de données qui est un fichier Excel, on va pouvoir avoir un certain nombre de vérifications
pour vérifier qu'on a bien les bons points, qu'on n'a pas un seul point sur une température de
condensation donnée par exemple, condenseur par exemple, et derrière dans le fichier Excel,
on appuie sur un bouton, ça nous exporte notre table de copes CSV et là on peut la mettre dans le
design. Donc on a un certain nombre de vérifications qui se font en un moment de design pour vérifier
que la table de copes est cohérente et après si on importe juste une table de copes pour tester,
on peut très bien demander à Nicolas de la supprimer et il le fait directement. Je vais peut-être un peu trop loin mais
quelque part ça devrait être un droit d'administrateur de pouvoir importer les tables de copes et pas un
droit user pour qu'on soit sûr qu'on ne change pas le process et qu'il n'y ait pas des
erreurs qui soient commises. Après dans tous les cas on voit que majoritairement c'est plutôt la R&D
quand il y a une nouvelle chaufferie bas carbone avec une nouvelle table de copes qui va intégrer
cette table de copes dans le design et donc on fait les bonnes vérifications plutôt que les autres.
Deuxième question et dernière question concernant comment on peut faire la différence
alors il y a dans le nom peut-être mais est-ce que c'est suffisant pour différencier les tables de
copes de pack provenant du fournisseur versus les tables de copes étendues qui est une notion
purement Accenta qui nous simplifie la vie pour le dimensionnement mais qui représente un petit
risque en tout cas de bien différencier les deux. C'est pour ça du coup qu'on avait placé les
commentaires en fin de nom après ils ressortent peut-être un petit peu plus parce qu'ils sont en
fin de nom désormais mais on sait qu'on pourra aussi ajouter un moment des tags dépendant de
ces commentaires pour bien faire ressortir le tag par exemple Extendible quand c'est une table de
copes qu'on a étendue nous-mêmes à partir de celles du fabricant donc c'est dans la roadmap
de les transformer en tag. D'accord parce que j'ai en fait je pense que c'est intéressant de là
dans le nom on voit assez bien effectivement parce que c'est à la fin donc c'est intéressant de
distinguer dans le nom mais c'est aussi intéressant de rappeler dans un résultat qu'en fait ce
résultat il a été réalisé avec une table étendue et pas une table réelle. C'est une très bonne idée
de le faire en page de résultats. Ok je note. Est-ce qu'il y a d'autres remarques ou questions ?
Je crois que je vais arrêter mon partage. Merci d'avoir écouté. Merci Nicolas.
Du coup c'est moi qui enchaîne. Du coup là on vient de parler avec Nicolas de l'outil Design
qui nous sert à dimensionner de façon, je vais dire bonjour à tout le monde même si j'avais
commencé à parler, pardon. Donc design qui nous permet de dimensionner de façon grosse maille
nos chaufferies bas carbone et donc de définir les différentes puissances de nos pompes à
chaleur, les différentes longueurs de BTS etc. C'est un peu l'image que je montre là mais dès
qu'on va rentrer dans une phase plus détaillée de conception notamment quand le client une fois
qu'on lui a présenté l'étude de faisabilité signe avec nous pour une conception détaillée
pour derrière installer une chaufferie bas carbone. On doit passer de cette vision design
à une vision un petit peu plus détaillée où on va devoir aller sélectionner l'ensemble des
équipements notamment les pompes à chaleur, les pompes et également placer ces différents
équipements sur un schéma et donc ça c'est toute la phase de conception. C'est une phase qui est
assurée par l'équipe opération à la fois par des chargés d'affaires et des chargés d'études
bas carbone et pour cette phase actuellement il n'y avait pas forcément d'outils développés par
la R&D pour y répondre et donc c'était un ensemble de fichiers Excel qui était utilisé par l'équipe
opération pour faire l'ensemble des calculs hydrauliques. C'était ensuite des sites web
des fabricants notamment des fabricants de pompes qui était utilisé pour aller sélectionner les
équipements et c'était également un powerpoint qui était utilisé qui est utilisé pour réaliser
les schémas de nos chaufferies. Aujourd'hui je vais vous présenter des évolutions de l'outil
config qu'on développe pour répondre à cette phase de conception et pour simplifier cette
phase de conception, la rendre plus rapide pour les ops, éviter les erreurs etc. Et donc config
s'articule autour de deux outils qu'on vous a déjà présenté dans les démos précédentes. D'un côté
config hydro qui permet d'aller sélectionner précisément les différents équipements qu'on
va installer notamment les packs, les pompes et de l'autre côté config schéma qui avait été
aussi présenté plusieurs fois par Pascal qui permet de représenter schématiquement les
différents équipements sur un schéma qui est disponible sur un outil web. Et donc d'un côté
config hydro on a déjà une version 0.1 qui était sortie, que je vous ai présenté en démo, qui
permettait de définir les régimes dimensionnants des packs, d'aller sélectionner les packs
essentiellement pour l'instant jusqu'à présent c'était essentiellement des packs géo qui étaient
disponibles dans notre base de données et ça a changé avec la nouvelle version que je vais
vous présenter. Ça permettait aussi de définir les équipements hydrauliques présents et donc de
générer une liste de variables des équipements hydrauliques présents pour l'intégrer dans
config schéma. Config schéma traçait ensuite le schéma de l'installation, on pouvait l'animer,
on pouvait l'amender en ajoutant ou en supprimant des équipements. Et donc aujourd'hui je vais vous
présenter une nouvelle version de config hydro qui règle un certain nombre de problèmes qu'il y
avait sur la première version et qui permet d'aller plus loin dans la phase de conception.
Donc les grosses nouveautés de cette version 2, c'est déjà d'avoir intégré les packs R dans la
base de données de nos packs et donc d'être capable pour un utilisateur de sélectionner à
la fois des packs géo et des packs aéro. C'est également la création d'une grosse base de données
qui englobe les modèles de pompes à chaleur, les tables de cop et les polynômes parce qu'avant
on avait trois bases de données séparées qui n'étaient pas interconnectées, le but ça a été
de les interconnecter. La troisième nouveauté qui est la plus importante c'est après la sélection
des packs de pouvoir aller sur la sélection des pompes, de définir leur point de fonctionnement
dimensionnant et de calculer les puissances, débit, perte de charge de ces pompes là sur
ces différents points de fonctionnement pour derrière sélectionner la pompe Ouido qui va bien.
Et il y a également des nouveaux schémas qui avaient été introduits dans Config Schéma,
qui sont gérés depuis quelques semaines dans Config Schéma mais qui n'étaient pas gérés par
Config Hydro et donc qui ont été intégrés à l'outil. C'est un outil qui est parlé chargé
de conception pour gagner du temps, pour éviter les erreurs et comme je l'avais dit dans la
dernière démo, pour l'instant on l'a fait sous une version Excel pour bien prototyper le besoin,
pour bien réaliser les différentes étapes de la conception et derrière le but, une fois qu'il sera
utilisé sur quelques conceptions de chaufferie, ça sera d'aller sur une version web directement.
Donc je vais vous montrer les évolutions dans l'Excel. Pour petit rappel, quand on rentre dans
l'Excel, le but est d'aller définir quels sont les usages qu'on a sur notre bâtiment et
leur point de fonctionnement dimensionnant pour les packs. Une fois qu'on a fait ça,
derrière on va dans la sélection des packs, on a un catalogue de packs qui est disponible,
on peut sélectionner des packs, cette fois à la fois Geo et Aéro, c'est ce qui a été rajouté
dans la 0.2, là en l'occurrence j'ai sélectionné le ROS qui est de techno Aéro et ensuite ma
sélection de packs est listée et je peux configurer mes packs, dire si elles sont sur du
chauffe, ECS, etc. Et pour ces différents régimes de fonctionnement et pour les différentes packs,
obtenir les puissances de mes packs vis-à-vis des puissances demandées par les usages,
par le bâtiment, vérifier que je n'ai pas de surpuissance, etc. Donc ça c'était déjà en
grande partie intégré par la 0.1. Ce qu'on a rajouté, c'est les packers, c'est également une
base de données de pack qui intègre les packers mais également qui est interconnectée avec nos
bases de données de table de copes, donc les différents points de fonctionnement d'un modèle
de pack et notre base de données de polynôme, donc ça c'est ce qui permet quand on connaît le
polynôme de la pack d'aller calculer des puissances de fonctionnement en fonction de
température de fonctionnement et on a du coup intégré, interconnecté cette base de données
de pack avec la base de données de polynôme, on est capable de dire sur une pack est-ce que le
polynôme est dispo, quel est son compresseur et du coup d'aller chercher son polynôme derrière
et puis également d'aller dire est-ce qu'il y a une table de copes qui est dispo pour ce modèle
et le but c'est de rajouter de plus en plus de table de copes pour en avoir plus en plus
disponible dans l'outil. Et donc la grosse nouveauté également c'est de pouvoir aller
sélectionner des compres pour nos différentes packs et donc ce que va faire l'utilisateur c'est
pour les différents usages du bâtiment d'aller définir les différents points de fonctionnement
dimensionnant de ces pompes cette fois et pas de ces packs, côté évaporateur, côté condenseur et
pour ces différents points de fonctionnement donc les différentes températures de fonctionnement
d'aller, l'outil va aller calculer, j'ai foutu mes images n'importe où pardon,
c'est le danger du live, j'ai foutu des images que j'arrive plus à bouger,
je vais expliquer ce que ça fait du coup, désolé de ne pas pouvoir le montrer mieux, mais en gros
du coup on a défini nos points de fonctionnement des différentes pompes, ensuite on va calculer
les puissances et débits de nos packs sur ces différents points de fonctionnement, je vais
l'ouvrir et le refermer, j'explique en même temps, sur ces différents points de fonctionnement donc ça
nous donne les puissances et débits de nos pompes, évaporateur et condenseur et ensuite pour
choisir une pompe, il nous faut savoir également quelle est la perte de charge que cette pompe va
devoir combattre et pour calculer les pertes de charge qu'une pompe va devoir combattre, il va
falloir aller se dire, par exemple la pompe PU1 qui est située ici, elle va devoir combattre des
pertes de charge dans les tuyaux, dans les tubulures de la pack, dans les collecteurs, mais également
dans les différentes sources et destinations, donc les destinations chaud, froid, ECS et les
sources, par exemple le BTS, et donc pour calculer ces pertes de charge, Johan a développé un nouveau
calculateur de perte de charge, où on va définir un petit peu nos différentes sections hydrauliques,
les longueurs de collecteurs, les matériaux, les diamètres, etc. et à partir de ça, l'outil va
aller calculer un certain nombre de pertes de charge, et c'est ces pertes de charge que la
chaufferie va devoir combattre, donc ça c'est pour la partie BTS, mais voilà ces calculs de pertes
de charge, c'est un truc générique qu'on peut utiliser pour calculer des pertes de charge à
d'autres endroits de la chaufferie, et donc on a réutilisé ce moteur de calcul dans l'onglet
pack-pompes, où derrière, on vient calculer les pertes de charge dans la pack, sur les tubulures
de la pack, dans les collecteurs de la pack, et aux différentes destinations et sources, ce qui
nous donne derrière des pertes de charge totales, qui vont devoir être combattues par les pompes,
et donc derrière, dans l'outil, pour chacune des pompes, on va savoir quel est le débit dimensionnant,
et quelle est la perte de charge dimensionnante, ce qui nous permet après d'aller dans le logiciel,
par exemple, Willow Select, et de rentrer ces débits et ces pertes de charge à combattre, pour derrière,
que l'outil nous propose des pompes, qui pourraient correspondre à notre besoin, et qu'on puisse les choisir.
Désolé pour la présentation un petit peu saccadée sur l'Excel, qui est un peu buggée,
je pense que vous avez vu l'essentiel, les prochaines étapes, c'est vraiment de faire
maintenant une conception de chaufferie avec un Key User côté opération, pour qu'on puisse
vraiment tester bien l'outil, voir qu'il n'y a pas des bugs quelque part, voir s'il répond correctement
aux différents besoins des Ops, et nous, en parallèle, on va faire en sorte de robustifier aussi notre Excel,
pour éviter qu'il soit cassable facilement si on vient manipuler des onglets.
Est-ce que vous avez des questions ou des remarques ?
Oui, j'ai une question Thierry Foussereau, quel est le niveau de fiabilité de ces calculs de perte de charge ?
On sait l'estimer à peu près ou pas ?
On sait qu'on avait un premier calculateur de perte de charge qui avait un certain nombre d'erreurs,
ou en tout cas qui ne respectait pas exactement ce que disait la littérature scientifique,
là c'est justement ce qui a été repris par Johan pour respecter parfaitement ce que disait la littérature scientifique
pour des calculs de perte de charge, et donc les erreurs ne sont pas vraiment sur les calculs de perte de charge qu'on fait,
mais certainement plus sur les données d'entrée qu'on va mettre dans ces calculs-là.
D'accord, ok, merci.
Moi j'ai une petite question Loïc, mais qui est peut-être un peu désaxée, parce que c'est une question peut-être
qui est plus pour moi pour comprendre un peu, c'est qu'est-ce que le polynôme d'une pompe à chaleur en fait ?
Parce que tu as parlé de polynôme à plusieurs moments et je n'ai pas trop compris à quoi ça correspondait.
En fait c'est juste une équation polynomiale qui te permet à partir des températures côté condenseur, évaporateur,
d'aller calculer les puissances délivrées par ton compresseur ou tes compresseurs qui sont à l'intérieur de la pompe à chaleur.
Et donc en fait pour calculer les puissances d'une pompe à chaleur, soit tu utilises ce polynôme de compresseur,
soit tu peux également utiliser les différents points de fonctionnement donnés par la table de copes et donc donnés par le fabricant.
D'accord, en gros vous interpellez un polynôme à partir des points de fonctionnement pour en déduire le truc,
soit il y a une modélisation, soit vous faites de manière un peu empirique avec un graphe.
La table de copes, le graphe c'est donné par le fabricant et le polynôme, j'ai remarqué l'erreur mais pour moi il est donné aussi directement par le fabricant.
Sachant que dans tous les cas, quand un fabricant donne des tables de copes ou des graphiques, ils sont extraits de polynômes eux-mêmes.
Ah d'accord, ok.
Et parce que à la communauté de chauffagistes, ils donnent des graphes parce que s'ils donnaient des polynômes, je pense que personne ne peut l'utiliser.
Très bien, merci Loïc pour la précision.
Et sinon je confirme pour Thierry ce qu'a répondu Loïc, la problématique c'est les données d'entrée pour les pertes de charges, ce n'est pas le calcul lui-même.
Oui bien sûr.
Parce que tu changes la rigidité d'un tube, tu mets 001 au lieu de 002 et tes pertes de charges explosent de 30%.
Oui.
Donc voilà.
Ok, merci.
Donc bravo.
Il faut voir la suite.
Je pense que maintenant le calcul se réserve à la main à côté d'une chaufferie.
Et puis regardez si on retombe à peu près à 5-10% de prix au même calcul."
"""


PROMPT = "Peux-tu me résumer le transcript suivant d'une réunion R&D :\n\n" + WHISPER_OUTPUT

RESP = """Lors de la réunion, Nicolas a présenté deux nouveautés dans le design. La première nouveauté concerne la deuxième version du comparateur, qui permet de comparer plusieurs résultats dans le design. Dans cette nouvelle version, toutes les sections, y compris les commentaires, les warnings, les graphiques et les tableaux, peuvent être comparées. Nicolas a montré comment les éléments graphiques peuvent être affichés pour la comparaison.

Philippe a fait une remarque positive sur cette nouveauté, en soulignant que cela rendrait l'utilisation du design plus facile, surtout pour comparer des résultats obtenus à différents moments. Il a également suggéré de mettre en évidence les sections comportant des différences entre les résultats, afin de faciliter leur identification. Loïc a répondu que cela faisait partie de la roadmap du projet et que les différences seraient mises en évidence dans les tableaux et les graphiques.

Ensuite, Loïc a présenté une amélioration de la section des tables de copes dans la page performance du design. Il a expliqué que les tables de copes des packs installées sur les showprix bas carbone seraient désormais intégrées systématiquement et que des listes déroulantes plus pratiques et lisibles seraient disponibles. De plus, les fichiers de table de copes pourraient maintenant être téléchargés. Loïc a également mentionné la possibilité de différencier les tables de copes provenant du fournisseur et les tables de copes étendues par Accenta, en utilisant des commentaires et des tags.

Ensuite, Loïc a présenté les évolutions de l'outil config, qui permet de simplifier la phase de conception des chaufferies bas carbone. Il a expliqué que config hydro permet de sélectionner les packs et les pompes à chaleur, et que config schéma permet de représenter schématiquement les équipements sur un schéma. Loïc a présenté les nouveautés de la version 2 de config hydro, notamment l'intégration des packs aéro dans la base de données, la création d'une base de données interconnectée pour les pompes à chaleur, les tables de copes et les polynômes, et la possibilité de sélectionner les compresseurs pour les packs. Il a également mentionné l'utilisation d'un calculateur de pertes de charge pour les pompes, qui permet de choisir les pompes adaptées aux besoins. Loïc a également expliqué que config schéma avait été mis à jour pour prendre en compte ces évolutions.

Des questions ont été posées sur la fiabilité des calculs de perte de charge, et il a été expliqué que les calculs étaient fiables mais que les erreurs pouvaient se trouver dans les données d'entrée. Finalement, la réunion s'est terminée par des félicitations et des remarques encourageantes sur les progrès réalisés.
"""

import gradio as gr

tts_examples = [
    "I love learning machine learning",
    "How do you do?",
]

def whisper_fn(file_path):
    return ""

def chat_fn(message, history):
    return ""

whisper_demo = gr.Interface(fn=whisper_fn, inputs=gr.Audio(value="/home/jeremie/Téléchargements/démo_iagen/backup/demo_rnd_2023-05-26.mp3"), outputs=gr.Textbox(value=WHISPER_OUTPUT))

chatgpt_demo = gr.ChatInterface(chat_fn, chatbot=gr.Chatbot(value=[[PROMPT, RESP]], height=600), retry_btn=None, undo_btn=None, clear_btn=None)


demo = gr.TabbedInterface([whisper_demo, chatgpt_demo], ["Whisper", "ChatGPT"])

if __name__ == "__main__":
    demo.launch()


