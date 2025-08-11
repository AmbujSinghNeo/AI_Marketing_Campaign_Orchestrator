# 🤖 AI Marketing Campaign Orchestrator

Automated marketing content generation powered by CrewAI multi-agent system. Generate comprehensive marketing campaigns from research to social posts in minutes.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![CrewAI](https://img.shields.io/badge/CrewAI-Latest-green.svg)](https://crewai.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 What It Does

Transform any product idea into a complete marketing campaign:
- **Research** competitors and market opportunities
- **Generate** SEO-optimized blog posts
- **Create** platform-specific social media content  
- **Extract** high-impact keywords
- **Schedule** content in marketing calendars

## 🏗️ System Architecture

graph TD
A[Product Input] --> B[Marketing Head Agent]
B --> C[Market Research]
C --> D[Executive Summary]
D --> E[Blog Writer Agent]
E --> F[SEO Specialist Agent]
F --> G[Social Media Agent]
G --> H[Content Calendar]

text
I[Web Scraper] --> B
J[Search Engine] --> B
K[Cache System] --> B

H --> L[marketing_outputs/]
L --> M[blog_post.md]
L --> N[social_posts.txt]
L --> O[seo_keywords.txt]
L --> P[content_calendar.md]
text

## 🚀 Quick Start

### Installation
git clone https://github.com/AmbujSinghNeo/AI_Marketing_Campaign_Orchestrator.git
cd AI_Marketing_Campaign_Orchestrator
pip install -r requirements.txt

text

### Environment Setup
Create `.env` file:
GROQ_API_KEY_1=your_groq_api_key
GROQ_API_KEY_2=your_groq_api_key
SERPER_API_KEY=your_serper_api_key

text

### Run Campaign Generation
cd main/
python main.py

text

## 📁 Project Structure

├── config/
│ ├── agents.yaml # AI agent configurations
│ └── tasks.yaml # Campaign workflow tasks
├── main/
│ ├── main.py # Application entry point
│ └── config.py # Core configurations
├── marketing_outputs/ # Generated content
└── cache/ # API response cache

text

## 🎮 Usage Example

**Input:**
crew.kickoff(inputs={
"product_name": "AI Excel Automation Tool",
"product_description": "Automates Excel tasks with AI"
})

text

**Generated Output:**
- **Market Research** (150-200 words)
- **Blog Post** with SEO optimization
- **Social Posts** for LinkedIn & X/Twitter
- **Keywords** for search ranking
- **Content Calendar** for 5-day schedule

## ⚙️ Key Features

| Feature | Description |
|---------|-------------|
| 🧠 **Multi-Agent AI** | 4 specialized agents working collaboratively |
| 🔍 **Smart Research** | Automated web scraping & competitor analysis |
| ✍️ **Content Creation** | SEO-optimized blogs & social posts |
| 📈 **SEO Optimization** | Keyword extraction & search ranking |
| 📅 **Content Planning** | Structured marketing calendars |
| ⚡ **Caching System** | Optimized API usage & cost reduction |

## 🛠️ Tech Stack

- **CrewAI** - Multi-agent orchestration
- **GROQ** - LLM provider (Gemma2-9b-it)
- **Python 3.8+** - Core language
- **YAML** - Configuration management
- **Custom Tools** - Web scraping & search

## 📊 Sample Output

### Generated Blog Post
Revolutionize Your Excel Workflow with AI Automation
Transform repetitive Excel tasks into automated workflows...

✅ 90% time reduction on data processing

✅ Error-free calculations and reporting

✅ Smart data analysis and insights

[Get Started Today →]

text

### Social Media Posts
LinkedIn: Tired of manual Excel work? Our AI tool automates spreadsheet tasks,
saving 10+ hours weekly. Perfect for SMEs! #ExcelAutomation #ProductivityAI

X: Excel automation just got smarter 🤖 Save hours on repetitive tasks with
AI-powered workflows. Built for modern businesses! #Excel #AI

text

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -m 'Add new feature'`)
4. Push to branch (`git push origin feature/new-feature`)
5. Open Pull Request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🔗 Links

- **Repository**: [GitHub](https://github.com/AmbujSinghNeo/AI_Marketing_Campaign_Orchestrator)
- **Issues**: [Report Bug](https://github.com/AmbujSinghNeo/AI_Marketing_Campaign_Orchestrator/issues)
- **Author**: [AmbujSinghNeo](https://github.com/AmbujSinghNeo)

---

**⭐ Star this repo if it helps your marketing workflow!**
