"""Help sheets for each action of the pre-assessment.

For every question: the evidence to gather for a CSR assessment and one KPI
to track. Texts in French, English and Japanese.
"""

HELP_SHEETS = {
    "ENV1": {
        "evidence": {
            "fr": ["Politique environnementale datée et signée par la direction", "Versions traduites pour chaque pays", "Preuve de diffusion (intranet, e-mail, affichage)"],
            "en": ["Environmental policy dated and signed by top management", "Translated versions for each country", "Proof of communication (intranet, email, posters)"],
            "ja": ["経営層が署名し日付を記載した環境方針", "各国語の翻訳版", "周知の証跡（イントラネット、メール、掲示）"],
        },
        "kpi": {"fr": "Part des pays où la politique est diffusée", "en": "Share of countries where the policy is communicated", "ja": "方針を周知している国の割合"},
    },
    "ENV2": {
        "evidence": {
            "fr": ["Bilan carbone avec méthode et périmètre (scopes 1, 2 et 3)", "Fichier de calcul et facteurs d'émission utilisés", "Données sources (factures d'énergie, achats, cloud, transport)"],
            "en": ["Carbon footprint with method and scope (scopes 1, 2 and 3)", "Calculation file and emission factors used", "Source data (energy bills, purchases, cloud, transport)"],
            "ja": ["算定方法と範囲を明記した排出量算定書（スコープ1・2・3）", "計算ファイルと使用した排出係数", "元データ（エネルギー請求書、購買、クラウド、輸送）"],
        },
        "kpi": {"fr": "Émissions totales en tonnes de CO2e, dont part du scope 3", "en": "Total emissions in tonnes of CO2e, including scope 3 share", "ja": "総排出量（t-CO2e）とスコープ3の比率"},
    },
    "ENV3": {
        "evidence": {
            "fr": ["Objectifs chiffrés et datés validés par la direction", "Trajectoire de réduction et plan d'actions associé", "Lettre d'engagement ou validation SBTi si disponible"],
            "en": ["Quantified, dated targets approved by top management", "Reduction pathway and related action plan", "SBTi commitment letter or validation if available"],
            "ja": ["経営層が承認した定量・期限付きの目標", "削減の道筋と関連する行動計画", "SBTiのコミットメントレターまたは認定（ある場合）"],
        },
        "kpi": {"fr": "Écart entre émissions réelles et trajectoire cible", "en": "Gap between actual emissions and target pathway", "ja": "実績排出量と目標の道筋との差"},
    },
    "ENV4": {
        "evidence": {
            "fr": ["Inventaire du parc informatique avec dates d'achat", "Rapports énergie ou carbone des fournisseurs cloud et data centers", "Certificats de recyclage du matériel en fin de vie"],
            "en": ["IT equipment inventory with purchase dates", "Energy or carbon reports from cloud and data centre providers", "Recycling certificates for end-of-life equipment"],
            "ja": ["購入日を記載したIT機器の台帳", "クラウド・データセンター事業者のエネルギーまたは排出量報告", "使用済み機器のリサイクル証明書"],
        },
        "kpi": {"fr": "Durée moyenne d'utilisation des ordinateurs portables", "en": "Average lifetime of laptops", "ja": "ノートPCの平均使用年数"},
    },
    "ENV5": {
        "evidence": {
            "fr": ["Grille de sélection des transporteurs avec critère carbone", "Bilan des émissions du transport par flux", "Résultats du pilote (report modal ou emballages réutilisables)"],
            "en": ["Carrier selection grid including a carbon criterion", "Transport emissions report by flow", "Pilot results (modal shift or reusable packaging)"],
            "ja": ["CO2基準を含む運送会社の選定表", "輸送ルート別の排出量報告", "試行結果（モーダルシフトまたは再利用梱包）"],
        },
        "kpi": {"fr": "Émissions par tonne transportée et par kilomètre", "en": "Emissions per tonne-kilometre transported", "ja": "輸送トンキロ当たりの排出量"},
    },
    "SOC1": {
        "evidence": {
            "fr": ["Évaluation des risques professionnels par site", "Registre des accidents et plan de prévention annuel", "Attestations de formation sécurité, sous-traitants compris"],
            "en": ["Occupational risk assessment per site", "Accident log and yearly prevention plan", "Safety training records, including subcontractors"],
            "ja": ["拠点ごとの労働安全リスク評価", "労働災害の記録と年間の予防計画", "協力会社を含む安全教育の受講記録"],
        },
        "kpi": {"fr": "Taux de fréquence des accidents du travail", "en": "Lost-time injury frequency rate", "ja": "労働災害の度数率"},
    },
    "SOC2": {
        "evidence": {
            "fr": ["Socle social groupe validé (temps de travail, salaires, dialogue social)", "Tableau de conformité pays par pays", "Comptes rendus des instances de dialogue social"],
            "en": ["Approved group labour baseline (working hours, wages, social dialogue)", "Country-by-country compliance table", "Minutes of employee representative bodies"],
            "ja": ["承認済みのグループ共通労働基準（労働時間、賃金、労使対話）", "国別の適合状況一覧", "労使協議の議事録"],
        },
        "kpi": {"fr": "Part des pays conformes au socle social", "en": "Share of countries compliant with the labour baseline", "ja": "共通労働基準に適合している国の割合"},
    },
    "SOC3": {
        "evidence": {
            "fr": ["Politique diversité et inclusion signée", "Indicateurs publiés (femmes managers, écart salarial)", "Plan d'actions et formations associées"],
            "en": ["Signed diversity and inclusion policy", "Published KPIs (women in management, pay gap)", "Action plan and related training"],
            "ja": ["署名済みのD&I方針", "公表している指標（女性管理職比率、賃金格差）", "行動計画と関連する研修"],
        },
        "kpi": {"fr": "Part de femmes dans les postes de management", "en": "Share of women in management roles", "ja": "管理職に占める女性の割合"},
    },
    "SOC4": {
        "evidence": {
            "fr": ["Plan de formation annuel incluant le numérique et l'IA", "Suivi des heures de formation par salarié", "Comptes rendus des entretiens professionnels"],
            "en": ["Yearly training plan including digital and AI", "Training hours tracked per employee", "Records of career review meetings"],
            "ja": ["デジタルとAIを含む年間研修計画", "従業員ごとの研修時間の記録", "キャリア面談の記録"],
        },
        "kpi": {"fr": "Heures de formation par salarié et par an", "en": "Training hours per employee per year", "ja": "従業員一人当たりの年間研修時間"},
    },
    "SOC5": {
        "evidence": {
            "fr": ["Cartographie des risques droits humains par pays et par activité", "Plan de mesures pour les risques les plus élevés", "Mention dans le plan de vigilance si vous y êtes soumis"],
            "en": ["Human rights risk map by country and activity", "Measures for the highest risks", "Reference in the due diligence plan if you are subject to one"],
            "ja": ["国別・事業別の人権リスクマップ", "リスクの高い項目への対策計画", "該当する場合はデューデリジェンス計画への記載"],
        },
        "kpi": {"fr": "Part des risques élevés couverts par une mesure", "en": "Share of high risks covered by a measure", "ja": "対策が講じられている高リスク項目の割合"},
    },
    "ETH1": {
        "evidence": {
            "fr": ["Code de conduite traduit dans chaque langue", "Module de formation et taux de complétion", "Accusés de lecture signés par les salariés"],
            "en": ["Code of conduct translated into each language", "Training module and completion rate", "Read acknowledgements signed by employees"],
            "ja": ["各国語に翻訳された行動規範", "研修教材と受講完了率", "従業員が署名した受領確認書"],
        },
        "kpi": {"fr": "Taux de salariés formés au code de conduite", "en": "Share of employees trained on the code of conduct", "ja": "行動規範の研修を受けた従業員の割合"},
    },
    "ETH2": {
        "evidence": {
            "fr": ["Cartographie des risques de corruption", "Politique cadeaux, invitations et conflits d'intérêts", "Registre des vérifications sur les intermédiaires"],
            "en": ["Corruption risk map", "Gifts, hospitality and conflicts of interest policy", "Log of integrity checks on intermediaries"],
            "ja": ["腐敗リスクマップ", "贈答品・接待・利益相反に関する方針", "仲介者に対する確認の記録"],
        },
        "kpi": {"fr": "Part des salariés exposés formés à l'anticorruption", "en": "Share of exposed employees trained on anti-corruption", "ja": "対象となる従業員のうち腐敗防止研修の受講者の割合"},
    },
    "ETH3": {
        "evidence": {
            "fr": ["Procédure d'alerte publiée et accessible aux tiers", "Langues disponibles et canaux d'accès", "Registre anonymisé du traitement des alertes"],
            "en": ["Whistleblowing procedure published and open to third parties", "Available languages and access channels", "Anonymised log of case handling"],
            "ja": ["公開され、社外の関係者も利用できる通報手続き", "対応言語と利用経路", "匿名化した通報対応の記録"],
        },
        "kpi": {"fr": "Délai moyen de traitement des alertes", "en": "Average case handling time", "ja": "通報への平均対応期間"},
    },
    "ETH4": {
        "evidence": {
            "fr": ["Certificat ISO 27001 ou rapport SOC 2, avec son périmètre", "Politique de sécurité de l'information", "Clauses de sécurité dans les contrats prestataires"],
            "en": ["ISO 27001 certificate or SOC 2 report, with its scope", "Information security policy", "Security clauses in provider contracts"],
            "ja": ["適用範囲を明記したISO 27001認証書またはSOC 2報告書", "情報セキュリティ方針", "委託先契約のセキュリティ条項"],
        },
        "kpi": {"fr": "Part des prestataires critiques avec exigences de sécurité", "en": "Share of critical providers with security requirements", "ja": "セキュリティ要件を課している重要委託先の割合"},
    },
    "ETH5": {
        "evidence": {
            "fr": ["Registre des traitements à jour", "Clauses de transfert pour les données hors Union européenne", "Procédure de traitement des demandes des personnes"],
            "en": ["Up-to-date records of processing", "Transfer clauses for data outside the European Union", "Procedure for data subject requests"],
            "ja": ["最新の処理活動の記録", "EU域外へのデータ移転に関する条項", "本人からの請求に対応する手順"],
        },
        "kpi": {"fr": "Délai moyen de réponse aux demandes des personnes", "en": "Average response time to data subject requests", "ja": "本人からの請求への平均回答期間"},
    },
    "ACH1": {
        "evidence": {
            "fr": ["Politique d'achats responsables signée", "Code de conduite fournisseurs", "Liste des fournisseurs signataires"],
            "en": ["Signed sustainable procurement policy", "Supplier code of conduct", "List of suppliers who signed it"],
            "ja": ["署名済みの持続可能な調達方針", "サプライヤー行動規範", "署名したサプライヤーの一覧"],
        },
        "kpi": {"fr": "Part des achats couverts par le code fournisseurs signé", "en": "Share of spend covered by a signed supplier code", "ja": "署名済み行動規範でカバーされる調達額の割合"},
    },
    "ACH2": {
        "evidence": {
            "fr": ["Cartographie des risques fournisseurs (pays, catégorie, volume)", "Méthode de notation des risques", "Liste des fournisseurs prioritaires et actions prévues"],
            "en": ["Supplier risk map (country, category, spend)", "Risk scoring method", "List of priority suppliers and planned actions"],
            "ja": ["サプライヤーリスクマップ（国、カテゴリー、取引額）", "リスク評価の方法", "優先サプライヤーの一覧と予定している対応"],
        },
        "kpi": {"fr": "Part des achats couverts par la cartographie", "en": "Share of spend covered by the risk map", "ja": "リスクマップでカバーされる調達額の割合"},
    },
    "ACH3": {
        "evidence": {
            "fr": ["Résultats d'évaluation RSE des fournisseurs stratégiques", "Score minimum défini pour le référencement", "Rapports d'audit sur site si disponibles"],
            "en": ["CSR assessment results of strategic suppliers", "Minimum score defined for listing", "On-site audit reports if available"],
            "ja": ["戦略的サプライヤーのCSR評価結果", "取引登録に必要な最低スコアの基準", "現地監査報告書（ある場合）"],
        },
        "kpi": {"fr": "Part des fournisseurs stratégiques évalués", "en": "Share of strategic suppliers assessed", "ja": "評価を実施した戦略的サプライヤーの割合"},
    },
    "ACH4": {
        "evidence": {
            "fr": ["Liste des sous-traitants déclarés par les fournisseurs clés", "Données de traçabilité sur la catégorie pilote", "Déclarations d'origine des matières (par exemple minerais)"],
            "en": ["Subcontractor list declared by key suppliers", "Traceability data on the pilot category", "Origin declarations for materials (for example minerals)"],
            "ja": ["主要サプライヤーが申告した下請け先一覧", "試験カテゴリーのトレーサビリティデータ", "原材料の原産地申告（鉱物など）"],
        },
        "kpi": {"fr": "Part des achats à risque tracés jusqu'au rang 2", "en": "Share of high-risk spend traced to tier 2", "ja": "二次サプライヤーまで追跡できている高リスク調達額の割合"},
    },
    "ACH5": {
        "evidence": {
            "fr": ["Plans d'actions correctives signés et suivis", "Programme climat fournisseurs et objectifs fixés", "Comptes rendus des revues avec les fournisseurs"],
            "en": ["Signed and tracked corrective action plans", "Supplier climate programme and agreed targets", "Minutes of supplier review meetings"],
            "ja": ["署名・進捗管理されている是正措置計画", "サプライヤー向け気候プログラムと合意した目標", "サプライヤーとのレビュー会議の議事録"],
        },
        "kpi": {"fr": "Part des actions correctives clôturées dans les délais", "en": "Share of corrective actions closed on time", "ja": "期限内に完了した是正措置の割合"},
    },
}
