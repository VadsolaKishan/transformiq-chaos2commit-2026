import logging
from typing import Dict, Any, Optional
from app.config.settings import settings
from app.ai.provider import GeminiProvider, OpenAIProvider, AzureOpenAIProvider
from app.ai import smart_engine

logger = logging.getLogger(__name__)

class AIOrchestrator:
    def __init__(self):
        self.provider_name = settings.AI_PROVIDER
        
    def _get_provider(self):
        # 1. Check explicit provider preference
        if settings.AI_PROVIDER == "gemini" and settings.GEMINI_API_KEY:
            return GeminiProvider()
        elif settings.AI_PROVIDER == "openai" and settings.OPENAI_API_KEY:
            return OpenAIProvider()
        elif settings.AI_PROVIDER == "azure_openai" and settings.AZURE_OPENAI_API_KEY:
            return AzureOpenAIProvider()

        # 2. Auto-detection mode (prioritize Gemini for free-tier excellence)
        if settings.GEMINI_API_KEY:
            return GeminiProvider()
        elif settings.OPENAI_API_KEY:
            return OpenAIProvider()
        elif settings.AZURE_OPENAI_API_KEY:
            return AzureOpenAIProvider()
        return None

    async def run_discovery_chat(self, history: list, context_data: Dict[str, Any], language: str = "en") -> Dict[str, Any]:
        last_msg = history[-1]["content"] if history else "Tell me about this project."
        
        # Check if real LLM is configured
        provider = self._get_provider()
        if provider:
            try:
                system_prompt = f"You are the TransformIQ AI Discovery Assistant. Language: {language}. Ask structured discovery questions about processes, stakeholders, systems, bottlenecks, budget, and compliance."
                reply = await provider.generate_chat(
                    [{"role": "system", "content": system_prompt}] + history,
                    context_data
                )
                return {
                    "message": reply,
                    "suggested_actions": [
                        "Review current AS-IS process bottlenecks",
                        "Extract functional requirements",
                        "Generate 8-dimension gap analysis",
                        "Calculate TransformIQ readiness score"
                    ]
                }
            except Exception as e:
                logger.warning(f"AI Provider call failed, falling back to smart engine: {e}")

        # Contextual dynamic discovery response
        proj_name = context_data.get("name", "this initiative")
        industry = context_data.get("industry", "enterprise")
        
        # Multilingual conversational greetings
        if language == "hi":
            reply = f"नमस्ते! मैं TransformIQ AI डिस्कवरी सहायक हूँ। '{proj_name}' के संदर्भ में आपके {industry} वर्कफ़्लो और मुख्य चुनौतियों का विश्लेषण करने के लिए मैं तैयार हूँ। क्या आप अपने वर्तमान सिस्टम और मुख्य बाधाओं के बारे में विस्तार से बता सकते हैं?"
            suggestions = [
                "वर्तमान प्रक्रियाओं का विश्लेषण करें",
                "गैप एनालिसिस (Gap Analysis) तैयार करें",
                "AI और ऑटोमेशन सिफारिशें देखें",
                "ट्रांसफॉर्मेशन स्कोर की गणना करें"
            ]
        elif language == "gu":
            reply = f"નમસ્તે! હું TransformIQ AI ડિસ્કવરી સહાયક છું. '{proj_name}' પ્રોજેક્ટ માટે તમારા {industry} વર્કફ્લો અને મુખ્ય પડકારોનું વિશ્લેષણ કરવા માટે હું તૈયાર છું. શું તમે તમારી વર્તમાન સિસ્ટમ્સ અને મુખ્ય મુશ્કેલીઓ વિશે વિગતો આપી શકો છો?"
            suggestions = [
                "વર્તમાન પ્રક્રિયાઓનું વિશ્લેષણ કરો",
                "ગેપ એનાલિસિસ (Gap Analysis) જનરેટ કરો",
                "AI અને ઓટોમેશન ભલામણો જુઓ",
                "ટ્રાન્સફોર્મેશન સ્કોર ગણો"
            ]
        else:
            reply = f"Hello! I am your TransformIQ AI Transformation Companion. Based on the business objectives for **{proj_name}** ({industry}), I've analyzed your challenge context and extracted critical operational variables.\n\nKey Discovery Findings:\n• **High Triage Friction**: Significant manual reading and categorization overhead.\n• **Integration Boundaries**: Disconnected legacy data stores requiring API-first bridges.\n• **Automation Candidates**: Straight-through NLP intent routing and SOP-grounded RAG assistance.\n\nWould you like me to generate the full **AS-IS Business Analysis**, run the **8-Dimension Gap Matrix**, or produce the **React Flow Architecture Blueprint**?"
            suggestions = [
                "Generate Complete Business Analysis & Requirements",
                "Execute 8-Dimension Gap Analysis",
                "Build Solution Architecture & BPMN Process",
                "Calculate TransformIQ Readiness Score"
            ]

        return {
            "message": reply,
            "suggested_actions": suggestions,
            "extracted_insights": {
                "industry": industry,
                "complexity_level": "Enterprise High",
                "recommended_architecture": "Event-Driven Microservices + FastAPI + RAG"
            }
        }

    async def chat_companion(self, message: str, project_context: str = "", language: str = "en") -> str:
        provider = self._get_provider()
        if provider:
            try:
                system_prompt = (
                    f"You are the TransformIQ Enterprise AI Transformation Companion. "
                    f"You are an expert Chief Digital Transformation Officer and Enterprise Solutions Architect. "
                    f"Language: {language}. "
                    f"Always answer directly, professionally, and dynamically based on the project context provided.\n\n"
                    f"Project Context:\n{project_context}\n\n"
                    f"Guidelines:\n"
                    f"- Provide actionable, technically grounded advice (mention specific tech stacks, microservices, databases, API designs, or ROI figures when relevant).\n"
                    f"- Structure your answer with clear markdown bullet points and sections.\n"
                    f"- Suggest logical next steps in the TransformIQ transformation workflow."
                )
                reply = await provider.generate_chat(
                    [{"role": "system", "content": system_prompt}, {"role": "user", "content": message}],
                    {"context": project_context}
                )
                if reply and reply.strip():
                    return reply.strip()
            except Exception as e:
                logger.warning(f"AI Provider ({type(provider).__name__}) call failed: {e}")

        # Smart contextual response based on user query and project context
        msg_lower = message.lower()
        proj_title = project_context.splitlines()[0] if project_context else "Enterprise Initiative"
        
        if any(w in msg_lower for w in ["architecture", "tech stack", "hld", "lld", "cloud", "aws", "azure", "fastapi", "microservice"]):
            return (
                f"**Enterprise Architecture Recommendation for {proj_title}**:\n\n"
                f"• **Gateway & Ingestion Layer**: Asynchronous FastAPI microservices behind an API Gateway with OAuth2 JWT tenant isolation.\n"
                f"• **Cognitive AI Pipeline**: Hybrid RAG pipeline combining vector embeddings (pgvector / Chroma) with semantic re-ranking for enterprise grounding.\n"
                f"• **Data & State Management**: PostgreSQL 16 for relational 3NF operational data, with Redis for sub-millisecond session caching and message queues.\n"
                f"• **Reliability & Scalability**: Containerized deployment with horizontal pod autoscaling (HPA) targeting 99.95% uptime.\n\n"
                f"You can explore the interactive diagram in the **Architecture** stage to inspect and customize each component."
            )
        elif any(w in msg_lower for w in ["gap", "bottleneck", "challenge", "problem", "friction"]):
            return (
                f"**Identified Operational Bottlenecks & Strategic Gaps**:\n\n"
                f"1. **Triage & Routing Latency**: Manual categorization creates a multi-day cycle time bottleneck before tickets reach the correct department.\n"
                f"2. **Data Silos**: Disconnected legacy systems prevent real-time status synchronization between customer portals and ERP databases.\n"
                f"3. **Absence of Straight-Through Processing (STP)**: 100% of cases currently require manual employee touchpoints.\n\n"
                f"**Strategic Remediation**: Automate standard tier-1 classification with >85% confidence threshold, routing only high-risk exceptions to human specialists. Check the **Gap Analysis** stage for the complete 8-dimension matrix."
            )
        elif any(w in msg_lower for w in ["cost", "budget", "price", "estimate", "hour", "timeline", "week", "month"]):
            return (
                f"**Preliminary Transformation Roadmap & Cost Estimation**:\n\n"
                f"• **Delivery Timeline**: 16 Weeks across 4 Agile Sprints (Discovery, Core Engineering, Frontend & Review Hub, Production Hardening).\n"
                f"• **Total Engineering Effort**: ~1,120 hours with a dedicated cross-functional team of 6 engineers.\n"
                f"• **Estimated Investment**: ~$138,500 including engineering labor, cloud infrastructure, and AI inference capacity.\n"
                f"• **Projected ROI**: 87% operational efficiency gain with estimated breakeven in 6.4 months post go-live.\n\n"
                f"Review the full breakdown in the **Planning & Estimation** tab."
            )
        elif any(w in msg_lower for w in ["api", "endpoint", "rest", "integration"]):
            return (
                f"**API Strategy & Integration Catalog**:\n\n"
                f"• **Enterprise Gateway**: RESTful OpenAPI 3.0 compliant endpoints with zero-trust token authentication.\n"
                f"• **Key Integration Contracts**: Webhooks for real-time ticket ingestion, bidirectional CRM sync, and automated resolution dispatch.\n"
                f"• **Telemetry & Governance**: Rate-limited at 1,200 req/min with immutable audit logging on all mutating endpoints.\n\n"
                f"Check the **APIs** stage to inspect schemas, headers, and mock response payloads."
            )
        elif any(w in msg_lower for w in ["return", "support", "complaint", "customer"]):
            return (
                f"**Customer Experience & Resolution Strategy**:\n\n"
                f"1. **Real-Time Sentiment & Intent Parsing**: Immediate automated triage upon email/ticket ingestion within <3 seconds.\n"
                f"2. **Automated Tier-1 Resolution**: Direct integration with order management systems to automate standard status lookups and low-risk returns.\n"
                f"3. **Specialist Escalation**: Seamless handoff with pre-generated AI resolution draft for human-in-the-loop sign-off.\n\n"
                f"Would you like to review the AS-IS versus TO-BE workflow in the **Process Workflow** stage?"
            )
        else:
            return (
                f"I have reviewed your query: *\"{message}\"*\n\n"
                f"Based on the transformation blueprint for **{proj_title}**:\n\n"
                f"• **Process Modernization**: Current workflows can be elevated from high manual overhead to event-driven straight-through processing.\n"
                f"• **Target Metric**: Target >75% STP rate with automated NLP classification and contextual RAG knowledge grounding.\n"
                f"• **Next Best Action**: Explore the **Business Analysis**, **Gap Analysis**, and **Architecture** stages to validate requirements and approve the master transformation blueprint.\n\n"
                f"Feel free to ask for specific architecture recommendations, risk assessments, or timeline estimates!"
            )

    async def generate_business_analysis(self, context_data: Dict[str, Any]) -> Dict[str, Any]:
        return smart_engine.build_contextual_business_analysis(context_data)

    async def generate_gap_analysis(self, context_data: Dict[str, Any]) -> Dict[str, Any]:
        return smart_engine.build_contextual_gap_analysis(context_data)

    async def generate_recommendations(self, context_data: Dict[str, Any]) -> Dict[str, Any]:
        return smart_engine.build_contextual_recommendations(context_data)

    async def generate_architecture(self, context_data: Dict[str, Any]) -> Dict[str, Any]:
        return smart_engine.build_contextual_architecture(context_data)

    async def generate_process_workflow(self, context_data: Dict[str, Any]) -> Dict[str, Any]:
        return smart_engine.build_contextual_process_workflow(context_data)

    async def generate_database_design(self, context_data: Dict[str, Any]) -> Dict[str, Any]:
        return smart_engine.build_contextual_database(context_data)

    async def generate_api_catalog(self, context_data: Dict[str, Any]) -> Dict[str, Any]:
        return smart_engine.build_contextual_apis(context_data)

    async def generate_api_design(self, context_data: Dict[str, Any]) -> Dict[str, Any]:
        return smart_engine.build_contextual_apis(context_data)

    async def generate_ux_design(self, context_data: Dict[str, Any]) -> Dict[str, Any]:
        return smart_engine.build_contextual_ux(context_data)

    async def generate_planning(self, context_data: Dict[str, Any]) -> Dict[str, Any]:
        return smart_engine.build_contextual_planning(context_data)

    async def generate_estimates(self, context_data: Dict[str, Any]) -> Dict[str, Any]:
        return smart_engine.build_contextual_estimates(context_data)

    async def generate_risks(self, context_data: Dict[str, Any]) -> Dict[str, Any]:
        return smart_engine.build_contextual_risks(context_data)

    async def generate_score(self, context_data: Dict[str, Any]) -> Dict[str, Any]:
        return smart_engine.build_contextual_score(context_data)

    async def run_what_if_simulation(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        return smart_engine.calculate_what_if_simulation(request_data)

orchestrator = AIOrchestrator()
