-- Script para crear tabla de sesiones activas
-- Esta tabla mantendrá las sesiones activas hasta que el usuario cierre sesión explícitamente

CREATE TABLE IF NOT EXISTS sesiones_activas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    server_id VARCHAR(50) NOT NULL,
    login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    UNIQUE KEY unique_user_session (username, server_id),
    INDEX idx_username (username),
    INDEX idx_server_id (server_id),
    INDEX idx_active (is_active)
);
