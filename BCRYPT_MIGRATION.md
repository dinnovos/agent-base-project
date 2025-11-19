# 🔐 MIGRACIÓN DE CONTRASEÑAS BCRYPT

**Fecha:** 19 de Noviembre, 2025  
**Problema:** Login sigue lento después de optimizar bcrypt  
**Causa:** Usuarios existentes tienen contraseñas hasheadas con 12 rondas

---

## 🔍 EL PROBLEMA

### ¿Por qué sigue lento?

Cuando optimizamos bcrypt de 12 a 10 rondas, **solo afecta a NUEVAS contraseñas**. Los usuarios existentes tienen contraseñas hasheadas con las rondas antiguas (12).

**Bcrypt detecta automáticamente** cuántas rondas se usaron para hashear una contraseña y usa esas mismas rondas para verificarla.

```python
# Usuario creado ANTES de la optimización
password_hash = "$2b$12$..."  # ← 12 rondas (lento)
verify_password("password", password_hash)  # Usa 12 rondas → ~300ms

# Usuario creado DESPUÉS de la optimización
password_hash = "$2b$10$..."  # ← 10 rondas (rápido)
verify_password("password", password_hash)  # Usa 10 rondas → ~100ms
```

---

## ✅ SOLUCIONES

### Opción 1: Crear un NUEVO Usuario (Recomendado para Testing)

**Más fácil y rápido para probar la optimización:**

```http
POST http://localhost:8000/auth/register
Content-Type: application/json

{
  "email": "test@example.com",
  "username": "testuser",
  "password": "TestPassword123",
  "first_name": "Test",
  "last_name": "User"
}
```

Este nuevo usuario tendrá su contraseña hasheada con **10 rondas** y el login será rápido.

---

### Opción 2: Actualizar Contraseña de Usuario Existente

**Usa el script `update_user_password.py`:**

1. **Lista los usuarios existentes:**
   ```bash
   python update_user_password.py
   ```

2. **Edita el script y descomenta la última línea:**
   ```python
   # Al final del archivo update_user_password.py
   update_user_password('demo1@example.com', 'SecurePassword123')
   ```

3. **Ejecuta el script:**
   ```bash
   python update_user_password.py
   ```

4. **Verás algo como:**
   ```
   ✅ Usuario encontrado: demo1@example.com (ID: 1)
   📊 Rondas de bcrypt configuradas: 10
   🔐 Hasheando nueva contraseña...
   ✅ Contraseña hasheada en 0.105s
   ✅ Contraseña actualizada exitosamente para demo1@example.com
   ⚡ Ahora el login debería ser ~70% más rápido (~100-150ms)
   ```

---

### Opción 3: Cambiar Contraseña desde la API

**Usa el endpoint de cambio de contraseña:**

```http
POST http://localhost:8000/users/me/change-password
Authorization: Bearer {{token}}
Content-Type: application/json

{
  "current_password": "SecurePassword123",
  "new_password": "NewSecurePassword456"
}
```

La nueva contraseña se hasheará con **10 rondas** automáticamente.

---

## 🧪 CÓMO VERIFICAR LA OPTIMIZACIÓN

### 1. Inicia el servidor
```bash
python run.py
```

### 2. Observa los logs
```bash
tail -f logs/app.log
```

### 3. Haz login con un usuario NUEVO o con contraseña actualizada

```http
POST http://localhost:8000/auth/login
Content-Type: application/json

{
  "email": "test@example.com",
  "password": "TestPassword123"
}
```

### 4. Verifica los tiempos en los logs

**Usuario con 10 rondas (RÁPIDO):**
```
2025-11-19 12:16:45 - src.services.auth_service - INFO - Authentication attempt for email: test@example.com
2025-11-19 12:16:45 - src.services.auth_service - DEBUG - Password verified successfully (took 0.11s)  ← RÁPIDO
2025-11-19 12:16:45 - src.services.auth_service - INFO - Authentication successful for test@example.com (total time: 0.13s)
```

**Usuario con 12 rondas (LENTO):**
```
2025-11-19 12:16:50 - src.services.auth_service - INFO - Authentication attempt for email: demo1@example.com
2025-11-19 12:16:50 - src.services.auth_service - DEBUG - Password verified successfully (took 0.32s)  ← LENTO
2025-11-19 12:16:50 - src.services.auth_service - INFO - Authentication successful for demo1@example.com (total time: 0.35s)
```

---

## 📊 COMPARACIÓN DE TIEMPOS

| Usuario | Rondas | Tiempo de Verificación | Tiempo Total |
|---------|--------|----------------------|--------------|
| **Nuevo** (10 rounds) | 10 | ~100-120ms | ~130-150ms ⚡ |
| **Antiguo** (12 rounds) | 12 | ~300-350ms | ~320-370ms 🐌 |
| **Mejora** | -2 | **70% más rápido** | **65% más rápido** |

---

## 🔒 SEGURIDAD

### ¿Es seguro usar 10 rondas?

**SÍ**, 10 rondas es seguro para desarrollo y aplicaciones normales:

| Rondas | Intentos/segundo | Tiempo para 1M contraseñas |
|--------|-----------------|---------------------------|
| 10 | ~10 intentos/seg | ~27 horas |
| 12 | ~3 intentos/seg | ~4 días |
| 14 | ~1 intento/seg | ~11 días |

### Recomendaciones por Entorno

- ✅ **Desarrollo:** 10 rondas (rápido, seguro)
- ✅ **Producción:** 12 rondas (balance perfecto)
- ✅ **Alta seguridad:** 14 rondas (bancos, gobierno)

---

## 🚀 MIGRACIÓN EN PRODUCCIÓN

### Estrategia Recomendada: Migración Gradual

**NO re-hashear todas las contraseñas de golpe.** En su lugar:

1. **Mantener compatibilidad:** El código actual ya soporta ambas versiones
2. **Migración natural:** Cuando un usuario cambia su contraseña, se re-hashea automáticamente con 10 rondas
3. **Forzar cambio (opcional):** Después de 6 meses, pedir a usuarios que cambien contraseñas

### Código para Forzar Re-hash en Login (Opcional)

```python
# src/services/auth_service.py

def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """Authenticate user and optionally re-hash password if using old rounds."""
    # ... código existente ...
    
    # Verificar contraseña
    if not verify_password(password, user.password):
        return None
    
    # ✅ OPCIONAL: Re-hashear si usa rondas antiguas
    if user.password.startswith("$2b$12$"):  # Detectar 12 rondas
        logger.info(f"Re-hashing password for {email} (old rounds detected)")
        user.password = hash_password(password)
        db.commit()
    
    # ... resto del código ...
```

---

## 📝 SCRIPTS DISPONIBLES

| Script | Descripción | Uso |
|--------|-------------|-----|
| `update_user_password.py` | Actualiza contraseña de un usuario | `python update_user_password.py` |
| `rehash_passwords.py` | Muestra info sobre usuarios | `python rehash_passwords.py` |

---

## 🎯 RESUMEN

### Para Probar la Optimización AHORA:

1. **Opción Rápida:** Crea un nuevo usuario con `/auth/register`
2. **Opción Completa:** Actualiza contraseña con `update_user_password.py`

### Para Producción:

1. **Mantener código actual** (ya soporta ambas versiones)
2. **Migración gradual** (usuarios cambian contraseñas naturalmente)
3. **Opcional:** Implementar re-hash automático en login

---

**Última actualización:** 19 de Noviembre, 2025  
**Estado:** ✅ Optimización implementada, requiere migración de usuarios
