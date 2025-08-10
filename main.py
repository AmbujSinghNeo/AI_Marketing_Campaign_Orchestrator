# main/main.py

import os
import sys
import yaml
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import from config.py (SIMPLIFIED - same directory import)
from config import (
    ensure_dir,
    SummarizedSearchTool,
    SummarizedScrapingTool,
    load_dotenv,
    ChatGroq
)

from crewai import Agent, Task, Crew, Process


def load_yaml_config(file_path):
    """Load YAML configuration file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

def create_agents_from_config(config_data, llm_mapping, tools_mapping):
    """Create agents from YAML configuration."""
    agents = {}
    
    for agent_name, agent_config in config_data.items():
        # Map LLM type to actual LLM instance
        llm = llm_mapping.get(agent_config['llm'])
        
        # Map tool names to actual tool instances
        tools = []
        for tool_name in agent_config.get('tools', []):
            if tool_name in tools_mapping:
                tools.append(tools_mapping[tool_name])
        
        agents[agent_name] = Agent(
            role=agent_config['role'],
            goal=agent_config['goal'],
            backstory=agent_config['backstory'],
            llm=llm,
            tools=tools,
            verbose=agent_config.get('verbose', False),
            max_iter=agent_config.get('max_iter', 1),
            allow_delegation=agent_config.get('allow_delegation', False),
            max_rpm=agent_config.get('max_rpm', 1)
        )
    
    return agents

def create_tasks_from_config(task_config, agents):
    """Create tasks from YAML configuration."""
    tasks = {}
    
    for task_name, task_data in task_config.items():
        # Determine which agent to assign based on task type
        agent_mapping = {
            'market_research': 'marketing_head',
            'executive_summary': 'marketing_head',
            'blog_post': 'blogger',
            'seo_keywords': 'seo_specialist',
            'social_media_posts': 'social_writer',
            'content_calendar': 'marketing_head'
        }
        
        agent = agents[agent_mapping[task_name]]
        
        # Create context list if needed (FIXED CONTEXT HANDLING)
        context = []
        if task_name == 'executive_summary':
            context = [tasks['market_research']] if 'market_research' in tasks else []
        elif task_name == 'blog_post':
            context = [tasks['executive_summary']] if 'executive_summary' in tasks else []
        elif task_name == 'seo_keywords':
            context = [t for t in [tasks.get('executive_summary'), tasks.get('blog_post')] if t]
        elif task_name == 'social_media_posts':
            context = [t for t in [tasks.get('blog_post'), tasks.get('seo_keywords')] if t]
        elif task_name == 'content_calendar':
            context = [t for t in [tasks.get('blog_post'), tasks.get('social_media_posts'), tasks.get('seo_keywords')] if t]
        
        tasks[task_name] = Task(
            description=task_data['description'],
            expected_output=task_data['expected_output'],
            agent=agent,
            context=context,
            output_file=task_data['output_file']
        )
    
    return tasks

def main():
    """Main function to run the marketing automation crew."""
    # Load environment variables
    load_dotenv()
    ensure_dir("marketing_outputs")
    ensure_dir("cache")
    
    # Load YAML configurations
    agents_config = load_yaml_config(project_root / "config" / "agents.yaml")
    tasks_config = load_yaml_config(project_root / "config" / "tasks.yaml")
    
    # Initialize LLMs
    writer_llm = ChatGroq(
        api_key=os.getenv("GROQ_API_KEY_1"),
        model_name="groq/gemma2-9b-it",
        temperature=0.5
    )
    utility_llm = ChatGroq(
        api_key=os.getenv("GROQ_API_KEY_2"),
        model_name="groq/gemma2-9b-it",
        temperature=0.2
    )
    
    # LLM mapping for agents
    llm_mapping = {
        'writer': writer_llm,
        'utility': utility_llm
    }
    
    # Initialize tools
    search_tool = SummarizedSearchTool()
    scraping_tool = SummarizedScrapingTool()
    
    # Tools mapping for agents
    tools_mapping = {
        'scraper_tool': scraping_tool,
        'serper_tool': search_tool
    }
    
    # Create agents from config
    agents = create_agents_from_config(agents_config, llm_mapping, tools_mapping)
    
    # Create tasks from config (FIXED ORDER)
    task_order = ['market_research', 'executive_summary', 'blog_post', 'seo_keywords', 'social_media_posts', 'content_calendar']
    tasks = {}
    
    for task_name in task_order:
        if task_name in tasks_config:
            task_data = tasks_config[task_name]
            agent_mapping = {
                'market_research': 'marketing_head',
                'executive_summary': 'marketing_head',
                'blog_post': 'blogger',
                'seo_keywords': 'seo_specialist',
                'social_media_posts': 'social_writer',
                'content_calendar': 'marketing_head'
            }
            
            agent = agents[agent_mapping[task_name]]
            
            # Create context list
            context = []
            if task_name == 'executive_summary':
                context = [tasks['market_research']] if 'market_research' in tasks else []
            elif task_name == 'blog_post':
                context = [tasks['executive_summary']] if 'executive_summary' in tasks else []
            elif task_name == 'seo_keywords':
                context = [t for t in [tasks.get('executive_summary'), tasks.get('blog_post')] if t]
            elif task_name == 'social_media_posts':
                context = [t for t in [tasks.get('blog_post'), tasks.get('seo_keywords')] if t]
            elif task_name == 'content_calendar':
                context = [t for t in [tasks.get('blog_post'), tasks.get('social_media_posts'), tasks.get('seo_keywords')] if t]
            
            tasks[task_name] = Task(
                description=task_data['description'],
                expected_output=task_data['expected_output'],
                agent=agent,
                context=context,
                output_file=task_data['output_file']
            )
    
    # Create crew
    crew = Crew(
        agents=list(agents.values()),
        tasks=list(tasks.values()),
        process=Process.sequential,
        verbose=False,
        max_rpm=3
    )
    
    print("Kicking off the optimized marketing crew...")
    result = crew.kickoff(inputs={
        "product_name": "AI Powered Excel Automation Tool",
        "product_description": "Automates repetitive Excel tasks with AI to save time and reduce errors."
    })
    print("Finished. Outputs in marketing_outputs/")
    print(result)

if __name__ == "__main__":
    main()


