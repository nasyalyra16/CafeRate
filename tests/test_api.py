def create_cafe(client, headers, payload):
    return client.post("/api/v1/cafes", headers=headers, json=payload)


def create_review(client, headers, cafe_id, payload):
    return client.post(
        f"/api/v1/cafes/{cafe_id}/reviews", headers=headers, json=payload
    )


def test_root_is_public(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["service"] == "CafeRate API"


def test_create_cafe_returns_201(client, auth_headers, cafe_payload):
    response = create_cafe(client, auth_headers, cafe_payload)
    assert response.status_code == 201
    assert response.json()["name"] == "Kopi Sudut"


def test_create_cafe_has_initial_empty_rating(client, auth_headers, cafe_payload):
    response = create_cafe(client, auth_headers, cafe_payload)
    assert response.json()["review_count"] == 0
    assert response.json()["average_rating"] is None


def test_list_cafes_empty(client, auth_headers):
    response = client.get("/api/v1/cafes", headers=auth_headers)
    assert response.status_code == 200
    assert response.json() == []


def test_list_cafes_returns_created_cafe(client, auth_headers, cafe_payload):
    create_cafe(client, auth_headers, cafe_payload)
    response = client.get("/api/v1/cafes", headers=auth_headers)
    assert len(response.json()) == 1


def test_filter_cafes_by_area_case_insensitive(client, auth_headers, cafe_payload):
    create_cafe(client, auth_headers, cafe_payload)
    response = client.get("/api/v1/cafes?area=samata", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_cafe_by_id(client, auth_headers, cafe_payload):
    created = create_cafe(client, auth_headers, cafe_payload).json()
    response = client.get(f"/api/v1/cafes/{created['id']}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_missing_cafe_returns_404(client, auth_headers):
    response = client.get("/api/v1/cafes/999", headers=auth_headers)
    assert response.status_code == 404


def test_duplicate_cafe_returns_409(client, auth_headers, cafe_payload):
    create_cafe(client, auth_headers, cafe_payload)
    response = create_cafe(client, auth_headers, cafe_payload)
    assert response.status_code == 409


def test_invalid_cafe_payload_returns_422(client, auth_headers, cafe_payload):
    cafe_payload["name"] = "X"
    response = create_cafe(client, auth_headers, cafe_payload)
    assert response.status_code == 422


def test_extra_field_is_rejected(client, auth_headers, cafe_payload):
    cafe_payload["owner_password"] = "should-not-be-accepted"
    response = create_cafe(client, auth_headers, cafe_payload)
    assert response.status_code == 422


def test_endpoint_requires_api_key(client, cafe_payload):
    response = client.post("/api/v1/cafes", json=cafe_payload)
    assert response.status_code == 401


def test_invalid_api_key_is_rejected(client, cafe_payload):
    response = client.post(
        "/api/v1/cafes",
        headers={"X-API-Key": "wrong-key"},
        json=cafe_payload,
    )
    assert response.status_code == 401


def test_create_review_returns_201_and_average(client, auth_headers, cafe_payload, review_payload):
    cafe = create_cafe(client, auth_headers, cafe_payload).json()
    response = create_review(client, auth_headers, cafe["id"], review_payload)
    assert response.status_code == 201
    assert response.json()["overall_rating"] == 4.67


def test_review_for_missing_cafe_returns_404(client, auth_headers, review_payload):
    response = create_review(client, auth_headers, 999, review_payload)
    assert response.status_code == 404


def test_rating_out_of_range_returns_422(client, auth_headers, cafe_payload, review_payload):
    cafe = create_cafe(client, auth_headers, cafe_payload).json()
    review_payload["taste_rating"] = 6
    response = create_review(client, auth_headers, cafe["id"], review_payload)
    assert response.status_code == 422


def test_list_reviews_for_cafe(client, auth_headers, cafe_payload, review_payload):
    cafe = create_cafe(client, auth_headers, cafe_payload).json()
    create_review(client, auth_headers, cafe["id"], review_payload)
    response = client.get(f"/api/v1/cafes/{cafe['id']}/reviews", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_rating_card_updates_after_review(client, auth_headers, cafe_payload, review_payload):
    cafe = create_cafe(client, auth_headers, cafe_payload).json()
    create_review(client, auth_headers, cafe["id"], review_payload)
    response = client.get(
        f"/api/v1/cafes/{cafe['id']}/rating-card", headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()["review_count"] == 1
    assert response.json()["rating_label"] == "Favorit pengunjung"


def test_get_single_review(client, auth_headers, cafe_payload, review_payload):
    cafe = create_cafe(client, auth_headers, cafe_payload).json()
    review = create_review(client, auth_headers, cafe["id"], review_payload).json()
    response = client.get(f"/api/v1/reviews/{review['id']}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["visitor_alias"] == "PengunjungA"


def test_delete_review_returns_204(client, auth_headers, cafe_payload, review_payload):
    cafe = create_cafe(client, auth_headers, cafe_payload).json()
    review = create_review(client, auth_headers, cafe["id"], review_payload).json()
    response = client.delete(f"/api/v1/reviews/{review['id']}", headers=auth_headers)
    assert response.status_code == 204


def test_delete_missing_review_returns_404(client, auth_headers):
    response = client.delete("/api/v1/reviews/999", headers=auth_headers)
    assert response.status_code == 404


def test_deleted_review_is_no_longer_found(client, auth_headers, cafe_payload, review_payload):
    cafe = create_cafe(client, auth_headers, cafe_payload).json()
    review = create_review(client, auth_headers, cafe["id"], review_payload).json()
    client.delete(f"/api/v1/reviews/{review['id']}", headers=auth_headers)
    response = client.get(f"/api/v1/reviews/{review['id']}", headers=auth_headers)
    assert response.status_code == 404
