import httpx
import asyncio

URL_BASE = "http://127.0.0.1:5000"
URL_BASE_API = f"{URL_BASE}/api/v1"

async def get_equipos():
    url_equipos = f"{URL_BASE_API}/equipos/"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url_equipos)
            response.raise_for_status()
            equipos = response.json()
            print("Lista de equipos recuperada con éxito.")
            return equipos
        except httpx.HTTPStatusError as exc:
            print(f"Error del servidor ({exc.response.status_code}) al pedir equipos.")
        except httpx.RequestError as exc:
            print(f"Error de red conectando a {exc.request.url}")

async def get_equipo_by_id(equipo_id: int):
    url_equipo = f"{URL_BASE_API}/equipos/{equipo_id}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url_equipo)
            response.raise_for_status()
            equipo = response.json()
            print(f"Equipo {equipo_id} recuperado con éxito.")
            return equipo
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 404:
                print(f"El equipo con ID {equipo_id} no existe en la base de datos.")
            else:
                print(f"Error HTTP {exc.response.status_code}.")
        except httpx.RequestError as exc:
            print(f"Error de red: {exc}")

async def create_equipo(new_equipo: dict):
    url_equipos = f"{URL_BASE_API}/equipos/"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url_equipos, json=new_equipo)
            response.raise_for_status()
            equipo = response.json()
            print("Nuevo equipo creado correctamente.")
            return equipo
        except httpx.HTTPStatusError as exc:
            print(f"Error al crear equipo. El servidor rechazó los datos ({exc.response.status_code}).")
            print(f"Detalle del servidor: {exc.response.json()}")
        except httpx.RequestError as exc:
            print(f"Error de red: {exc}")

async def delete_equipo(equipo_id: int):
    url_equipo = f"{URL_BASE_API}/equipos/{equipo_id}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.delete(url_equipo)
            response.raise_for_status()
            print(f"Equipo con ID {equipo_id} eliminado correctamente.")
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 404:
                print(f"El equipo con ID {equipo_id} no existe para borrarlo.")
            else:
                print(f"Error HTTP {exc.response.status_code} al borrar.")
        except httpx.RequestError as exc:
            print(f"🔌 Error de red: {exc}")

async def main():
    print("--- Obteniendo todos los equipos ---")
    await get_equipos()

    print("\n--- Creando un equipo nuevo ---")
    nuevo_equipo = {
        "nombre": "CP Irlandesas",
        "ciudad": "Sevilla",
        "ccaa": "Andalucia",
        "fundacion": 2009,
        "pabellon": "El Poli",
        "capacidad": 11500
    }
    equipo_creado = await create_equipo(nuevo_equipo)

    print("\n--- Obteniendo el equipo recién creado ---")
    if equipo_creado and "id" in equipo_creado:
        await get_equipo_by_id(equipo_creado["id"])

    print("\n--- Borrando el equipo recién creado ---")
    if equipo_creado and "id" in equipo_creado:
        await delete_equipo(equipo_creado["id"])

    print("\n--- Forzando un error (equipo que no existe) ---")
    await get_equipo_by_id(9999)

if __name__ == '__main__':
    asyncio.run(main())