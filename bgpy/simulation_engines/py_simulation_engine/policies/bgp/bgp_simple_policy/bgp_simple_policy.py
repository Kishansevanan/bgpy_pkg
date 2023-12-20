from typing import Callable, Optional, TYPE_CHECKING
from weakref import CallableProxyType

# Propagation functionality
from .propagate_funcs import propagate_to_providers
from .propagate_funcs import propagate_to_customers
from .propagate_funcs import propagate_to_peers
from .propagate_funcs import _propagate
from .propagate_funcs import _policy_propagate
from .propagate_funcs import _process_outgoing_ann
from .propagate_funcs import _prev_sent

# Process incoming announcements
from .process_incoming_funcs import receive_ann
from .process_incoming_funcs import process_incoming_anns
from .process_incoming_funcs import _valid_ann
from .process_incoming_funcs import _copy_and_process
from .process_incoming_funcs import _reset_q

# Gao rexford functions
from .gao_rexford import _new_ann_better
from .gao_rexford import _new_rel_better
from .gao_rexford import _new_as_path_shorter
from .gao_rexford import _new_wins_ties

from bgpy.enums import Relationships, GaoRexfordPref
from bgpy.simulation_engines.base import Policy
from bgpy.simulation_engines.py_simulation_engine.ann_containers import LocalRIB
from bgpy.simulation_engines.py_simulation_engine.ann_containers import RecvQueue
from bgpy.simulation_engines.py_simulation_engine.announcement import (
    Announcement as Ann,
)

if TYPE_CHECKING:
    from bgpy.as_graphs import AS


GAO_REXFORD_FUNC = Callable[
    [Ann, bool, Relationships, Ann, bool, Relationships], GaoRexfordPref
]


class BGPSimplePolicy(Policy):
    name: str = "BGP Simple"

    def __init__(
        self,
        _local_rib: Optional[LocalRIB] = None,
        _recv_q: Optional[RecvQueue] = None,
        as_: Optional["AS"] = None,
    ):
        """Add local rib and data structures here

        This way they can be easily cleared later without having to redo
        the graph

        This is also useful for regenerating an AS from YAML
        """

        self._local_rib = _local_rib if _local_rib else LocalRIB()
        self._recv_q = _recv_q if _recv_q else RecvQueue()
        # This gets set within the AS class so it's fine
        self.as_: CallableProxyType["AS"] = as_  # type: ignore

    def __eq__(self, other) -> bool:
        raise NotImplementedError(
            "Not sure what this was used for, but it needs refactoring "
            "since we've separated policies and AS classes this no longer works"
        )
        # if isinstance(other, BGPSimplePolicy):
        #     # Ugh this is bad
        #     for attr in [x for x in self.__dict__ if x not in self.base_slots]:
        #         if not hasattr(self, attr) == hasattr(other, attr):
        #             return False
        #         elif hasattr(self, attr):
        #             if not getattr(self, attr) == getattr(other, attr):
        #                 return False
        #     return True
        # else:
        #     return NotImplemented

    @property
    def _gao_rexford_funcs(self) -> tuple[GAO_REXFORD_FUNC, ...]:
        return (
            self._new_rel_better,
            self._new_as_path_shorter,
            self._new_wins_ties,
        )

    # Propagation functionality
    propagate_to_providers = propagate_to_providers
    propagate_to_customers = propagate_to_customers
    propagate_to_peers = propagate_to_peers
    _propagate = _propagate
    _policy_propagate = _policy_propagate
    _process_outgoing_ann = _process_outgoing_ann
    _prev_sent = _prev_sent

    # Process incoming announcements
    receive_ann = receive_ann
    process_incoming_anns = process_incoming_anns
    _valid_ann = _valid_ann
    _copy_and_process = _copy_and_process
    _reset_q = _reset_q

    # Gao rexford functions
    _new_ann_better = _new_ann_better
    _new_rel_better = _new_rel_better
    _new_as_path_shorter = _new_as_path_shorter
    _new_wins_ties = _new_wins_ties

    ##############
    # Yaml funcs #
    ##############

    def __to_yaml_dict__(self):
        """This optional method is called when you call yaml.dump()"""

        return {"_local_rib": self._local_rib, "_recv_q": self._recv_q}

    @classmethod
    def __from_yaml_dict__(cls, dct, yaml_tag):
        """This optional method is called when you call yaml.load()"""

        # We can type ignore here because we add this in the AS class
        # Only way to do it, otherwise it's a circular reference
        return cls(**dct)  # type: ignore