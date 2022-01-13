import pytest
from app import schemas

def test_get_all_posts(authorised_client, test_posts):
    res = authorised_client.get("/posts/")

    assert res.status_code == 200
    assert len(res.json()) == len(test_posts)


def test_unautorised_user_get_all_post(client):
    res = client.get('/posts/')

    assert res.status_code == 401


def test_unautorised_user_get_one_post(client, test_posts):
    res = client.get(f'/posts/{test_posts[0].id}')

    assert res.status_code == 401


def test_get_one_post_not_exist(authorised_client):
    res = authorised_client.get('/posts/88888')

    assert res.status_code == 404


def test_get_one_post(authorised_client, test_posts):
    res = authorised_client.get(f'/posts/{test_posts[0].id}')
    post = schemas.PostOut(**res.json())

    assert post.Post.id == test_posts[0].id
    assert post.Post.title == test_posts[0].title
    assert post.Post.content == test_posts[0].content


@pytest.mark.parametrize("title, content, published", [
    ("First", "The life and death of pizza", True),
    ("Second", "How the pizza began", True),
    ("Final", "Pizza a memo", False),
])
def test_create_post(authorised_client, test_user_1, title, content, published):
    res = authorised_client.post(
        '/posts/', 
        json={"title":title, "content":content, "published":published}
    )
    created_post = schemas.PostResponse(**res.json())

    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user_1["id"]


def test_create_post_default_published_true(authorised_client, test_user_1):
    res = authorised_client.post(
        '/posts/', 
        json={"title":"Test T", "content":"Open T"}
    )

    created_post = schemas.PostResponse(**res.json())
    
    assert res.status_code == 201
    assert created_post.title == "Test T"
    assert created_post.content == "Open T"
    assert created_post.published == True
    assert created_post.owner_id == test_user_1["id"]


def test_unautorised_user_create_post(client):
    res = client.post(
        '/posts/', 
        json={"title":"Test Title", "content":"Content Test"}
    )

    assert res.status_code == 401

def test_unauthorised_user_delete_post(client, test_posts):
    res = client.delete(
        f"/posts/{test_posts[0].id}"
    )
    assert res.status_code == 401


def test__delete_post_success(authorised_client, test_posts):
    res = authorised_client.delete(
        f"/posts/{test_posts[0].id}"
    )
    assert res.status_code == 204

def test_delete_post_none_exist(authorised_client):
    res = authorised_client.delete(
        "/posts/9000"
    )

    assert res.status_code == 404


def test_delete_other_user_post(authorised_client, test_posts):
    res = authorised_client.delete(
        f"/posts/{test_posts[3].id}"
    )

    assert res.status_code == 403


def test_update_post(authorised_client, test_posts):
    data = {
        "title": "update title", 
        "content": " update content",
        "id": test_posts[0].id
    }
    res = authorised_client.put(
        f"/posts/{test_posts[0].id}", 
        json = data
    )

    updated_post = schemas.PostResponse(**res.json())

    assert res.status_code == 200
    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]


def test_update_other_user_post(authorised_client, test_posts):
    data = {
        "title": "update title",
        "content": "update content",
        "id": test_posts[3].id
    }

    res = authorised_client.put(
        f"/posts/{test_posts[3].id}",
        json = data
    )

    assert res.status_code == 403


def test_unauthorised_user_update_post(client, test_posts):
    data = {
        "title": "update title", 
        "content": " update content",
        "id": test_posts[0].id
    }
    res = client.put(
        f"/posts/{test_posts[0].id}", 
        json = data
    )

    assert res.status_code == 401


def test_update_post_none_exist(authorised_client, test_posts):
    data = {
        "title": "update title", 
        "content": " update content",
        "id": test_posts[0].id
    }
    res = authorised_client.put(
        "/posts/9000", 
        json = data
    )

    assert res.status_code == 404