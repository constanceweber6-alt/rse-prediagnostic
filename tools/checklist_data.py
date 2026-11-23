"""Generic CSR improvement actions for the checklist page (docs/checklist.html).

Each item: (id, French label, English label, tags)
Tags: "quick" = quick win, "reg" = linked to a regulation or a frequent
customer requirement.
"""

CATEGORIES = [
    {
        "id": "GOV",
        "name": {"fr": "Gouvernance et stratégie RSE", "en": "CSR governance and strategy"},
        "items": [
            ("GOV01", "Nommer un responsable RSE avec un mandat clair de la direction", "Appoint a CSR lead with a clear mandate from top management", ["quick"]),
            ("GOV02", "Réaliser une analyse de double matérialité", "Run a double materiality assessment", ["reg"]),
            ("GOV03", "Formaliser une feuille de route RSE à 3 ans avec des objectifs chiffrés", "Formalise a 3-year CSR roadmap with quantified targets", []),
            ("GOV04", "Intégrer des critères RSE dans la rémunération variable des dirigeants", "Add CSR criteria to executive variable pay", []),
            ("GOV05", "Créer un comité RSE qui se réunit au moins chaque trimestre", "Set up a CSR committee that meets at least every quarter", ["quick"]),
            ("GOV06", "Nommer un relais RSE dans chaque pays ou filiale", "Appoint a CSR contact in each country or subsidiary", []),
            ("GOV07", "Cartographier les attentes des parties prenantes (clients, salariés, investisseurs)", "Map stakeholder expectations (customers, employees, investors)", []),
            ("GOV08", "Présenter les résultats RSE au conseil d'administration une fois par an", "Present CSR results to the board once a year", ["quick"]),
        ],
    },
    {
        "id": "CLI",
        "name": {"fr": "Climat et énergie", "en": "Climate and energy"},
        "items": [
            ("CLI01", "Réaliser un bilan carbone scopes 1 et 2", "Measure scope 1 and 2 emissions", ["reg"]),
            ("CLI02", "Étendre le bilan carbone au scope 3 (achats, cloud, transport, déplacements)", "Extend the carbon footprint to scope 3 (purchases, cloud, transport, travel)", ["reg"]),
            ("CLI03", "Fixer des objectifs de réduction alignés sur l'Accord de Paris", "Set reduction targets aligned with the Paris Agreement", []),
            ("CLI04", "Faire valider les objectifs par la SBTi", "Have targets validated by the SBTi", []),
            ("CLI05", "Passer à un contrat d'électricité renouvelable", "Switch to a renewable electricity contract", ["quick"]),
            ("CLI06", "Suivre les consommations d'énergie par site chaque mois", "Track energy use per site every month", ["quick"]),
            ("CLI07", "Mettre en place une politique de déplacements professionnels bas carbone", "Set up a low-carbon business travel policy", []),
            ("CLI08", "Analyser les risques climatiques physiques sur les sites clés", "Assess physical climate risks for key sites", ["reg"]),
            ("CLI09", "Réaliser un audit énergétique des bâtiments", "Run an energy audit of buildings", ["reg"]),
        ],
    },
    {
        "id": "GIT",
        "name": {"fr": "Green IT et numérique responsable", "en": "Green IT and responsible digital"},
        "items": [
            ("GIT01", "Faire l'inventaire du parc informatique et de son empreinte", "Inventory IT equipment and its footprint", []),
            ("GIT02", "Allonger la durée d'utilisation des ordinateurs et smartphones", "Extend the lifetime of laptops and smartphones", ["quick"]),
            ("GIT03", "Acheter du matériel reconditionné quand c'est possible", "Buy refurbished equipment when possible", ["quick"]),
            ("GIT04", "Passer par une filière certifiée pour le recyclage des déchets électroniques", "Use a certified partner for e-waste recycling", ["reg"]),
            ("GIT05", "Choisir des hébergeurs et clouds avec énergie renouvelable et bon PUE", "Choose hosting and cloud providers with renewable energy and a good PUE", []),
            ("GIT06", "Supprimer les données et environnements inutilisés dans le cloud", "Delete unused data and environments in the cloud", ["quick"]),
            ("GIT07", "Intégrer l'écoconception dans les projets logiciels", "Include eco-design in software projects", []),
            ("GIT08", "Sensibiliser les équipes à la sobriété numérique", "Raise team awareness of digital sobriety", ["quick"]),
            ("GIT09", "Mesurer l'empreinte des usages d'IA générative", "Measure the footprint of generative AI use", []),
        ],
    },
    {
        "id": "LOG",
        "name": {"fr": "Logistique, transport et emballages", "en": "Logistics, transport and packaging"},
        "items": [
            ("LOG01", "Mesurer les émissions du transport par flux et par mode", "Measure transport emissions by flow and mode", []),
            ("LOG02", "Ajouter des critères carbone dans le choix des transporteurs", "Add carbon criteria to carrier selection", []),
            ("LOG03", "Tester le report modal (rail, fluvial) sur un flux pilote", "Pilot modal shift (rail, river) on one flow", []),
            ("LOG04", "Optimiser le taux de remplissage des camions", "Improve truck fill rates", []),
            ("LOG05", "Réduire les emballages plastiques à usage unique", "Reduce single-use plastic packaging", ["reg"]),
            ("LOG06", "Mettre en place des emballages réutilisables avec les partenaires clés", "Set up reusable packaging with key partners", []),
            ("LOG07", "Rejoindre un programme de transport responsable (type EVE ou SmartWay)", "Join a responsible freight programme (such as SmartWay)", []),
            ("LOG08", "Rationaliser les stocks pour limiter les pertes et la casse", "Streamline inventory to limit waste and damage", []),
        ],
    },
    {
        "id": "SOC",
        "name": {"fr": "Social et conditions de travail", "en": "Labour and working conditions"},
        "items": [
            ("SOC01", "Tenir à jour l'évaluation des risques professionnels de chaque site", "Keep the occupational risk assessment of each site up to date", ["reg"]),
            ("SOC02", "Suivre le taux de fréquence et de gravité des accidents", "Track accident frequency and severity rates", []),
            ("SOC03", "Étendre les exigences santé et sécurité aux sous-traitants", "Extend health and safety requirements to subcontractors", []),
            ("SOC04", "Définir un socle social commun à tous les pays", "Define a common labour baseline for every country", []),
            ("SOC05", "Garantir un salaire décent dans tous les pays d'implantation", "Guarantee a living wage in every country of operation", []),
            ("SOC06", "Mener une enquête annuelle d'engagement des salariés", "Run a yearly employee engagement survey", ["quick"]),
            ("SOC07", "Construire un plan de formation sur le numérique et l'IA", "Build a training plan on digital and AI", []),
            ("SOC08", "Encadrer le droit à la déconnexion et le télétravail", "Frame the right to disconnect and remote work", ["quick"]),
            ("SOC09", "Proposer un accompagnement psychologique confidentiel", "Offer confidential psychological support", []),
        ],
    },
    {
        "id": "DEI",
        "name": {"fr": "Diversité et inclusion", "en": "Diversity and inclusion"},
        "items": [
            ("DEI01", "Publier une politique diversité et non-discrimination", "Publish a diversity and non-discrimination policy", ["quick"]),
            ("DEI02", "Mesurer l'écart de rémunération femmes-hommes", "Measure the gender pay gap", ["reg"]),
            ("DEI03", "Fixer un objectif de femmes dans les postes de direction", "Set a target for women in leadership roles", []),
            ("DEI04", "Former les managers aux biais dans le recrutement", "Train managers on hiring bias", []),
            ("DEI05", "Rendre les postes et les outils accessibles aux personnes en situation de handicap", "Make roles and tools accessible to people with disabilities", ["reg"]),
            ("DEI06", "Soutenir des réseaux internes (femmes, LGBT+, générations)", "Support employee networks (women, LGBT+, generations)", ["quick"]),
            ("DEI07", "Accueillir des alternants et des profils en reconversion", "Welcome apprentices and career changers", []),
        ],
    },
    {
        "id": "ETH",
        "name": {"fr": "Éthique et conformité", "en": "Ethics and compliance"},
        "items": [
            ("ETH01", "Rédiger un code de conduite et le traduire pour chaque pays", "Write a code of conduct and translate it for each country", []),
            ("ETH02", "Former tous les salariés au code de conduite chaque année", "Train all employees on the code of conduct every year", []),
            ("ETH03", "Cartographier les risques de corruption par pays et par processus", "Map corruption risks by country and process", ["reg"]),
            ("ETH04", "Encadrer les cadeaux, invitations et conflits d'intérêts", "Frame gifts, hospitality and conflicts of interest", ["quick", "reg"]),
            ("ETH05", "Vérifier l'intégrité des intermédiaires et partenaires", "Run integrity checks on intermediaries and partners", ["reg"]),
            ("ETH06", "Mettre en place un canal d'alerte multilingue ouvert aux tiers", "Set up a multilingual whistleblowing channel open to third parties", ["reg"]),
            ("ETH07", "Publier une politique sur le lobbying et les contributions politiques", "Publish a policy on lobbying and political contributions", []),
            ("ETH08", "Encadrer l'usage éthique de l'IA (charte, comité, revue des cas d'usage)", "Frame the ethical use of AI (charter, committee, use case review)", ["reg"]),
        ],
    },
    {
        "id": "CYB",
        "name": {"fr": "Cybersécurité et données", "en": "Cybersecurity and data"},
        "items": [
            ("CYB01", "Rédiger une politique de sécurité de l'information", "Write an information security policy", ["quick"]),
            ("CYB02", "Activer l'authentification multifacteur pour tous les comptes", "Enable multi-factor authentication for every account", ["quick"]),
            ("CYB03", "Lancer une démarche de certification ISO 27001", "Start an ISO 27001 certification programme", ["reg"]),
            ("CYB04", "Organiser une sensibilisation au phishing chaque année", "Run phishing awareness training every year", ["quick"]),
            ("CYB05", "Tester le plan de continuité et de reprise d'activité", "Test the business continuity and disaster recovery plan", ["reg"]),
            ("CYB06", "Tenir à jour le registre des traitements de données personnelles", "Keep the records of personal data processing up to date", ["reg"]),
            ("CYB07", "Encadrer les transferts de données hors Union européenne", "Frame data transfers outside the European Union", ["reg"]),
            ("CYB08", "Ajouter des exigences de sécurité dans les contrats prestataires", "Add security requirements to provider contracts", []),
        ],
    },
    {
        "id": "ACH",
        "name": {"fr": "Achats responsables et vigilance", "en": "Sustainable procurement and due diligence"},
        "items": [
            ("ACH01", "Rédiger une politique d'achats responsables", "Write a sustainable procurement policy", ["quick"]),
            ("ACH02", "Faire signer un code de conduite à tous les fournisseurs", "Have every supplier sign a code of conduct", ["quick"]),
            ("ACH03", "Cartographier les risques fournisseurs par pays et par catégorie", "Map supplier risks by country and category", ["reg"]),
            ("ACH04", "Demander une évaluation RSE aux fournisseurs stratégiques", "Ask strategic suppliers for a CSR assessment", []),
            ("ACH05", "Fixer un score RSE minimum pour référencer un fournisseur", "Set a minimum CSR score to list a supplier", []),
            ("ACH06", "Auditer sur site les fournisseurs les plus à risque", "Audit the highest-risk suppliers on site", []),
            ("ACH07", "Suivre les plans d'actions correctives des fournisseurs", "Track supplier corrective action plans", []),
            ("ACH08", "Identifier les fournisseurs de rang 2 sur les catégories à risque", "Identify tier-2 suppliers in high-risk categories", ["reg"]),
            ("ACH09", "Lancer un programme climat avec les plus gros fournisseurs émetteurs", "Launch a climate programme with the largest emitting suppliers", []),
            ("ACH10", "Respecter les délais de paiement des PME", "Pay small suppliers on time", ["quick", "reg"]),
            ("ACH11", "Publier un plan de vigilance et son compte rendu de mise en œuvre", "Publish a due diligence plan and its implementation report", ["reg"]),
        ],
    },
    {
        "id": "REP",
        "name": {"fr": "Reporting et communication", "en": "Reporting and communication"},
        "items": [
            ("REP01", "Définir une liste d'indicateurs RSE suivis chaque année", "Define a list of CSR KPIs tracked every year", ["quick"]),
            ("REP02", "Collecter les données RSE de toutes les filiales avec un outil commun", "Collect CSR data from every subsidiary with a shared tool", []),
            ("REP03", "Préparer le reporting CSRD (normes ESRS)", "Prepare CSRD reporting (ESRS standards)", ["reg"]),
            ("REP04", "Faire vérifier les données RSE par un tiers", "Have CSR data verified by a third party", ["reg"]),
            ("REP05", "Répondre aux questionnaires RSE des clients avec un dossier de preuves prêt", "Answer customer CSR questionnaires with a ready evidence pack", ["quick"]),
            ("REP06", "Publier un rapport ou une page RSE accessible au public", "Publish a public CSR report or page", []),
            ("REP07", "Éviter l'écoblanchiment : chaque affirmation appuyée par une preuve", "Avoid greenwashing: back every claim with evidence", ["quick", "reg"]),
            ("REP08", "Partager les résultats RSE avec les salariés en interne", "Share CSR results with employees internally", ["quick"]),
        ],
    },
]


def as_json():
    return [
        {
            "id": c["id"],
            "name": c["name"],
            "items": [
                {"id": i, "label": {"fr": fr, "en": en}, "tags": tags}
                for i, fr, en, tags in c["items"]
            ],
        }
        for c in CATEGORIES
    ]
