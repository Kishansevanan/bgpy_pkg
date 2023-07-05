from bgp_simulator_pkg.enums import Plane

from .metric import Metric


class MetricSubclassFactory:
    def __init__(self) -> list[type[Metric]]:
        """Generates a list of all metric subclasses to use"""

        self.metric_subclasses: list[type[Metric]] = list()

        for i, args in enumerate(self._all_metric_combos()):
            class_dict = {
                "label_prefix": self._get_label_prefix_func(*args),
                "_add_numerator": self._get_add_numerator_func(*args),
                "_add_denominator": self._get_add_denominator_func(*args),
            }
            self.metric_subclasses.append(type(f"Metric{i}", (Metric,), class_dict))

    def get_metric_subclasses(self) -> list[Metric]:
        """Returns a list of all combinations of metric objects"""

        return [Cls() for Cls in self.metric_subclasses]

    def _all_metric_combos(self):
        """Returns all possible metric combos"""

        for plane in Plane:
            for as_group in ASGroups:
                for outcome in [x for x in Outcomes if x != Outcomes.UNDETERMINED]:
                    yield plane, as_group, outcome

#######################
# Function Generators #
#######################

    def _get_label_prefix_func(
        self,
        plane: Plane,
        as_group: ASGroup,
        outcome: Outcome
    ) -> Callable:

        return property(lambda self: f"{plane.value}_{as_group.value}_{outcome.value}")

    def _get_add_numerator_func(
        self,
        plane: Plane,
        as_group: ASGroup,
        outcome: Outcome
    ) -> Callable:
        """Returns the _add_numerator func"""

        def _add_numerator(
            self,
            *,
            as_obj: AS,
            engine: SimulationEngine,
            scenario: Scenario,
            ctrl_plane_outcome: Outcomes,
            data_plane_outcome: Outcomes,
        ):
            """Adds result to numerator"""

            result = data_plane_outcome if Plane.DATA else ctrl_plane_outcome
            if as_obj in engine.as_groups[as_group.value] and outcome == result:
                self._numerators[as_obj.__class__] += 1

        return _add_numerator

    def _get_add_denominator_func(
        self,
        plane: Plane,
        as_group: ASGroup,
        outcome: Outcome
    ) -> Callable:
        """Returns the _add_denominator_func"""

         def _add_denominator(
            self,
            *,
            as_obj: AS,
            engine: SimulationEngine,
            scenario: Scenario,
            ctrl_plane_outcome: Outcomes,
            data_plane_outcome: Outcomes,
        ) -> None:
            """Adds result to the denominator"""

            if as_obj in engine.as_groups[as_group.value:
                self._denominators[as_obj.__class__] += 1

        return _add_denominator