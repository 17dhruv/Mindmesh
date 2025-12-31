"""Gemini AI Service for Mindmesh application."""

import json
import logging
import re
import time
from typing import Dict, List, Optional, Any
from uuid import UUID

import google.generativeai as genai
from tenacity import retry, stop_after_attempt, wait_exponential

from .config import settings
from .database import User, Plan, Task, AIInteraction, async_session

# Configure logging
logger = logging.getLogger(__name__)

# Configure Gemini
genai.configure(api_key=settings.google_api_key)


class GeminiAIService:
    """Service for integrating with Google Gemini AI."""

    def __init__(self):
        """Initialize the Gemini AI service."""
        self.model = genai.GenerativeModel(
            model_name=settings.gemini_model,
            generation_config={
                "temperature": settings.gemini_temperature,
                "max_output_tokens": settings.gemini_max_tokens,
            }
        )
        self.safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            }
        ]

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def _generate_content(self, prompt: str) -> str:
        """Generate content using Gemini with retry logic."""
        try:
            response = self.model.generate_content(
                prompt,
                safety_settings=self.safety_settings
            )
            return response.text
        except Exception as e:
            logger.error(f"Gemini API error: {str(e)}")
            raise

    def _extract_json_from_response(self, response: str) -> str:
        """Extract JSON from Gemini response (removes markdown code blocks)."""
        import re

        # First, try to parse directly
        try:
            json.loads(response.strip())
            return response.strip()
        except json.JSONDecodeError:
            pass

        # Look for JSON in markdown code blocks
        json_patterns = [
            r'```json\s*\n(.*?)\n```',
            r'```json\n(.*?)\n```',
            r'```\s*\n(.*?)\n```',
            r'```\n(.*?)\n```',
            r'```json\s*(.*?)```',
            r'```\s*(.*?)```'
        ]

        for pattern in json_patterns:
            match = re.search(pattern, response, re.DOTALL | re.MULTILINE)
            if match:
                json_content = match.group(1).strip()
                try:
                    # Validate that it's actually JSON
                    json.loads(json_content)
                    return json_content
                except json.JSONDecodeError:
                    # Try to clean up common JSON issues
                    cleaned_content = json_content.replace('\n', ' ').replace('\r', '')
                    try:
                        json.loads(cleaned_content)
                        return cleaned_content
                    except json.JSONDecodeError:
                        continue

        # Look for JSON-like structure in the text
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            json_str = json_match.group(0).strip()
            try:
                json.loads(json_str)
                return json_str
            except json.JSONDecodeError:
                # Try to clean up
                cleaned_json = json_str.replace('\n', ' ').replace('\r', '')
                try:
                    json.loads(cleaned_json)
                    return cleaned_json
                except json.JSONDecodeError:
                    pass

        # If all else fails, return the original response
        return response.strip()

    async def analyze_user_context(self, user_id: str) -> Dict[str, Any]:
        """Analyze user's historical patterns and preferences."""
        async with async_session() as session:
            # Get user's plans and tasks
            result = await session.execute(
                """
                SELECT p.title, p.description, p.status, p.created_at,
                       t.title as task_title, t.description as task_desc,
                       t.priority, t.status as task_status, t.ai_category
                FROM plans p
                LEFT JOIN tasks t ON p.id = t.plan_id
                WHERE p.user_id = :user_id
                ORDER BY p.created_at DESC, t.created_at DESC
                """,
                {"user_id": user_id}
            )

            data = result.fetchall()

            # Analyze patterns
            plans = {}
            task_categories = set()
            priority_patterns = []

            for row in data:
                plan_key = row.title
                if plan_key not in plans:
                    plans[plan_key] = {
                        "title": row.title,
                        "description": row.description,
                        "status": row.status,
                        "tasks": []
                    }

                if row.task_title:
                    task_info = {
                        "title": row.task_title,
                        "description": row.task_desc,
                        "priority": row.priority,
                        "status": row.task_status,
                        "category": row.ai_category
                    }
                    plans[plan_key]["tasks"].append(task_info)

                    if row.ai_category:
                        task_categories.add(row.ai_category)
                    priority_patterns.append(row.priority)

            # Generate context summary
            context = {
                "total_plans": len(plans),
                "plan_data": list(plans.values()),
                "task_categories": list(task_categories),
                "priority_distribution": {
                    "high": priority_patterns.count(5),
                    "medium_high": priority_patterns.count(4),
                    "medium": priority_patterns.count(3),
                    "medium_low": priority_patterns.count(2),
                    "low": priority_patterns.count(1)
                }
            }

            return context

    async def categorize_tasks(self, tasks: List[Dict[str, Any]], context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Group tasks into logical categories using semantic analysis."""

        # Prepare task information for AI
        task_info = []
        for i, task in enumerate(tasks):
            task_info.append(
                f"Task {i+1}: {task['title']}\n"
                f"Description: {task.get('description', 'No description')}\n"
                f"Current Priority: {task.get('priority', 3)}"
            )

        # Get user's preferred categories from context
        existing_categories = context.get("task_categories", [])

        prompt = f"""
        Analyze the following tasks and group them into logical categories.
        Consider the user's historical preferences: {existing_categories}

        Tasks to categorize:

        {chr(10).join(task_info)}

        Provide a JSON response with this structure:
        {{
            "categories": [
                {{
                    "name": "Category Name",
                    "description": "Brief description of what this category includes",
                    "tasks": [task_indices],
                    "priority_ranking": 1-5
                }}
            ],
            "reasoning": "Explanation of the categorization logic"
        }}

        Guidelines:
        - Create 3-7 meaningful categories
        - Each task should belong to exactly one category
        - Categories should be logical and actionable
        - Consider task types, complexity, and goals
        - Priority ranking: 1 (lowest priority) to 5 (highest priority category)
        """

        try:
            response = await self._generate_content(prompt)

            # Parse JSON response with extraction
            json_response = self._extract_json_from_response(response)
            ai_result = json.loads(json_response)

            # Map categories back to tasks
            categorized_tasks = []
            for category in ai_result.get("categories", []):
                for task_idx in category.get("tasks", []):
                    if 0 <= task_idx < len(tasks):
                        task_data = tasks[task_idx].copy()
                        task_data["ai_category"] = category["name"]
                        task_data["category_description"] = category["description"]
                        task_data["category_priority_ranking"] = category.get("priority_ranking", 3)
                        categorized_tasks.append(task_data)

            return {
                "categorized_tasks": categorized_tasks,
                "categories": ai_result.get("categories", []),
                "reasoning": ai_result.get("reasoning", ""),
                "uncategorized_tasks": [task for task in tasks if task not in categorized_tasks]
            }

        except Exception as e:
            logger.error(f"Error in task categorization: {str(e)}")
            # Fallback to basic categorization
            return {
                "categorized_tasks": tasks,
                "categories": [{"name": "General", "description": "Uncategorized tasks", "tasks": list(range(len(tasks))), "priority_ranking": 3}],
                "reasoning": "AI categorization failed, using default grouping",
                "uncategorized_tasks": []
            }

    async def score_priorities(self, tasks: List[Dict[str, Any]], context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Rank tasks by priority with AI reasoning."""

        task_info = []
        for i, task in enumerate(tasks):
            task_info.append(
                f"Task {i+1}: {task['title']}\n"
                f"Description: {task.get('description', 'No description')}\n"
                f"Category: {task.get('ai_category', 'No category')}\n"
                f"Current Priority: {task.get('priority', 3)}"
            )

        prompt = f"""
        Analyze and rank the following tasks by priority. Consider:
        - User's historical priority patterns: {context.get('priority_distribution', {})}
        - Task dependencies and logical flow
        - Estimated effort vs. impact
        - Urgency and importance

        Tasks to prioritize:

        {chr(10).join(task_info)}

        Provide a JSON response with this structure:
        {{
            "ranked_tasks": [
                {{
                    "task_index": 0,
                    "ai_priority_score": 1-10,
                    "reasoning": "Specific reason for this priority",
                    "estimated_effort": "Low/Medium/High",
                    "dependencies": ["task_indices"],
                    "impact_level": "Low/Medium/High"
                }}
            ],
            "recommendations": ["List of priority recommendations"]
        }}

        Scoring guidelines:
        - 1-3: Low priority (can be deferred)
        - 4-6: Medium priority (important but not urgent)
        - 7-8: High priority (important and somewhat urgent)
        - 9-10: Critical priority (urgent and critical)
        """

        try:
            response = await self._generate_content(prompt)
            json_response = self._extract_json_from_response(response)
            ai_result = json.loads(json_response)

            # Apply priority scores to tasks
            scored_tasks = []
            for task_score in ai_result.get("ranked_tasks", []):
                task_idx = task_score.get("task_index", 0)
                if 0 <= task_idx < len(tasks):
                    task_data = tasks[task_idx].copy()
                    task_data.update({
                        "ai_priority_score": task_score.get("ai_priority_score", 5),
                        "ai_reasoning": task_score.get("reasoning", ""),
                        "estimated_effort": task_score.get("estimated_effort", "Medium"),
                        "dependencies": task_score.get("dependencies", []),
                        "impact_level": task_score.get("impact_level", "Medium")
                    })
                    scored_tasks.append(task_data)

            return {
                "scored_tasks": scored_tasks,
                "recommendations": ai_result.get("recommendations", []),
                "unscored_tasks": [task for task in tasks if task not in scored_tasks]
            }

        except Exception as e:
            logger.error(f"Error in priority scoring: {str(e)}")
            # Fallback to basic priority scoring
            for task in tasks:
                task["ai_priority_score"] = task.get("priority", 3) * 2
                task["ai_reasoning"] = "Using original priority as fallback"
            return {
                "scored_tasks": tasks,
                "recommendations": ["AI scoring failed, using original priorities"],
                "unscored_tasks": []
            }

    async def generate_dashboard_suggestion(self, plan_id: str, user_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate complete dashboard with categories and ranked priorities."""
        start_time = time.time()

        async with async_session() as session:
            # Get plan and tasks
            plan_result = await session.execute(
                "SELECT * FROM plans WHERE id = :plan_id",
                {"plan_id": plan_id}
            )
            plan = plan_result.fetchone()

            tasks_result = await session.execute(
                "SELECT * FROM tasks WHERE plan_id = :plan_id",
                {"plan_id": plan_id}
            )
            tasks = [dict(row) for row in tasks_result.fetchall()]

        if not plan:
            raise ValueError(f"Plan with ID {plan_id} not found")

        # Convert tasks to dict format
        task_dicts = []
        for task in tasks:
            task_dicts.append({
                "id": task["id"],
                "title": task["title"],
                "description": task["description"],
                "priority": task["priority"],
                "status": task["status"]
            })

        # Step 1: Categorize tasks
        categorization_result = await self.categorize_tasks(task_dicts, user_context)

        # Step 2: Score priorities for categorized tasks
        priority_result = await self.score_priorities(
            categorization_result["categorized_tasks"],
            user_context
        )

        # Step 3: Generate final dashboard suggestion
        dashboard_prompt = f"""
        Create a comprehensive dashboard suggestion based on this analysis:

        Plan: {plan.title}
        Description: {plan.description}

        Categorized Tasks: {len(categorization_result['categorized_tasks'])}
        Categories: {len(categorization_result['categories'])}

        Priority Analysis: {len(priority_result['scored_tasks'])} tasks scored

        Provide a JSON response:
        {{
            "dashboard_title": "Suggested Dashboard Title",
            "summary": "Brief summary of the analysis",
            "categories": [...],
            "priority_groups": {{
                "critical": [],
                "high": [],
                "medium": [],
                "low": []
            }},
            "recommendations": [],
            "estimated_completion_time": "Time estimate",
            "next_steps": ["Immediate next steps"]
        }}
        """

        try:
            response = await self._generate_content(dashboard_prompt)
            json_response = self._extract_json_from_response(response)
            dashboard_data = json.loads(json_response)

            # Calculate response time
            response_time_ms = int((time.time() - start_time) * 1000)

            # Prepare final suggestion
            suggestion = {
                "plan_id": plan_id,
                "plan_title": plan.title,
                "dashboard_data": dashboard_data,
                "categorization": categorization_result,
                "priority_analysis": priority_result,
                "metadata": {
                    "total_tasks": len(task_dicts),
                    "categorized_tasks": len(categorization_result["categorized_tasks"]),
                    "response_time_ms": response_time_ms,
                    "model_used": settings.gemini_model
                }
            }

            return suggestion

        except Exception as e:
            logger.error(f"Error generating dashboard: {str(e)}")
            raise

    async def record_ai_interaction(
        self,
        user_id: str,
        plan_id: str,
        interaction_type: str,
        request_data: Dict[str, Any],
        response_data: Dict[str, Any],
        tokens_used: int = 0,
        response_time_ms: int = 0
    ) -> AIInteraction:
        """Record AI interaction for analytics and tracking."""
        async with async_session() as session:
            interaction = AIInteraction(
                user_id=user_id,
                plan_id=plan_id,
                interaction_type=interaction_type,
                request_data=json.dumps(request_data),
                response_data=json.dumps(response_data),
                tokens_used=tokens_used,
                model_used=settings.gemini_model,
                response_time_ms=response_time_ms,
                cost_estimate=self._estimate_cost(tokens_used)
            )

            session.add(interaction)
            await session.commit()
            await session.refresh(interaction)

            return interaction

    def _estimate_cost(self, tokens_used: int) -> float:
        """Estimate cost based on token usage."""
        # Gemini pricing (example rates - update with actual pricing)
        # These are placeholder rates - replace with actual Gemini pricing
        input_cost_per_1k = 0.0005  # $0.0005 per 1k input tokens
        output_cost_per_1k = 0.0015  # $0.0015 per 1k output tokens

        # Assume 50/50 split between input and output
        estimated_cost = (tokens_used / 1000) * ((input_cost_per_1k + output_cost_per_1k) / 2)
        return estimated_cost

    async def organize_into_categories(self, messy_prompt: str, user_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Convert messy user prompt into organized categories with todo/doing/upcoming blocks."""

        prompt = f"""
        You are a task organization expert. The user will give you a messy, unorganized prompt about their goals, ideas, or thoughts.
        Your job is to:
        1. Extract clear, actionable tasks from their messy input
        2. Group tasks into logical categories (3-7 categories)
        3. Assign each task to a status: "todo" (not started), "doing" (in progress), or "upcoming" (blocked/future)

        User's messy input:
        {messy_prompt}

        Provide a JSON response with this structure:
        {{
            "categories": [
                {{
                    "name": "Category Name",
                    "description": "Brief description of this category's focus",
                    "icon": "emoji-or-icon-name",
                    "color": "blue|green|purple|orange|red|yellow|pink",
                    "tasks": {{
                        "todo": [
                            {{
                                "title": "Clear task title",
                                "description": "Detailed description",
                                "priority": 1-10,
                                "reasoning": "Why this task matters and why it's in todo"
                            }}
                        ],
                        "doing": [
                            {{
                                "title": "Task currently in progress",
                                "description": "Detailed description",
                                "priority": 1-10,
                                "reasoning": "Why this task is actively being worked on"
                            }}
                        ],
                        "upcoming": [
                            {{
                                "title": "Future task",
                                "description": "Detailed description",
                                "priority": 1-10,
                                "reasoning": "Why this task is upcoming (dependencies, timing, etc.)"
                            }}
                        ]
                    }}
                }}
            ],
            "summary": "Brief summary of what you organized",
            "total_tasks": count,
            "suggested_next_steps": ["Immediate action items"]
        }}

        Guidelines:
        - Extract 5-20 actionable tasks total
        - Create 3-7 logical categories based on themes (e.g., Development, Design, Marketing, Research, etc.)
        - Assign statuses based on task nature:
          * "todo" - Tasks ready to start now, clear next steps
          * "doing" - Tasks that seem to be in progress or actively happening
          * "upcoming" - Tasks blocked by dependencies, future phases, or lower priority
        - Priority 1-10: 1-3 (low), 4-6 (medium), 7-8 (high), 9-10 (critical)
        - Be specific and actionable in task titles
        - Provide clear reasoning for status assignments
        """

        try:
            response = await self._generate_content(prompt)
            json_response = self._extract_json_from_response(response)
            result = json.loads(json_response)

            # Validate and enhance the response
            if "categories" not in result:
                raise ValueError("Invalid response: missing categories")

            # Ensure each category has all three status arrays
            for category in result["categories"]:
                if "tasks" not in category:
                    category["tasks"] = {}
                if "todo" not in category["tasks"]:
                    category["tasks"]["todo"] = []
                if "doing" not in category["tasks"]:
                    category["tasks"]["doing"] = []
                if "upcoming" not in category["tasks"]:
                    category["tasks"]["upcoming"] = []

                # Assign default icon if missing
                if "icon" not in category or not category["icon"]:
                    category["icon"] = self._get_default_icon(category["name"])

                # Assign default color if missing
                if "color" not in category or not category["color"]:
                    category["color"] = self._get_default_color(category["name"])

            return result

        except Exception as e:
            logger.error(f"Error organizing prompt: {str(e)}")
            # Fallback to basic organization
            return {
                "categories": [
                    {
                        "name": "General",
                        "description": "Tasks extracted from your input",
                        "icon": "📋",
                        "color": "blue",
                        "tasks": {
                            "todo": [
                                {
                                    "title": "Review your input",
                                    "description": messy_prompt[:200] + "..." if len(messy_prompt) > 200 else messy_prompt,
                                    "priority": 5,
                                    "reasoning": "AI organization failed - please manually organize"
                                }
                            ],
                            "doing": [],
                            "upcoming": []
                        }
                    }
                ],
                "summary": "AI organization encountered an error. Please manually organize your tasks.",
                "total_tasks": 1,
                "suggested_next_steps": ["Try breaking down your input into smaller chunks", "Be more specific with your goals"]
            }

    def _get_default_icon(self, category_name: str) -> str:
        """Get default icon based on category name."""
        category_lower = category_name.lower()
        icon_map = {
            "development": "💻",
            "dev": "💻",
            "code": "💻",
            "design": "🎨",
            "marketing": "📢",
            "research": "🔍",
            "testing": "🧪",
            "deployment": "🚀",
            "planning": "📋",
            "documentation": "📝",
            "learning": "📚",
            "infrastructure": "🏗️",
            "security": "🔒",
            "performance": "⚡",
        }
        for key, icon in icon_map.items():
            if key in category_lower:
                return icon
        return "📁"

    def _get_default_color(self, category_name: str) -> str:
        """Get default color based on category name."""
        category_lower = category_name.lower()
        color_map = {
            "development": "blue",
            "dev": "blue",
            "code": "blue",
            "design": "purple",
            "marketing": "orange",
            "research": "green",
            "testing": "yellow",
            "deployment": "red",
            "planning": "blue",
            "documentation": "gray",
            "learning": "pink",
        }
        for key, color in color_map.items():
            if key in category_lower:
                return color
        return "blue"


# Global AI service instance
ai_service = GeminiAIService()