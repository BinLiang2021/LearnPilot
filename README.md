# 🚀 LearnPilot: AI-Driven Research Paper Assistant

> *Your intelligent companion for navigating the vast world of academic research*

**LearnPilot** is an AI-powered research assistant that revolutionizes how you discover, organize, and interact with academic papers. Built with OpenAI Agents SDK and modern web technologies, it transforms your research workflow with intelligent paper filtering, conversational AI, and collaborative learning features.

## 🌟 Vision

LearnPilot bridges the gap between overwhelming paper repositories and meaningful research insights. Whether you're a researcher, student, or industry professional, LearnPilot helps you:

- **Discover**: Automatically find and filter relevant papers from arXiv based on your preferences
- **Interact**: Chat with AI agents that understand your selected papers deeply
- **Learn**: Create structured learning paths with mind maps, summaries, and personalized study plans
- **Collaborate**: Manage multiple research conversations with persistent memory

## ✨ Key Features

### 📡 Intelligent Paper Discovery
- **Automated arXiv Monitoring**: Daily retrieval of new papers based on your research interests
- **Smart Filtering**: AI-powered relevance scoring and categorization
- **Personalized Recommendations**: Learning algorithm that adapts to your reading patterns
- **Multi-format Support**: PDF, Markdown, and text file processing

### 💬 Conversational Research Assistant
- **Multi-Paper Chat**: Interactive conversations with AI agents about your selected papers
- **Memory Persistence**: Each chat window maintains context across sessions
- **Multiple Workspaces**: Organize different research topics in separate chat environments
- **Contextual Understanding**: AI agents with deep knowledge of your paper collection

### 📚 Structured Learning Environment
- **Three-Panel Interface**: Papers list (left) + Chat (center) + Tools (right)
- **Interactive Paper Preview**: Hover to view abstracts, keywords, and key insights
- **Learning Tools**: Generate mind maps, study plans, and concept diagrams
- **Progress Tracking**: Monitor your learning journey across different research areas

### 🔐 User Management System
- **Role-based Authentication**: Admin approval workflow for new users
- **Personal Preferences**: Customizable research interests and difficulty levels
- **Session Management**: Secure multi-device access with persistent settings

## 🏗️ Architecture

### Backend (FastAPI + Python)
```
src/learn_pilot/
├── agents/           # OpenAI Agents SDK implementations
├── auth/            # Authentication and authorization
├── database/        # SQLAlchemy models and database logic
├── services/        # Business logic and external API integrations
├── web/            # FastAPI routes and API endpoints
├── ai/             # AI optimization and monitoring
├── tools/          # Utility functions and helpers
└── literature_utils/ # Paper processing and analysis
```

### Frontend (React + TypeScript)
```
frontend/
├── src/
│   ├── pages/      # Main application pages
│   ├── components/ # Reusable UI components  
│   ├── services/   # API client and data management
│   └── styles/     # Application styling
└── public/         # Static assets
```

### Key Technologies
- **AI Framework**: OpenAI Agents SDK, GPT-4 integration
- **Backend**: FastAPI, SQLAlchemy, PostgreSQL/SQLite
- **Frontend**: React, TypeScript, Vite, Tailwind CSS
- **Paper Processing**: Marker PDF extraction, arXiv API
- **Authentication**: JWT tokens, role-based access control

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ 
- Node.js 16+
- OpenAI API key

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/your-username/LearnPilot.git
cd LearnPilot
```

2. **Set up the backend**
```bash
# Install Python dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your OpenAI API key

# Initialize database
python -c "from src.learn_pilot.database import init_database; init_database()"

# Start the backend server
./start_web.sh
```

3. **Set up the frontend**
```bash
cd frontend

# Install Node.js dependencies
npm install

# Start the development server
npm run dev
```

4. **Access the application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Admin Setup
```bash
# The default admin account is created automatically
# Username: admin
# Password: admin123 (⚠️ Change this after first login!)

# Use the admin tools for user management
python simple_admin.py
```

## 📖 Usage Guide

### 1. User Registration & Approval
- New users register through the web interface
- Admin approval required for account activation
- Use `python simple_admin.py` for user management

### 2. Paper Discovery
- Configure research interests in user preferences
- System automatically fetches relevant papers from arXiv
- Review and select papers for your research collection

### 3. Interactive Learning
- Open the Learning Page with selected papers
- Chat with AI agents about paper content, methods, and implications
- Generate study materials using the right-panel tools

### 4. Multi-Session Management
- Create separate chat sessions for different research topics
- Each session maintains conversation history and context
- Switch between sessions without losing progress

## 🛣️ Development Roadmap

### Phase 1: Core Infrastructure ✅
- [x] User authentication and admin system
- [x] Basic paper upload and storage
- [x] Simple chat interface
- [x] Database architecture

### Phase 2: AI Integration (In Progress)
- [ ] OpenAI Agents SDK integration
- [ ] Multi-paper context understanding
- [ ] Conversation memory management
- [ ] Paper content analysis agents

### Phase 3: Learning Tools (Planned)
- [ ] Interactive learning interface
- [ ] Mind map generation
- [ ] Study plan creation
- [ ] Progress tracking system

### Phase 4: Discovery & Automation (Planned)
- [ ] arXiv monitoring and filtering
- [ ] Personalized recommendations
- [ ] Automated paper preprocessing
- [ ] Advanced search capabilities

### Phase 5: Advanced Features (Future)
- [ ] Collaborative features
- [ ] Citation network analysis
- [ ] Research trend visualization
- [ ] Export and sharing tools

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines and open issues for areas where you can help.

### Development Setup
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Code formatting
black src/
isort src/
```

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for the Agents SDK and API access
- arXiv for open access to research papers
- The open source community for amazing tools and libraries

---

*LearnPilot: Making research accessible, interactive, and intelligent.* 🧠✨