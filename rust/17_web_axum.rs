"""
17_web_axum.rs - Web API dengan Axum

Tahap 5: Proyek Nyata - Rust
Materi: axum, tokio, REST API, routing, JSON, state
"""

use axum::{
    routing::{get, post},
    Json, Router,
};
use serde::{Deserialize, Serialize};
use std::net::SocketAddr;
use std::sync::Arc;
use tokio::sync::Mutex;
use tower_http::trace::TraceLayer;

// --- Model Data ---

#[derive(Clone, Debug, Serialize, Deserialize)]
struct User {
    id: u32,
    nama: String,
    email: String,
}

#[derive(Debug, Deserialize)]
struct CreateUser {
    nama: String,
    email: String,
}

#[derive(Debug, Serialize)]
struct ApiResponse<T> {
    status: String,
    data: T,
}

#[derive(Debug, Serialize)]
struct ErrorResponse {
    status: String,
    error: String,
}

// --- App State ---

type AppState = Arc<Mutex<Vec<User>>>;

// --- Handlers ---

async fn root_handler() -> Json<ApiResponse<String>> {
    Json(ApiResponse {
        status: "success".to_string(),
        data: "Selamat datang di Belajar Rust Axum API".to_string(),
    })
}

async fn get_users(state: axum::extract::State<AppState>) -> Json<ApiResponse<Vec<User>>> {
    let users = state.lock().await;
    Json(ApiResponse {
        status: "success".to_string(),
        data: users.clone(),
    })
}

async fn create_user(
    state: axum::extract::State<AppState>,
    Json(payload): Json<CreateUser>,
) -> Json<ApiResponse<User>> {
    let mut users = state.lock().await;
    let id = users.iter().map(|u| u.id).max().unwrap_or(0) + 1;
    let user = User {
        id,
        nama: payload.nama,
        email: payload.email,
    };
    users.push(user.clone());
    Json(ApiResponse {
        status: "success".to_string(),
        data: user,
    })
}

async fn get_user(
    axum::extract::Path(user_id): axum::extract::Path<u32>,
    state: axum::extract::State<AppState>,
) -> Result<Json<ApiResponse<User>>, Json<ErrorResponse>> {
    let users = state.lock().await;
    match users.iter().find(|u| u.id == user_id) {
        Some(user) => Ok(Json(ApiResponse {
            status: "success".to_string(),
            data: user.clone(),
        })),
        None => Err(Json(ErrorResponse {
            status: "error".to_string(),
            error: format!("User dengan id {} tidak ditemukan", user_id),
        })),
    }
}

#[tokio::main]
async fn main() {
    // Inisialisasi state dengan data dummy
    let initial_users = vec![
        User {
            id: 1,
            nama: "Budi".to_string(),
            email: "budi@example.com".to_string(),
        },
        User {
            id: 2,
            nama: "Siti".to_string(),
            email: "siti@example.com".to_string(),
        },
    ];
    let state: AppState = Arc::new(Mutex::new(initial_users));

    // Buat router
    let app = Router::new()
        .route("/", get(root_handler))
        .route("/users", get(get_users).post(create_user))
        .route("/users/:id", get(get_user))
        .layer(TraceLayer::new_for_http())
        .with_state(state);

    // Jalankan server
    let addr = SocketAddr::from(([127, 0, 0, 1], 3000));
    println!("Server berjalan di http://{}", addr);

    let listener = tokio::net::TcpListener::bind(addr).await.unwrap();
    axum::serve(listener, app).await.unwrap();
}
