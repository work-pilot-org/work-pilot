"""
IT Service client.

Provides a clean interface for interacting with the WorkPilot IT Service.
"""

from __future__ import annotations

from typing import Any
from uuid import UUID

from shared_infrastructure.core.config import settings
from infrastructure.integrations.base_client import BaseClient
from modules.it.schemas import (
    AccessRequestStatusUpdate,
    AssignAssetRequest,
    AssignDeviceRequest,
    AssignLicenseRequest,
    AssignTicketRequest,
    CompleteMaintenanceRequest,
    CreateAccessRequest,
    CreateAssetRequest,
    CreateDeviceRequest,
    CreateInstallationRequest,
    CreateInstallRequest,
    CreateLicenseRequest,
    CreateMaintenanceHistoryRequest,
    CreateMaintenanceRecord,
    CreateSoftwareRequest,
    CreateTicketRequest,
    UpdateAccessRequest,
    UpdateAssetRequest,
    UpdateDeviceRequest,
    UpdateLicenseRequest,
    UpdateMaintenanceRecord,
    UpdateSoftwareRequest,
    UpdateTicketRequest,
)


class ITClient:
    """
    Client responsible for communicating with the IT Service.
    """

    def __init__(self) -> None:
        self._client = BaseClient()
        self._base_url = settings.it_service_url

    # ==========================================================
    # Help Desk
    # ==========================================================

    async def create_ticket(
        self,
        payload: CreateTicketRequest,
        headers: dict[str, str] | None = None,
    ) -> Any:
        return await self._client.post(
            f"{self._base_url}/tickets",
            json=payload.model_dump(mode="json"),
            headers=headers,
        )

    async def list_tickets(
        self,
        headers: dict[str, str] | None = None,
    ) -> Any:
        return await self._client.get(
            f"{self._base_url}/tickets",
            headers=headers,
        )

    async def get_ticket(
        self,
        ticket_id: UUID,
        headers: dict[str, str] | None = None,
    ) -> Any:
        return await self._client.get(
            f"{self._base_url}/tickets/{ticket_id}",
            headers=headers,
        )

    async def update_ticket(
        self,
        ticket_id: UUID,
        payload: UpdateTicketRequest,
        headers: dict[str, str] | None = None,
    ) -> Any:
        return await self._client.patch(
            f"{self._base_url}/tickets/{ticket_id}",
            json=payload.model_dump(
                exclude_none=True,
                mode="json",
            ),
            headers=headers,
        )

    async def delete_ticket(
        self,
        ticket_id: UUID,
        headers: dict[str, str] | None = None,
    ) -> Any:
        return await self._client.delete(
            f"{self._base_url}/tickets/{ticket_id}",
            headers=headers,
        )

    async def assign_ticket(
        self,
        ticket_id: UUID,
        payload: AssignTicketRequest,
        headers: dict[str, str] | None = None,
    ) -> Any:
        return await self._client.patch(
            f"{self._base_url}/tickets/{ticket_id}/assign",
            json=payload.model_dump(mode="json"),
            headers=headers,
        )

    async def change_ticket_status(
        self,
        ticket_id: UUID,
        payload: dict[str, Any],
        headers: dict[str, str] | None = None,
    ) -> Any:
        return await self._client.patch(
            f"{self._base_url}/tickets/{ticket_id}/status",
            json=payload,
            headers=headers,
        )

    # ==========================================================
    # Assets
    # ==========================================================

    async def create_asset(
        self,
        payload: CreateAssetRequest,
        headers: dict[str, str] | None = None,
    ) -> Any:
        return await self._client.post(
            f"{self._base_url}/assets",
            json=payload.model_dump(mode="json"),
            headers=headers,
        )

    async def list_assets(
        self,
        category: str | None = None,
        status: str | None = None,
        assigned_to: UUID | None = None,
        search: str | None = None,
        skip: int = 0,
        limit: int = 20,
        headers: dict[str, str] | None = None,
    ) -> Any:
        params = {
            "category": category,
            "status": status,
            "assigned_to": str(assigned_to) if assigned_to else None,
            "search": search,
            "skip": skip,
            "limit": limit,
        }

        params = {k: v for k, v in params.items() if v is not None}

        return await self._client.get(
            f"{self._base_url}/assets",
            params=params,
            headers=headers,
        )

    async def get_asset(
        self,
        asset_id: UUID,
        headers: dict[str, str] | None = None,
    ) -> Any:
        return await self._client.get(
            f"{self._base_url}/assets/{asset_id}",
            headers=headers,
        )

    async def update_asset(
        self,
        asset_id: UUID,
        payload: UpdateAssetRequest,
        headers: dict[str, str] | None = None,
    ) -> Any:
        return await self._client.put(
            f"{self._base_url}/assets/{asset_id}",
            json=payload.model_dump(
                exclude_none=True,
                mode="json",
            ),
            headers=headers,
        )

    async def delete_asset(
        self,
        asset_id: UUID,
        headers: dict[str, str] | None = None,
    ) -> Any:
        return await self._client.delete(
            f"{self._base_url}/assets/{asset_id}",
            headers=headers,
        )

    async def assign_asset(
        self,
        asset_id: UUID,
        payload: AssignAssetRequest,
        headers: dict[str, str] | None = None,
    ) -> Any:
        return await self._client.post(
            f"{self._base_url}/assets/{asset_id}/assign",
            json=payload.model_dump(mode="json"),
            headers=headers,
        )

    async def return_asset(
        self,
        asset_id: UUID,
        headers: dict[str, str] | None = None,
    ) -> Any:
        return await self._client.post(
            f"{self._base_url}/assets/{asset_id}/return",
            headers=headers,
        )
        
    # ==========================================================
    # Devices
    # ==========================================================

    async def create_device(
        self,
        payload: CreateDeviceRequest,
        headers: dict[str, str] | None = None,
    ):
        return await self._client.post(
            f"{self._base_url}/devices",
            json=payload.model_dump(mode="json"),
            headers=headers,
        )


    async def list_devices(
        self,
        headers: dict[str, str] | None = None,
    ):
        return await self._client.get(
            f"{self._base_url}/devices",
            headers=headers,
        )


    async def get_device(
        self,
        device_id: UUID,
        headers: dict[str, str] | None = None,
    ):
        return await self._client.get(
            f"{self._base_url}/devices/{device_id}",
            headers=headers,
        )


    async def update_device(
        self,
        device_id: UUID,
        payload: UpdateDeviceRequest,
        headers: dict[str, str] | None = None,
    ):
        return await self._client.put(
            f"{self._base_url}/devices/{device_id}",
            json=payload.model_dump(
                exclude_none=True,
                mode="json",
            ),
            headers=headers,
        )


    async def delete_device(
        self,
        device_id: UUID,
        headers: dict[str, str] | None = None,
    ):
        return await self._client.delete(
            f"{self._base_url}/devices/{device_id}",
            headers=headers,
        )


    async def assign_device(
        self,
        device_id: UUID,
        payload: AssignDeviceRequest,
        headers: dict[str, str] | None = None,
    ):
        return await self._client.post(
            f"{self._base_url}/devices/{device_id}/assign",
            json=payload.model_dump(mode="json"),
            headers=headers,
        )


    async def return_device(
        self,
        device_id: UUID,
        headers: dict[str, str] | None = None,
    ):
        return await self._client.post(
            f"{self._base_url}/devices/{device_id}/return",
            headers=headers,
        )


    async def add_maintenance_log(
        self,
        device_id: UUID,
        payload: CreateMaintenanceHistoryRequest,
        headers: dict[str, str] | None = None,
    ):
        return await self._client.post(
            f"{self._base_url}/devices/{device_id}/maintenance",
            json=payload.model_dump(mode="json"),
            headers=headers,
        )


    async def get_maintenance_history(
        self,
        device_id: UUID,
        headers: dict[str, str] | None = None,
    ):
        return await self._client.get(
            f"{self._base_url}/devices/{device_id}/maintenance",
            headers=headers,
        )
        


    # ==========================================================
    # Software
    # ==========================================================

    async def create_software(
        self,
        payload: CreateSoftwareRequest,
        headers: dict[str, str] | None = None,
    ):
        return await self._client.post(
            f"{self._base_url}/software",
            json=payload.model_dump(mode="json"),
            headers=headers,
        )


    async def list_software(
        self,
        headers: dict[str, str] | None = None,
    ):
        return await self._client.get(
            f"{self._base_url}/software",
            headers=headers,
        )


    async def get_software(
        self,
        software_id: UUID,
        headers: dict[str, str] | None = None,
    ):
        return await self._client.get(
            f"{self._base_url}/software/{software_id}",
            headers=headers,
        )


    async def update_software(
        self,
        software_id: UUID,
        payload: UpdateSoftwareRequest,
        headers: dict[str, str] | None = None,
    ):
        return await self._client.put(
            f"{self._base_url}/software/{software_id}",
            json=payload.model_dump(exclude_none=True, mode="json"),
            headers=headers,
        )


    async def delete_software(
        self,
        software_id: UUID,
        headers: dict[str, str] | None = None,
    ):
        return await self._client.delete(
            f"{self._base_url}/software/{software_id}",
            headers=headers,
        )


    async def install_software(
        self,
        software_id: UUID,
        payload: CreateInstallRequest,
        headers: dict[str, str] | None = None,
    ):
        return await self._client.post(
            f"{self._base_url}/software/{software_id}/install",
            json=payload.model_dump(mode="json"),
            headers=headers,
        )


    async def uninstall_software(
        self,
        install_id: UUID,
        headers: dict[str, str] | None = None,
    ):
        return await self._client.delete(
            f"{self._base_url}/software/installations/{install_id}",
            headers=headers,
        )


    async def list_device_installations(
        self,
        device_id: UUID,
        headers: dict[str, str] | None = None,
    ):
        return await self._client.get(
            f"{self._base_url}/software/installations/device/{device_id}",
            headers=headers,
        )


    async def list_user_installations(
        self,
        user_id: UUID,
        headers: dict[str, str] | None = None,
    ):
        return await self._client.get(
            f"{self._base_url}/software/installations/user/{user_id}",
            headers=headers,
        )


    async def create_installation_request(
        self,
        payload: CreateInstallationRequest,
        headers: dict[str, str] | None = None,
    ):
        return await self._client.post(
            f"{self._base_url}/software/requests",
            json=payload.model_dump(mode="json"),
            headers=headers,
        )


    async def list_installation_requests(
        self,
        headers: dict[str, str] | None = None,
    ):
        return await self._client.get(
            f"{self._base_url}/software/requests",
            headers=headers,
        )


    async def get_installation_request(
        self,
        request_id: UUID,
        headers: dict[str, str] | None = None,
    ):
        return await self._client.get(
            f"{self._base_url}/software/requests/{request_id}",
            headers=headers,
        )


# ==========================================================
# Licenses
# ==========================================================

    async def create_license(
        self,
        payload: CreateLicenseRequest,
        headers: dict[str, str] | None = None,
    ):
        return await self._client.post(
            f"{self._base_url}/licenses",
            json=payload.model_dump(mode="json"),
            headers=headers,
        )


    async def list_licenses(
        self,
        headers: dict[str, str] | None = None,
    ):
        return await self._client.get(
            f"{self._base_url}/licenses",
            headers=headers,
        )


    async def get_license(
        self,
        license_id: UUID,
        headers: dict[str, str] | None = None,
    ):
        return await self._client.get(
            f"{self._base_url}/licenses/{license_id}",
            headers=headers,
        )


    async def update_license(
        self,
        license_id: UUID,
        payload: UpdateLicenseRequest,
        headers: dict[str, str] | None = None,
    ):
        return await self._client.put(
            f"{self._base_url}/licenses/{license_id}",
            json=payload.model_dump(
                exclude_none=True,
                mode="json",
            ),
            headers=headers,
        )


    async def delete_license(
        self,
        license_id: UUID,
        headers: dict[str, str] | None = None,
    ):
        return await self._client.delete(
            f"{self._base_url}/licenses/{license_id}",
            headers=headers,
        )


    async def assign_license(
        self,
        license_id: UUID,
        payload: AssignLicenseRequest,
        headers: dict[str, str] | None = None,
    ):
        return await self._client.post(
            f"{self._base_url}/licenses/{license_id}/assign",
            json=payload.model_dump(mode="json"),
            headers=headers,
        )


    async def return_license(
        self,
        license_id: UUID,
        headers: dict[str, str] | None = None,
    ):
        return await self._client.post(
            f"{self._base_url}/licenses/{license_id}/return",
            headers=headers,
        )


    async def list_license_assignments(
        self,
        license_id: UUID,
        headers: dict[str, str] | None = None,
    ):
        return await self._client.get(
            f"{self._base_url}/licenses/{license_id}/assignments",
            headers=headers,
        )
        
    # ==========================================================
    # Access
    # ==========================================================

    async def create_access_request(
        self,
        payload: CreateAccessRequest,
        headers: dict[str, str] | None = None,
    ):
        return await self._client.post(
            f"{self._base_url}/access",
            json=payload.model_dump(mode="json"),
            headers=headers,
        )


    async def list_access_requests(
        self,
        headers: dict[str, str] | None = None,
    ):
        return await self._client.get(
            f"{self._base_url}/access",
            headers=headers,
        )


    async def get_access_request(
        self,
        request_id: UUID,
        headers: dict[str, str] | None = None,
    ):
        return await self._client.get(
            f"{self._base_url}/access/{request_id}",
            headers=headers,
        )


    async def update_access_request(
        self,
        request_id: UUID,
        payload: UpdateAccessRequest,
        headers: dict[str, str] | None = None,
    ):
        return await self._client.put(
            f"{self._base_url}/access/{request_id}",
            json=payload.model_dump(
                exclude_none=True,
                mode="json",
            ),
            headers=headers,
        )


    async def update_access_status(
        self,
        request_id: UUID,
        payload: AccessRequestStatusUpdate,
        headers: dict[str, str] | None = None,
    ):
        return await self._client.patch(
            f"{self._base_url}/access/{request_id}/status",
            json=payload.model_dump(mode="json"),
            headers=headers,
        )


    async def delete_access_request(
        self,
        request_id: UUID,
        headers: dict[str, str] | None = None,
    ):
        return await self._client.delete(
            f"{self._base_url}/access/{request_id}",
            headers=headers,
        )
        
    
    # ==========================================================
    # Maintenance
    # ==========================================================

    async def create_maintenance_record(
        self,
        payload: CreateMaintenanceRecord,
        headers: dict[str, str] | None = None,
    ):
        return await self._client.post(
            f"{self._base_url}/maintenance",
            json=payload.model_dump(mode="json"),
            headers=headers,
        )


    async def list_maintenance_records(
        self,
        headers: dict[str, str] | None = None,
    ):
        return await self._client.get(
            f"{self._base_url}/maintenance",
            headers=headers,
        )


    async def get_maintenance_record(
        self,
        maintenance_id: UUID,
        headers: dict[str, str] | None = None,
    ):
        return await self._client.get(
            f"{self._base_url}/maintenance/{maintenance_id}",
            headers=headers,
        )


    async def update_maintenance_record(
        self,
        maintenance_id: UUID,
        payload: UpdateMaintenanceRecord,
        headers: dict[str, str] | None = None,
    ):
        return await self._client.put(
            f"{self._base_url}/maintenance/{maintenance_id}",
            json=payload.model_dump(
                exclude_none=True,
                mode="json",
            ),
            headers=headers,
        )


    async def delete_maintenance_record(
        self,
        maintenance_id: UUID,
        headers: dict[str, str] | None = None,
    ):
        return await self._client.delete(
            f"{self._base_url}/maintenance/{maintenance_id}",
            headers=headers,
        )


    async def complete_maintenance(
        self,
        maintenance_id: UUID,
        payload: CompleteMaintenanceRequest,
        headers: dict[str, str] | None = None,
    ):
        return await self._client.post(
            f"{self._base_url}/maintenance/{maintenance_id}/complete",
            json=payload.model_dump(mode="json"),
            headers=headers,
        )


    async def list_device_maintenance(
        self,
        device_id: UUID,
        headers: dict[str, str] | None = None,
    ):
        return await self._client.get(
            f"{self._base_url}/maintenance/device/{device_id}",
            headers=headers,
        )    

it_client = ITClient()