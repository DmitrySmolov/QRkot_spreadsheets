from aiogoogle import Aiogoogle

from app.core.config import GoogleSettings, settings


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    service = await wrapper_services.discover(
        api_name=GoogleSettings.SPREADSHEETS_API_NAME,
        api_version=GoogleSettings.SPREADSHEETS_API_VERSION
    )
    spreadsheet_body = {
        'properties': {'title': GoogleSettings.SPREADSHEETS_TITLE,
                       'locale': GoogleSettings.SPREADSHEETS_LOCALE},
        'sheets': [GoogleSettings.SHEETS_PROPERTIES]
    }
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheet_id = response['spreadsheetId']
    return spreadsheet_id


async def set_user_permissions(
    spreadsheet_id: str,
    wrapper_services: Aiogoogle
) -> None:
    permissions_body = {
        'type': GoogleSettings.DRIVE_PERMISSION_TYPE,
        'role': GoogleSettings.DRIVE_PERMISSION_ROLE,
        'emailAddress': settings.email
    }
    service = await wrapper_services.discover(
        api_name=GoogleSettings.DRIVE_API_NAME,
        api_version=GoogleSettings.DRIVE_API_VERSION
    )
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields=GoogleSettings.DRIVE_PERMISSION_FIELDS
        )
    )


async def spreadsheets_update_value(
    spreadsheet_id: str,
    charity_projects: list[list[str, str, str]],
    wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover(
        api_name=GoogleSettings.SPREADSHEETS_API_NAME,
        api_version=GoogleSettings.SPREADSHEETS_API_VERSION
    )
    table_values = GoogleSettings.TABLE_HEADER + charity_projects
    update_body = {
        'majorDimension': GoogleSettings.TABLE_UPD_MAJ_DIMENSIONS,
        'values': table_values
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=GoogleSettings.TABLE_UPD_RANGE,
            valueInputOption=GoogleSettings.TABLE_UPD_VAL_INPUT_OPT,
            json=update_body
        )
    )
