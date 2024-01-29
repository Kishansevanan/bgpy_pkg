from frozendict import frozendict
from bgpy.enums import ASNs
from bgpy.tests.engine_tests.as_graph_infos import as_graph_info_000
from bgpy.tests.engine_tests.utils import EngineTestConfig

from bgpy.simulation_engine import BGPSimplePolicy, PathendSimplePolicy
from bgpy.simulation_framework import (
    ScenarioConfig,
    AccidentalRouteLeak,
    preprocess_anns_funcs,
)


desc = (
    "accidental route leak against pathend simple\n"
    "Pathend checks the end of the path for valid providers\n"
    "so anything beyond the third AS is not protected"
)

ex_config_020 = EngineTestConfig(
    name="ex_020_route_leak_pathend_simple",
    desc=desc,
    propagation_rounds=2,  # Required for route leaks
    scenario_config=ScenarioConfig(
        ScenarioCls=AccidentalRouteLeak,
        preprocess_anns_func=preprocess_anns_funcs.noop,
        BasePolicyCls=BGPSimplePolicy,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict(
            {
                1: PathendSimplePolicy,
                ASNs.VICTIM.value: PathendSimplePolicy,
            }
        ),
    ),
    as_graph_info=as_graph_info_000,
)