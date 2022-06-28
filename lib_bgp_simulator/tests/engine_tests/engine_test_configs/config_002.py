from ..graphs import Graph001
from ..utils import EngineTestConfig

from ....engine import BGPAS
from ....enums import ASNs
from ....scenarios import SubprefixHijack


class Config002(EngineTestConfig):
    """Contains config options to run a test"""

    name = "002"
    desc = "BGP hidden hijack"
    scenario = SubprefixHijack(attacker_asn=ASNs.ATTACKER.value,
                               victim_asn=ASNs.VICTIM.value,
                               AdoptASCls=None,
                               BaseASCls=BGPAS)
    graph = Graph001()
    non_default_as_cls_dict = dict()
    propagation_rounds = 1
