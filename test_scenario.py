import requests

BASE_URL = "http://localhost:8000"

def main():
    # 1) Приглашение на регистрацию как прорабу
    role_payload = {"role_id": "prorab", "email": "trofimov.mat@yandex.ru"}
    r1 = requests.post(f"{BASE_URL}/role/notification", json=role_payload, timeout=20)
    print("\n=== POST /role/notification ===")
    print("Status:", r1.status_code)
    print("Headers:", dict(r1.headers))
    print("Body:", r1.text)

    # 2) Обычное уведомление этому же пользователю (user_id допустим 1001)
    user_id = 1001
    send_payload = {"user_id": user_id, "email": "trofimov.mat@yandex.ru", "subject": "Тест", "message": "Привет!"}
    r2 = requests.post(f"{BASE_URL}/send/notification", json=send_payload, timeout=20)
    print("\n=== POST /send/notification ===")
    print("Status:", r2.status_code)
    print("Headers:", dict(r2.headers))
    print("Body:", r2.text)

    # 3) Получить список всех уведомлений для пользователя
    r3 = requests.get(f"{BASE_URL}/notifications/{user_id}", timeout=20)
    print("\n=== GET /notifications/{user_id} ===")
    print("Status:", r3.status_code)
    print("Headers:", dict(r3.headers))
    print("Body:", r3.text)
    data = {}
    try:
        data = r3.json()
    except Exception:
        pass
    print("notifications count:", len(data.get("notifications", [])))

    # 4) Промаркировать все как прочитанные
    for n in data.get("notifications", []):
        nid = n["id"]
        r = requests.patch(f"{BASE_URL}/notifications/{nid}/read", timeout=20)
        print(f"\n=== PATCH /notifications/{nid}/read ===")
        print("Status:", r.status_code)
        print("Headers:", dict(r.headers))
        print("Body:", r.text)

if __name__ == "__main__":
    main()


