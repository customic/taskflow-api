# Taskflow API

Taskflow API to projekt zaliczeniowy wykonany w Django REST Framework.  
Aplikacja udostępnia REST API do zarządzania projektami, zadaniami, etykietami i komentarzami z uwierzytelnianiem oraz autoryzacją użytkowników.

---

## Technologie

- Python
- Django
- Django REST Framework
- Token Authentication
- SQLite

---

## Modele

W projekcie zaimplementowano cztery modele:

- **Project** – projekty należące do użytkownika
- **Task** – zadania przypisane do projektów (status, priorytet)
- **Label** – etykiety przypisywane do zadań
- **Comment** – komentarze do zadań

Relacje:
- User → Project (1:N)
- Project → Task (1:N)
- Task → Label (N:M)
- Task → Comment (1:N)
- Comment → User (autor)

---

## Uwierzytelnianie i autoryzacja

- Głównym mechanizmem uwierzytelniania jest **Token Authentication**.
- Dodatkowo włączono **Session Authentication** w celu testowania API w przeglądarce.
- Aplikacja obsługuje wielu użytkowników.
- Zwykli użytkownicy mają dostęp wyłącznie do swoich danych.
- Administrator ma rozszerzone uprawnienia.

Endpoint do uzyskania tokenu:
- POST /api/auth/token/

---

## Endpointy API

### CRUD
Dla wszystkich modeli dostępne są operacje Create, Retrieve, Update oraz Delete:

- `/api/projects/`
- `/api/tasks/`
- `/api/labels/`
- `/api/comments/`

### Endpointy dodatkowe (poza CRUD)

1. **Lista zadań według statusu**
GET /api/tasks/by-status/?status=todo|doing|done

2. **Statystyki zadań według statusu**
GET /api/tasks/stats/

---

## Uwagi

- Endpoint rejestracji użytkownika nie został zaimplementowany (był opcjonalny).
- Projekt koncentruje się na warstwie backendowej (REST API).
