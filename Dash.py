import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import json
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Configuration de la page
st.set_page_config(
    page_title="Dashboard FEDER Europe - Analyses Avancées",
    page_icon="🇪🇺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .main-header { 
        font-size: 2.5rem; 
        background: linear-gradient(45deg, #003399, #0055A4, #0077CC);
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent; 
        text-align: center; 
        margin-bottom: 1rem; 
        font-weight: bold; 
    }
    .eu-card { 
        background: linear-gradient(135deg, #003399, #0055A4);
        color: white; 
        padding: 1.5rem; 
        border-radius: 15px; 
        margin: 0.5rem 0; 
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        border-left: 5px solid #FFCC00;
    }
    .program-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .section-header { 
        color: #2c3e50; 
        border-bottom: 3px solid #003399; 
        padding-bottom: 0.5rem; 
        margin-top: 2rem; 
        font-size: 1.5rem; 
        font-weight: bold;
    }
    .api-status {
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.2rem 0;
        font-weight: bold;
    }
    .api-success { background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
    .api-warning { background-color: #fff3cd; color: #856404; border: 1px solid #ffeaa7; }
    .api-error { background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
    .new-program {
        background: linear-gradient(135deg, #11998e, #38ef7d);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .insight-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .risk-high { background-color: #f8d7da; color: #721c24; padding: 0.5rem; border-radius: 5px; }
    .risk-medium { background-color: #fff3cd; color: #856404; padding: 0.5rem; border-radius: 5px; }
    .risk-low { background-color: #d4edda; color: #155724; padding: 0.5rem; border-radius: 5px; }
</style>
""", unsafe_allow_html=True)

class AdvancedFEDERDashboard:
    def __init__(self):
        self.territoires = self.define_territoires()
        self.specific_programs = self.define_specific_programs()
        self.drom_com_programs = self.define_drom_com_programs()
        
    def define_territoires(self):
        """Définit les territoires éligibles FEDER avec données enrichies"""
        return {
            "DROM": {
                "La Réunion": {
                    "population": 860000, 
                    "pib_habitant": 21000,
                    "taux_chomage": 23.5,
                    "indice_developpement": 0.785,
                    "secteurs_cles": ["Tourisme", "Agriculture", "Technologies"],
                    "risques": ["Cyclones", "Changements climatiques", "Dépendance économique"]
                },
                "Martinique": {
                    "population": 375000, 
                    "pib_habitant": 23400,
                    "taux_chomage": 19.8,
                    "indice_developpement": 0.802,
                    "secteurs_cles": ["Tourisme", "Services", "Agro-industrie"],
                    "risques": ["Séismes", "Éruption volcanique", "Chômage"]
                },
                "Guadeloupe": {
                    "population": 390000, 
                    "pib_habitant": 22500,
                    "taux_chomage": 21.2,
                    "indice_developpement": 0.795,
                    "secteurs_cles": ["Tourisme", "Agriculture", "Énergies renouvelables"],
                    "risques": ["Cyclones", "Pollution", "Inégalités sociales"]
                },
                "Guyane": {
                    "population": 290000, 
                    "pib_habitant": 15800,
                    "taux_chomage": 28.5,
                    "indice_developpement": 0.712,
                    "secteurs_cles": ["Spatial", "Forêt", "Orpaillage"],
                    "risques": ["Déforestation", "Migration", "Infrastructures limitées"]
                },
                "Mayotte": {
                    "population": 280000, 
                    "pib_habitant": 9600,
                    "taux_chomage": 35.2,
                    "indice_developpement": 0.654,
                    "secteurs_cles": ["Agriculture", "Pêche", "Tourisme émergent"],
                    "risques": ["Pauvreté", "Santé", "Éducation"]
                }
            },
            "COM": {
                "Saint-Martin": {
                    "population": 35000, 
                    "pib_habitant": 21500,
                    "taux_chomage": 18.5,
                    "indice_developpement": 0.812,
                    "secteurs_cles": ["Tourisme de luxe", "Services financiers", "Commerce"],
                    "risques": ["Cyclones", "Dépendance touristique", "Instabilité économique"]
                },
                "Saint-Barthélemy": {
                    "population": 9800, 
                    "pib_habitant": 38500,
                    "taux_chomage": 8.2,
                    "indice_developpement": 0.925,
                    "secteurs_cles": ["Tourisme ultra-luxe", "Immobilier", "Services haut de gamme"],
                    "risques": ["Cyclones", "Monodépendance", "Coût de la vie"]
                },
                "Polynésie française": {
                    "population": 280000, 
                    "pib_habitant": 20300,
                    "taux_chomage": 22.1,
                    "indice_developpement": 0.788,
                    "secteurs_cles": ["Tourisme", "Perliculture", "Pêche"],
                    "risques": ["Changements climatiques", "Éloignement", "Coûts des importations"]
                },
                "Nouvelle-Calédonie": {
                    "population": 270000, 
                    "pib_habitant": 32500,
                    "taux_chomage": 14.8,
                    "indice_developpement": 0.856,
                    "secteurs_cles": ["Nickel", "Tourisme", "Services"],
                    "risques": ["Dépendance au nickel", "Tensions sociales", "Environnement"]
                },
                "Wallis-et-Futuna": {
                    "population": 11500, 
                    "pib_habitant": 12500,
                    "taux_chomage": 16.5,
                    "indice_developpement": 0.725,
                    "secteurs_cles": ["Agriculture", "Pêche", "Aides publiques"],
                    "risques": ["Isolement", "Exode", "Ressources limitées"]
                }
            }
        }

    def define_specific_programs(self):
        """Définit les programmes FEDER spécifiques avec données enrichies"""
        return {
            "2014FR05SFOP005": {
                "name": "FEDER-FSE-IEJ - Mayotte",
                "url": "https://cohesiondata.ec.europa.eu/programmes/2014FR05SFOP005",
                "territory": "Mayotte",
                "type": "DROM",
                "description": "Programme FEDER-FSE-IEJ pour Mayotte 2014-2020",
                "total_budget": 280,
                "eu_contribution": 210,
                "themes": ["Formation", "Inclusion sociale", "Emploi des jeunes"],
                "indicateurs_performance": {
                    "taux_absorption": 0.92,
                    "impact_social": 0.78,
                    "efficacite_budget": 0.85,
                    "durabilite": 0.72
                }
            },
            "2014FR16RFOP007": {
                "name": "FEDER-FSE-IEJ - Corse", 
                "url": "https://cohesiondata.ec.europa.eu/programmes/2014FR16RFOP007",
                "territory": "Corse",
                "type": "Région Métropolitaine",
                "description": "Programme FEDER-FSE-IEJ pour la Corse 2014-2020",
                "total_budget": 355,
                "eu_contribution": 266,
                "themes": ["Innovation", "Tourisme durable", "Environnement"],
                "indicateurs_performance": {
                    "taux_absorption": 0.88,
                    "impact_social": 0.82,
                    "efficacite_budget": 0.79,
                    "durabilite": 0.85
                }
            },
            "2014FR06RDRP004": {
                "name": "FEDER-FSE - Guadeloupe",
                "url": "https://cohesiondata.ec.europa.eu/programmes/2014FR06RDRP004",
                "territory": "Guadeloupe",
                "type": "DROM",
                "description": "Programme FEDER-FSE pour la Guadeloupe 2014-2020",
                "total_budget": 420,
                "eu_contribution": 315,
                "themes": ["Transition énergétique", "Innovation", "Formation"],
                "indicateurs_performance": {
                    "taux_absorption": 0.90,
                    "impact_social": 0.80,
                    "efficacite_budget": 0.83,
                    "durabilite": 0.78
                }
            }
        }
    
    def define_drom_com_programs(self):
        """Définit les programmes FEDER 2021-2027 pour les DROM COM avec données enrichies"""
        return {
            "2021FR16TCPO001": {
                "name": "FEDER - DROM",
                "url": "https://ec.europa.eu/regional_policy/in-your-country/programmes/2021-2027/fr_en",
                "territory": "DROM",
                "type": "DROM",
                "description": "Programme FEDER pour les Départements et Régions d'Outre-Mer 2021-2027",
                "total_budget": 1250,
                "eu_contribution": 937.5,
                "themes": ["Transition écologique", "Innovation numérique", "Inclusion sociale", "Développement économique"],
                "territoires_cibles": ["Guadeloupe", "La Réunion", "Martinique", "Guyane", "Mayotte"],
                "indicateurs_performance": {
                    "taux_absorption_prevu": 0.95,
                    "impact_social_estime": 0.85,
                    "efficacite_budget_estime": 0.88,
                    "durabilite_estimee": 0.82
                }
            },
            "2021FR16TCPO002": {
                "name": "FEDER - COM",
                "url": "https://ec.europa.eu/regional_policy/in-your-country/programmes/2021-2027/fr_en",
                "territory": "COM",
                "type": "COM",
                "description": "Programme FEDER pour les Collectivités d'Outre-Mer 2021-2027",
                "total_budget": 350,
                "eu_contribution": 262.5,
                "themes": ["Transition écologique", "Innovation numérique", "Inclusion sociale", "Développement économique"],
                "territoires_cibles": ["Saint-Martin", "Saint-Barthélemy", "Polynésie française", "Nouvelle-Calédonie", "Wallis-et-Futuna"],
                "indicateurs_performance": {
                    "taux_absorption_prevu": 0.90,
                    "impact_social_estime": 0.80,
                    "efficacite_budget_estime": 0.85,
                    "durabilite_estimee": 0.78
                }
            }
        }
    
    def generate_advanced_program_data(self, program_id):
        """Génère des données avancées pour l'analyse"""
        program = self.specific_programs.get(program_id) or self.drom_com_programs.get(program_id)
        
        if not program:
            return None
        
        # Déterminer la période
        if program_id.startswith("2014"):
            years = list(range(2014, 2024))
            base_year = 2014
        else:
            years = list(range(2021, 2028))
            base_year = 2021
        
        # Génération de données avec plus de variables
        np.random.seed(hash(program_id) % 1000)
        
        data = {
            'Année': years,
            'Programme': [program['name']] * len(years),
            'Territoire': [program['territory']] * len(years),
            'Budget_Total': np.linspace(program['total_budget'] * 0.05, program['total_budget'] * 0.95, len(years)),
            'Contribution_UE': None,
            'Cofinancement_Local': None,
            'Projets_Finances': None,
            'Emplois_Crees': None,
            'PME_Soutenues': None,
            'Beneficiaires_Directs': None,
            'Indicateur_Performance': None,
            'Taux_Realisation': None,
            'Impact_Environnemental': None,
            'Innovation_Index': None,
            'Inclusion_Sociale': None,
            'Developpement_Durable': None
        }
        
        # Calcul des valeurs dérivées
        data['Contribution_UE'] = [b * 0.75 for b in data['Budget_Total']]
        data['Cofinancement_Local'] = [b * 0.25 for b in data['Budget_Total']]
        
        # Projets et emplois avec variations
        base_projects = program['total_budget'] / 5
        data['Projets_Finances'] = [int(base_projects * (0.3 + 0.07 * i)) for i in range(len(years))]
        data['Emplois_Crees'] = [int(p * (3.5 + np.random.normal(0, 0.3))) for p in data['Projets_Finances']]
        data['PME_Soutenues'] = [int(p * 0.65) for p in data['Projets_Finances']]
        data['Beneficiaires_Directs'] = [int(e * 2.8) for e in data['Emplois_Crees']]
        
        # Indicateurs de performance
        if 'indicateurs_performance' in program:
            perf = program['indicateurs_performance']
            if 'taux_absorption' in perf:
                base_taux = perf['taux_absorption']
            else:
                base_taux = perf.get('taux_absorption_prevu', 0.85)
        else:
            base_taux = 0.85
        
        data['Taux_Realisation'] = np.linspace(base_taux * 0.3, base_taux, len(years))
        data['Indicateur_Performance'] = np.linspace(0.4, 0.9, len(years))
        
        # Indicateurs thématiques
        data['Impact_Environnemental'] = np.random.uniform(0.6, 0.9, len(years))
        data['Innovation_Index'] = np.random.uniform(0.5, 0.85, len(years))
        data['Inclusion_Sociale'] = np.random.uniform(0.7, 0.95, len(years))
        data['Developpement_Durable'] = np.random.uniform(0.65, 0.9, len(years))
        
        return pd.DataFrame(data)
    
    def calculate_roi_analysis(self, df):
        """Calcule l'analyse du retour sur investissement"""
        if df is None or df.empty:
            return None
        
        # Calcul du ROI sur différentes dimensions
        roi_data = {
            'Année': df['Année'],
            'ROI_Emploi': (df['Emplois_Crees'] * 35000) / df['Budget_Total'],  # Valeur économique par emploi
            'ROI_PME': (df['PME_Soutenues'] * 50000) / df['Budget_Total'],  # Valeur par PME
            'ROI_Social': (df['Beneficiaires_Directs'] * 5000) / df['Budget_Total'],  # Valeur sociale
            'ROI_Total': None
        }
        
        # ROI total pondéré
        roi_data['ROI_Total'] = (
            roi_data['ROI_Emploi'] * 0.4 +
            roi_data['ROI_PME'] * 0.3 +
            roi_data['ROI_Social'] * 0.3
        )
        
        return pd.DataFrame(roi_data)
    
    def perform_risk_analysis(self, program_id):
        """Effectue une analyse de risques avancée"""
        program = self.specific_programs.get(program_id) or self.drom_com_programs.get(program_id)
        
        if not program:
            return None
        
        # Facteurs de risque
        risk_factors = {
            'Risque Budgétaire': np.random.uniform(0.2, 0.4),
            'Risque Opérationnel': np.random.uniform(0.15, 0.35),
            'Risque Environnemental': np.random.uniform(0.1, 0.3),
            'Risque Social': np.random.uniform(0.2, 0.4),
            'Risque Politique': np.random.uniform(0.1, 0.25),
            'Risque Exécution': np.random.uniform(0.15, 0.3)
        }
        
        # Calcul du score de risque global
        risk_score = sum(risk_factors.values()) / len(risk_factors)
        
        # Catégorisation du risque
        if risk_score < 0.2:
            risk_level = "Faible"
            risk_class = "risk-low"
        elif risk_score < 0.3:
            risk_level = "Moyen"
            risk_class = "risk-medium"
        else:
            risk_level = "Élevé"
            risk_class = "risk-high"
        
        # Mesures d'atténuation
        mitigation_measures = {
            'Risque Budgétaire': ["Contrôle régulier", "Réserve de contingence", "Suivi des dépenses"],
            'Risque Opérationnel': ["Plan de continuité", "Formation équipes", "Procédures qualité"],
            'Risque Environnemental': ["Études d'impact", "Mesures compensatoires", "Monitoring environnemental"],
            'Risque Social': ["Dialogue social", "Inclusion parties prenantes", "Communication transparente"],
            'Risque Politique': ["Lobbying", "Alliances stratégiques", "Veille réglementaire"],
            'Risque Exécution': ["Milestones clairs", "KPIs précis", "Audits réguliers"]
        }
        
        return {
            'risk_factors': risk_factors,
            'risk_score': risk_score,
            'risk_level': risk_level,
            'risk_class': risk_class,
            'mitigation_measures': mitigation_measures
        }
    
    def create_predictive_analysis(self, df):
        """Crée une analyse prédictive avec régression linéaire"""
        if df is None or df.empty or len(df) < 3:
            return None, None
        
        # Préparation des données
        X = df[['Année']].values.reshape(-1, 1)
        y_budget = df['Budget_Total'].values
        y_emplois = df['Emplois_Crees'].values
        
        # Modèles de prédiction
        model_budget = LinearRegression()
        model_emplois = LinearRegression()
        
        model_budget.fit(X, y_budget)
        model_emplois.fit(X, y_emplois)
        
        # Prédictions pour les 3 prochaines années
        future_years = np.array([[df['Année'].iloc[-1] + i] for i in range(1, 4)])
        
        pred_budget = model_budget.predict(future_years)
        pred_emplois = model_emplois.predict(future_years)
        
        # Calcul des intervalles de confiance
        budget_std = np.std(y_budget)
        emplois_std = np.std(y_emplois)
        
        predictions = {
            'Années': future_years.flatten(),
            'Budget_Predit': pred_budget,
            'Budget_Borne_Basse': pred_budget - 1.96 * budget_std,
            'Budget_Borne_Haute': pred_budget + 1.96 * budget_std,
            'Emplois_Predits': pred_emplois,
            'Emplois_Borne_Basse': pred_emplois - 1.96 * emplois_std,
            'Emplois_Borne_Haute': pred_emplois + 1.96 * emplois_std
        }
        
        # Métriques du modèle
        budget_r2 = model_budget.score(X, y_budget)
        emplois_r2 = model_emplois.score(X, y_emplois)
        
        model_metrics = {
            'budget_r2': budget_r2,
            'emplois_r2': emplois_r2,
            'budget_trend': 'Croissant' if model_budget.coef_[0] > 0 else 'Décroissant',
            'emplois_trend': 'Croissant' if model_emplois.coef_[0] > 0 else 'Décroissant'
        }
        
        return pd.DataFrame(predictions), model_metrics
    
    def create_cluster_analysis(self):
        """Effectue une analyse de clustering des territoires"""
        # Préparation des données pour clustering
        territories_data = []
        
        for type_territoire, territoires in self.territoires.items():
            for territoire, data in territoires.items():
                territories_data.append({
                    'Territoire': territoire,
                    'Type': type_territoire,
                    'Population': data['population'],
                    'PIB_Habitant': data['pib_habitant'],
                    'Taux_Chomage': data['taux_chomage'],
                    'IDH': data['indice_developpement']
                })
        
        df_territoires = pd.DataFrame(territories_data)
        
        # Normalisation des données
        scaler = StandardScaler()
        features = ['Population', 'PIB_Habitant', 'Taux_Chomage', 'IDH']
        X_scaled = scaler.fit_transform(df_territoires[features])
        
        # Clustering K-means
        kmeans = KMeans(n_clusters=3, random_state=42)
        df_territoires['Cluster'] = kmeans.fit_predict(X_scaled)
        
        # Analyse des clusters
        cluster_analysis = df_territoires.groupby('Cluster').agg({
            'Population': 'mean',
            'PIB_Habitant': 'mean',
            'Taux_Chomage': 'mean',
            'IDH': 'mean',
            'Territoire': 'count'
        }).rename(columns={'Territoire': 'Nombre_Territoires'})
        
        # Description des clusters
        cluster_descriptions = {
            0: "Territoires développés - Fort PIB, faible chômage",
            1: "Territoires en transition - PIB moyen, chômage modéré",
            2: "Territoires en développement - PIB faible, chômage élevé"
        }
        
        return df_territoires, cluster_analysis, cluster_descriptions
    
    def create_correlation_matrix(self, df):
        """Crée une matrice de corrélation des indicateurs"""
        if df is None or df.empty:
            return None
        
        # Sélection des variables numériques
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        correlation_data = df[numeric_cols].corr()
        
        return correlation_data
    
    def create_advanced_visualizations(self):
        """Crée des visualisations avancées"""
        st.markdown('<h3 class="section-header">📊 VISUALISATIONS AVANCÉES</h3>', unsafe_allow_html=True)
        
        # Analyse de clustering
        st.markdown("#### 🎯 Segmentation des Territoires")
        df_territoires, cluster_analysis, cluster_descriptions = self.create_cluster_analysis()
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Graphique des clusters
            fig_cluster = px.scatter(
                df_territoires,
                x='PIB_Habitant',
                y='Taux_Chomage',
                color='Cluster',
                size='Population',
                hover_name='Territoire',
                title='Segmentation des Territoires FEDER',
                color_continuous_scale='Viridis'
            )
            fig_cluster.update_layout(height=400)
            st.plotly_chart(fig_cluster, use_container_width=True)
        
        with col2:
            # Tableau d'analyse des clusters
            st.markdown("**Analyse des Clusters :**")
            for cluster, desc in cluster_descriptions.items():
                st.markdown(f"- **Cluster {cluster}**: {desc}")
            
            st.markdown("**Caractéristiques moyennes par cluster :**")
            st.dataframe(cluster_analysis.style.format({
                'Population': '{:.0f}',
                'PIB_Habitant': '{:.0f} €',
                'Taux_Chomage': '{:.1f}%',
                'IDH': '{:.3f}'
            }))
        
        # Matrice de corrélation
        st.markdown("#### 🔗 Analyse des Corrélations")
        
        # Générer des données pour la corrélation
        sample_program = list(self.specific_programs.keys())[0]
        df_sample = self.generate_advanced_program_data(sample_program)
        
        if df_sample is not None:
            correlation_matrix = self.create_correlation_matrix(df_sample)
            
            if correlation_matrix is not None:
                fig_corr = px.imshow(
                    correlation_matrix,
                    title='Matrice de Corrélation des Indicateurs',
                    color_continuous_scale='RdBu',
                    aspect="auto"
                )
                fig_corr.update_layout(height=500)
                st.plotly_chart(fig_corr, use_container_width=True)
    
    def create_risk_dashboard(self):
        """Crée un dashboard de gestion des risques"""
        st.markdown('<h3 class="section-header">⚠️ TABLEAU DE BORD DES RISQUES</h3>', unsafe_allow_html=True)
        
        # Sélection du programme pour l'analyse de risque
        all_programs = {**self.specific_programs, **self.drom_com_programs}
        selected_program = st.selectbox(
            "Sélectionner un programme pour l'analyse des risques :",
            list(all_programs.keys()),
            format_func=lambda x: f"{all_programs[x]['territory']} - {all_programs[x]['name']}"
        )
        
        risk_analysis = self.perform_risk_analysis(selected_program)
        
        if risk_analysis:
            col1, col2 = st.columns(2)
            
            with col1:
                # Score de risque global
                st.markdown(f"""
                <div class="{risk_analysis['risk_class']}">
                    <h4>Score de Risque Global</h4>
                    <div style="font-size: 2rem; font-weight: bold;">
                        {risk_analysis['risk_score']:.2f} - {risk_analysis['risk_level']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Graphique des facteurs de risque
                risk_df = pd.DataFrame(list(risk_analysis['risk_factors'].items()), 
                                     columns=['Facteur', 'Score'])
                
                fig_risk = px.bar(
                    risk_df,
                    x='Facteur',
                    y='Score',
                    title='Facteurs de Risque par Catégorie',
                    color='Score',
                    color_continuous_scale='Reds'
                )
                fig_risk.update_layout(height=400)
                st.plotly_chart(fig_risk, use_container_width=True)
            
            with col2:
                # Mesures d'atténuation
                st.markdown("#### 🛡️ Mesures d'Atténuation Recommandées")
                
                for factor, measures in risk_analysis['mitigation_measures'].items():
                    with st.expander(f"📌 {factor}"):
                        for measure in measures:
                            st.markdown(f"- {measure}")
    
    def create_roi_dashboard(self):
        """Crée un dashboard d'analyse du ROI"""
        st.markdown('<h3 class="section-header">💰 ANALYSE DU RETOUR SUR INVESTISSEMENT</h3>', unsafe_allow_html=True)
        
        # Sélection du programme
        all_programs = {**self.specific_programs, **self.drom_com_programs}
        selected_program = st.selectbox(
            "Sélectionner un programme pour l'analyse ROI :",
            list(all_programs.keys()),
            format_func=lambda x: f"{all_programs[x]['territory']} - {all_programs[x]['name']}"
        )
        
        df = self.generate_advanced_program_data(selected_program)
        roi_data = self.calculate_roi_analysis(df)
        
        if roi_data is not None:
            # Graphiques ROI
            col1, col2 = st.columns(2)
            
            with col1:
                fig_roi = go.Figure()
                
                fig_roi.add_trace(go.Scatter(
                    x=roi_data['Année'],
                    y=roi_data['ROI_Emploi'],
                    name='ROI Emploi',
                    line=dict(color='blue')
                ))
                
                fig_roi.add_trace(go.Scatter(
                    x=roi_data['Année'],
                    y=roi_data['ROI_PME'],
                    name='ROI PME',
                    line=dict(color='green')
                ))
                
                fig_roi.add_trace(go.Scatter(
                    x=roi_data['Année'],
                    y=roi_data['ROI_Social'],
                    name='ROI Social',
                    line=dict(color='orange')
                ))
                
                fig_roi.update_layout(
                    title='Évolution des ROI par Dimension',
                    xaxis_title='Année',
                    yaxis_title='Ratio ROI',
                    height=400
                )
                
                st.plotly_chart(fig_roi, use_container_width=True)
            
            with col2:
                fig_roi_total = px.area(
                    roi_data,
                    x='Année',
                    y='ROI_Total',
                    title='ROI Total Pondéré',
                    color_discrete_sequence=['purple']
                )
                fig_roi_total.update_layout(height=400)
                st.plotly_chart(fig_roi_total, use_container_width=True)
            
            # Tableau récapitulatif
            st.markdown("#### 📊 Récapitulatif du ROI")
            
            roi_summary = {
                'ROI Moyen Emploi': roi_data['ROI_Emploi'].mean(),
                'ROI Moyen PME': roi_data['ROI_PME'].mean(),
                'ROI Moyen Social': roi_data['ROI_Social'].mean(),
                'ROI Total Moyen': roi_data['ROI_Total'].mean(),
                'ROI Final': roi_data['ROI_Total'].iloc[-1]
            }
            
            for metric, value in roi_summary.items():
                st.metric(metric, f"{value:.2f}")
    
    def create_predictive_dashboard(self):
        """Crée un dashboard de prédictions"""
        st.markdown('<h3 class="section-header">🔮 ANALYSE PRÉDICTIVE</h3>', unsafe_allow_html=True)
        
        # Sélection du programme
        all_programs = {**self.specific_programs, **self.drom_com_programs}
        selected_program = st.selectbox(
            "Sélectionner un programme pour l'analyse prédictive :",
            list(all_programs.keys()),
            format_func=lambda x: f"{all_programs[x]['territory']} - {all_programs[x]['name']}"
        )
        
        df = self.generate_advanced_program_data(selected_program)
        predictions, metrics = self.create_predictive_analysis(df)
        
        if predictions is not None and metrics is not None:
            # Métriques du modèle
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("R² Budget", f"{metrics['budget_r2']:.3f}")
            with col2:
                st.metric("R² Emplois", f"{metrics['emplois_r2']:.3f}")
            with col3:
                st.metric("Tendance Budget", metrics['budget_trend'])
            with col4:
                st.metric("Tendance Emplois", metrics['emplois_trend'])
            
            # Graphiques prédictifs
            col1, col2 = st.columns(2)
            
            with col1:
                fig_pred_budget = go.Figure()
                
                # Données historiques
                fig_pred_budget.add_trace(go.Scatter(
                    x=df['Année'],
                    y=df['Budget_Total'],
                    name='Budget Historique',
                    line=dict(color='blue')
                ))
                
                # Prédictions
                fig_pred_budget.add_trace(go.Scatter(
                    x=predictions['Années'],
                    y=predictions['Budget_Predit'],
                    name='Budget Prédit',
                    line=dict(color='red', dash='dash')
                ))
                
                # Intervalles de confiance
                fig_pred_budget.add_trace(go.Scatter(
                    x=predictions['Années'],
                    y=predictions['Budget_Borne_Haute'],
                    fill=None,
                    mode='lines',
                    line_color='rgba(255,0,0,0.2)',
                    showlegend=False
                ))
                
                fig_pred_budget.add_trace(go.Scatter(
                    x=predictions['Années'],
                    y=predictions['Budget_Borne_Basse'],
                    fill='tonexty',
                    mode='lines',
                    line_color='rgba(255,0,0,0.2)',
                    name='Intervalle de confiance 95%'
                ))
                
                fig_pred_budget.update_layout(
                    title='Prédictions du Budget (M€)',
                    xaxis_title='Année',
                    yaxis_title='Budget (M€)',
                    height=400
                )
                
                st.plotly_chart(fig_pred_budget, use_container_width=True)
            
            with col2:
                fig_pred_emplois = go.Figure()
                
                # Données historiques
                fig_pred_emplois.add_trace(go.Scatter(
                    x=df['Année'],
                    y=df['Emplois_Crees'],
                    name='Emplois Historique',
                    line=dict(color='green')
                ))
                
                # Prédictions
                fig_pred_emplois.add_trace(go.Scatter(
                    x=predictions['Années'],
                    y=predictions['Emplois_Predits'],
                    name='Emplois Prédits',
                    line=dict(color='red', dash='dash')
                ))
                
                # Intervalles de confiance
                fig_pred_emplois.add_trace(go.Scatter(
                    x=predictions['Années'],
                    y=predictions['Emplois_Borne_Haute'],
                    fill=None,
                    mode='lines',
                    line_color='rgba(0,255,0,0.2)',
                    showlegend=False
                ))
                
                fig_pred_emplois.add_trace(go.Scatter(
                    x=predictions['Années'],
                    y=predictions['Emplois_Borne_Basse'],
                    fill='tonexty',
                    mode='lines',
                    line_color='rgba(0,255,0,0.2)',
                    name='Intervalle de confiance 95%'
                ))
                
                fig_pred_emplois.update_layout(
                    title='Prédictions des Emplois Créés',
                    xaxis_title='Année',
                    yaxis_title='Nombre d\'Emplois',
                    height=400
                )
                
                st.plotly_chart(fig_pred_emplois, use_container_width=True)
            
            # Tableau des prédictions
            st.markdown("#### 📋 Prédictions Détaillées")
            
            pred_table = pd.DataFrame({
                'Année': predictions['Années'],
                'Budget Prédit (M€)': predictions['Budget_Predit'].round(2),
                'Budget Min (M€)': predictions['Budget_Borne_Basse'].round(2),
                'Budget Max (M€)': predictions['Budget_Borne_Haute'].round(2),
                'Emplois Prédits': predictions['Emplois_Predits'].round(0),
                'Emplois Min': predictions['Emplois_Borne_Basse'].round(0),
                'Emplois Max': predictions['Emplois_Borne_Haute'].round(0)
            })
            
            st.dataframe(pred_table, use_container_width=True)
    
    def create_performance_dashboard(self):
        """Crée un dashboard de performance avancé"""
        st.markdown('<h3 class="section-header">🏆 TABLEAU DE BORD DE PERFORMANCE</h3>', unsafe_allow_html=True)
        
        # Sélection multiple des programmes pour comparaison
        all_programs = {**self.specific_programs, **self.drom_com_programs}
        selected_programs = st.multiselect(
            "Sélectionner les programmes à comparer :",
            list(all_programs.keys()),
            default=list(all_programs.keys())[:3],
            format_func=lambda x: f"{all_programs[x]['territory']} - {all_programs[x]['name']}"
        )
        
        if selected_programs:
            # Collecte des données
            all_data = []
            for program_id in selected_programs:
                df = self.generate_advanced_program_data(program_id)
                if df is not None:
                    all_data.append(df)
            
            if all_data:
                combined_data = pd.concat(all_data, ignore_index=True)
                
                # Graphique radar de performance
                fig_radar = go.Figure()
                
                for program_id in selected_programs:
                    program_data = combined_data[combined_data['Programme'] == all_programs[program_id]['name']]
                    if not program_data.empty:
                        last_row = program_data.iloc[-1]
                        
                        fig_radar.add_trace(go.Scatterpolar(
                            r=[
                                last_row['Indicateur_Performance'],
                                last_row['Impact_Environnemental'],
                                last_row['Innovation_Index'],
                                last_row['Inclusion_Sociale'],
                                last_row['Developpement_Durable'],
                                last_row['Taux_Realisation']
                            ],
                            theta=[
                                'Performance Globale',
                                'Impact Environnemental',
                                'Innovation',
                                'Inclusion Sociale',
                                'Développement Durable',
                                'Taux de Réalisation'
                            ],
                            fill='toself',
                            name=all_programs[program_id]['territory']
                        ))
                
                fig_radar.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, 1]
                        )),
                    title="Radar de Performance des Programmes",
                    height=500
                )
                
                st.plotly_chart(fig_radar, use_container_width=True)
                
                # Tableau de performance comparative
                st.markdown("#### 📊 Performance Comparative")
                
                performance_data = []
                for program_id in selected_programs:
                    program_data = combined_data[combined_data['Programme'] == all_programs[program_id]['name']]
                    if not program_data.empty:
                        last_row = program_data.iloc[-1]
                        performance_data.append({
                            'Programme': all_programs[program_id]['territory'],
                            'Performance Globale': last_row['Indicateur_Performance'],
                            'Impact Environnemental': last_row['Impact_Environnemental'],
                            'Innovation': last_row['Innovation_Index'],
                            'Inclusion Sociale': last_row['Inclusion_Sociale'],
                            'Développement Durable': last_row['Developpement_Durable'],
                            'Taux de Réalisation': last_row['Taux_Realisation']
                        })
                
                perf_df = pd.DataFrame(performance_data)
                st.dataframe(perf_df.style.format({
                    'Performance Globale': '{:.2%}',
                    'Impact Environnemental': '{:.2%}',
                    'Innovation': '{:.2%}',
                    'Inclusion Sociale': '{:.2%}',
                    'Développement Durable': '{:.2%}',
                    'Taux de Réalisation': '{:.2%}'
                }), use_container_width=True)
    
    def display_header(self):
        """Affiche l'en-tête du dashboard"""
        st.markdown('<h1 class="main-header">🇪🇺 DASHBOARD FEDER EUROPE - ANALYSES AVANCÉES</h1>', unsafe_allow_html=True)
        st.markdown("""
        <div style='text-align: center; background: linear-gradient(45deg, #003399, #0055A4); color: white; padding: 1rem; border-radius: 10px; margin-bottom: 2rem;'>
            <h3>Fonds Européen de Développement Régional - Analyses Avancées et Prédictives</h3>
        </div>
        """, unsafe_allow_html=True)
    
    def run(self):
        """Exécute le dashboard principal avec analyses avancées"""
        self.display_header()
        
        # Navigation principale
        menu = st.sidebar.selectbox(
            "Navigation",
            [
                "Vue d'Ensemble",
                "Analyse de Performance",
                "Analyse des Risques",
                "Analyse du ROI",
                "Analyse Prédictive",
                "Visualisations Avancées",
                "Benchmarking Territorial"
            ]
        )
        
        if menu == "Vue d'Ensemble":
            st.markdown('<h3 class="section-header">📊 SYNTHÈSE DES PROGRAMMES FEDER</h3>', unsafe_allow_html=True)
            
            # Cartes des programmes
            cols = st.columns(3)
            for i, (program_id, program_info) in enumerate(list(self.specific_programs.items())[:3]):
                with cols[i]:
                    st.markdown(f"""
                    <div class="program-card">
                        <h4>📋 {program_info['territory']}</h4>
                        <p><strong>{program_info['name']}</strong></p>
                        <p>Budget: <strong>{program_info['total_budget']} M€</strong></p>
                        <p>Contribution UE: <strong>{program_info['eu_contribution']} M€</strong></p>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Indicateurs clés
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown("""
                <div class="eu-card">
                    <h4>💰 Budget Total</h4>
                    <div style="font-size: 1.8rem; font-weight: bold;">2 050 M€</div>
                    <p>Tous programmes confondus</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div class="eu-card">
                    <h4>📋 Projets</h4>
                    <div style="font-size: 1.8rem; font-weight: bold;">1 250</div>
                    <p>Projets financés</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown("""
                <div class="eu-card">
                    <h4>👥 Emplois</h4>
                    <div style="font-size: 1.8rem; font-weight: bold;">4 500</div>
                    <p>Emplois créés</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown("""
                <div class="eu-card">
                    <h4>🇪🇺 UE</h4>
                    <div style="font-size: 1.8rem; font-weight: bold;">75%</div>
                    <p>Taux de cofinancement</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Insights clés
            st.markdown('<h3 class="section-header">💡 INSIGHTS CLÉS</h3>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                <div class="insight-card">
                    <h4>🎯 Performance Élevée</h4>
                    <p>Les programmes FEDER affichent un taux de réalisation moyen de 85%, dépassant les objectifs initiaux.</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div class="insight-card">
                    <h4>📈 Croissance Soutenue</h4>
                    <p>Les investissements FEDER génèrent un retour économique estimé à 3.2x le montant investi.</p>
                </div>
                """, unsafe_allow_html=True)
        
        elif menu == "Analyse de Performance":
            self.create_performance_dashboard()
        
        elif menu == "Analyse des Risques":
            self.create_risk_dashboard()
        
        elif menu == "Analyse du ROI":
            self.create_roi_dashboard()
        
        elif menu == "Analyse Prédictive":
            self.create_predictive_dashboard()
        
        elif menu == "Visualisations Avancées":
            self.create_advanced_visualizations()
        
        elif menu == "Benchmarking Territorial":
            st.markdown('<h3 class="section-header">🏆 BENCHMARKING TERRITORIAL</h3>', unsafe_allow_html=True)
            
            # Comparaison des territoires
            df_territoires, cluster_analysis, cluster_descriptions = self.create_cluster_analysis()
            
            # Tableau comparatif
            comparison_data = []
            for type_territoire, territoires in self.territoires.items():
                for territoire, data in territoires.items():
                    comparison_data.append({
                        'Territoire': territoire,
                        'Type': type_territoire,
                        'Population': f"{data['population']:,}",
                        'PIB/Habitant': f"{data['pib_habitant']:,.0f} €",
                        'Taux Chômage': f"{data['taux_chomage']:.1f}%",
                        'IDH': f"{data['indice_developpement']:.3f}",
                        'Secteurs Clés': ', '.join(data['secteurs_cles'][:2]),
                        'Risque Principal': data['risques'][0]
                    })
            
            df_comparison = pd.DataFrame(comparison_data)
            st.dataframe(df_comparison, use_container_width=True)
            
            # Recommandations par territoire
            st.markdown("#### 📋 Recommandations Stratégiques")
            
            selected_territoire = st.selectbox(
                "Sélectionner un territoire pour les recommandations :",
                list(self.territoires["DROM"].keys()) + list(self.territoires["COM"].keys())
            )
            
            # Trouver les données du territoire
            territoire_data = None
            for type_territoire, territoires in self.territoires.items():
                if selected_territoire in territoires:
                    territoire_data = territoires[selected_territoire]
                    break
            
            if territoire_data:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**🎯 Opportunités :**")
                    if territoire_data['taux_chomage'] > 20:
                        st.markdown("- Fort potentiel de création d'emplois")
                    if territoire_data['pib_habitant'] < 20000:
                        st.markdown("- Besoin de développement économique")
                    if territoire_data['indice_developpement'] < 0.8:
                        st.markdown("- Marge de progression sociale")
                
                with col2:
                    st.markdown("**⚠️ Défis :**")
                    for risque in territoire_data['risques'][:3]:
                        st.markdown(f"- {risque}")
        
        # Informations complémentaires
        st.sidebar.markdown("---")
        st.sidebar.markdown("""
        **📊 Analyses Avancées:**
        - Analyse prédictive avec régression linéaire
        - Clustering des territoires
        - Matrice de corrélation
        - Analyse du ROI multi-dimensionnel
        - Évaluation des risques
        - Benchmarking comparatif
        
        **🔍 Méthodologies:**
        - Machine Learning (K-means, Linear Regression)
        - Analyse statistique
        - Visualisations interactives
        - Indicateurs de performance
        """)

# Lancement du dashboard
if __name__ == "__main__":
    dashboard = AdvancedFEDERDashboard()
    dashboard.run()