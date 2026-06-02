import requests
import allure
from jsonschema import validate
from config import BASE_URL
from data import booking_data
from schemas.booking_schema import BOOKING_SCHEMA

@allure.story("E2E Тест бронирования")
@allure.severity(allure.severity_level.CRITICAL)
def test_booking_e2e(auth_headers):
    booking_id = None

    with allure.step("Шаг 1-2: Создать новую бронь"):
        create_res = requests.post(f"{BASE_URL}/booking", json=booking_data.NEW_BOOKING_DATA)
        assert create_res.status_code == 200
        assert "bookingid" in create_res.json()

    with allure.step("Шаг 3: Сохранить bookingid"):
        booking_id = create_res.json()["bookingid"]
        # Прикрепляем созданный ID к отчету Allure
        allure.attach(str(booking_id), name="ID бронирования", attachment_type=allure.attachment_type.TEXT)

    with allure.step("Шаг 4: Получить созданную бронь по ID"):
        get_res = requests.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_res.status_code == 200
        booking_body = get_res.json()
        assert booking_body["firstname"] == "John"

    with allure.step("Шаг 5: Валидировать JSON-схему ответа"):
        validate(instance=booking_body, schema=BOOKING_SCHEMA)

    with allure.step("Шаг 6: Обновить бронь (полное обновление через PUT)"):
        put_res = requests.put(
            f"{BASE_URL}/booking/{booking_id}",
            json=booking_data.UPDATE_BOOKING_DATA,
            headers=auth_headers
        )
        assert put_res.status_code == 200
        assert put_res.json()["firstname"] == "Updated"

    with allure.step("Шаг 7: Проверить обновление через GET"):
        get_updated_res = requests.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_updated_res.status_code == 200
        assert get_updated_res.json()["firstname"] == "Updated"

    with allure.step("Шаг 8: Частично обновить бронь (PATCH)"):
        patch_res = requests.patch(
            f"{BASE_URL}/booking/{booking_id}",
            json=booking_data.PATCH_BOOKING_DATA,
            headers=auth_headers
        )
        assert patch_res.status_code == 200
        assert patch_res.json()["totalprice"] == 200

    with allure.step("Шаг 9: Удалить бронь (DELETE)"):
        delete_res = requests.delete(f"{BASE_URL}/booking/{booking_id}", headers=auth_headers)
        assert delete_res.status_code == 201

    with allure.step("Шаг 10: Проверить удаление (GET ожидает 404)"):
        final_get_res = requests.get(f"{BASE_URL}/booking/{booking_id}")
        assert final_get_res.status_code == 404

    with allure.step("Шаг 11: Проверить время ответа"):
        assert get_res.elapsed.total_seconds() < 2.0

    with allure.step("Шаг 12: Проверить заголовок Content-Type"):
        assert "application/json" in get_res.headers["Content-Type"]
