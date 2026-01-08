import random

# Danh sach cac lua chon hop le (tieng Viet khong dau)
CHOICES = ["keo", "bua", "bao"]


def play_game(client_choice: str) -> dict:
    """
    Ham xu ly game Keo - Bua - Bao

    :param client_choice: lua chon tu client (keo / bua / bao)
    :return: dictionary chua ket qua game
    """

    client_choice = client_choice.lower()

    # Kiem tra lua chon hop le
    if client_choice not in CHOICES:
        return {
            "status": "error",
            "message": "Lua chon khong hop le. Hay chon keo, bua hoac bao."
        }

    # Server chon ngau nhien
    server_choice = random.choice(CHOICES)

    # So sanh ket qua
    if client_choice == server_choice:
        result = "hoa"
    elif (
        (client_choice == "keo" and server_choice == "bao") or
        (client_choice == "bua" and server_choice == "keo") or
        (client_choice == "bao" and server_choice == "bua")
    ):
        result = "thang"
    else:
        result = "thua"

    return {
        "status": "ok",
        "lua_chon_client": client_choice,
        "lua_chon_server": server_choice,
        "ket_qua": result
    }
