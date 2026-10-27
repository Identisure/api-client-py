from identisure_client.endpoints.bankid_se import AsyncBankIdSeEndpoint, BankIdSeEndpoint
from identisure_client.endpoints.bankid_no import AsyncBankIdNoEndpoint, BankIdNoEndpoint
from identisure_client.endpoints.freja import AsyncFrejaEndpoint, FrejaEndpoint
from identisure_client.endpoints.mitid import AsyncMitIdEndpoint, MitIdEndpoint
from identisure_client.endpoints.ftn import AsyncFtnEndpoint, FtnEndpoint
from identisure_client.endpoints.vipps import AsyncVippsEndpoint, VippsEndpoint
from identisure_client.endpoints.document import AsyncDocumentEndpoint, DocumentEndpoint

__all__ = [
    "AsyncBankIdSeEndpoint", "BankIdSeEndpoint",
    "AsyncBankIdNoEndpoint", "BankIdNoEndpoint",
    "AsyncFrejaEndpoint", "FrejaEndpoint",
    "AsyncMitIdEndpoint", "MitIdEndpoint",
    "AsyncFtnEndpoint", "FtnEndpoint",
    "AsyncVippsEndpoint", "VippsEndpoint",
    "AsyncDocumentEndpoint", "DocumentEndpoint",
]
