from idkollen_client.endpoints.bankid_se import AsyncBankIdSeEndpoint, BankIdSeEndpoint
from idkollen_client.endpoints.bankid_no import AsyncBankIdNoEndpoint, BankIdNoEndpoint
from idkollen_client.endpoints.freja import AsyncFrejaEndpoint, FrejaEndpoint
from idkollen_client.endpoints.mitid import AsyncMitIdEndpoint, MitIdEndpoint
from idkollen_client.endpoints.ftn import AsyncFtnEndpoint, FtnEndpoint
from idkollen_client.endpoints.vipps import AsyncVippsEndpoint, VippsEndpoint
from idkollen_client.endpoints.document import AsyncDocumentEndpoint, DocumentEndpoint

__all__ = [
    "AsyncBankIdSeEndpoint", "BankIdSeEndpoint",
    "AsyncBankIdNoEndpoint", "BankIdNoEndpoint",
    "AsyncFrejaEndpoint", "FrejaEndpoint",
    "AsyncMitIdEndpoint", "MitIdEndpoint",
    "AsyncFtnEndpoint", "FtnEndpoint",
    "AsyncVippsEndpoint", "VippsEndpoint",
    "AsyncDocumentEndpoint", "DocumentEndpoint",
]
