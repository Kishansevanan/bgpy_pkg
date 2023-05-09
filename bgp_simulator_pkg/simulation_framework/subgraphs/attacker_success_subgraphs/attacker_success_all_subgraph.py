from .attacker_success_subgraph import AttackerSuccessSubgraph
from ....enums import Outcomes
from ...scenarios import ScenarioTrial


class AttackerSuccessAllSubgraph(AttackerSuccessSubgraph):
    """A graph for attacker success for etc ASes that adopt"""

    name: str = "attacker_success_all"

    def _get_subgraph_key(self, scenario: ScenarioTrial, *args) -> str:
        """Returns the key to be used in shared_data on the subgraph"""

        return f"all_{Outcomes.ATTACKER_SUCCESS.name}_perc"
