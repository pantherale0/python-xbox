from typing import ClassVar

from pythonxbox.api.provider.account.models import (
    ChangeGamertagResult,
    ClaimGamertagResult,
    FamilyGroupResponse,
    FamilyMemberSettings,
)
from pythonxbox.api.provider.baseprovider import BaseProvider


class AccountProvider(BaseProvider):
    BASE_URL_USER_MGT = "https://user.mgt.xboxlive.com"
    BASE_URL_ACCOUNT = "https://accounts.xboxlive.com"

    HEADERS_USER_MGT: ClassVar = {"x-xbl-contract-version": "1"}
    HEADERS_ACCOUNT: ClassVar = {"x-xbl-contract-version": "2"}
    HEADERS_FAMILY: ClassVar = {"x-xbl-contract-version": "6"}

    async def claim_gamertag(
        self, xuid: str, gamertag: str, **kwargs
    ) -> ClaimGamertagResult:
        """
        Claim gamertag

        XLE error codes:
            400 - Bad API request
            401 - Unauthorized
            409 - Gamertag unavailable
            429 - Too many requests
            200 - Gamertag available

        Args:
            xuid (int): Your xuid as integer
            gamertag (str): Desired gamertag

        Returns: ClaimGamertagResult
        """
        url = self.BASE_URL_USER_MGT + "/gamertags/reserve"
        post_data = {"Gamertag": gamertag, "ReservationId": str(xuid)}
        resp = await self.client.session.post(
            url, json=post_data, headers=self.HEADERS_USER_MGT, **kwargs
        )
        try:
            return ClaimGamertagResult(resp.status_code)
        except ValueError:
            resp.raise_for_status()

    async def change_gamertag(
        self, xuid: str, gamertag: str, preview: bool = False, **kwargs
    ) -> ChangeGamertagResult:
        """
        Change your gamertag.

        XLE error codes:
            200 - success
            1020 - No free gamertag changes available

        Args:
            xuid (int): Your Xuid as integer
            gamertag (str): Desired gamertag name
            preview (bool): Preview the change

        Returns: ChangeGamertagResult
        """
        url = self.BASE_URL_ACCOUNT + "/users/current/profile/gamertag"
        post_data = {
            "gamertag": gamertag,
            "preview": preview,
            "reservationId": int(xuid),
        }
        resp = await self.client.session.post(
            url, json=post_data, headers=self.HEADERS_ACCOUNT, **kwargs
        )
        try:
            return ChangeGamertagResult(resp.status_code)
        except ValueError:
            resp.raise_for_status()

    async def get_family_group(
        self, xuid: str, **kwargs
    ) -> FamilyGroupResponse:
        """
        Get members in your family group.
        

        Args:
            xuid (int): Your Xuid as integer
        
        Returns: FamilyGroupResponse
        """
        url = self.BASE_URL_ACCOUNT + f"/family/memberXuid({xuid})"
        resp = await self.client.session.get(
            url, headers=self.HEADERS_FAMILY, **kwargs
        )
        resp.raise_for_status()
        return FamilyGroupResponse(**resp.json())

    async def get_family_member(
        self, xuid: str, user_id: str, **kwargs
    ) -> FamilyMemberSettings:
        """
        Get a single member of the family group.
        
        Args:
            xuid (int): Your Xuid as integer
            user_id (guid): Individual ID of the member to return.
        
        Returns: FamilyMemberSettings
        """
        url = self.BASE_URL_ACCOUNT + f"/family/memberXuid({xuid})/user/{user_id}"
        resp = await self.client.session.get(
            url, headers=self.HEADERS_FAMILY, **kwargs
        )
        resp.raise_for_status()
        return FamilyMemberSettings(**resp.json())
