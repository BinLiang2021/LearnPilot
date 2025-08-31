# 🚧 LearnPilot Development Plan

## 📋 Vision & Objectives

Transform LearnPilot into a comprehensive AI-powered research assistant with:

1. **Automated Paper Discovery**: Daily arXiv monitoring with AI-powered filtering
2. **Multi-Session Chat System**: Multiple concurrent conversations with OpenAI Agents SDK
3. **Interactive Learning Environment**: Three-panel interface for structured learning
4. **User Management**: Role-based authentication with admin approval workflow

## 🎯 Development Phases

### Phase 1: Core Infrastructure Enhancement (Week 1-2)
**Goal**: Establish robust foundation for all backend services

#### 1.1 Authentication System (`src/learn_pilot/auth/`)
- [x] **Current**: Basic login/register with JWT tokens
- [ ] **Enhancement Tasks**:
  - [ ] Implement role-based permissions (User/Admin/Researcher)
  - [ ] Add password reset functionality
  - [ ] Session management with refresh tokens
  - [ ] API rate limiting per user
  - [ ] User preference storage system

**Implementation**:
```python
# src/learn_pilot/auth/permissions.py
from enum import Enum
class UserRole(Enum):
    ADMIN = "admin"
    USER = "user"
    RESEARCHER = "researcher"

# src/learn_pilot/auth/middleware.py
class RateLimitMiddleware:
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
```

#### 1.2 Database Architecture (`src/learn_pilot/database/`)
- [x] **Current**: Basic User model
- [ ] **New Models**:
  ```python
  # models.py additions
  class Paper(Base):
      id = Column(Integer, primary_key=True)
      title = Column(String, nullable=False)
      authors = Column(JSON)
      abstract = Column(Text)
      arxiv_id = Column(String, unique=True)
      pdf_path = Column(String)
      markdown_content = Column(Text)
      upload_date = Column(DateTime)
      user_id = Column(Integer, ForeignKey('users.id'))
  
  class ChatSession(Base):
      id = Column(Integer, primary_key=True)
      name = Column(String, nullable=False)
      user_id = Column(Integer, ForeignKey('users.id'))
      created_at = Column(DateTime)
      context_data = Column(JSON)
  
  class ChatMessage(Base):
      id = Column(Integer, primary_key=True)
      session_id = Column(Integer, ForeignKey('chat_sessions.id'))
      role = Column(String)  # 'user' or 'assistant'
      content = Column(Text)
      timestamp = Column(DateTime)
  
  class UserPreferences(Base):
      id = Column(Integer, primary_key=True)
      user_id = Column(Integer, ForeignKey('users.id'))
      research_interests = Column(JSON)
      arxiv_categories = Column(JSON)
      difficulty_level = Column(String)
      daily_paper_limit = Column(Integer)
  ```

#### 1.3 Configuration Management (`src/learn_pilot/core/config/`)
- [ ] **Enhanced Config System**:
  - [ ] Environment-specific configurations (dev/staging/prod)
  - [ ] Feature flags for gradual rollout
  - [ ] API key rotation and validation
  - [ ] User preference templates

### Phase 2: AI Agent Integration (Week 3-4)
**Goal**: Implement OpenAI Agents SDK with multi-paper context understanding

#### 2.1 OpenAI Agents SDK Setup (`src/learn_pilot/agents/`)
- [ ] **Core Agent Factory**:
  ```python
  # agents/agent_factory.py
  from openai import OpenAI
  from typing import Dict, Any, List
  
  class AgentFactory:
      def __init__(self, api_key: str):
          self.client = OpenAI(api_key=api_key)
      
      async def create_chat_agent(self, 
                                papers: List[str], 
                                user_context: Dict) -> 'ChatAgent':
          # Initialize agent with paper context
          pass
      
      async def create_analysis_agent(self, 
                                    paper_content: str) -> 'PaperAnalysisAgent':
          # Create specialized analysis agent
          pass
  ```

- [ ] **Agent Implementations**:
  - [ ] `ChatAgent`: Multi-paper conversational AI
  - [ ] `PaperAnalysisAgent`: Deep paper analysis and summarization
  - [ ] `LearningAssistantAgent`: Study plan and mind map generation
  - [ ] `FilterAgent`: arXiv paper relevance scoring

#### 2.2 Memory Management (`src/learn_pilot/ai/memory_store.py`)
- [ ] **Conversation Memory**:
  - [ ] Session-based context storage
  - [ ] Paper-aware conversation history
  - [ ] Context summarization for long conversations
  - [ ] Memory persistence across sessions

### Phase 3: Paper Discovery & Processing (Week 5-6)
**Goal**: Automated arXiv monitoring with intelligent filtering

#### 3.1 arXiv Integration (`src/learn_pilot/services/arxiv_monitor/`)
- [ ] **Daily Paper Fetching**:
  ```python
  # services/arxiv_monitor/daily_fetcher.py
  class ArxivDailyFetcher:
      def __init__(self):
          self.categories = ['cs.AI', 'cs.CL', 'cs.LG', 'cs.CV']
      
      async def fetch_daily_papers(self, 
                                 user_preferences: Dict) -> List[Paper]:
          # Fetch papers based on user interests
          pass
      
      async def score_relevance(self, 
                              paper: Paper, 
                              user_interests: List[str]) -> float:
          # AI-powered relevance scoring
          pass
  ```

- [ ] **Paper Processing Pipeline**:
  - [ ] PDF to Markdown conversion (using existing Marker integration)
  - [ ] Content extraction and indexing
  - [ ] Metadata enrichment (citations, related papers)
  - [ ] Automatic tagging and categorization

#### 3.2 Recommendation Engine (`src/learn_pilot/services/recommendation_engine.py`)
- [ ] **Personalized Recommendations**:
  - [ ] Learning from user reading patterns
  - [ ] Collaborative filtering with similar users
  - [ ] Topic trend analysis
  - [ ] Difficulty level matching

#### 3.3 Vector Search (`src/learn_pilot/services/vector_search/`)
- [ ] **Semantic Search System**:
  - [ ] Paper embedding generation
  - [ ] FAISS index management
  - [ ] Multi-modal search (text + concepts)
  - [ ] Related paper discovery

### Phase 4: Multi-Session Chat System (Week 7-8)
**Goal**: Multiple concurrent chat workspaces with persistent memory

#### 4.1 Chat Service Architecture (`src/learn_pilot/services/chat_service.py`)
- [ ] **Session Management**:
  ```python
  class ChatService:
      async def create_session(self, 
                             user_id: int, 
                             name: str, 
                             selected_papers: List[int]) -> ChatSession:
          # Create new chat workspace
          pass
      
      async def send_message(self, 
                           session_id: int, 
                           message: str) -> str:
          # Process message with AI agent
          pass
      
      async def get_session_history(self, 
                                  session_id: int) -> List[ChatMessage]:
          # Retrieve conversation history
          pass
  ```

#### 4.2 WebSocket Integration (`src/learn_pilot/web/websocket/`)
- [ ] **Real-time Communication**:
  - [ ] WebSocket connection management
  - [ ] Message broadcasting
  - [ ] Typing indicators
  - [ ] Session synchronization across devices

### Phase 5: Three-Panel Learning Interface (Week 9-10)
**Goal**: Interactive learning environment with paper management

#### 5.1 Frontend Architecture Enhancement

##### Paper Management Panel (Left)
```typescript
// frontend/src/components/papers/PaperListPanel.tsx
export const PaperListPanel: React.FC = () => {
  const [papers, setPapers] = useState<Paper[]>([])
  const [selectedPapers, setSelectedPapers] = useState<number[]>([])
  
  return (
    <div className="paper-list-panel">
      <PaperFilters onFilterChange={handleFilterChange} />
      <PaperGrid papers={papers} onSelect={handlePaperSelect} />
      <PaperPreview paper={selectedPaper} />
    </div>
  )
}
```

##### Chat Interface (Center)
```typescript
// frontend/src/components/chat/ChatPanel.tsx
export const ChatPanel: React.FC = () => {
  const [sessions, setSessions] = useState<ChatSession[]>([])
  const [activeSession, setActiveSession] = useState<string>()
  
  return (
    <div className="chat-panel">
      <SessionTabs sessions={sessions} activeSession={activeSession} />
      <MessageList messages={messages} />
      <MessageInput onSend={handleSendMessage} />
    </div>
  )
}
```

##### Learning Tools Panel (Right)
```typescript
// frontend/src/components/learning/LearningToolsPanel.tsx
export const LearningToolsPanel: React.FC = () => {
  return (
    <div className="learning-tools-panel">
      <ToolButton icon="🧠" title="生成思维导图" onClick={() => generateMindMap()} />
      <ToolButton icon="📋" title="创建学习计划" onClick={() => createStudyPlan()} />
      <ToolButton icon="❓" title="生成测试题" onClick={() => generateQuestions()} />
      <GeneratedContent results={generatedContent} />
    </div>
  )
}
```

#### 5.2 Learning Tools Implementation (`src/learn_pilot/services/learning_tools/`)
- [ ] **Mind Map Generation**:
  ```python
  class MindMapGenerator:
      async def generate_from_papers(self, 
                                   papers: List[Paper]) -> Dict[str, Any]:
          # Create hierarchical concept map
          pass
  ```

- [ ] **Study Plan Creation**:
  ```python
  class StudyPlanGenerator:
      async def create_personalized_plan(self, 
                                       papers: List[Paper],
                                       user_level: str,
                                       time_budget: int) -> StudyPlan:
          # Generate structured learning schedule
          pass
  ```

### Phase 6: Advanced Features (Week 11-12)
**Goal**: Polish and advanced functionality

#### 6.1 Notification System (`src/learn_pilot/services/notification_service.py`)
- [ ] **Smart Notifications**:
  - [ ] Daily paper recommendations
  - [ ] Learning progress reminders
  - [ ] New papers in user's interest areas
  - [ ] Study session scheduling

#### 6.2 Analytics and Insights (`src/learn_pilot/tools/analytics/`)
- [ ] **Learning Analytics**:
  - [ ] Reading time tracking
  - [ ] Concept mastery progress
  - [ ] Paper recommendation accuracy
  - [ ] User engagement metrics

## 🛠️ Implementation Strategy

### Backend Directory Activation Plan

#### `src/learn_pilot/agents/` (Priority: High)
**Current Status**: Basic structure exists, needs OpenAI SDK integration
**Action Items**:
1. Install OpenAI Agents SDK
2. Implement agent factory pattern
3. Create specialized agent classes for different tasks
4. Add conversation memory management

#### `src/learn_pilot/services/` (Priority: High)
**Current Status**: Minimal services
**Action Items**:
1. Build arxiv monitoring service
2. Implement chat session management
3. Create recommendation engine
4. Add paper processing pipeline

#### `src/learn_pilot/ai/` (Priority: Medium)
**Current Status**: Empty
**Action Items**:
1. Context manager for multi-paper conversations
2. Memory store for persistent agent memory
3. Performance optimization and monitoring
4. Cost tracking for API usage

#### `src/learn_pilot/literature_utils/` (Priority: Medium)
**Current Status**: Basic PDF processing exists
**Action Items**:
1. Enhance PDF to Markdown conversion
2. Add arxiv API client
3. Implement content analysis tools
4. Vector search integration

#### `src/learn_pilot/tools/` (Priority: Low)
**Current Status**: Database tools exist
**Action Items**:
1. Add file system management utilities
2. Create translation tools for multi-language support
3. Build pricing calculators for API costs
4. Analytics and reporting tools

### Frontend Development Phases

#### Phase A: Component Library (Week 1-2)
- [ ] Build reusable UI components
- [ ] Implement design system with Tailwind CSS
- [ ] Create responsive layout components
- [ ] Add accessibility features

#### Phase B: Core Pages (Week 3-4)
- [ ] Enhanced Dashboard with interactive features
- [ ] Paper management interface
- [ ] Chat interface with session management
- [ ] User preferences and settings

#### Phase C: Three-Panel Interface (Week 5-6)
- [ ] Integrated learning environment
- [ ] Drag-and-drop functionality
- [ ] Real-time updates via WebSocket
- [ ] Progressive loading and caching

## 📊 Success Metrics

### Technical Metrics
- [ ] 100% API endpoint coverage
- [ ] <500ms average response time
- [ ] 99.9% uptime
- [ ] Zero security vulnerabilities

### User Experience Metrics
- [ ] <3 clicks to start paper analysis
- [ ] <10s paper upload and processing
- [ ] 90%+ user satisfaction with recommendations
- [ ] <2min average onboarding time

### Business Metrics
- [ ] Daily active users growth
- [ ] Paper processing volume
- [ ] User retention rates
- [ ] Feature adoption rates

## 🔧 Development Tools & Setup

### Required Dependencies
```bash
# Backend
pip install openai>=1.0.0 agents-sdk arxiv faiss-cpu sentence-transformers

# Frontend  
npm install @types/react-router-dom websocket lucide-react framer-motion

# Development
pip install black isort pytest coverage
npm install @testing-library/react vitest
```

### Environment Configuration
```bash
# .env.production
OPENAI_API_KEY=your_key_here
DATABASE_URL=postgresql://user:pass@host:port/dbname
REDIS_URL=redis://localhost:6379
ARXIV_API_BASE_URL=http://export.arxiv.org/api/query
```

### Deployment Architecture
```yaml
# docker-compose.prod.yml
services:
  backend:
    build: .
    environment:
      - DATABASE_URL=${DATABASE_URL}
    depends_on:
      - postgres
      - redis
  
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
  
  postgres:
    image: postgres:14
    environment:
      POSTGRES_DB: learnpilot
  
  redis:
    image: redis:7-alpine
```

## ⚡ Quick Start Commands

### Development Setup
```bash
# Backend development
cd /path/to/LearnPilot
pip install -r requirements.txt
python -m src.learn_pilot.database.init_database
./start_web.sh

# Frontend development
cd frontend
npm install
npm run dev

# Full stack development
docker-compose up -d
```

### Testing Commands
```bash
# Backend tests
python -m pytest tests/ -v --coverage

# Frontend tests
cd frontend && npm run test

# Integration tests
python tests/test_integration.py
```

### Deployment
```bash
# Production deployment
docker-compose -f docker-compose.prod.yml up -d

# Database migrations
python -m alembic upgrade head

# Static assets
cd frontend && npm run build
```

## 🎯 Next Immediate Actions

1. **Week 1 Focus**: Implement OpenAI Agents SDK integration
2. **Week 2 Focus**: Build multi-session chat backend
3. **Week 3 Focus**: Create three-panel frontend interface
4. **Week 4 Focus**: Add arXiv monitoring and filtering

This development plan transforms all `src/` directories into functional components while delivering the envisioned product features systematically.