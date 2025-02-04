from rpc.lrpc_reward_api import LRpcRewardApiImpl
from rpc.prpc_reward_api import PRpcRewardApiImpl
from rpc.rpc_block_api import RpcBlockApiImpl
from rpc.rpc_reward_api import RpcRewardApiImpl
from dunscan.dunscan import DunScanMirrorSelector
from dunscan.dunscan_block_api import DunScanBlockApiImpl
from dunscan.dunscan_reward_api import DunScanRewardApiImpl


class ProviderFactory:
    URL = "{}.tzbeta.net/"
    URL = "{}.tezrpc.me/"
    url_prefixes = {"MAINNET": "rpc", "ALPHANET": "rpcalpha", "ZERONET": "rpczero"}
    url_prefixes = {"MAINNET": "mainnet", "ALPHANET": "alphanet", "ZERONET": "zeronet"}

    def __init__(self, provider, verbose=False):
        self.provider = provider
        self.mirror_selector = None
        self.verbose = verbose

    def newRewardApi(self, network_config, baking_address, wllt_clnt_mngr, node_url):
        if self.provider == 'rpc':
            return LRpcRewardApiImpl(network_config, baking_address, node_url, wllt_clnt_mngr, verbose=self.verbose)
        elif self.provider == 'prpc':
            url_prefix = self.url_prefixes[network_config['NAME']]
            return PRpcRewardApiImpl(network_config,  baking_address, self.URL.format(url_prefix), verbose=self.verbose)
        elif self.provider == 'dunscan':
            if not self.mirror_selector:
                self.init_mirror_selector(network_config)
            return DunScanRewardApiImpl(network_config, baking_address, self.mirror_selector, verbose=self.verbose)

        raise Exception("No supported reward data provider : {}".format(self.provider))

    def init_mirror_selector(self, network_config):
        self.mirror_selector = DunScanMirrorSelector(network_config)
        self.mirror_selector.initialize()

    def newBlockApi(self, network_config, wllt_clnt_mngr, node_url):
        if self.provider == 'rpc' or self.provider == 'prpc':
            return RpcBlockApiImpl(network_config, wllt_clnt_mngr, node_url)
        elif self.provider == 'dunscan':
            if not self.mirror_selector:
                self.init_mirror_selector(network_config)
            return DunScanBlockApiImpl(network_config,self.mirror_selector)

        raise Exception("No supported reward data provider : {}".format(self.provider))
