# 🏗️ LearnPilot System Architecture

## 📋 Overview

LearnPilot is designed as a modern, scalable AI-powered research assistant with the following core capabilities:

1. **Intelligent Paper Discovery**: Automated arXiv monitoring and filtering
2. **Multi-Session Chat Interface**: Conversational AI with memory persistence
3. **Interactive Learning Environment**: Three-panel interface for structured learning
4. **User Management**: Role-based authentication with admin approval workflow

## 🎯 Product Requirements

### 1. Paper Discovery & Filtering
- Daily arXiv paper retrieval based on user preferences
- AI-powered relevance scoring and categorization
- Personal recommendation engine that learns from user behavior
- Support for manual paper upload (PDF, Markdown, TXT)

### 2. Multi-Session Chat System
- Multiple concurrent chat windows/workspaces
- Each session maintains conversation history and context
- OpenAI Agents SDK integration for intelligent responses
- Paper-aware conversational AI that understands selected documents

### 3. Structured Learning Interface
- **Left Panel**: Interactive paper list with hover previews
- **Center Panel**: Chat interface with AI agent
- **Right Panel**: Learning tools (mind maps, study plans, summaries)
- Generated content displays as expandable cards below tools

### 4. User Experience
- Secure authentication with admin approval workflow
- Personalized preferences and learning paths
- Session persistence across devices
- Responsive design for various screen sizes

## 🏛️ System Architecture

### Backend Architecture (FastAPI + Python)

```
src/learn_pilot/
├── agents/              # OpenAI Agents SDK implementations
│   ├── chat_agent.py          # Main conversational agent
│   ├── paper_analyst.py       # Paper analysis and summarization
│   ├── learning_assistant.py  # Study plan and mind map generation
│   ├── filter_agent.py        # Paper relevance filtering
│   └── memory_manager.py      # Conversation memory handling
├── ai/                  # AI optimization and monitoring
│   ├── agent_factory.py       # Agent instantiation and management
│   ├── context_manager.py     # Multi-paper context handling
│   ├── memory_store.py        # Persistent memory storage
│   └── optimization.py        # Performance monitoring
├── auth/               # Authentication and authorization
│   ├── auth.py                # User authentication logic
│   ├── admin_auth.py          # Admin-specific authentication
│   └── middleware.py          # Authentication middleware
├── core/               # Core system components
│   ├── config/                # Configuration management
│   ├── logging/               # Logging and monitoring
│   └── agents/                # Base agent classes
├── database/           # Database models and operations
│   ├── models.py              # SQLAlchemy models
│   ├── service.py             # Database service layer
│   └── migrations/            # Database migration scripts
├── services/           # Business logic services
│   ├── arxiv_monitor/         # arXiv paper monitoring
│   ├── paper_service.py       # Paper management logic
│   ├── chat_service.py        # Chat session management
│   ├── user_service.py        # User preference management
│   ├── recommendation_engine.py # Personalized recommendations
│   └── vector_search/         # Semantic search capabilities
├── literature_utils/   # Paper processing utilities
│   ├── knowledge_parser/      # PDF to text extraction
│   ├── knowledge_search/      # Content search and indexing
│   ├── arxiv_client.py        # arXiv API integration
│   └── content_analyzer.py    # Paper content analysis
├── tools/              # Utility functions
│   ├── database/              # Database management tools
│   ├── file_system/           # File handling utilities
│   ├── translation/           # Multi-language support
│   └── pricing/               # Cost monitoring for AI APIs
└── web/               # FastAPI routes and API endpoints
    ├── api/                   # API route definitions
    ├── static/                # Static file serving
    └── templates/             # HTML templates (if needed)
```

### Frontend Architecture (React + TypeScript)

```
frontend/
├── src/
│   ├── components/     # Reusable UI components
│   │   ├── chat/              # Chat interface components
│   │   ├── papers/            # Paper list and preview components
│   │   ├── learning/          # Learning tools components
│   │   ├── auth/              # Authentication components
│   │   └── ui/                # Basic UI elements
│   ├── pages/         # Main application pages
│   │   ├── LoginPage.tsx      # User authentication
│   │   ├── DashboardPage.tsx  # Main dashboard
│   │   ├── ChatPage.tsx       # Multi-session chat interface
│   │   ├── LearningPage.tsx   # Three-panel learning environment
│   │   ├── PapersPage.tsx     # Paper management
│   │   └── SettingsPage.tsx   # User preferences
│   ├── services/      # API client and data management
│   │   ├── api.ts             # API client configuration
│   │   ├── auth.ts            # Authentication service
│   │   ├── chat.ts            # Chat session management
│   │   ├── papers.ts          # Paper management service
│   │   └── websocket.ts       # Real-time communication
│   ├── stores/        # State management
│   │   ├── authStore.ts       # Authentication state
│   │   ├── chatStore.ts       # Chat sessions state
│   │   ├── papersStore.ts     # Papers collection state
│   │   └── uiStore.ts         # UI state management
│   ├── hooks/         # Custom React hooks
│   │   ├── useChat.ts         # Chat functionality
│   │   ├── usePapers.ts       # Paper management
│   │   └── useAuth.ts         # Authentication helpers
│   └── utils/         # Utility functions
└── public/            # Static assets
```

## 🔄 Data Flow Architecture

### 1. Paper Discovery Flow
```
arXiv API → Paper Filtering Agent → Relevance Scoring → User Preferences → Database Storage → Frontend Display
```

### 2. Chat Session Flow
```
User Message → Context Manager → OpenAI Agent → Memory Store → Response Generation → Frontend Update
```

### 3. Learning Tools Flow
```
Selected Papers → Learning Assistant Agent → Tool Generation (Mind Map/Study Plan) → Database Storage → Frontend Display
```

## 🗄️ Database Schema Design

### Core Tables

#### Users & Authentication
- `users`: User profiles and preferences
- `admins`: Admin users with special permissions
- `user_sessions`: Active user sessions
- `user_preferences`: Research interests and settings

#### Papers & Content
- `papers`: Paper metadata and content
- `paper_collections`: User-organized paper groups
- `paper_tags`: Categorization and tagging
- `paper_summaries`: AI-generated summaries

#### Chat & Conversations
- `chat_sessions`: Individual chat workspaces
- `chat_messages`: Conversation history
- `chat_context`: Conversation memory and context
- `agent_memory`: Persistent agent memory stores

#### Learning & Tools
- `learning_materials`: Generated mind maps, study plans
- `user_progress`: Learning progress tracking
- `recommendations`: Personalized paper suggestions

## 🔌 External Integrations

### OpenAI Services
- **Agents SDK**: Core conversational AI capabilities
- **GPT-4/GPT-3.5**: Text generation and analysis
- **Embeddings API**: Semantic similarity and search

### Research Data Sources
- **arXiv API**: Paper metadata and full-text access
- **Semantic Scholar**: Citation networks and paper relationships
- **CrossRef**: DOI resolution and metadata enrichment

### Infrastructure
- **PostgreSQL**: Primary database for production
- **SQLite**: Development and testing database
- **Redis**: Caching and session storage
- **WebSocket**: Real-time chat updates

## 🚀 Deployment Architecture

### Development Environment
- Local SQLite database
- File-based storage for papers
- Hot-reload enabled for both frontend and backend

### Production Environment
- PostgreSQL database with read replicas
- Object storage (S3/MinIO) for paper files
- Load balancer for API endpoints
- WebSocket clustering for chat functionality

## 🔒 Security Considerations

### Authentication & Authorization
- JWT-based authentication
- Role-based access control (User/Admin)
- API rate limiting
- Input validation and sanitization

### Data Privacy
- User conversation history encryption
- Paper content access logging
- GDPR compliance for EU users
- Secure API key management

### AI Safety
- Content filtering for inappropriate requests
- Cost monitoring for OpenAI API usage
- Response validation and moderation
- User consent for data processing

## 📊 Monitoring & Analytics

### System Metrics
- API response times and error rates
- Database query performance
- AI agent response quality
- User engagement metrics

### Business Intelligence
- User learning pattern analysis
- Popular paper topics and trends
- Feature usage statistics
- Cost optimization insights

## 🔮 Future Scalability

### Horizontal Scaling
- Microservices architecture readiness
- Stateless API design
- Database sharding strategies
- CDN integration for static content

### AI Enhancement
- Custom model fine-tuning
- Multi-modal content processing (images, graphs)
- Advanced reasoning capabilities
- Collaborative filtering improvements

This architecture provides a solid foundation for building the envisioned LearnPilot system while maintaining flexibility for future enhancements and scaling needs.