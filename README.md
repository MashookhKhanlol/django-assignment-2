# Django Blog API

A complete blogging API built with Django featuring user authentication, blog posts, comments, and like functionality. Built without Django REST Framework (DRF) using only core Django.

## Features

- ✅ User registration and authentication
- ✅ Create, read, edit, and delete blog posts
- ✅ Comment system with CRUD operations
- ✅ Like/unlike posts functionality
- ✅ Pagination for post listings
- ✅ Session-based authentication
- ✅ Permission-based access control
- ✅ Clean error handling

## Setup Instructions

### Prerequisites
- Python 3.8+
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd django-blog-api
   ```

2. **Install dependencies**
   ```bash
   pip install django
   ```

3. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

5. **Run the development server**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000/`

## API Documentation

### Authentication Endpoints

#### Register User
- **URL:** `POST /api/register/`
- **Description:** Register a new user
- **Request Body:**
  ```json
  {
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepassword123"
  }
  ```
- **Response:**
  ```json
  {
    "message": "User registered successfully"
  }
  ```

#### Login
- **URL:** `POST /api/login/`
- **Description:** Authenticate user and create session
- **Request Body:**
  ```json
  {
    "username": "johndoe",
    "password": "securepassword123"
  }
  ```
- **Response:**
  ```json
  {
    "message": "Login successful"
  }
  ```

### Post Endpoints

#### Create Post
- **URL:** `POST /api/create-post/`
- **Authentication:** Required
- **Request Body:**
  ```json
  {
    "title": "My First Blog Post",
    "content": "This is the content of my blog post..."
  }
  ```
- **Response:**
  ```json
  {
    "message": "Post created",
    "post_id": 1
  }
  ```

#### List Posts
- **URL:** `GET /api/posts/`
- **Authentication:** Not required
- **Query Parameters:**
  - `page`: Page number (default: 1)
- **Response:**
  ```json
  {
    "posts": [
      {
        "id": 1,
        "title": "My First Blog Post",
        "author": "johndoe",
        "created_at": "2024-01-15T10:30:00Z",
        "like_count": 5
      }
    ],
    "pagination": {
      "current_page": 1,
      "total_pages": 3,
      "has_next": true,
      "has_previous": false
    }
  }
  ```

#### Get Post Detail
- **URL:** `GET /api/post/<id>/`
- **Authentication:** Not required
- **Response:**
  ```json
  {
    "id": 1,
    "title": "My First Blog Post",
    "content": "This is the content...",
    "author": "johndoe",
    "created_at": "2024-01-15T10:30:00Z",
    "like_count": 5,
    "comments": [
      {
        "id": 1,
        "user": "janedoe",
        "text": "Great post!",
        "created_at": "2024-01-15T11:00:00Z"
      }
    ]
  }
  ```

#### Edit Post
- **URL:** `PUT /api/post/<id>/edit/`
- **Authentication:** Required (post author only)
- **Request Body:**
  ```json
  {
    "title": "Updated Title",
    "content": "Updated content..."
  }
  ```
- **Response:**
  ```json
  {
    "message": "Post updated successfully"
  }
  ```

#### Delete Post
- **URL:** `DELETE /api/post/<id>/delete/`
- **Authentication:** Required (post author only)
- **Response:**
  ```json
  {
    "message": "Post deleted successfully"
  }
  ```

### Comment Endpoints

#### Add Comment
- **URL:** `POST /api/post/<id>/comment/`
- **Authentication:** Required
- **Request Body:**
  ```json
  {
    "text": "This is my comment on the post"
  }
  ```
- **Response:**
  ```json
  {
    "message": "Comment added",
    "comment_id": 1
  }
  ```

#### Edit Comment
- **URL:** `PUT /api/comment/<id>/edit/`
- **Authentication:** Required (comment author only)
- **Request Body:**
  ```json
  {
    "text": "Updated comment text"
  }
  ```
- **Response:**
  ```json
  {
    "message": "Comment updated successfully"
  }
  ```

#### Delete Comment
- **URL:** `DELETE /api/comment/<id>/delete/`
- **Authentication:** Required (comment author only)
- **Response:**
  ```json
  {
    "message": "Comment deleted successfully"
  }
  ```

### Like Endpoints

#### Like Post
- **URL:** `POST /api/post/<id>/like/`
- **Authentication:** Required
- **Response:**
  ```json
  {
    "message": "Post liked",
    "liked": true
  }
  ```

#### Unlike Post
- **URL:** `DELETE /api/post/<id>/unlike/`
- **Authentication:** Required
- **Response:**
  ```json
  {
    "message": "Post unliked",
    "liked": false
  }
  ```

## Error Responses

All endpoints return appropriate HTTP status codes and error messages:

- `400 Bad Request`: Invalid input data
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Permission denied
- `404 Not Found`: Resource not found
- `405 Method Not Allowed`: Wrong HTTP method

Example error response:
```json
{
  "error": "Authentication required"
}
```

## Testing the API

### Using curl

1. **Register a user:**
   ```bash
   curl -X POST http://localhost:8000/api/register/ \
     -H "Content-Type: application/json" \
     -d '{"username": "testuser", "email": "test@example.com", "password": "password123"}'
   ```

2. **Login:**
   ```bash
   curl -X POST http://localhost:8000/api/login/ \
     -H "Content-Type: application/json" \
     -d '{"username": "testuser", "password": "password123"}' \
     -c cookies.txt
   ```

3. **Create a post:**
   ```bash
   curl -X POST http://localhost:8000/api/create-post/ \
     -H "Content-Type: application/json" \
     -b cookies.txt \
     -d '{"title": "Test Post", "content": "This is a test post"}'
   ```

4. **Get posts:**
   ```bash
   curl http://localhost:8000/api/posts/
   ```

### Using Postman

1. Import the collection or create requests manually
2. For authenticated endpoints, use the "Cookies" tab to manage session cookies
3. Set Content-Type header to `application/json` for POST/PUT requests

## Project Structure

```
django-blog-api/
├── blog_api/          # Django project settings
├── blog/              # Main app
│   ├── models.py      # Post, Comment, Like models
│   ├── views.py       # API views
│   ├── urls.py        # URL routing
│   └── migrations/    # Database migrations
├── manage.py          # Django management script
└── README.md          # This file
```

## Database Models

- **User**: Django's built-in User model
- **Post**: Blog posts with author, title, content, timestamps
- **Comment**: Comments on posts with user, text, timestamps
- **Like**: User likes on posts (unique constraint)

## Security Features

- Session-based authentication
- CSRF protection (exempted for API endpoints)
- Permission-based access control
- Input validation and sanitization
- SQL injection protection (Django ORM)

## Future Enhancements

- JWT token authentication
- Rate limiting
- Search functionality
- Image uploads
- User profiles
- Email notifications
- Social media sharing

## License

This project is open source and available under the MIT License. 