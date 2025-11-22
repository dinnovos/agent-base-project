# Sistema de Planes Dinámicos

## 📋 Descripción General

El sistema de planes permite gestionar límites de rate limiting de forma dinámica por usuario, reemplazando la configuración estática basada en variables de entorno.

Cada usuario está asociado a un plan que define:
- **query_limit**: Número máximo de consultas permitidas
- **query_window_hours**: Ventana de tiempo en horas para el límite de consultas

---

## 🏗️ Arquitectura

### Modelo Plan

```python
class Plan(Base):
    id: int
    name: str                    # Nombre del plan (ej: "Free", "Pro", "Enterprise")
    description: str             # Descripción del plan
    query_limit: int             # Límite de consultas
    query_window_hours: int      # Ventana de tiempo en horas
    is_active: bool              # Si el plan está activo
    created_at: datetime
    updated_at: datetime
```

### Relación User-Plan

- Cada usuario tiene un `plan_id` (Foreign Key a `plans.id`)
- Relación: `user.plan` → Acceso al plan del usuario
- Relación inversa: `plan.users` → Lista de usuarios con ese plan

---

## 🚀 Migración desde Variables de Entorno

### Antes (Configuración Estática)
```python
# .env
CHATBOT_QUERY_LIMIT=5
CHATBOT_QUERY_WINDOW_HOURS=24

# Código
can_query, used, remaining = check_chatbot_rate_limit(db, user_id)
# Usaba settings.CHATBOT_QUERY_LIMIT
```

### Ahora (Configuración Dinámica)
```python
# Base de datos
Plan(name="Free", query_limit=5, query_window_hours=24)

# Código
can_query, used, remaining, limit, window = check_chatbot_rate_limit(db, user_id)
# Usa user.plan.query_limit y user.plan.query_window_hours
```

**Nota**: Las variables de entorno se mantienen como fallback en caso de errores.

---

## 📦 Plan por Defecto: "Free"

Al ejecutar la migración, se crea automáticamente el plan "Free":

```python
Plan(
    name="Free",
    description="Plan gratuito con límites básicos",
    query_limit=5,
    query_window_hours=24,
    is_active=True
)
```

**Todos los nuevos usuarios se asignan automáticamente al plan "Free".**

---

## 🔧 Uso del Sistema

### 1. Crear un Nuevo Plan (Manual)

```python
from src.services.plan_service import create_plan
from src.schemas.plan import PlanCreate

plan_data = PlanCreate(
    name="Pro",
    description="Plan profesional con límites extendidos",
    query_limit=50,
    query_window_hours=24,
    is_active=True
)

plan = create_plan(db, plan_data)
```

### 2. Cambiar el Plan de un Usuario (Manual)

```python
from src.services.user_service import change_user_plan

# Cambiar usuario 123 al plan 2
updated_user = change_user_plan(db, user_id=123, plan_id=2)
```

### 3. Consultar el Plan de un Usuario

```python
from src.services.user_service import get_user_by_id

user = get_user_by_id(db, user_id=123)
print(f"Plan: {user.plan.name}")
print(f"Límite: {user.plan.query_limit} consultas/{user.plan.query_window_hours}h")
```

### 4. Listar Todos los Planes

```python
from src.services.plan_service import get_all_plans

plans = get_all_plans(db)
for plan in plans:
    print(f"{plan.name}: {plan.query_limit} consultas/{plan.query_window_hours}h")
```

---

## 🗄️ Gestión de Planes en Base de Datos

### Crear Plan Directamente en PostgreSQL

```sql
INSERT INTO plans (name, description, query_limit, query_window_hours, is_active)
VALUES ('Premium', 'Plan premium con límites altos', 100, 24, true);
```

### Actualizar Plan

```sql
UPDATE plans
SET query_limit = 20, query_window_hours = 12
WHERE name = 'Pro';
```

### Cambiar Plan de Usuario

```sql
-- Cambiar usuario al plan "Pro"
UPDATE users
SET plan_id = (SELECT id FROM plans WHERE name = 'Pro')
WHERE email = 'usuario@example.com';
```

### Listar Usuarios por Plan

```sql
SELECT u.username, u.email, p.name as plan_name, p.query_limit
FROM users u
JOIN plans p ON u.plan_id = p.id
WHERE p.name = 'Free';
```

---

## 📊 Ejemplos de Planes Sugeridos

| Plan       | query_limit | query_window_hours | Descripción                    |
|------------|-------------|-------------------|--------------------------------|
| Free       | 5           | 24                | Plan gratuito básico           |
| Basic      | 20          | 24                | Plan básico de pago            |
| Pro        | 100         | 24                | Plan profesional               |
| Enterprise | 1000        | 24                | Plan empresarial               |
| Unlimited  | 999999      | 1                 | Sin límites prácticos          |

---

## 🔍 Rate Limiting con Planes

### Funcionamiento

1. Usuario hace una petición al chatbot
2. `verify_chatbot_rate_limit()` dependency se ejecuta
3. Se obtiene el usuario y su plan asociado
4. Se cuentan las consultas únicas (por `main_call_tid`) en la ventana de tiempo del plan
5. Si `consultas_usadas < plan.query_limit` → ✅ Permitir
6. Si `consultas_usadas >= plan.query_limit` → ❌ HTTP 429 Too Many Requests

### Respuesta de Error (HTTP 429)

```json
{
  "detail": {
    "message": "Rate limit exceeded. You have used 5 of 5 queries in the last 24 hours (Plan: Free).",
    "queries_used": 5,
    "queries_limit": 5,
    "window_hours": 24,
    "queries_remaining": 0,
    "plan": "Free"
  }
}
```

**Headers:**
```
X-RateLimit-Limit: 5
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 24
```

---

## 🔄 Migración de Base de Datos

### Ejecutar Migración

1. **Mover el archivo de migración:**
   ```bash
   # El archivo migration_add_plans.py está en la raíz del proyecto
   # Moverlo a: alembic/versions/5f3a2b1c8d9e_add_plans_table_and_user_plan_relationship.py
   ```

2. **Ejecutar migración:**
   ```bash
   alembic upgrade head
   ```

### Qué hace la Migración

1. ✅ Crea tabla `plans`
2. ✅ Inserta plan "Free" por defecto
3. ✅ Agrega columna `plan_id` a tabla `users`
4. ✅ Asigna plan "Free" a todos los usuarios existentes
5. ✅ Crea foreign key constraint

### Rollback (Revertir)

```bash
alembic downgrade -1
```

Esto eliminará:
- Foreign key constraint
- Columna `plan_id` de `users`
- Tabla `plans`

---

## ⚠️ Consideraciones Importantes

### 1. Usuarios Existentes
- Todos los usuarios existentes se asignan automáticamente al plan "Free"
- No se pierden datos de usuarios

### 2. Fallback
- Si hay un error al obtener el plan del usuario, se usan los valores de `.env` como fallback
- Esto previene que el sistema falle completamente

### 3. Performance
- Se agrega un JOIN adicional en `check_chatbot_rate_limit()`
- Impacto mínimo gracias a índices en `plan_id`

### 4. Seguridad
- Solo administradores pueden crear/modificar planes (gestión manual)
- Los usuarios no pueden cambiar su propio plan

---

## 🧪 Testing

### Ejecutar Tests

```bash
pytest tests/test_plans.py -v
pytest tests/test_auth.py -v
```

### Tests Incluidos

- ✅ Creación de planes
- ✅ Obtención de plan por ID/nombre
- ✅ Plan por defecto "Free"
- ✅ Actualización de planes
- ✅ Activación/desactivación de planes
- ✅ Relación User-Plan
- ✅ Registro de usuarios con plan Free

---

## 📝 Archivos Modificados/Creados

### Nuevos Archivos (7)
1. `src/models/plan.py` - Modelo Plan
2. `src/schemas/plan.py` - Schemas de Plan
3. `src/services/plan_service.py` - Servicio de planes
4. `tests/test_plans.py` - Tests de planes
5. `migration_add_plans.py` - Migración Alembic (mover a alembic/versions/)
6. `PLANS_SYSTEM.md` - Esta documentación

### Archivos Modificados (11)
1. `src/models/user.py` - Agregado plan_id y relación
2. `src/models/__init__.py` - Export Plan
3. `src/schemas/__init__.py` - Export schemas de Plan
4. `src/services/user_service.py` - Asignación de plan Free, change_user_plan()
5. `src/services/usage_log_service.py` - Rate limiting con planes
6. `src/dependencies.py` - Mensajes con info del plan
7. `src/core/config.py` - Variables marcadas como deprecated
8. `.env.example` - Documentación actualizada
9. `tests/conftest.py` - Fixture test_plan
10. `tests/test_auth.py` - Verificación de plan en registro
11. `README.md` - (Pendiente) Mención del sistema de planes

---

## 🎯 Próximos Pasos (Opcional)

1. **Endpoints de Administración** (No implementado)
   - `GET /plans/` - Listar planes
   - `POST /plans/` - Crear plan (superuser)
   - `PUT /plans/{id}` - Actualizar plan (superuser)
   - `PATCH /users/{id}/plan` - Cambiar plan de usuario (superuser)

2. **Dashboard de Administración**
   - Interfaz web para gestionar planes
   - Visualización de usuarios por plan

3. **Métricas y Analytics**
   - Uso de consultas por plan
   - Conversión entre planes

---

## 📞 Soporte

Para cambiar el plan de un usuario o crear nuevos planes, actualmente se debe hacer manualmente mediante:
- Scripts Python usando los servicios
- Consultas SQL directas a la base de datos

---

**Última actualización:** 21 de Noviembre, 2025
