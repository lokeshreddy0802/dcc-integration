import requests

BASE_URL = "http://127.0.0.1:8000"

def test_add_item():
    response = requests.post(f"{BASE_URL}/add-item?name=testItem&quantity=10")
    print("✅ Add Item Response:", response.json())  # Debug print
    assert response.status_code == 200
    assert response.json()["status"] == "Item added"

def test_remove_item():
    response = requests.post(f"{BASE_URL}/remove-item?name=testItem")
    print("✅ Remove Item Response:", response.json())  # Debug print
    assert response.status_code == 200
    assert response.json()["status"] == "Item removed"

def test_update_quantity():
    response = requests.post(f"{BASE_URL}/update-quantity?name=testItem&new_quantity=5")
    print("✅ Update Quantity Response:", response.json())  # Debug print
    assert response.status_code == 200
    assert response.json()["status"] == "Item quantity updated"  # 🔹 FIXED EXPECTED RESPONSE

if __name__ == "__main__":
    test_add_item()
    test_remove_item()
    test_update_quantity()
    print("🎉✅ All tests passed successfully!")

