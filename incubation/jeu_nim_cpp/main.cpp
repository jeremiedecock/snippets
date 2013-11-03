/*
 * Jérémie Decock 2013
 * Jeu écrit pour le ... IUT (2013)
 */

#include <iostream>
#include <cstdlib>
#include <ctime>

using namespace std;

const int NB_MIN_ALLUMETTES = 10;
const int NB_MAX_ALLUMETTES = 80;

const int NB_MIN_ALLUMETTES_ENLEVEES = 1;
const int NB_MAX_ALLUMETTES_ENLEVEES = 3;

const int ORDINATEUR = 0;
const int JOUEUR = 1;

int main() {

    int joueur;
    int nb_allumettes;
    int nb_allumettes_a_retirer;
    char recommencer;

    // Initialisation du générateur de nombres aléatoires
    srand(time(NULL));

    do {
        // Qu. 1
        cout << "Saisir le nombre d'allumettes (entier compris entre " << NB_MIN_ALLUMETTES << " et " << NB_MAX_ALLUMETTES << ") : ";
        cin >> nb_allumettes;
        while((nb_allumettes < NB_MIN_ALLUMETTES) || (nb_allumettes > NB_MAX_ALLUMETTES)) {
            cout << "Valeur incorrecte!" << endl;
            cout << "Saisir le nombre d'allumettes (entier compris entre " << NB_MIN_ALLUMETTES << " et " << NB_MAX_ALLUMETTES << ") : ";
            cin >> nb_allumettes;
        }
        
        // Qu. 2
        cout << "Il reste " << nb_allumettes << " allumettes" << endl; ;
        for(int i=0 ; i<nb_allumettes ; i++) {
            cout << "|";
        }
        cout << endl;
    
        // Qu. 3
        //cout << "Qui commence (" << ORDINATEUR << " pour moi et " << JOUEUR << " pour toi) ? ";
        //cin >> joueur;
        //while((joueur != ORDINATEUR) && (joueur != JOUEUR)) {
        //    cout << "Valeur incorrecte!" << endl;
        //    cout << "Qui commence (" << ORDINATEUR << " pour moi et " << JOUEUR << " pour toi) ? ";
        //    cin >> joueur;
        //}
        
        // Qu. 9
        joueur = rand() % 2 + 1;

        // Qu. 6
        do {
            if(joueur == JOUEUR) {
                // Qu. 4
                cout << "Saisir le nombre d'allumettes à enlever (entier compris entre " << NB_MIN_ALLUMETTES_ENLEVEES << " et " << (nb_allumettes < NB_MAX_ALLUMETTES_ENLEVEES ? nb_allumettes : NB_MAX_ALLUMETTES_ENLEVEES) << ") : ";
                cin >> nb_allumettes_a_retirer;
                while((nb_allumettes_a_retirer < NB_MIN_ALLUMETTES_ENLEVEES) || (nb_allumettes_a_retirer > NB_MAX_ALLUMETTES_ENLEVEES) || (nb_allumettes_a_retirer > nb_allumettes)) {
                    cout << "Valeur incorrecte!" << endl;
                    cout << "Saisir le nombre d'allumettes à enlever (entier compris entre " << NB_MIN_ALLUMETTES_ENLEVEES << " et " << (nb_allumettes < NB_MAX_ALLUMETTES_ENLEVEES ? nb_allumettes : NB_MAX_ALLUMETTES_ENLEVEES) << ") : ";
                    cin >> nb_allumettes_a_retirer;
                }
            } else {
                // Qu. 8
                nb_allumettes_a_retirer = nb_allumettes % 4; // stratégie optimale
                if(nb_allumettes_a_retirer == 0) {
                    // Qu. 5
                    do {
                        nb_allumettes_a_retirer = rand() % NB_MAX_ALLUMETTES_ENLEVEES + 1;
                    } while(nb_allumettes_a_retirer > nb_allumettes);
                }
            }

            nb_allumettes -= nb_allumettes_a_retirer;

            // Qu. 2
            cout << "Il reste " << nb_allumettes << " allumettes" << endl; ;
            for(int i=0 ; i<nb_allumettes ; i++) {
                cout << "|";
            }
            cout << endl;

            if(nb_allumettes > 0) {
                joueur = (joueur + 1) % 2;
            }
        } while(nb_allumettes > 0);

        // Qu. 7
        cout << (joueur == JOUEUR ? "Tu as" : "J'ai") << " gagné!" << endl;

        cout << "Recommencer (O/N) ? ";
        cin >> recommencer;
    } while((recommencer == 'o') || (recommencer == 'O'));

    cout << "Bye!" << endl;

    return 0;
}
