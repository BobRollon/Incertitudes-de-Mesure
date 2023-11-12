# -*- coding: utf-8 -*-
# Test de crash
# Test client : prgm facile d'utilisation et de coprehension ?
"""
1er bug : entré pas entre les ;
2eme bug : gérer les erreurs
3eme bug : 
"""
try:
    import numpy as nu
    import numpy.random as rd
    from math import sqrt
    from sympy.core import sympify
    import re as re
    import os as os
    from typing import Tuple
except ModuleNotFoundError:
    print("Error import. The program requires sympy and numpy libraries.")
    print(
        "Install the various libraries with 'pip install' command in your powershell, then restart the program."
    )
    exit()
C = 3.2974
D = 2.5000
E = 1.9954
F = 4.2181
G = 2.0055
B = F - G
A = B * C / (D * E)
u_C = 0.012
u_D = 0.020
u_E = 0.015
u_F = 0.012
u_G = 0.011
u_B = sqrt(u_F**2 + u_G**2)
u_A = A * sqrt(
    (u_B / B) ** 2 + (u_C / C) ** 2 + (u_D / D**2) + (u_E / E) ** 2
)
N = 10**3
table_mesure = [(C, u_C), (D, u_D), (E, u_E), (B, u_B)]
formule = " "


class Measure:
    """docstring for Mesure"""

    _names = set()

    def control_format_attribut(name, value, precision):
        bool_validité = True
        if not VerificationVariable(re.split("[.\-*]", value)):
            bool_validité = False # ATTENTION type numpy après simulation !!!!
            raise ValueError(
                f"Error Entry. Enter again the value. Check the requirements of entry.\n{value} not correct."
            )
            value = " "
        if not VerificationVariable(re.split("[.\-*]", precision)):
            bool_validité = False
            raise ValueError(
                f"Error Entry. Enter again the precision. Check the requirements of entry.\n{precision} not correct"
            )
            precision = " "
        if name in Measure._names and name != " ":
            name = " "
            return name, value, precision
            raise ValueError(
                f"Error Entry. Enter again the name. Check the requirements of entry.\n{name} not correct."
            )
        return name, value, precision, bool_validité

    def __init__(self, name, value, precision):
        (
            name,
            value,
            precision,
            bool_validité,
        ) = Measure.control_format_attribut(name, value, precision)
        Measure._names.add(name)
        self.name = name
        self.value = float (value)
        self.precision = float (precision)
        self.valide = bool_validité

def VerificationVariable(variable: list):  # len(x) POURQUOI CA MARCHE ?
    """
    prends une liste de deux éléments et vérifie si les deux sont bien des entiers
    """
    for element in variable:
        if (
            element.isdecimal() == True or element == ""
        ) and variable != False:
            variable = True
        else:
            variable = False
    return variable

def Parsing_FindAssociatedReversedParenthese(
    formule :str, index_first_parenthese : int
):  # complexité : [:len(x)]
    """
    Va chercher l'indice de la parenthèse complémentaire d'une parenthèse donné
    """
    compte = 0
    index_reversed_parenthese = 0
    for element in formule[index_first_parenthese:]:
        if element == ")" and compte == 1:
            have_index_reversed_parenthese = True
            break
        elif element == "(":
            compte = compte + 1
        elif element == ")" and compte != 1:
            compte = compte - 1
        index_reversed_parenthese = index_reversed_parenthese + 1
    return index_reversed_parenthese


def Parsing_Calcul(
    list_element_calcul, local_variable, rang_to_start, string_operateur
):  # complexite: len (x) car appelé par boucle for
    Parsing_Addition = lambda terme1, terme2: terme1 + terme2
    Parsing_Modulo = lambda terme1, terme2: terme1 % terme2
    Parsing_floor = lambda terme1, terme2: terme1 // terme2
    Parsing_Division = lambda terme1, terme2: terme1 / terme2
    Parsing_Multiplication = lambda terme1, terme2: terme1 * terme2
    Parsing_Soustraction = lambda terme1, terme2: terme1 - terme2
    dic_operation_first_priority = {
        "*": Parsing_Multiplication,
        "//": Parsing_floor,
        "/": Parsing_Division,
        "%": Parsing_Modulo,
    }
    dic_operation_seconde_priority = {
        "+": Parsing_Addition,
        "-": Parsing_Soustraction,
    }
    dic_set_of_operation = {
        "+-": dic_operation_seconde_priority,
        "*//%": dic_operation_first_priority,
    }
    index_list_ = rang_to_start
    while list_element_calcul[index_list_] not in string_operateur:
        index_list_ = index_list_ + 1
    variable_1 = local_variable[f"{list_element_calcul[index_list_ - 1]}"]
    variable_2 = local_variable[f"{list_element_calcul[index_list_ + 1]}"]
    resultat = [
        dic_set_of_operation[
           	string_operateur
        ][list_element_calcul[index_list_]](variable_1, variable_2)
    ]
    elements_before = list_element_calcul[: index_list_ - 1]
    elements_after = list_element_calcul[index_list_ + 2 :]
    list_result_calcul = elements_before + resultat + elements_after
    rang_at_end = index_list_ - 1
    return list_result_calcul, rang_at_end


def Parsing_IterationInParenthesis(
    element_formule, local_variable
):  # complexité: 3 len(x)
    rang_operateur = 0
    rang_var = 0
    for operateur in element_formule:
        if (
            operateur == "-"
            and not VerificationVariable(
                element_formule[rang_operateur - 1].split(".")
            )
            and operateur not in local_variable.keys()
        ):
            element_formule = (
                element_formule[: rang_operateur - 1]
                + [-local_variable[f"{element_formule[rang_operateur+1]}"]]
                + element_formule[rang_operateur + 2 :]
            )
        rang_operateur = rang_operateur + 1
    while "**" in element_formule:
        elements_before = element_formule[: element_formule.index("**") - 1]
        elements_after = element_formule[element_formule.index("**") + 2 :]
        operation = [
            element_formule[element_formule.index("**") - 1]
            ** element_formule[element_formule.index("**") + 1]
        ]
        element_formule = elements_before + operation + elements_after
    rang_last_loop = 0
    while (
        "*" in element_formule
        or "/" in element_formule
        or "%" in element_formule
    ):
        element_formule, rang_last_loop = Parsing_Calcul(
            element_formule, local_variable, rang_last_loop, "*//%"
        )
        local_variable[str(element_formule[rang_last_loop])] = element_formule[
            rang_last_loop
        ]
    rang_last_loop = 0
    while "+" in element_formule[-1] or "-" in element_formule[-1]:
        element_formule, rang_last_loop = Parsing_Calcul(
            element_formule, local_variable, rang_last_loop, "+-"
        )
        local_variable[str(element_formule[rang_last_loop])] = element_formule[
            rang_last_loop
        ]
    return element_formule


def Parsing_OperatingOrderEtablishment(formule :list, local_variable :dict) -> Tuple[list, list] :  # len (x)**2
    """
	Compte les parenthèse et relève leurs coordonnés dans formule et note les propriétés opératoires
    """
    list_classe = [0] # index numero = index de la parenthèse correspondante dans borne_parenthese
    classe = 0 # propriété opératoire du terme à l'index donné
    borne_parenthese = [[0, len(formule)]] # 1er parenthèse de position 0 à fin
    # element : [index of first element in parenthe, index parenthese supplementaire]
    index_terme = 0
    for terme in formule:
        if "(" == terme:
            borne_parenthese.append(
                [
                    index_terme + 1,
                    Parsing_FindAssociatedReversedParenthese(  #
                        formule, index_terme
                    )
                    
                ]
            )
            list_classe.append(classe)
            classe = classe + 1
        elif ")" == terme:
            classe = classe - 1
        elif VerificationVariable(terme.split(".")): # passe si term est un float
            local_variable[f"{terme}"] = float(terme)
            #local_variable[f"{terme}"] = Measure (f"{terme}",float(terme),0) # rajoute au dico les constantes pour le parsing
        index_terme = index_terme + 1
    return borne_parenthese, list_classe


def Parsing(
    formule : str, local_variable : dict
):  # len(x)**2 + 3len(x) + n**2 (n le nombre de parenthèse)
    """

	"""
    formule = formule.split() # str => list 
    borne_parenthese, list_classe = Parsing_OperatingOrderEtablishment(  
        formule, local_variable
    )
    list_variable = []
    while len(borne_parenthese) != 0:
        borne_element = borne_parenthese[list_classe.index(max(list_classe))]
        number = Parsing_IterationInParenthesis(
            formule[borne_element[0] : borne_element[1]], local_variable
        )
        local_variable[f"{number[0]}"] = number[0]
        décalage = len(number) - (
            len(formule[borne_element[0] : borne_element[1]]) + 2
        )
        if borne_parenthese[list_classe.index(max(list_classe))][0] - 1 < 0:
            formule = (
                formule[:0]
                + number
                + formule[
                    borne_parenthese[list_classe.index(max(list_classe))][1]
                    + 1 :
                ]
            )
        else:
            formule = (
                formule[
                    : borne_parenthese[list_classe.index(max(list_classe))][0]
                    - 1
                ]
                + number
                + formule[
                    borne_parenthese[list_classe.index(max(list_classe))][1]
                    + 1 :
                ]
            )
        for borne in range(len(borne_parenthese)):
            if (
                borne_parenthese[borne][0]
                >= borne_parenthese[list_classe.index(max(list_classe))][0]
            ):
                borne_parenthese[borne][0] = (
                    borne_parenthese[borne][0] + décalage
                )
            if (
                borne_parenthese[borne][1]
                >= borne_parenthese[list_classe.index(max(list_classe))][1]
            ):
                borne_parenthese[borne][1] = (
                    borne_parenthese[borne][1] + décalage
                )
        borne_parenthese.remove(
            borne_parenthese[list_classe.index(max(list_classe))]
        )
        list_classe.remove(list_classe[list_classe.index(max(list_classe))])
    return formule[0]


def Initialisation_VerificationAndEtablishmentFormula (test, list_name) -> tuple:
    formule = ""
    formule_sim = ""
    boul = True
    for var in range(len(test)):
        if (
            test[var] not in list_name
            and test[var] not in "-+**/()"
            and test[var].isdigit() != True
        ):  # si l'element n'est ni une variable, ni un nombre, ni un opérateur
            boul = False
            print(
                "Error Entry. Enter again the formula. Check the requirements of entry."
            )
            print(f"{test[var]} not correct.")
            formule = " "
        elif test[var] in list_name:
            formule = formule + test[var]
            formule_sim = formule_sim + test[var] + "_sim" + " "
        elif test[var + 1] not in "**%//+-()" and test[var] not in "**%//+-()":
            formule = formule + test[var] + "." + test[var + 1]
            formule_sim = formule_sim + test[var] + "." + test[var + 1] + " "
        elif (
            test[var - 1] not in "**%//+-()" and test[var] not in "**%//+-()"
        ):  # pass car déja compté dans le précédent passage avec la condition supérieur
            pass
        else:
            formule = formule + test[var]
            formule_sim = formule_sim + test[var] + " "
    return formule, formule_sim, boul

def Initialisation(nbr_entrys_require : int, formule: str, dico_mesure : dict) -> tuple:
    # Créer un fichier config en txt, l'ouvre, le lis, vérfie validité des entrées, si l'une non correcte et rouvre le document avec les données non valide effacé jusqu'à validité de toute les entrée
    bool_variable = [False]  # False necessaire à l'entré dans while
    bool_formule = False
    while not bool_variable or not bool_formule: # bool_formule carac. validité de la fonction 
        Measure._names.clear()
        with open("ConfigFile.txt", "w") as config:
            space = " "
            list_exigence_variable = [
                "Exigences du format:\n",
                f"{space :5}- La première lettre doit être une majuscule\n",
                f"{space :5}- Le nom peut être un mot ou une lettre. Veillez à ne pas mettre des noms trop difficile pour limiter les erreurs de frappe.\n",
                f"{space :5}- Toutes les mesures doivent être dans des unités homogènes et les précisions dans la même unité que sa mesure\n",
                f"{space :5}- Ne pas mettre les unités derrière les valeurs\n",
                f"{space :5}- Entré sous la forme nom;mesure;precision/incertitude\n\n",
            ]
            list_exigence_formule = [
                "\nExigences du format:\n",
                f"{space :5}- Nom de Variable de la formule doivent être les noms de Variable des mesures entrer\n",
                f"{space :5}- Les noms, les opérateurs et les constantes doivent être séparé par des espaces.\n",
                f"{space :5}- En cas de simulation de mesure simple tapez seulement Entrer.\n",
                f"{space :5}- N'accepte pas les modulo et les divisions euclidiennes.\n",
                f"{space :5}- Les decimales se marquent avec un '.' et non une ','.\n",
                f"{space :5}- Les virgulent doivent être des points\n\n",
            ]
            config.writelines(list_exigence_variable)
            numero_variable = 0
            for entry in Measure._names :
                config.write(
                    f"variable {numero_variable}; {entry.name};{entry.value};{entry.precision};\n"
                )  # entre les données déjà existante
                numero_variable = numero_variable + 1
            if (
                Measure._names.__len__() < nbr_entrys_require
            ):  # si première formule => liste d'espace; len (list_name) = len (list_mesure) = len (list_precision) = nbr_entrys_require NECESSAIRE
                for entry in range(
                    nbr_entrys_require
                ):  # créer les intitulées a completer par l'utilisateur
                    config.write(f"variable {entry + 1}; ; ; ;\n")
            config.write(f"\n\n\n")
            config.writelines(list_exigence_formule)
            config.write(f"formule :{formule}")
        os.startfile("ConfigFile.txt")
        input(
            "\n\nTapez entrer une fois le fichier modifié et sauvegardé.\n\n"
        )
        number_error = 0
        with open("ConfigFile.txt", "r") as config:
            data = config.readlines()
            while not "formule" in data[-1]:
                data = data[:-1]
            formule = data[-1].split("formule :")[1].strip()
            data = [
                line.split(";")[1:-1] for line in data if ";" in line
            ]  # => [["name", valeur, precision], ["name", valeur, precision]]
            # filtre puis Séparation des différentes donné ; élément 0 => intitulé généré dans le doc
            data.remove(["mesure"])  # suppression de l'exemple
            for line in data:
                line = [element.strip() for element in line]
                try:
                    dico_mesure [line[0]] = Measure(line[0], line[1], line[2])
                except ValueError:
                    bool_variable.append(False)
                    dico_mesure [""] = Measure(
                        " ", line[1], line[2]
                    )
                    number_error = number_error + 1

            (
                formule,
                formule_sim,
                bool_formule,
            ) = Initialisation_VerificationAndEtablishmentFormula(
                re.split("[ .]", formule), Measure._names
            )
            # verification de la validité de la formule et transformation de la formule
            # split par point pour pouvoir utiliser isdigit sur des floats
    return formule, formule_sim, dico_mesure


def CalculIncertitudeMonteCarlo(u : float, X : float, N_1 : int, mesure: str):
	# u => ; X=> ;
    while True:
        calcul_type = input(
            f"Veuillez entrer le type d'incertitude de la mesure {mesure}.\n"
        )
        if ("IT" in calcul_type or "IT".lower() in calcul_type) and (
            "P" not in calcul_type and "P".lower() not in calcul_type
        ):
            X_sim = X + rd.normal(0, u, N_1)
            break
        elif (
            "IT" not in calcul_type and "IT".lower() not in calcul_type
        ) and ("P" in calcul_type or "P".lower() in calcul_type):
            X_sim = X + rd.normal(0, u / sqrt(3), N_1)
            break
        else:
            print(
                "Error Entry. Enter only 'IT' or 'P' without inverted comma."
            )
    return X_sim


def CalculIncertitudeMethodeB(formule : str, n : int, mesure : float) -> float:
	if "*" in formule :
		somme = 0
		for i in dico_variable.keys () :
			sommme =+ (dico_variable[i][1]/dico_variable[i][0])**2
		incertitude_mesure = mesure*sqrt(somme)
	elif "+" in formule :
		somme = 0
		for i in dico_variable.keys () :
			somme =+ (dico_variable[i][1])**2
		incertitude_mesure = sqrt(somme)
	return (incertitude_mesure)


    

def main (formule : str) -> int :
	dico_mesure = {}
	print(
	    " Test de crash\n Test client : prgm facile d'utilisation et de comprehension ?\n"
	)

	while True:  # Test de validité
	    nbr_variable = input("\nEntrez le nombre de mesures.\n")
	    if (
	        nbr_variable.isdigit() == True
	    ):  # Verifie que l'entré est un nombre entier
	        nbr_variable = int(nbr_variable)  # transforme la string en integer
	        break  # sortie de la boucle infinie
	    else:
	        print(
	            "Error Entry. Require an Integer. Enter again your value."
	        )  # message d'erreur si test échou, retour dans la boucle

	formule, formule_sim, dico_mesure = Initialisation(
	    nbr_variable, formule, dico_mesure
	)  # Appel de la fonction pour entrer la formule et la rendre exploitable
	if (
	    formule != ""
	):  # si il y a une formule, calcul de celle-ci avec les variables entrées précédemment
	    dico_variable = {}
	    for mesure in dico_mesure.items():
	    	dico_variable [mesure[1].name] = mesure[1].value
	    calcul = sympify(formule, locals=dico_variable)
	    calcul = eval (formule, dico_variable)
	else:
	    calcul = dico_variable[
	        f"{list (dico_variable.keys())}"[0] # prends la "première" mesure du dico. A CHANGER
	    ]  # A faire : => calcul => list des mesures; calcul_sim list des simulation de chq mesure de manière indépendante

	print(
	    "\nExigences du format:\n - Entrez 'IT' pour incertitude-type.\n - Entrez 'P' pour une précision ou une demi-mesure.\n - Respectez les majuscules."
	)
	dico_variable_sim = {}
	for mesure in dico_mesure.keys() :  # Balaye toute les variables entrées
	    dico_variable_sim [mesure+"_sim"] = CalculIncertitudeMonteCarlo(
	        dico_mesure[mesure].precision, dico_mesure[mesure].value, N, mesure
	    )
	    # Calcul l'incertitude type de chq mesure
	if formule_sim != "":  # si formule entré
	    calcul_sim = Parsing(
	        formule_sim, dico_variable_sim
	    )  # exploitation et calcul de la formule avec les variables simulées
	else:
	    calcul_sim = dico_variable_sim[
	        f"{list (dico_variable_sim.keys())}"[0]
	    ]  # A faire

	calcul_moy = nu.average(
	    calcul_sim
	)  # calcul de la valeur moyenne de la simulation de la formule
	u_A_1 = nu.std(calcul_sim, ddof=1)  # calcul de l'incertitude type de la formule

	print("A = ", A, "+-", u_A, "Méthode B")
	print("A = ", calcul_moy, "+-", u_A_1, "Méthode Monte-Carlo")



if __name__ == "__main__":
	exit(main(formule))