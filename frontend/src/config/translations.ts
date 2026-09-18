export type Language = 'en' | 'hi' | 'gu';

export interface TranslationEntry {
  en: string;
  hi: string;
  gu: string;
}

export type TranslationDictionary = Record<string, TranslationEntry>;

export const extraTranslations: TranslationDictionary = {
  // --- Admin Portal & Governance ---
  "enterprise_administration__governance": {
    en: "Enterprise Administration & Governance",
    hi: "एंटरप्राइज प्रशासन और शासन",
    gu: "એન્ટરપ્રાઇઝ વહીવટ અને શાસન"
  },
  "platform_control_center": {
    en: "Chaos2Commit 2026 Platform Control Center • Centralized RBAC, Multi-Tenant Hierarchy & AI Telemetry",
    hi: "Chaos2Commit 2026 प्लेटफॉर्म नियंत्रण केंद्र • केंद्रीकृत RBAC, बहु-किराएदार पदानुक्रम और AI टेलीमेट्री",
    gu: "Chaos2Commit 2026 પ્લેટફોર્મ નિયંત્રણ કેન્દ્ર • કેન્દ્રીયકૃત RBAC, બહુ-ટેનન્ટ પદાનુક્રમ અને AI ટેલિમેટ્રી"
  },
  "total_users": {
    en: "Total Users",
    hi: "कुल उपयोगकर्ता",
    gu: "કુલ વપરાશકર્તાઓ"
  },
  "all_7_roles_active": {
    en: "All 7 Roles Active",
    hi: "सभी 7 भूमिकाएं सक्रिय",
    gu: "તમામ 7 ભૂમિકાઓ સક્રિય"
  },
  "organizations": {
    en: "Organizations",
    hi: "संगठन",
    gu: "સંસ્થાઓ"
  },
  "multi_tenant_scoped": {
    en: "Multi-Tenant Scoped",
    hi: "मल्टी-टेनेंट स्कोप्ड",
    gu: "મલ્ટિ-ટેનન્ટ સ્કોપ્ડ"
  },
  "initiatives": {
    en: "Initiatives",
    hi: "पहल / परियोजनाएं",
    gu: "પહેલ / પ્રોજેક્ટ્સ"
  },
  "13_pipeline_stages": {
    en: "13 Pipeline Stages",
    hi: "13 पाइपलाइन चरण",
    gu: "13 પાઇપલાઇન તબક્કા"
  },
  "ai_invocations": {
    en: "AI Invocations",
    hi: "एआई कॉल / उपयोग",
    gu: "એઆઈ કૉલ્સ / વપરાશ"
  },
  "mtd_spend": {
    en: "MTD Spend",
    hi: "इस महीने का खर्च",
    gu: "આ મહિનાનો ખર્ચ"
  },
  "security__rbac_enforcement_status": {
    en: "Security & RBAC Enforcement Status",
    hi: "सुरक्षा और आरबीएसी प्रवर्तन स्थिति",
    gu: "સુરક્ષા અને RBAC અમલીકરણ સ્થિતિ"
  },
  "tenant_isolation_policy": {
    en: "Tenant Isolation Policy",
    hi: "किराएदार अलगाव नीति",
    gu: "ટેનન્ટ અલગતા નીતિ"
  },
  "data_encryption_standard": {
    en: "Data Encryption Standard",
    hi: "डेटा एन्क्रिप्शन मानक",
    gu: "ડેટા એન્ક્રિપ્શન માનક"
  },
  "vector_search_engine": {
    en: "Vector Search Engine",
    hi: "वेक्टर खोज इंजन",
    gu: "વેક્ટર સર્ચ એન્જિન"
  },
  "immutable_audit_logging": {
    en: "Immutable Audit Logging",
    hi: "अपरिवर्तनीय ऑडिट लॉगिंग",
    gu: "અપરિવર્તનીય ઓડિટ લોગીંગ"
  },
  "quick_administration_workflows": {
    en: "Quick Administration Workflows",
    hi: "त्वरित प्रशासनिक कार्यप्रवाह",
    gu: "ઝડપી વહીવટી વર્કફ્લો"
  },
  "manage_users": {
    en: "Manage Users",
    hi: "उपयोगकर्ता प्रबंधित करें",
    gu: "વપરાશકર્તાઓ સંચાલિત કરો"
  },
  "assign_roles__status": {
    en: "Assign roles & status",
    hi: "भूमिकाएं और स्थिति असाइन करें",
    gu: "ભૂમિકાઓ અને સ્થિતિ સોંપો"
  },
  "organization": {
    en: "Organization",
    hi: "संगठन प्रोफाइल",
    gu: "સંસ્થા પ્રોફાઇલ"
  },
  "profile__compliance": {
    en: "Profile & compliance",
    hi: "प्रोफ़ाइल और अनुपालन",
    gu: "પ્રોફાઇલ અને અનુપાલન"
  },
  "ai_token_telemetry": {
    en: "AI Token Telemetry",
    hi: "एआई टोकन टेलीमेट्री",
    gu: "એઆઈ ટોકન ટેલિમેટ્રી"
  },
  "monitor_model_spend": {
    en: "Monitor model spend",
    hi: "मॉडल खर्च की निगरानी करें",
    gu: "મોડેલ ખર્ચની દેખરેખ રાખો"
  },
  "audit_trail": {
    en: "Audit Trail",
    hi: "ऑडिट ट्रेल",
    gu: "ઓડિટ ટ્રેઇલ"
  },
  "review_security_logs": {
    en: "Review security logs",
    hi: "सुरक्षा लॉग की समीक्षा करें",
    gu: "સુરક્ષા લોગની સમીક્ષા કરો"
  },
  "recent_platform_governance_events": {
    en: "Recent Platform Governance Events",
    hi: "हालिया प्लेटफॉर्म गवर्नेंस ईवेंट्स",
    gu: "તાજેતરના પ્લેટફોર્મ ગવર્નન્સ ઇવેન્ટ્સ"
  },
  "view_full_audit_log": {
    en: "View Full Audit Log",
    hi: "पूरा ऑडिट लॉग देखें",
    gu: "સંપૂર્ણ ઓડિટ લોગ જુઓ"
  },
  "platform_status_healthy": {
    en: "Platform Status: Healthy (99.98%)",
    hi: "प्लेटफॉर्म स्थिति: स्वस्थ (99.98%)",
    gu: "પ્લેટફોર્મ સ્થિતિ: હેલ્ધી (99.98%)"
  },
  "sync": {
    en: "Sync",
    hi: "सिंक करें",
    gu: "સિંક કરો"
  },

  // --- Dashboard & Role Perspectives ---
  "transformation_portfolio": {
    en: "Transformation Portfolio",
    hi: "रूपांतरण पोर्टफोलियो",
    gu: "રૂપાંતરણ પોર્ટફોલિયો"
  },
  "view_all_projects": {
    en: "View All Projects",
    hi: "सभी परियोजनाएं देखें",
    gu: "બધા પ્રોજેક્ટ્સ જુઓ"
  },
  "avg_transformation_score": {
    en: "Avg Transformation Score",
    hi: "औसत रूपांतरण स्कोर",
    gu: "સરેરાશ ટ્રાન્સફોર્મેશન સ્કોર"
  },
  "ai_readiness": {
    en: "AI Readiness",
    hi: "एआई तत्परता",
    gu: "એઆઈ સજ્જતા"
  },
  "automation_potential": {
    en: "Automation Potential",
    hi: "स्वचालन क्षमता",
    gu: "ઓટોમેશન ક્ષમતા"
  },
  "delivery_readiness": {
    en: "Delivery Readiness",
    hi: "वितरण तत्परता",
    gu: "ડિલિવરી સજ્જતા"
  },
  "projects_at_risk": {
    en: "Projects At Risk",
    hi: "जोखिम में परियोजनाएं",
    gu: "જોખમમાં પ્રોજેક્ટ્સ"
  },
  "readiness_assessment": {
    en: "TransformIQ Readiness Assessment (6 Dimensions)",
    hi: "ट्रांसफॉर्म आईक्यू तत्परता मूल्यांकन (6 आयाम)",
    gu: "ટ્રાન્સફોર્મ આઈક્યુ સજ્જતા મૂલ્યાંકન (6 પરિમાણો)"
  },
  "cycle_time_reduction": {
    en: "Cycle Time Reduction: AS-IS vs TO-BE (Hours)",
    hi: "चक्र समय में कमी: AS-IS बनाम TO-BE (घंटे)",
    gu: "સાયકલ સમયમાં ઘટાડો: AS-IS વિ TO-BE (કલાકો)"
  },

  // --- Common Buttons & Controls ---
  "save_changes": {
    en: "Save Changes",
    hi: "बदलाव सहेजें",
    gu: "ફેરફારો સાચવો"
  },
  "cancel": {
    en: "Cancel",
    hi: "रद्द करें",
    gu: "રદ કરો"
  },
  "edit_settings": {
    en: "Edit Settings",
    hi: "सेटिंग्स संपादित करें",
    gu: "સેટિંગ્સ સંપાદિત કરો"
  },
  "add_user": {
    en: "Add User",
    hi: "उपयोगकर्ता जोड़ें",
    gu: "વપરાશકર્તા ઉમેરો"
  },
  "filter": {
    en: "Filter",
    hi: "फ़िल्टर",
    gu: "ફિલ્ટર"
  },
  "search": {
    en: "Search",
    hi: "खोजें",
    gu: "શોધો"
  },
  "actions": {
    en: "Actions",
    hi: "कार्रवाई",
    gu: "ક્રિયાઓ"
  },
  "status": {
    en: "Status",
    hi: "स्थिति",
    gu: "સ્થિતિ"
  },

  // --- Role Perspective Banners ---
  "platform_administration__governance_center": {
    en: "Platform Administration & Governance Center",
    hi: "प्लेटफॉर्म प्रशासन और शासन केंद्र",
    gu: "પ્લેટફોર્મ વહીવટ અને શાસન કેન્દ્ર"
  },
  "transformation_executive_portfolio": {
    en: "Transformation Executive Portfolio",
    hi: "रूपांतरण कार्यकारी पोर्टफोलियो",
    gu: "ટ્રાન્સફોર્મેશન એક્ઝિક્યુટિવ પોર્ટફોલિયો"
  },
  "business_analysis__requirements_hub": {
    en: "Business Analysis & Requirements Hub",
    hi: "व्यावसायिक विश्लेषण और आवश्यकताएं केंद्र",
    gu: "વ્યવસાય વિશ્લેષણ અને જરૂરિયાતો કેન્દ્ર"
  },
  "solution_architecture__technical_design_hub": {
    en: "Solution Architecture & Technical Design Hub",
    hi: "समाधान वास्तुकला और तकनीकी डिजाइन केंद्र",
    gu: "સોલ્યુશન આર્કિટેક્ચર અને ટેકનિકલ ડિઝાઇન કેન્દ્ર"
  },
  "executive_decision__governance_dashboard": {
    en: "Executive Decision & Governance Dashboard",
    hi: "कार्यकारी निर्णय और शासन डैशबोर्ड",
    gu: "એક્ઝિક્યુટિવ નિર્ણય અને શાસન ડેશબોર્ડ"
  },
  "transformation_team_collaboration_workspace": {
    en: "Transformation Team Collaboration Workspace",
    hi: "रूपांतरण टीम सहयोग कार्यक्षेत्र",
    gu: "ટ્રાન્સફોર્મેશન ટીમ સહયોગ કાર્યક્ષેત્ર"
  },
  "stakeholder_read_only_transformation_overview": {
    en: "Stakeholder Read-Only Transformation Overview",
    hi: "हितधारक केवल-पठन रूपांतरण अवलोकन",
    gu: "સ્ટેકહોલ્ડર રીડ-ઓન્લી ટ્રાન્સફોર્મેશન વિહંગાવલોકન"
  },

  // --- Pipeline & Studio Pages ---
  "requirements__business_analysis": {
    en: "Requirements & Business Analysis",
    hi: "आवश्यकताएं और व्यावसायिक विश्लेषण",
    gu: "જરૂરિયાતો અને વ્યવસાય વિશ્લેષણ"
  },
  "8_dimension_gap_matrix": {
    en: "8-Dimension Gap Matrix",
    hi: "8-आयामी गैप मैट्रिक्स",
    gu: "8-પરિમાણીય ગેપ મેટ્રિક્સ"
  },
  "ai_recommendations_engine": {
    en: "AI Recommendations Engine",
    hi: "एआई सिफारिशें इंजन",
    gu: "એઆઈ ભલામણો એન્જિન"
  },
  "high_level_architecture": {
    en: "High Level Solution Architecture (HLD)",
    hi: "उच्च स्तरीय समाधान वास्तुकला (HLD)",
    gu: "હાઇ લેવલ સોલ્યુશન આર્કિટેક્ચર (HLD)"
  },
  "bpmn_process_workflows": {
    en: "BPMN Process Workflows & Automation",
    hi: "BPMN प्रक्रिया कार्यप्रवाह और स्वचालन",
    gu: "BPMN પ્રક્રિયા વર્કફ્લો અને ઓટોમેશન"
  },
  "database_schema_design": {
    en: "Database Schema & Entity Models",
    hi: "डेटाबेस स्कीमा और इकाई मॉडल",
    gu: "ડેટાબેઝ સ્કીમા અને એન્ટિટી મોડલ્સ"
  },
  "openapi_contracts_catalog": {
    en: "OpenAPI Contracts & Catalog",
    hi: "OpenAPI अनुबंध और कैटलॉग",
    gu: "OpenAPI કરારો અને કેટલોગ"
  },
  "ux_wireframes__personas": {
    en: "UX Wireframes & User Personas",
    hi: "यूएक्स वायरफ्रेम और उपयोगकर्ता व्यक्तित्व",
    gu: "યુએક્સ વાયરફ્રેમ્સ અને વપરાશકર્તા પર્સના"
  },
  "planning__estimation_roadmap": {
    en: "Planning & Estimation Roadmap",
    hi: "योजना और अनुमान रोडमैप",
    gu: "આયોજન અને અંદાજ રોડમેપ"
  },
  "scenario_simulation__roi": {
    en: "Scenario Simulation & ROI Analysis",
    hi: "परिदृश्य सिमुलेशन और आरओआई विश्लेषण",
    gu: "સિનારીયો સિમ્યુલેશન અને ROI વિશ્લેષણ"
  },
  "master_transformation_blueprint": {
    en: "Master Transformation Blueprint",
    hi: "मास्टर रूपांतरण ब्लूप्रिंट",
    gu: "માસ્ટર ટ્રાન્સફોર્મેશન બ્લુપ્રિન્ટ"
  }
};
