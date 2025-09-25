from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

@CrewBase
class Sp():
    """Sp crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def visionary(self) -> Agent:
        return Agent(
            config=self.agents_config['visionary'],
            verbose=True
        )

    @agent
    def financial_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['financial_analyst'],
            verbose=True
        )

    @agent
    def engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['engineer'],
            verbose=True
        )

    @task
    def pitch_task(self) -> Task:
        return Task(
            config=self.tasks_config['pitch_task'],
            agent=self.visionary(),
        )

    @task
    def financial_task(self) -> Task:
        return Task(
            config=self.tasks_config['financial_task'],
            agent=self.financial_analyst(),
        )

    @task
    def engineering_task(self) -> Task:
        return Task(
            config=self.tasks_config['engineering_task'],
            agent=self.engineer(),
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Sp crew"""

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )

@CrewBase
class JurySp:
    """ Jury crew """

    @agent
    def jury(self) -> Agent:
        return Agent(
            config=self.agents_config['jury'],
            verbose=True
        )

    @task
    def evaluation_task(self) -> Task:
        cfg = self.tasks_config['evaluation_task'].copy()
        cfg.pop("agent", None)  # avoid CrewBase trying to resolve other agents
        return Task(config=cfg, agent=self.jury())

    @crew
    def crew(self) -> Crew:
        """Evaluates the variations"""

        return Crew(
            agents=[self.jury()],
            tasks=[self.evaluation_task()],
            process=Process.sequential,
            verbose=True,
        )