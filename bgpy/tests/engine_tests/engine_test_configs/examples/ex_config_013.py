from frozendict import frozendict
from bgpy.enums import ASNs
from bgpy.tests.engine_tests.as_graph_infos import as_graph_info_000
from bgpy.tests.engine_tests.utils import EngineTestConfig

from bgpy.simulation_engine import (
    ROVSimplePolicy,
)
from bgpy.simulation_framework import (
    ScenarioConfig,
    PrefixHijack,
    preprocess_anns_funcs,
)


desc = (
    "Origin spoofing prefix hijack thwarting ROV\n"
    "This attack reaches more ASes than just the origin hijack"
)

ex_config_013 = EngineTestConfig(
    name="ex_013_origin_spoofing_hijack_rov_simple",
    desc=desc,
    scenario_config=ScenarioConfig(
        ScenarioCls=PrefixHijack,
        preprocess_anns_func=preprocess_anns_funcs.origin_spoofing_hijack,
        BasePolicyCls=ROVSimplePolicy,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict({}),
    ),
    as_graph_info=as_graph_info_000,
)
