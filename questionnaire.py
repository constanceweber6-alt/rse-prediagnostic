"""Questionnaire of the CSR pre-assessment, focused on IT and supply chain.

The four themes follow the structure of the main CSR ratings used by large
groups to assess their suppliers and subsidiaries (environment, labour and
human rights, ethics, sustainable procurement). Each question is scored from
0 to 3 depending on maturity. Texts are available in French and English.
"""

from dataclasses import dataclass, field

LANGS = ("fr", "en")

ANSWER_SCALE = {
    "fr": {
        0: "Rien en place",
        1: "Démarche initiée (actions ponctuelles, rien d'écrit)",
        2: "Formalisé (politique ou procédure écrite)",
        3: "Déployé et mesuré dans tous les pays (indicateurs, preuves)",
    },
    "en": {
        0: "Nothing in place",
        1: "Started (one-off actions, nothing written)",
        2: "Formalised (written policy or procedure)",
        3: "Deployed and measured in every country (KPIs, evidence)",
    },
}

PILLARS = {
    "ENV": {"fr": "Environnement et Green IT", "en": "Environment and Green IT"},
    "SOC": {"fr": "Social et droits humains", "en": "Labour and human rights"},
    "ETH": {"fr": "Éthique et cybersécurité", "en": "Ethics and cybersecurity"},
    "ACH": {"fr": "Achats responsables et vigilance", "en": "Sustainable procurement and due diligence"},
}

SECTORS = {
    "IT": {"fr": "IT et services numériques", "en": "IT and digital services"},
    "SCM": {"fr": "Supply chain et logistique", "en": "Supply chain and logistics"},
    "HOSP": {"fr": "Hôtellerie et services multi-sites", "en": "Hospitality and multi-site services"},
    "HW": {"fr": "Matériel et électronique", "en": "Hardware and electronics"},
}

ENTITY_TYPES = {
    "GROUP": {"fr": "Groupe (vision consolidée)", "en": "Group (consolidated view)"},
    "SUB": {"fr": "Filiale ou pays", "en": "Subsidiary or country"},
    "SUP": {"fr": "Fournisseur", "en": "Supplier"},
}

REGIONS = {
    "EU": {"fr": "Europe", "en": "Europe"},
    "NA": {"fr": "Amérique du Nord", "en": "North America"},
    "APAC": {"fr": "Asie-Pacifique", "en": "Asia-Pacific"},
    "LATAM": {"fr": "Amérique latine", "en": "Latin America"},
    "MEA": {"fr": "Moyen-Orient et Afrique", "en": "Middle East and Africa"},
}

REGULATIONS = {
    "CSRD": {
        "fr": "CSRD (reporting de durabilité européen)",
        "en": "CSRD (EU sustainability reporting)",
    },
    "CSDDD": {
        "fr": "CSDDD (devoir de vigilance européen)",
        "en": "CSDDD (EU corporate sustainability due diligence)",
    },
    "VIGILANCE": {
        "fr": "Loi française sur le devoir de vigilance",
        "en": "French Duty of Vigilance Law",
    },
    "SAPIN2": {
        "fr": "Loi Sapin II (anticorruption)",
        "en": "Sapin II Law (French anti-corruption)",
    },
    "NIS2": {
        "fr": "Directive NIS 2 (cybersécurité)",
        "en": "NIS 2 Directive (cybersecurity)",
    },
    "GDPR": {
        "fr": "RGPD (données personnelles)",
        "en": "GDPR (personal data)",
    },
}

# Regions where labour and supply chain risks are usually higher.
# Simplification for prioritisation only, not a country risk index.
HIGHER_RISK_REGIONS = {"APAC", "LATAM", "MEA"}

# Weight of each theme by sector (sum = 1).
# Inspired by market practice, not an official rating grid.
SECTOR_WEIGHTS = {
    "IT": {"ENV": 0.25, "SOC": 0.25, "ETH": 0.30, "ACH": 0.20},
    "SCM": {"ENV": 0.35, "SOC": 0.25, "ETH": 0.15, "ACH": 0.25},
    "HOSP": {"ENV": 0.25, "SOC": 0.35, "ETH": 0.15, "ACH": 0.25},
    "HW": {"ENV": 0.30, "SOC": 0.25, "ETH": 0.15, "ACH": 0.30},
}


@dataclass(frozen=True)
class Question:
    id: str
    pillar: str
    text: dict
    help: dict
    action: dict
    impact: int  # 1 = low, 3 = high
    effort: int  # 1 = quick, 3 = heavy
    regulations: tuple = ()
    # Extra priority for some sectors (multiplier, default 1)
    sector_boost: dict = field(default_factory=dict)
    # More critical when the entity operates in several or higher-risk regions
    international: bool = False
    risk_sensitive: bool = False


QUESTIONS = [
    # Environment and Green IT
    Question(
        "ENV1", "ENV",
        text={
            "fr": "Avez-vous une politique environnementale signée par la direction et appliquée dans tous les pays ?",
            "en": "Do you have an environmental policy signed by top management and applied in every country?",
        },
        help={
            "fr": "Un seul document de référence pour le groupe, traduit et relayé localement.",
            "en": "One reference document for the whole group, translated and relayed locally.",
        },
        action={
            "fr": "Rédiger une politique environnementale groupe d'une page, la faire signer par la direction et la traduire pour chaque pays.",
            "en": "Write a one-page group environmental policy, have it signed by top management and translate it for each country.",
        },
        impact=3, effort=1, international=True,
    ),
    Question(
        "ENV2", "ENV",
        text={
            "fr": "Mesurez-vous vos émissions de gaz à effet de serre, scope 3 compris (achats, cloud, transport) ?",
            "en": "Do you measure your greenhouse gas emissions, including scope 3 (purchases, cloud, transport)?",
        },
        help={
            "fr": "Le scope 3 représente souvent plus de 80 % des émissions d'une entreprise IT ou logistique.",
            "en": "Scope 3 often represents most of the emissions of an IT or logistics company.",
        },
        action={
            "fr": "Réaliser un bilan carbone complet (scopes 1, 2 et 3) en commençant par les postes les plus lourds : achats, cloud, transport.",
            "en": "Run a full carbon footprint (scopes 1, 2 and 3), starting with the heaviest items: purchases, cloud, transport.",
        },
        impact=3, effort=2, regulations=("CSRD",),
    ),
    Question(
        "ENV3", "ENV",
        text={
            "fr": "Avez-vous des objectifs de réduction alignés sur la science (type SBTi) et suivis chaque année ?",
            "en": "Do you have science-based reduction targets (SBTi type) tracked every year?",
        },
        help={
            "fr": "Les grands donneurs d'ordre demandent de plus en plus des objectifs validés.",
            "en": "Large customers increasingly ask their suppliers for validated targets.",
        },
        action={
            "fr": "Fixer des objectifs de réduction à 2030 alignés sur l'Accord de Paris et publier leur suivi annuel.",
            "en": "Set 2030 reduction targets aligned with the Paris Agreement and publish yearly progress.",
        },
        impact=3, effort=2, regulations=("CSRD",),
    ),
    Question(
        "ENV4", "ENV",
        text={
            "fr": "Pilotez-vous l'impact de votre numérique (énergie des data centers et du cloud, durée de vie et recyclage du matériel) ?",
            "en": "Do you manage your digital footprint (data centre and cloud energy, device lifetime and recycling)?",
        },
        help={
            "fr": "Par exemple : PUE des data centers, part d'énergie renouvelable, reconditionnement des ordinateurs, filière DEEE.",
            "en": "For example: data centre PUE, share of renewable energy, refurbished laptops, e-waste recycling.",
        },
        action={
            "fr": "Lancer une démarche Green IT : suivre l'énergie du cloud, allonger la durée de vie du matériel et passer par une filière de recyclage certifiée.",
            "en": "Launch a Green IT plan: track cloud energy, extend device lifetime and use a certified e-waste recycling partner.",
        },
        impact=2, effort=2,
        sector_boost={"IT": 1.5, "HW": 1.3},
    ),
    Question(
        "ENV5", "ENV",
        text={
            "fr": "Réduisez-vous les impacts du transport et des emballages (choix des transporteurs, report modal, emballages réutilisables) ?",
            "en": "Do you reduce transport and packaging impacts (carrier selection, modal shift, reusable packaging)?",
        },
        help={
            "fr": "Le transport est un levier majeur pour la logistique et la distribution.",
            "en": "Transport is a major lever for logistics and distribution.",
        },
        action={
            "fr": "Intégrer des critères carbone dans le choix des transporteurs et tester le report modal ou les emballages réutilisables sur un flux pilote.",
            "en": "Add carbon criteria to carrier selection and pilot modal shift or reusable packaging on one flow.",
        },
        impact=2, effort=2,
        sector_boost={"SCM": 1.5, "HOSP": 1.2, "HW": 1.2},
    ),
    # Labour and human rights
    Question(
        "SOC1", "SOC",
        text={
            "fr": "Avez-vous un système santé et sécurité commun à tous les sites, sous-traitants compris ?",
            "en": "Do you have a health and safety system shared by all sites, including subcontractors?",
        },
        help={
            "fr": "Évaluation des risques, suivi des accidents, formation. La norme de référence est ISO 45001.",
            "en": "Risk assessment, accident tracking, training. The reference standard is ISO 45001.",
        },
        action={
            "fr": "Définir des standards santé et sécurité groupe, suivre le taux d'accidents par site et les étendre aux sous-traitants.",
            "en": "Define group health and safety standards, track the accident rate per site and extend them to subcontractors.",
        },
        impact=3, effort=2,
        sector_boost={"SCM": 1.5, "HOSP": 1.4, "HW": 1.3},
    ),
    Question(
        "SOC2", "SOC",
        text={
            "fr": "Avez-vous des standards sociaux minimum communs à tous les pays (temps de travail, salaires, liberté d'association) ?",
            "en": "Do you have minimum labour standards shared by every country (working hours, wages, freedom of association)?",
        },
        help={
            "fr": "Un socle commun évite les écarts entre filiales, surtout hors d'Europe.",
            "en": "A common baseline avoids gaps between subsidiaries, especially outside Europe.",
        },
        action={
            "fr": "Formaliser un socle social groupe (temps de travail, salaire décent, dialogue social) et vérifier son application pays par pays.",
            "en": "Formalise a group labour baseline (working hours, living wage, social dialogue) and check it country by country.",
        },
        impact=3, effort=2, international=True, risk_sensitive=True,
    ),
    Question(
        "SOC3", "SOC",
        text={
            "fr": "Avez-vous une politique diversité et inclusion avec des indicateurs suivis ?",
            "en": "Do you have a diversity and inclusion policy with tracked KPIs?",
        },
        help={
            "fr": "Par exemple : part de femmes dans le management, écart de rémunération, handicap.",
            "en": "For example: share of women in management, pay gap, disability inclusion.",
        },
        action={
            "fr": "Publier une politique diversité et inclusion et suivre 3 indicateurs : femmes managers, écart salarial, inclusion du handicap.",
            "en": "Publish a diversity and inclusion policy and track 3 KPIs: women in management, pay gap, disability inclusion.",
        },
        impact=2, effort=1, regulations=("CSRD",),
    ),
    Question(
        "SOC4", "SOC",
        text={
            "fr": "Accompagnez-vous les salariés dans l'évolution de leurs compétences (numérique, IA, reconversion) ?",
            "en": "Do you support employees as their skills evolve (digital, AI, reskilling)?",
        },
        help={
            "fr": "Plan de formation, parcours de reconversion, entretiens réguliers.",
            "en": "Training plan, reskilling paths, regular career reviews.",
        },
        action={
            "fr": "Construire un plan de montée en compétences sur le numérique et l'IA, et suivre le nombre d'heures de formation par salarié.",
            "en": "Build an upskilling plan on digital and AI, and track training hours per employee.",
        },
        impact=2, effort=2, sector_boost={"IT": 1.3},
    ),
    Question(
        "SOC5", "SOC",
        text={
            "fr": "Avez-vous cartographié les risques de droits humains liés à vos activités dans chaque pays ?",
            "en": "Have you mapped the human rights risks linked to your operations in each country?",
        },
        help={
            "fr": "Travail forcé, travail des enfants, conditions de travail des prestataires.",
            "en": "Forced labour, child labour, working conditions of service providers.",
        },
        action={
            "fr": "Réaliser une cartographie des risques droits humains par pays et par activité, puis définir des mesures pour les risques les plus élevés.",
            "en": "Map human rights risks by country and activity, then define measures for the highest risks.",
        },
        impact=3, effort=2,
        regulations=("VIGILANCE", "CSDDD"),
        international=True, risk_sensitive=True,
    ),
    # Ethics and cybersecurity
    Question(
        "ETH1", "ETH",
        text={
            "fr": "Avez-vous un code de conduite traduit dans toutes les langues et des formations suivies par tous ?",
            "en": "Do you have a code of conduct translated into every language, with training completed by all employees?",
        },
        help={
            "fr": "Un code non traduit ou jamais expliqué reste lettre morte dans les filiales.",
            "en": "A code that is not translated or explained stays a dead letter in subsidiaries.",
        },
        action={
            "fr": "Traduire le code de conduite dans les langues de chaque pays et lancer une formation en ligne obligatoire avec suivi du taux de complétion.",
            "en": "Translate the code of conduct for every country and launch mandatory e-learning with completion tracking.",
        },
        impact=3, effort=1, international=True,
    ),
    Question(
        "ETH2", "ETH",
        text={
            "fr": "Avez-vous un programme anticorruption basé sur une cartographie des risques ?",
            "en": "Do you have an anti-corruption programme based on a risk map?",
        },
        help={
            "fr": "Règles cadeaux et conflits d'intérêts, contrôle des intermédiaires, conformité Sapin II, FCPA ou UK Bribery Act.",
            "en": "Gifts and conflicts of interest rules, third-party checks, compliance with Sapin II, FCPA or UK Bribery Act.",
        },
        action={
            "fr": "Cartographier les risques de corruption par pays et par processus, puis encadrer cadeaux, conflits d'intérêts et intermédiaires.",
            "en": "Map corruption risks by country and process, then frame gifts, conflicts of interest and intermediaries.",
        },
        impact=3, effort=2, regulations=("SAPIN2",), risk_sensitive=True,
    ),
    Question(
        "ETH3", "ETH",
        text={
            "fr": "Avez-vous un dispositif d'alerte multilingue, accessible aussi aux fournisseurs et partenaires ?",
            "en": "Do you have a multilingual whistleblowing channel, also open to suppliers and partners?",
        },
        help={
            "fr": "Confidentiel, disponible dans toutes les langues du groupe, avec un traitement des alertes suivi.",
            "en": "Confidential, available in every group language, with tracked case handling.",
        },
        action={
            "fr": "Déployer un canal d'alerte en ligne multilingue, ouvert aux tiers, et suivre le délai de traitement des alertes.",
            "en": "Deploy a multilingual online whistleblowing channel open to third parties and track case handling time.",
        },
        impact=2, effort=1, regulations=("SAPIN2", "VIGILANCE"), international=True,
    ),
    Question(
        "ETH4", "ETH",
        text={
            "fr": "Votre sécurité de l'information est-elle certifiée (ISO 27001, SOC 2) et exigée de vos prestataires ?",
            "en": "Is your information security certified (ISO 27001, SOC 2) and required from your providers?",
        },
        help={
            "fr": "Point critique pour les entreprises IT et pour tout groupe qui manipule des données clients.",
            "en": "Critical for IT companies and any group handling customer data.",
        },
        action={
            "fr": "Engager une démarche ISO 27001 sur le périmètre le plus sensible et ajouter des exigences de sécurité dans les contrats prestataires.",
            "en": "Start an ISO 27001 programme on the most sensitive scope and add security requirements to provider contracts.",
        },
        impact=3, effort=3, regulations=("NIS2",), sector_boost={"IT": 1.5},
    ),
    Question(
        "ETH5", "ETH",
        text={
            "fr": "Êtes-vous en conformité avec les lois sur les données personnelles dans chaque pays (RGPD, transferts internationaux) ?",
            "en": "Do you comply with personal data laws in each country (GDPR, international transfers)?",
        },
        help={
            "fr": "Registre des traitements, clauses de transfert hors UE, gestion des demandes des personnes.",
            "en": "Records of processing, transfer clauses outside the EU, handling of data subject requests.",
        },
        action={
            "fr": "Mettre à jour le registre des traitements, sécuriser les transferts de données hors UE et nommer un relais données par pays.",
            "en": "Update the records of processing, secure data transfers outside the EU and appoint a data contact in each country.",
        },
        impact=2, effort=2, regulations=("GDPR",), international=True,
        sector_boost={"IT": 1.3, "HOSP": 1.3},
    ),
    # Sustainable procurement and due diligence
    Question(
        "ACH1", "ACH",
        text={
            "fr": "Avez-vous une politique d'achats responsables et un code de conduite fournisseurs signé ?",
            "en": "Do you have a sustainable procurement policy and a signed supplier code of conduct?",
        },
        help={
            "fr": "Le code fournisseurs fixe vos attentes en matière d'environnement, de social et d'éthique.",
            "en": "The supplier code sets your expectations on environment, labour and ethics.",
        },
        action={
            "fr": "Rédiger une politique d'achats responsables et faire signer un code de conduite à tous les nouveaux fournisseurs.",
            "en": "Write a sustainable procurement policy and have every new supplier sign a code of conduct.",
        },
        impact=3, effort=1,
    ),
    Question(
        "ACH2", "ACH",
        text={
            "fr": "Avez-vous cartographié les risques fournisseurs par pays et par catégorie d'achat ?",
            "en": "Have you mapped supplier risks by country and purchasing category?",
        },
        help={
            "fr": "Base du plan de vigilance : savoir où concentrer les contrôles.",
            "en": "Basis of a due diligence plan: knowing where to focus checks.",
        },
        action={
            "fr": "Construire une cartographie des risques fournisseurs (pays, catégorie, volume) pour cibler les 20 % de fournisseurs les plus exposés.",
            "en": "Build a supplier risk map (country, category, spend) to target the 20% most exposed suppliers.",
        },
        impact=3, effort=2,
        regulations=("VIGILANCE", "CSDDD"),
        international=True, risk_sensitive=True,
    ),
    Question(
        "ACH3", "ACH",
        text={
            "fr": "Évaluez-vous la performance RSE de vos fournisseurs stratégiques (notation, questionnaire, audit) ?",
            "en": "Do you assess the CSR performance of your strategic suppliers (rating, questionnaire, audit)?",
        },
        help={
            "fr": "Par exemple via une plateforme de notation RSE ou des audits sur site.",
            "en": "For example through a CSR rating platform or on-site audits.",
        },
        action={
            "fr": "Demander une évaluation RSE à vos fournisseurs stratégiques et fixer un score minimum pour être référencé.",
            "en": "Ask your strategic suppliers for a CSR assessment and set a minimum score to be listed.",
        },
        impact=3, effort=2, risk_sensitive=True,
    ),
    Question(
        "ACH4", "ACH",
        text={
            "fr": "Connaissez-vous vos fournisseurs de rang 2 et l'origine des matières ou services à risque ?",
            "en": "Do you know your tier-2 suppliers and the origin of high-risk materials or services?",
        },
        help={
            "fr": "Minerais pour le matériel, sous-traitance en cascade pour les services, denrées pour l'hôtellerie.",
            "en": "Minerals for hardware, cascading subcontracting for services, food supplies for hospitality.",
        },
        action={
            "fr": "Lancer un projet de traçabilité sur une catégorie pilote à risque et demander la liste des sous-traitants aux fournisseurs clés.",
            "en": "Launch a traceability project on one high-risk pilot category and ask key suppliers for their subcontractor list.",
        },
        impact=2, effort=3, regulations=("CSDDD",), risk_sensitive=True,
        sector_boost={"HW": 1.6, "SCM": 1.3, "HOSP": 1.2},
    ),
    Question(
        "ACH5", "ACH",
        text={
            "fr": "Accompagnez-vous vos fournisseurs avec des plans d'actions correctives et des objectifs climat ?",
            "en": "Do you support your suppliers with corrective action plans and climate targets?",
        },
        help={
            "fr": "Indispensable pour réduire le scope 3, qui dépend largement des fournisseurs.",
            "en": "Essential to reduce scope 3, which largely depends on suppliers.",
        },
        action={
            "fr": "Mettre en place des plans d'actions correctives pour les fournisseurs à risque et un programme climat pour les plus gros émetteurs.",
            "en": "Set up corrective action plans for risky suppliers and a climate programme for the largest emitters.",
        },
        impact=2, effort=2, regulations=("CSRD",),
    ),
]


def questions_by_pillar(pillar: str) -> list:
    return [q for q in QUESTIONS if q.pillar == pillar]
